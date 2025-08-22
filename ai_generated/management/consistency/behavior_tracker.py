#!/opt/homebrew/opt/python@3.10/bin/python3.10
"""
RP Argument Behavior Tracker
Analyzes HOW arguments are implemented across functions to spot subtle inconsistencies
and opportunities for code reuse/standardization.
"""

import ast
import re
import json
from typing import Dict, List, Set, Tuple, Any, Optional
from collections import defaultdict
from dataclasses import dataclass, asdict

@dataclass
class ArgumentBehavior:
    arg_name: str
    function: str
    default_value: Any
    usage_pattern: str  # How the argument is used in the function
    validation_code: str  # Any validation/assertion code
    transformation_code: str  # How the argument is transformed/processed
    error_handling: str  # How errors with this argument are handled
    documentation: str  # Parameter description from docstring

class RPBehaviorTracker:
    def __init__(self, rp_path: str = "/opt/homebrew/lib/python3.10/site-packages/rp/r.py"):
        self.rp_path = rp_path
        self.behaviors = []  # List of ArgumentBehavior objects
        self.arg_to_functions = defaultdict(list)  # arg_name -> [function_names]
        self.behavioral_patterns = defaultdict(list)  # pattern_type -> [behaviors]
        
    def analyze_argument_behaviors(self):
        """Analyze how arguments are actually implemented across functions"""
        print("Loading function ASTs...")
        functions = self._load_all_functions()
        
        print("Analyzing argument behaviors...")
        for func_name, func_node in functions.items():
            self._analyze_function_argument_behaviors(func_name, func_node)
        
        print("Categorizing behavioral patterns...")
        self._categorize_behavioral_patterns()
        
        print("Detecting subtle inconsistencies...")
        inconsistencies = self._detect_behavioral_inconsistencies()
        
        return self.behaviors, inconsistencies
    
    def _load_all_functions(self) -> Dict[str, ast.FunctionDef]:
        """Load all function AST nodes"""
        with open(self.rp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        functions = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = node
                
        return functions
    
    def _analyze_function_argument_behaviors(self, func_name: str, func_node: ast.FunctionDef):
        """Analyze how each argument is used within a specific function"""
        # Get function arguments
        args_info = self._extract_function_args(func_node)
        
        # Get function body as string for pattern matching
        try:
            func_body = ast.unparse(func_node)
        except:
            func_body = ""
            
        # Analyze each argument
        for arg_info in args_info:
            arg_name = arg_info['name']
            
            # Skip special arguments
            if arg_name in ['self', 'cls', 'args', 'kwargs']:
                continue
                
            behavior = ArgumentBehavior(
                arg_name=arg_name,
                function=func_name,
                default_value=arg_info.get('default_value'),
                usage_pattern=self._extract_usage_pattern(arg_name, func_body),
                validation_code=self._extract_validation_code(arg_name, func_body),
                transformation_code=self._extract_transformation_code(arg_name, func_body),
                error_handling=self._extract_error_handling(arg_name, func_body),
                documentation=self._extract_arg_documentation(func_node, arg_name)
            )
            
            self.behaviors.append(behavior)
            self.arg_to_functions[arg_name].append(func_name)
    
    def _extract_function_args(self, func_node: ast.FunctionDef) -> List[Dict]:
        """Extract function arguments with defaults"""
        args_info = []
        
        # Regular arguments
        for i, arg in enumerate(func_node.args.args):
            arg_info = {'name': arg.arg, 'default_value': None}
            
            # Check for default value
            defaults_start = len(func_node.args.args) - len(func_node.args.defaults)
            if i >= defaults_start:
                default_idx = i - defaults_start
                arg_info['default_value'] = self._ast_to_value(func_node.args.defaults[default_idx])
                
            args_info.append(arg_info)
        
        # Keyword-only arguments
        for i, arg in enumerate(func_node.args.kwonlyargs):
            arg_info = {'name': arg.arg, 'default_value': None}
            
            if i < len(func_node.args.kw_defaults) and func_node.args.kw_defaults[i]:
                arg_info['default_value'] = self._ast_to_value(func_node.args.kw_defaults[i])
                
            args_info.append(arg_info)
        
        return args_info
    
    def _ast_to_value(self, node) -> Any:
        """Convert AST node to Python value"""
        try:
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.Name):
                return f"<{node.id}>"  # Variable reference
            else:
                return ast.unparse(node)
        except:
            return "<complex>"
    
    def _extract_usage_pattern(self, arg_name: str, func_body: str) -> str:
        """Extract how the argument is used in the function"""
        patterns = []
        
        # Direct usage patterns
        if re.search(rf'\b{arg_name}\s*==', func_body):
            patterns.append('equality_check')
        if re.search(rf'\bif\s+{arg_name}\b', func_body):
            patterns.append('boolean_condition')
        if re.search(rf'\b{arg_name}\s*is\s+None', func_body):
            patterns.append('none_check')
        if re.search(rf'\b{arg_name}\s*\[', func_body):
            patterns.append('indexing')
        if re.search(rf'\b{arg_name}\.\w+\(', func_body):
            patterns.append('method_call')
        if re.search(rf'len\s*\(\s*{arg_name}\s*\)', func_body):
            patterns.append('length_check')
        if re.search(rf'for\s+\w+\s+in\s+{arg_name}\b', func_body):
            patterns.append('iteration')
        if re.search(rf'\b{arg_name}\s*\+\s*', func_body):
            patterns.append('addition')
        if re.search(rf'isinstance\s*\(\s*{arg_name}\s*,', func_body):
            patterns.append('type_check')
        
        return ','.join(patterns) if patterns else 'simple_usage'
    
    def _extract_validation_code(self, arg_name: str, func_body: str) -> str:
        """Extract validation/assertion code for the argument"""
        validations = []
        
        # Common validation patterns
        assert_pattern = rf'assert\s+[^;\n]*\b{arg_name}\b[^;\n]*'
        assertions = re.findall(assert_pattern, func_body)
        validations.extend(assertions)
        
        # Type checks
        isinstance_pattern = rf'isinstance\s*\(\s*{arg_name}\s*,\s*[^)]+\)'
        type_checks = re.findall(isinstance_pattern, func_body)
        validations.extend(type_checks)
        
        # Range checks
        range_pattern = rf'({arg_name}\s*[<>=!]+\s*[\d\w\.]+|[\d\w\.]+\s*[<>=!]+\s*{arg_name})'
        range_checks = re.findall(range_pattern, func_body)
        validations.extend([check[0] if isinstance(check, tuple) else check for check in range_checks])
        
        return ' | '.join(validations[:3])  # Limit to avoid too much noise
    
    def _extract_transformation_code(self, arg_name: str, func_body: str) -> str:
        """Extract how the argument is transformed/processed"""
        transformations = []
        
        # Assignment patterns where arg is transformed
        transform_pattern = rf'{arg_name}\s*=\s*[^;\n]+'
        transforms = re.findall(transform_pattern, func_body)
        transformations.extend(transforms[:2])  # Limit to first 2
        
        # Function calls on the argument
        func_call_pattern = rf'\w+\s*\(\s*[^)]*{arg_name}[^)]*\)'
        func_calls = re.findall(func_call_pattern, func_body)
        transformations.extend(func_calls[:2])
        
        return ' | '.join(transformations)
    
    def _extract_error_handling(self, arg_name: str, func_body: str) -> str:
        """Extract error handling patterns for the argument"""
        error_patterns = []
        
        # Try-except blocks mentioning the argument
        try_blocks = re.findall(rf'try:\s*[^{{}}]*{arg_name}[^{{}}]*except[^{{}}]*', func_body, re.DOTALL)
        if try_blocks:
            error_patterns.append('try_except')
            
        # Conditional error handling
        if re.search(rf'if.*{arg_name}.*raise', func_body):
            error_patterns.append('conditional_raise')
            
        # Return None patterns
        if re.search(rf'return None.*{arg_name}', func_body):
            error_patterns.append('return_none')
            
        return ','.join(error_patterns)
    
    def _extract_arg_documentation(self, func_node: ast.FunctionDef, arg_name: str) -> str:
        """Extract argument documentation from docstring"""
        docstring = ast.get_docstring(func_node) or ""
        
        # Look for parameter documentation patterns
        param_patterns = [
            rf'{arg_name}\s*[:\(][^:\n]*',
            rf'-\s*{arg_name}\s*[:\(][^:\n]*',
            rf':\s*{arg_name}\s*[:\(][^:\n]*'
        ]
        
        for pattern in param_patterns:
            matches = re.findall(pattern, docstring, re.IGNORECASE)
            if matches:
                return matches[0].strip()[:200]  # First match, truncated
                
        return ""
    
    def _categorize_behavioral_patterns(self):
        """Categorize behaviors by patterns for analysis"""
        for behavior in self.behaviors:
            # Categorize by usage pattern
            for pattern in behavior.usage_pattern.split(','):
                if pattern:
                    self.behavioral_patterns[f"usage_{pattern}"].append(behavior)
            
            # Categorize by validation approach
            if behavior.validation_code:
                self.behavioral_patterns["has_validation"].append(behavior)
            else:
                self.behavioral_patterns["no_validation"].append(behavior)
            
            # Categorize by error handling
            for error_type in behavior.error_handling.split(','):
                if error_type:
                    self.behavioral_patterns[f"error_{error_type}"].append(behavior)
    
    def _detect_behavioral_inconsistencies(self) -> List[Dict]:
        """Detect subtle behavioral inconsistencies"""
        inconsistencies = []
        
        # For each argument used in multiple functions
        for arg_name, functions in self.arg_to_functions.items():
            if len(functions) < 3:  # Need enough functions to detect patterns
                continue
                
            # Get behaviors for this argument
            arg_behaviors = [b for b in self.behaviors if b.arg_name == arg_name]
            
            # Check for inconsistent validation patterns
            validations = [b.validation_code for b in arg_behaviors if b.validation_code]
            if len(set(validations)) > 1:
                inconsistencies.append({
                    'type': 'inconsistent_validation',
                    'arg_name': arg_name,
                    'different_validations': list(set(validations)),
                    'functions': [b.function for b in arg_behaviors if b.validation_code],
                    'severity': 'medium'
                })
            
            # Check for inconsistent error handling
            error_patterns = [b.error_handling for b in arg_behaviors if b.error_handling]
            if len(set(error_patterns)) > 1:
                inconsistencies.append({
                    'type': 'inconsistent_error_handling',
                    'arg_name': arg_name,
                    'different_patterns': list(set(error_patterns)),
                    'functions': [b.function for b in arg_behaviors if b.error_handling],
                    'severity': 'medium'
                })
            
            # Check for redundant transformation code
            transforms = [b.transformation_code for b in arg_behaviors if b.transformation_code]
            transform_counts = {}
            for transform in transforms:
                transform_counts[transform] = transform_counts.get(transform, 0) + 1
            
            common_transforms = [t for t, count in transform_counts.items() if count >= 3]
            if common_transforms:
                inconsistencies.append({
                    'type': 'potential_code_duplication',
                    'arg_name': arg_name,
                    'common_patterns': common_transforms,
                    'functions': functions,
                    'severity': 'low'
                })
        
        return inconsistencies
    
    def generate_behavior_database(self, output_path: str):
        """Generate searchable behavior database"""
        
        # Convert behaviors to serializable format
        behaviors_data = []
        for behavior in self.behaviors:
            behaviors_data.append(asdict(behavior))
        
        # Create searchable index
        behavior_db = {
            'metadata': {
                'total_behaviors_analyzed': len(self.behaviors),
                'unique_arguments': len(self.arg_to_functions),
                'behavioral_patterns': len(self.behavioral_patterns)
            },
            'arg_to_functions': dict(self.arg_to_functions),  # Quick lookup
            'behaviors': behaviors_data,  # Full details
            'common_patterns': self._summarize_common_patterns(),
            'validation_patterns': self._summarize_validation_patterns(),
            'error_handling_patterns': self._summarize_error_patterns()
        }
        
        with open(output_path, 'w') as f:
            json.dump(behavior_db, f, indent=2)
        
        print(f"Behavior database saved to: {output_path}")
        return behavior_db
    
    def _summarize_common_patterns(self) -> Dict:
        """Summarize most common usage patterns"""
        pattern_counts = defaultdict(int)
        for behavior in self.behaviors:
            for pattern in behavior.usage_pattern.split(','):
                if pattern:
                    pattern_counts[pattern] += 1
        
        return dict(sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:20])
    
    def _summarize_validation_patterns(self) -> Dict:
        """Summarize common validation approaches"""
        validation_counts = defaultdict(int)
        for behavior in self.behaviors:
            if behavior.validation_code:
                # Extract validation type
                if 'assert' in behavior.validation_code:
                    validation_counts['assertion'] += 1
                if 'isinstance' in behavior.validation_code:
                    validation_counts['type_check'] += 1
                if re.search(r'[<>=]', behavior.validation_code):
                    validation_counts['range_check'] += 1
                    
        return dict(validation_counts)
    
    def _summarize_error_patterns(self) -> Dict:
        """Summarize error handling approaches"""
        error_counts = defaultdict(int)
        for behavior in self.behaviors:
            for pattern in behavior.error_handling.split(','):
                if pattern:
                    error_counts[pattern] += 1
                    
        return dict(error_counts)
    
    def analyze_specific_argument(self, arg_name: str) -> Dict:
        """Deep analysis of a specific argument across all functions"""
        arg_behaviors = [b for b in self.behaviors if b.arg_name == arg_name]
        
        if not arg_behaviors:
            return {'error': f'Argument {arg_name} not found'}
        
        # Group by different implementation approaches
        by_default = defaultdict(list)
        by_validation = defaultdict(list)
        by_usage = defaultdict(list)
        
        for behavior in arg_behaviors:
            by_default[str(behavior.default_value)].append(behavior.function)
            by_validation[behavior.validation_code or 'none'].append(behavior.function)
            by_usage[behavior.usage_pattern].append(behavior.function)
        
        analysis = {
            'argument_name': arg_name,
            'total_functions': len(arg_behaviors),
            'default_value_analysis': {
                'different_defaults': len(by_default),
                'defaults_breakdown': dict(by_default)
            },
            'validation_analysis': {
                'different_validations': len(by_validation),
                'validation_breakdown': dict(by_validation)
            },
            'usage_analysis': {
                'different_patterns': len(by_usage),
                'usage_breakdown': dict(by_usage)
            },
            'recommendation': self._generate_argument_recommendation(arg_name, arg_behaviors)
        }
        
        return analysis
    
    def _generate_argument_recommendation(self, arg_name: str, behaviors: List[ArgumentBehavior]) -> str:
        """Generate recommendation for argument standardization"""
        defaults = [str(b.default_value) for b in behaviors]
        default_counts = {d: defaults.count(d) for d in set(defaults)}
        most_common_default = max(default_counts, key=default_counts.get)
        
        validations = [b.validation_code for b in behaviors if b.validation_code]
        
        recommendations = []
        
        # Default value recommendation
        if len(set(defaults)) > 1:
            if default_counts[most_common_default] > len(behaviors) * 0.6:
                recommendations.append(f"Consider standardizing to default={most_common_default} (used in {default_counts[most_common_default]}/{len(behaviors)} functions)")
            else:
                recommendations.append("Mixed defaults may be appropriate - analyze each function context")
        
        # Validation recommendation
        if validations and len(set(validations)) > 1:
            recommendations.append("Consider creating a shared validation function for this argument")
        elif not validations:
            recommendations.append("Consider adding validation if this argument has constraints")
        
        return " | ".join(recommendations) if recommendations else "Implementation appears consistent"

def generate_automatic_update_script():
    """Generate script to automatically update behavior database"""
    update_script = '''#!/opt/homebrew/opt/python@3.10/bin/python3.10
"""
Auto-update script for RP behavior tracking
Run this whenever r.py is modified to keep behavior database current
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from behavior_tracker import RPBehaviorTracker

def main():
    print("Updating RP argument behavior database...")
    
    tracker = RPBehaviorTracker()
    behaviors, inconsistencies = tracker.analyze_argument_behaviors()
    
    # Save updated database
    db_path = "/opt/homebrew/lib/python3.10/site-packages/rp/management/consistency/argument_behaviors.json"
    tracker.generate_behavior_database(db_path)
    
    # Save inconsistencies report
    inconsistencies_path = "/opt/homebrew/lib/python3.10/site-packages/rp/management/consistency/behavior_inconsistencies.json"
    with open(inconsistencies_path, 'w') as f:
        import json
        json.dump(inconsistencies, f, indent=2)
    
    print(f"Updated behavior database: {len(behaviors)} behaviors analyzed")
    print(f"Found {len(inconsistencies)} behavioral inconsistencies")
    
if __name__ == "__main__":
    main()
'''
    
    script_path = "/opt/homebrew/lib/python3.10/site-packages/rp/management/consistency/update_behaviors.py"
    with open(script_path, 'w') as f:
        f.write(update_script)
    
    # Make executable
    import os
    os.chmod(script_path, 0o755)
    
    print(f"Auto-update script created: {script_path}")

def main():
    tracker = RPBehaviorTracker()
    behaviors, inconsistencies = tracker.analyze_argument_behaviors()
    
    # Generate behavior database
    db = tracker.generate_behavior_database(
        "/opt/homebrew/lib/python3.10/site-packages/rp/management/consistency/argument_behaviors.json"
    )
    
    # Save inconsistencies
    with open("/opt/homebrew/lib/python3.10/site-packages/rp/management/consistency/behavior_inconsistencies.json", 'w') as f:
        json.dump(inconsistencies, f, indent=2)
    
    print(f"\n=== Behavioral Analysis Summary ===")
    print(f"Total behaviors analyzed: {len(behaviors)}")
    print(f"Inconsistencies found: {len(inconsistencies)}")
    
    # Show example of detailed analysis
    print(f"\n=== Example: 'strict' Argument Analysis ===")
    strict_analysis = tracker.analyze_specific_argument('strict')
    if 'error' not in strict_analysis:
        print(f"Used in {strict_analysis['total_functions']} functions")
        print(f"Different defaults: {strict_analysis['default_value_analysis']['different_defaults']}")
        print(f"Recommendation: {strict_analysis['recommendation']}")
    
    # Generate auto-update script
    generate_automatic_update_script()

if __name__ == "__main__":
    main()