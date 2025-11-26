"""
Unreachable code detection using AST analysis.

Detects code that can never be executed due to control flow.
"""
import ast
from typing import Set, List, Optional


class UnreachableCodeDetector:
    """
    Detects unreachable code using static AST analysis.

    Patterns detected:
    - Code after return/raise/break/continue at same indentation level
    - Code in `if False/0:` blocks
    - Else blocks in `if True/1:` statements
    - Code after `assert False`
    - Code after `sys.exit()` or `exit()` or `quit()`
    - Code after infinite loops (while True with no break)
    """

    def __init__(self, code: str):
        """Initialize with Python code string."""
        self.code = code
        self.lines = code.splitlines()
        self.unreachable_lines: Set[int] = set()
        self.unreachable_ranges: List[tuple] = []  # [(start_line, end_line), ...]

        try:
            self.tree = ast.parse(code)
            self._analyze()
        except SyntaxError:
            # Invalid Python - can't analyze
            self.tree = None

    def _analyze(self):
        """Run unreachable code analysis."""
        if not self.tree:
            return

        visitor = _UnreachableVisitor(self)
        visitor.visit(self.tree)

    def get_unreachable_lines(self) -> Set[int]:
        """Get all unreachable line numbers (1-indexed)."""
        return self.unreachable_lines

    def is_unreachable(self, line: int) -> bool:
        """Check if a specific line is unreachable."""
        return line in self.unreachable_lines


class _UnreachableVisitor(ast.NodeVisitor):
    """Internal visitor for detecting unreachable code."""

    def __init__(self, detector: UnreachableCodeDetector):
        self.detector = detector
        self.current_returns = []  # Stack of return-like statements

    def visit_FunctionDef(self, node):
        """Process function definitions."""
        self._check_body_for_unreachable(node.body)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Process async function definitions."""
        self._check_body_for_unreachable(node.body)
        self.generic_visit(node)

    def visit_If(self, node):
        """Process if statements to find always true/false conditions."""
        # Check if condition is constant
        const_value = self._get_constant_value(node.test)

        if const_value is True or const_value == 1:
            # if True: the else block is unreachable
            if node.orelse:
                self._mark_unreachable_nodes(node.orelse)
        elif const_value is False or const_value == 0:
            # if False: the if block is unreachable
            self._mark_unreachable_nodes(node.body)
            # Continue analyzing the else block
            for item in node.orelse:
                self.visit(item)
            return  # Don't visit the unreachable if body

        # Check bodies for unreachable code
        self._check_body_for_unreachable(node.body)
        self._check_body_for_unreachable(node.orelse)

        self.generic_visit(node)

    def visit_While(self, node):
        """Process while loops."""
        const_value = self._get_constant_value(node.test)

        if const_value is False or const_value == 0:
            # while False: the body is unreachable
            self._mark_unreachable_nodes(node.body)
            # Continue with else block
            for item in node.orelse:
                self.visit(item)
            return
        elif const_value is True or const_value == 1:
            # while True: check if there's a break
            has_break = self._has_break(node.body)
            if not has_break:
                # Infinite loop with no break - else is unreachable
                if node.orelse:
                    self._mark_unreachable_nodes(node.orelse)
                # Also mark this as a terminating statement for the parent scope
                # Store this info so parent can detect unreachable code after the loop
                self.is_infinite_loop = True

        self._check_body_for_unreachable(node.body)
        self._check_body_for_unreachable(node.orelse)
        self.generic_visit(node)

    def visit_For(self, node):
        """Process for loops."""
        self._check_body_for_unreachable(node.body)
        self._check_body_for_unreachable(node.orelse)
        self.generic_visit(node)

    def visit_Try(self, node):
        """Process try blocks."""
        self._check_body_for_unreachable(node.body)
        for handler in node.handlers:
            self._check_body_for_unreachable(handler.body)
        self._check_body_for_unreachable(node.orelse)
        self._check_body_for_unreachable(node.finalbody)
        self.generic_visit(node)

    def visit_With(self, node):
        """Process with statements."""
        self._check_body_for_unreachable(node.body)
        self.generic_visit(node)

    def _check_body_for_unreachable(self, body: List[ast.AST]):
        """Check a body of statements for unreachable code."""
        if not body:
            return

        for i, stmt in enumerate(body):
            # Check if this statement makes following code unreachable
            if self._is_terminating_statement(stmt):
                # Mark all following statements as unreachable
                for unreachable_stmt in body[i + 1:]:
                    self._mark_unreachable_nodes([unreachable_stmt])
                break

            # Check for infinite loops (while True without break)
            if isinstance(stmt, ast.While):
                const_value = self._get_constant_value(stmt.test)
                if const_value is True or const_value == 1:
                    if not self._has_break(stmt.body):
                        # Infinite loop - everything after is unreachable
                        for unreachable_stmt in body[i + 1:]:
                            self._mark_unreachable_nodes([unreachable_stmt])
                        # Still visit the loop body
                        self.visit(stmt)
                        break

            # Continue visiting this statement
            self.visit(stmt)

    def _is_terminating_statement(self, node: ast.AST) -> bool:
        """Check if a statement terminates control flow."""
        if isinstance(node, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
            return True

        # Check for assert False
        if isinstance(node, ast.Assert):
            const_value = self._get_constant_value(node.test)
            if const_value is False:
                return True

        # Check for sys.exit(), exit(), quit()
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if isinstance(call.func, ast.Name):
                if call.func.id in ('exit', 'quit'):
                    return True
            elif isinstance(call.func, ast.Attribute):
                # sys.exit()
                if (isinstance(call.func.value, ast.Name) and
                    call.func.value.id == 'sys' and
                    call.func.attr == 'exit'):
                    return True

        return False

    def _has_break(self, body: List[ast.AST]) -> bool:
        """Check if a body contains a break statement (not in nested loop)."""
        for stmt in body:
            if isinstance(stmt, ast.Break):
                return True
            # Don't look inside nested loops
            if not isinstance(stmt, (ast.For, ast.While)):
                # Check nested if/try/with blocks
                if isinstance(stmt, ast.If):
                    if self._has_break(stmt.body) or self._has_break(stmt.orelse):
                        return True
                elif isinstance(stmt, ast.Try):
                    if self._has_break(stmt.body):
                        return True
                    for handler in stmt.handlers:
                        if self._has_break(handler.body):
                            return True
                elif isinstance(stmt, ast.With):
                    if self._has_break(stmt.body):
                        return True
        return False

    def _get_constant_value(self, node: ast.AST) -> Optional[object]:
        """Get the constant value of a node if it's a constant."""
        if isinstance(node, ast.Constant):
            # Python 3.8+ uses ast.Constant
            return node.value
        elif isinstance(node, ast.NameConstant):
            # Python 3.7 uses ast.NameConstant for True/False/None
            return node.value
        elif isinstance(node, ast.Num):
            # Python 3.7 uses ast.Num for numbers
            return node.n
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            # Handle `not True`, `not False`, etc.
            inner = self._get_constant_value(node.operand)
            if inner is not None:
                return not inner
        return None

    def _mark_unreachable_nodes(self, nodes: List[ast.AST]):
        """Mark nodes as unreachable by adding their line ranges."""
        for node in nodes:
            if hasattr(node, 'lineno'):
                start_line = node.lineno
                end_line = getattr(node, 'end_lineno', start_line)

                # Add all lines in this range
                for line in range(start_line, end_line + 1):
                    self.detector.unreachable_lines.add(line)

                # Store the range for reference
                self.detector.unreachable_ranges.append((start_line, end_line))


def get_unreachable_positions(code: str) -> Set[tuple]:
    """
    Get all unreachable token positions in the code using actual lexer tokenization.

    Returns:
        Set of (line, column, length) tuples for unreachable code.
    """
    from pygments.lexers import PythonLexer
    from pygments import lex

    detector = UnreachableCodeDetector(code)
    unreachable_lines = detector.get_unreachable_lines()

    if not unreachable_lines:
        return set()

    positions = set()
    lexer = PythonLexer()

    # Tokenize the entire code with Pygments to get real token positions
    lines = code.splitlines(keepends=True)
    line_num = 1
    col = 0

    for token_type, text in lex(code, lexer):
        # Track line and column as we go through tokens
        if line_num in unreachable_lines:
            # Add this token's position if it's on an unreachable line
            positions.add((line_num, col, len(text)))

        # Update position tracking
        for char in text:
            if char == '\n':
                line_num += 1
                col = 0
            else:
                col += 1

    return positions