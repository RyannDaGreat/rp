#!/opt/homebrew/opt/python@3.10/bin/python3.10
"""
RP Consistency Tracker
Analyzes RP functions for consistency patterns and suggests improvements
"""

import re
import ast
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
from enum import Enum

class InconsistencyType(Enum):
    MISSING_PLURAL = "missing_plural"
    MISSING_SINGULAR = "missing_singular"
    INCONSISTENT_NAMING = "inconsistent_naming"
    MISSING_VIA_VARIANT = "missing_via_variant"
    INCONSISTENT_PARAMETERS = "inconsistent_parameters"
    MISSING_ALIAS = "missing_alias"
    ASYMMETRIC_PAIR = "asymmetric_pair"

@dataclass
class ConsistencyIssue:
    issue_type: InconsistencyType
    function_name: str
    description: str
    suggestion: str
    related_functions: List[str]
    priority: int  # 1-10, 10 being highest

class RPConsistencyTracker:
    def __init__(self, rp_path: str = "/opt/homebrew/lib/python3.10/site-packages/rp/r.py"):
        self.rp_path = rp_path
        self.functions = {}  # function_name -> AST node
        self.function_signatures = {}  # function_name -> parameter info
        self.issues = []  # List of ConsistencyIssue
        
        # RP naming patterns
        self.verb_noun_patterns = self._load_verb_noun_patterns()
        self.symmetric_pairs = self._load_expected_symmetric_pairs()
        
    def analyze_consistency(self) -> List[ConsistencyIssue]:
        """Analyze all functions for consistency issues"""
        self._load_functions()
        
        print("Checking pluralization patterns...")
        self._check_pluralization_consistency()
        
        print("Checking symmetric pairs...")
        self._check_symmetric_pairs()
        
        print("Checking naming consistency...")
        self._check_naming_consistency()
        
        print("Checking parameter consistency...")
        self._check_parameter_consistency()
        
        print("Checking via variant consistency...")
        self._check_via_variant_consistency()
        
        # Sort issues by priority
        self.issues.sort(key=lambda x: x.priority, reverse=True)
        
        return self.issues
    
    def _load_functions(self):
        """Load all function definitions and signatures"""
        with open(self.rp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.functions[node.name] = node
                self.function_signatures[node.name] = self._extract_signature(node)
    
    def _extract_signature(self, func_node: ast.FunctionDef) -> Dict:
        """Extract function signature information"""
        params = []
        defaults = []
        
        for arg in func_node.args.args:
            params.append(arg.arg)
            
        # Get default values
        if func_node.args.defaults:
            defaults = func_node.args.defaults
            
        return {
            'params': params,
            'defaults': defaults,
            'has_varargs': func_node.args.vararg is not None,
            'has_kwargs': func_node.args.kwarg is not None
        }
    
    def _check_pluralization_consistency(self):
        """Check for missing singular/plural function pairs"""
        # Group functions by potential singular/plural pairs
        singular_functions = {}
        plural_functions = {}
        
        for func_name in self.functions:
            if self._is_likely_plural(func_name):
                singular = self._get_singular_form(func_name)
                plural_functions[singular] = func_name
            else:
                singular_functions[func_name] = func_name
        
        # Check for missing plurals
        for singular in singular_functions:
            if singular not in plural_functions and self._should_have_plural(singular):
                expected_plural = self._get_plural_form(singular)
                
                self.issues.append(ConsistencyIssue(
                    issue_type=InconsistencyType.MISSING_PLURAL,
                    function_name=singular,
                    description=f"Function '{singular}' appears to work with single items but has no plural variant",
                    suggestion=f"Consider creating '{expected_plural}' that processes multiple items",
                    related_functions=[],
                    priority=self._calculate_pluralization_priority(singular)
                ))
        
        # Check for missing singulars
        for singular_form, plural in plural_functions.items():
            if singular_form not in singular_functions and self._should_have_singular(plural):
                self.issues.append(ConsistencyIssue(
                    issue_type=InconsistencyType.MISSING_SINGULAR,
                    function_name=plural,
                    description=f"Function '{plural}' appears to work with multiple items but has no singular variant",
                    suggestion=f"Consider creating '{singular_form}' that processes single items",
                    related_functions=[],
                    priority=self._calculate_pluralization_priority(plural)
                ))
    
    def _is_likely_plural(self, func_name: str) -> bool:
        """Determine if function name is likely plural"""
        # RP pluralization patterns
        plural_patterns = [
            r'.*images$', r'.*videos$', r'.*files$', r'.*sounds$',
            r'.*arrays$', r'.*tensors$', r'.*paths$', r'.*items$',
            r'.*functions$', r'.*operations$', r'.*processes$'
        ]
        
        return any(re.match(pattern, func_name) for pattern in plural_patterns)
    
    def _get_singular_form(self, func_name: str) -> str:
        """Convert plural function name to singular"""
        conversions = [
            (r'(.*)images$', r'\1image'),
            (r'(.*)videos$', r'\1video'),  
            (r'(.*)files$', r'\1file'),
            (r'(.*)sounds$', r'\1sound'),
            (r'(.*)arrays$', r'\1array'),
            (r'(.*)tensors$', r'\1tensor'),
            (r'(.*)paths$', r'\1path'),
            (r'(.*)items$', r'\1item'),
            (r'(.*)functions$', r'\1function'),
            (r'(.*)operations$', r'\1operation'),
            (r'(.*)processes$', r'\1process'),
            (r'(.*)s$', r'\1')  # General s removal
        ]
        
        for pattern, replacement in conversions:
            if re.match(pattern, func_name):
                return re.sub(pattern, replacement, func_name)
                
        return func_name
    
    def _get_plural_form(self, func_name: str) -> str:
        """Convert singular function name to plural"""
        # Common plural patterns in RP
        if func_name.endswith('image'):
            return func_name[:-5] + 'images'
        elif func_name.endswith('video'):
            return func_name[:-5] + 'videos'
        elif func_name.endswith('file'):
            return func_name[:-4] + 'files'
        elif func_name.endswith('sound'):
            return func_name[:-5] + 'sounds'
        elif func_name.endswith('array'):
            return func_name[:-5] + 'arrays'
        elif func_name.endswith('tensor'):
            return func_name[:-6] + 'tensors'
        elif func_name.endswith('path'):
            return func_name[:-4] + 'paths'
        elif func_name.endswith('y'):
            return func_name[:-1] + 'ies'
        else:
            return func_name + 's'
    
    def _should_have_plural(self, func_name: str) -> bool:
        """Determine if function should have a plural variant"""
        # Functions that typically work with single items and could benefit from plural versions
        likely_single_item_patterns = [
            'load_', 'save_', 'process_', 'convert_', 'resize_', 'crop_',
            'rotate_', 'filter_', 'transform_', 'analyze_', 'extract_',
            'compress_', 'decompress_', 'encode_', 'decode_'
        ]
        
        # Skip if already has obvious collection handling
        if any(word in func_name for word in ['batch', 'all', 'multiple', 'list', 'collection']):
            return False
            
        return any(func_name.startswith(pattern) for pattern in likely_single_item_patterns)
    
    def _should_have_singular(self, func_name: str) -> bool:
        """Determine if plural function should have singular variant"""
        # Most plural functions should have singular variants
        return True
    
    def _calculate_pluralization_priority(self, func_name: str) -> int:
        """Calculate priority for pluralization suggestions"""
        priority = 5  # Base priority
        
        # Higher priority for common operations
        high_priority_patterns = ['load_', 'save_', 'resize_', 'crop_', 'process_']
        if any(func_name.startswith(pattern) for pattern in high_priority_patterns):
            priority += 3
            
        # Higher priority for image/video functions (RP's strength)
        if any(word in func_name for word in ['image', 'video', 'sound']):
            priority += 2
            
        return min(priority, 10)
    
    def _check_symmetric_pairs(self):
        """Check for missing symmetric function pairs"""
        for pair_pattern in self.symmetric_pairs:
            func_a_pattern, func_b_pattern = pair_pattern
            
            # Find functions matching pattern A
            matching_a = [f for f in self.functions if re.match(func_a_pattern, f)]
            
            for func_a in matching_a:
                # Generate expected pair function name
                expected_func_b = re.sub(func_a_pattern, func_b_pattern, func_a)
                
                if expected_func_b not in self.functions:
                    self.issues.append(ConsistencyIssue(
                        issue_type=InconsistencyType.ASYMMETRIC_PAIR,
                        function_name=func_a,
                        description=f"Function '{func_a}' exists but missing symmetric pair '{expected_func_b}'",
                        suggestion=f"Consider implementing '{expected_func_b}' to complete the symmetric pair",
                        related_functions=[func_a],
                        priority=7
                    ))
    
    def _check_naming_consistency(self):
        """Check for naming consistency issues"""
        # Group functions by verb-noun patterns
        verb_groups = defaultdict(list)
        
        for func_name in self.functions:
            verb = self._extract_verb(func_name)
            if verb:
                verb_groups[verb].append(func_name)
        
        # Check for inconsistent naming within verb groups
        for verb, functions in verb_groups.items():
            if len(functions) > 3:  # Only check groups with multiple functions
                self._check_verb_group_consistency(verb, functions)
    
    def _check_parameter_consistency(self):
        """Check for parameter consistency across similar functions"""
        # Group functions by similar patterns
        similar_groups = self._group_similar_functions()
        
        for group_name, functions in similar_groups.items():
            if len(functions) < 2:
                continue
                
            # Check parameter consistency within group
            common_params = self._find_common_parameters(functions)
            inconsistent_params = self._find_inconsistent_parameters(functions, common_params)
            
            for func_name, missing_params in inconsistent_params.items():
                if missing_params:
                    self.issues.append(ConsistencyIssue(
                        issue_type=InconsistencyType.INCONSISTENT_PARAMETERS,
                        function_name=func_name,
                        description=f"Function missing common parameters: {', '.join(missing_params)}",
                        suggestion=f"Consider adding parameters: {', '.join(missing_params)} for consistency",
                        related_functions=[f for f in functions if f != func_name],
                        priority=4
                    ))
    
    def _check_via_variant_consistency(self):
        """Check for missing _via_ variants where they might be useful"""
        # Functions that could benefit from multiple backend implementations
        backend_candidates = []
        
        for func_name in self.functions:
            if (any(word in func_name for word in ['load', 'save', 'convert', 'resize', 'process']) and
                not func_name.startswith('_') and
                '_via_' not in func_name):
                
                # Check if it already has _via_ variants
                has_variants = any(f.startswith(f'{func_name}_via_') or f.startswith(f'_{func_name}_via_') 
                                 for f in self.functions)
                
                if not has_variants and self._could_benefit_from_variants(func_name):
                    backend_candidates.append(func_name)
        
        for func_name in backend_candidates:
            self.issues.append(ConsistencyIssue(
                issue_type=InconsistencyType.MISSING_VIA_VARIANT,
                function_name=func_name,
                description=f"Function could benefit from backend-specific _via_ variants",
                suggestion=f"Consider implementing {func_name}_via_[backend] variants for different backends",
                related_functions=[],
                priority=3
            ))
    
    def _could_benefit_from_variants(self, func_name: str) -> bool:
        """Determine if function could benefit from _via_ variants"""
        # Functions dealing with common formats that have multiple libraries
        benefit_patterns = [
            'image', 'video', 'audio', 'convert', 'resize', 'compress',
            'decode', 'encode', 'process', 'transform'
        ]
        return any(pattern in func_name for pattern in benefit_patterns)
    
    def _load_verb_noun_patterns(self) -> List[str]:
        """Load common verb patterns in RP"""
        return [
            'load_', 'save_', 'get_', 'set_', 'create_', 'delete_',
            'copy_', 'move_', 'resize_', 'crop_', 'rotate_', 'scale_',
            'convert_', 'transform_', 'process_', 'analyze_', 'extract_',
            'compress_', 'decompress_', 'encode_', 'decode_', 'validate_'
        ]
    
    def _load_expected_symmetric_pairs(self) -> List[Tuple[str, str]]:
        """Load expected symmetric function pairs"""
        return [
            (r'(.*)_to_clipboard$', r'\1_from_clipboard'),
            (r'(.*)_to_bytes$', r'\1_from_bytes'),
            (r'(.*)_to_string$', r'\1_from_string'),
            (r'(.*)_to_file$', r'\1_from_file'),
            (r'encode_(.*)$', r'decode_\1'),
            (r'compress_(.*)$', r'decompress_\1'),
            (r'serialize_(.*)$', r'deserialize_\1'),
            (r'pack_(.*)$', r'unpack_\1'),
        ]
    
    def _extract_verb(self, func_name: str) -> Optional[str]:
        """Extract verb from function name"""
        for verb in self.verb_noun_patterns:
            if func_name.startswith(verb):
                return verb.rstrip('_')
        return None
    
    def _check_verb_group_consistency(self, verb: str, functions: List[str]):
        """Check consistency within a verb group"""
        # This could check for consistent parameter patterns, naming conventions, etc.
        pass
    
    def _group_similar_functions(self) -> Dict[str, List[str]]:
        """Group functions by similarity"""
        groups = defaultdict(list)
        
        for func_name in self.functions:
            # Group by verb prefix
            verb = self._extract_verb(func_name)
            if verb:
                groups[f"{verb}_functions"].append(func_name)
                
            # Group by domain (image, video, audio, etc.)
            domains = ['image', 'video', 'audio', 'file', 'string', 'array', 'tensor']
            for domain in domains:
                if domain in func_name:
                    groups[f"{domain}_functions"].append(func_name)
        
        return groups
    
    def _find_common_parameters(self, functions: List[str]) -> Set[str]:
        """Find parameters common across multiple functions"""
        if not functions:
            return set()
            
        # Get parameter sets for each function
        param_sets = []
        for func_name in functions:
            if func_name in self.function_signatures:
                params = set(self.function_signatures[func_name]['params'])
                param_sets.append(params)
        
        if not param_sets:
            return set()
            
        # Find parameters that appear in at least half the functions
        all_params = set()
        for param_set in param_sets:
            all_params.update(param_set)
            
        common_params = set()
        for param in all_params:
            count = sum(1 for param_set in param_sets if param in param_set)
            if count >= len(param_sets) / 2:
                common_params.add(param)
                
        return common_params
    
    def _find_inconsistent_parameters(self, functions: List[str], 
                                    common_params: Set[str]) -> Dict[str, List[str]]:
        """Find functions missing common parameters"""
        inconsistent = {}
        
        for func_name in functions:
            if func_name in self.function_signatures:
                func_params = set(self.function_signatures[func_name]['params'])
                missing = common_params - func_params
                if missing:
                    inconsistent[func_name] = list(missing)
        
        return inconsistent
    
    def generate_consistency_report(self) -> str:
        """Generate comprehensive consistency report"""
        if not self.issues:
            self.analyze_consistency()
            
        report = "=== RP Function Consistency Analysis ===\n\n"
        
        # Summary by issue type
        issue_counts = Counter(issue.issue_type for issue in self.issues)
        
        report += "Issue Summary:\n"
        for issue_type, count in issue_counts.items():
            report += f"  {issue_type.value}: {count} issues\n"
            
        report += f"\nTotal Issues: {len(self.issues)}\n\n"
        
        # Top priority issues
        report += "=== High Priority Issues ===\n"
        high_priority = [issue for issue in self.issues if issue.priority >= 7]
        
        for issue in high_priority[:15]:  # Top 15
            report += f"\n{issue.function_name} [{issue.issue_type.value}] (Priority: {issue.priority}):\n"
            report += f"  {issue.description}\n"
            report += f"  Suggestion: {issue.suggestion}\n"
            
        return report

def generate_suggestions_file(tracker: RPConsistencyTracker, 
                            output_path: str = "/opt/homebrew/lib/python3.10/site-packages/rp/management/suggestions/consistency_suggestions.md"):
    """Generate a markdown file with all consistency suggestions"""
    
    if not tracker.issues:
        tracker.analyze_consistency()
    
    # Group issues by type
    issues_by_type = defaultdict(list)
    for issue in tracker.issues:
        issues_by_type[issue.issue_type].append(issue)
    
    content = "# RP Function Consistency Suggestions\n\n"
    content += f"Generated from analysis of {len(tracker.functions)} functions.\n\n"
    
    for issue_type, issues in issues_by_type.items():
        content += f"## {issue_type.value.replace('_', ' ').title()} ({len(issues)} issues)\n\n"
        
        # Sort by priority
        issues.sort(key=lambda x: x.priority, reverse=True)
        
        for issue in issues:
            content += f"### {issue.function_name} (Priority: {issue.priority})\n"
            content += f"**Issue**: {issue.description}\n\n"
            content += f"**Suggestion**: {issue.suggestion}\n\n"
            if issue.related_functions:
                content += f"**Related Functions**: {', '.join(issue.related_functions)}\n\n"
            content += "---\n\n"
    
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"Consistency suggestions saved to: {output_path}")

def main():
    tracker = RPConsistencyTracker()
    issues = tracker.analyze_consistency()
    
    # Generate report
    report = tracker.generate_consistency_report()
    print(report)
    
    # Generate suggestions file
    generate_suggestions_file(tracker)
    
    print(f"\nFound {len(issues)} consistency issues total")
    
    # Show some examples
    print("\n=== Example Pluralization Opportunities ===")
    plural_issues = [i for i in issues if i.issue_type == InconsistencyType.MISSING_PLURAL]
    for issue in plural_issues[:5]:
        print(f"  {issue.function_name} -> should have {tracker._get_plural_form(issue.function_name)}")

if __name__ == "__main__":
    main()