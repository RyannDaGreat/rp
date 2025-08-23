#!/opt/homebrew/opt/python@3.10/bin/python3.10
"""
RP Argument Consistency Tracker
Analyzes all function parameters to ensure naming consistency and track conventions
"""

import ast
import re
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict, Counter
from dataclasses import dataclass
import json

@dataclass
class ArgumentUsage:
    arg_name: str
    functions: List[str]  # Functions that use this argument
    types: Set[str]  # Detected types from defaults/annotations
    default_values: List[Any]  # Default values used
    descriptions: List[str]  # Extracted from docstrings
    common_patterns: List[str]  # Usage patterns

class RPArgumentTracker:
    def __init__(self, rp_path: str = "/opt/homebrew/lib/python3.10/site-packages/rp/r.py"):
        self.rp_path = rp_path
        self.argument_usage = {}  # arg_name -> ArgumentUsage
        self.function_args = {}  # function_name -> list of args
        self.inconsistencies = []
        
        # Known RP argument conventions (from documentation/analysis)
        self.standard_args = {
            'strict': {
                'type': 'bool|None',
                'default': True,
                'description': 'Error handling: True=raise error, False=skip, None=return None',
                'valid_values': [True, False, None]
            },
            'show_progress': {
                'type': 'bool|str', 
                'default': False,
                'description': "Progress display: True/False/'eta'/'tqdm'",
                'valid_values': [True, False, 'eta', 'tqdm']
            },
            'num_threads': {
                'type': 'int|None',
                'default': None,
                'description': 'Number of parallel threads (None=auto)',
                'valid_values': 'positive integer or None'
            },
            'use_cache': {
                'type': 'bool',
                'default': False, 
                'description': 'Enable caching of results',
                'valid_values': [True, False]
            },
            'copy': {
                'type': 'bool',
                'default': True,
                'description': 'Return copy vs in-place modification',
                'valid_values': [True, False]
            },
            'shutup': {
                'type': 'bool',
                'default': False,
                'description': 'Suppress output/warnings',
                'valid_values': [True, False]
            }
        }
        
    def analyze_all_arguments(self) -> Dict[str, ArgumentUsage]:
        """Analyze argument usage across all RP functions"""
        print("Loading function definitions...")
        functions = self._load_all_functions()
        
        print("Extracting argument information...")
        for func_name, func_node in functions.items():
            self._analyze_function_arguments(func_name, func_node)
            
        print("Building argument usage database...")
        self._build_argument_usage_db()
        
        print("Detecting inconsistencies...")
        self._detect_argument_inconsistencies()
        
        return self.argument_usage
    
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
    
    def _analyze_function_arguments(self, func_name: str, func_node: ast.FunctionDef):
        """Analyze arguments for a single function"""
        args_info = []
        
        # Get regular arguments
        for i, arg in enumerate(func_node.args.args):
            arg_info = {
                'name': arg.arg,
                'position': i,
                'type_annotation': self._get_type_annotation(arg),
                'default_value': None,
                'is_keyword_only': False
            }
            
            # Check for default value
            defaults_start = len(func_node.args.args) - len(func_node.args.defaults)
            if i >= defaults_start:
                default_idx = i - defaults_start
                arg_info['default_value'] = self._extract_default_value(
                    func_node.args.defaults[default_idx]
                )
                
            args_info.append(arg_info)
        
        # Get keyword-only arguments
        for i, arg in enumerate(func_node.args.kwonlyargs):
            arg_info = {
                'name': arg.arg,
                'position': len(func_node.args.args) + i,
                'type_annotation': self._get_type_annotation(arg),
                'default_value': None,
                'is_keyword_only': True
            }
            
            # Check for default value
            if i < len(func_node.args.kw_defaults):
                if func_node.args.kw_defaults[i] is not None:
                    arg_info['default_value'] = self._extract_default_value(
                        func_node.args.kw_defaults[i]
                    )
                        
            args_info.append(arg_info)
        
        # Add varargs and kwargs info
        if func_node.args.vararg:
            args_info.append({
                'name': func_node.args.vararg.arg,
                'position': -1,
                'is_varargs': True,
                'type_annotation': self._get_type_annotation(func_node.args.vararg)
            })
            
        if func_node.args.kwarg:
            args_info.append({
                'name': func_node.args.kwarg.arg, 
                'position': -2,
                'is_kwargs': True,
                'type_annotation': self._get_type_annotation(func_node.args.kwarg)
            })
        
        self.function_args[func_name] = args_info
    
    def _get_type_annotation(self, arg_node) -> Optional[str]:
        """Extract type annotation from argument"""
        if hasattr(arg_node, 'annotation') and arg_node.annotation:
            return ast.unparse(arg_node.annotation)
        return None
    
    def _extract_default_value(self, default_node) -> Any:
        """Extract default value from AST node"""
        try:
            if isinstance(default_node, ast.Constant):
                return default_node.value
            elif isinstance(default_node, ast.NameConstant):  # Python < 3.8
                return default_node.value  
            elif isinstance(default_node, ast.Name):
                return default_node.id  # Return variable name
            elif isinstance(default_node, ast.Str):  # String literal
                return default_node.s
            elif isinstance(default_node, ast.Num):  # Number literal
                return default_node.n
            else:
                return ast.unparse(default_node)  # Fallback to source code
        except:
            return "<complex_default>"
    
    def _build_argument_usage_db(self):
        """Build database of argument usage patterns"""
        arg_data = defaultdict(lambda: {
            'functions': [],
            'types': set(),
            'defaults': [],
            'descriptions': []
        })
        
        # Collect usage data
        for func_name, args_info in self.function_args.items():
            for arg_info in args_info:
                arg_name = arg_info['name']
                
                # Skip special arguments
                if arg_name in ['self', 'cls'] or arg_info.get('is_varargs') or arg_info.get('is_kwargs'):
                    continue
                    
                arg_data[arg_name]['functions'].append(func_name)
                
                if arg_info.get('type_annotation'):
                    arg_data[arg_name]['types'].add(arg_info['type_annotation'])
                    
                if arg_info.get('default_value') is not None:
                    arg_data[arg_name]['defaults'].append(arg_info['default_value'])
        
        # Extract descriptions from docstrings
        self._extract_argument_descriptions()
        
        # Create ArgumentUsage objects
        for arg_name, data in arg_data.items():
            self.argument_usage[arg_name] = ArgumentUsage(
                arg_name=arg_name,
                functions=data['functions'],
                types=data['types'],
                default_values=list(set(data['defaults'])),
                descriptions=data['descriptions'],
                common_patterns=self._detect_usage_patterns(arg_name, data['functions'])
            )
    
    def _extract_argument_descriptions(self):
        """Extract argument descriptions from function docstrings"""
        # This would parse docstrings to find parameter descriptions
        # Implementation would use regex to find Args:, Parameters:, etc.
        pass
    
    def _detect_usage_patterns(self, arg_name: str, functions: List[str]) -> List[str]:
        """Detect common usage patterns for an argument"""
        patterns = []
        
        # Pattern: argument used in similar function families
        function_families = defaultdict(list)
        for func in functions:
            # Group by verb prefix
            if '_' in func:
                prefix = func.split('_')[0]
                function_families[prefix].append(func)
        
        for family, family_funcs in function_families.items():
            if len(family_funcs) >= 3:
                patterns.append(f"Common in {family}_* functions ({len(family_funcs)} uses)")
        
        return patterns
    
    def _detect_argument_inconsistencies(self):
        """Detect inconsistent argument usage"""
        self.inconsistencies = []
        
        for arg_name, usage in self.argument_usage.items():
            if arg_name in self.standard_args:
                self._check_standard_argument_consistency(arg_name, usage)
            else:
                self._check_general_argument_consistency(arg_name, usage)
    
    def _check_standard_argument_consistency(self, arg_name: str, usage: ArgumentUsage):
        """Check consistency of standard RP arguments"""
        standard = self.standard_args[arg_name]
        
        # Check default values consistency
        inconsistent_defaults = []
        for default in usage.default_values:
            if standard['valid_values'] != 'positive integer or None':
                if default not in standard['valid_values']:
                    inconsistent_defaults.append(default)
        
        if inconsistent_defaults:
            self.inconsistencies.append({
                'type': 'inconsistent_standard_defaults',
                'arg_name': arg_name,
                'expected': standard['valid_values'],
                'found': inconsistent_defaults,
                'functions': usage.functions[:5],  # Sample functions
                'severity': 'high'
            })
        
        # Check if default should be standardized
        if len(set(usage.default_values)) > 1:
            self.inconsistencies.append({
                'type': 'multiple_defaults',
                'arg_name': arg_name,
                'defaults_found': usage.default_values,
                'recommended_default': standard['default'],
                'functions': usage.functions[:10],
                'severity': 'medium'
            })
    
    def _check_general_argument_consistency(self, arg_name: str, usage: ArgumentUsage):
        """Check consistency of general arguments"""
        # Check for similar argument names that might be inconsistent
        similar_args = self._find_similar_argument_names(arg_name)
        
        if similar_args:
            self.inconsistencies.append({
                'type': 'similar_argument_names',
                'arg_name': arg_name,
                'similar_names': similar_args,
                'suggestion': f"Consider standardizing to one name",
                'severity': 'low'
            })
        
        # Check for widely used arguments that might need standardization
        if len(usage.functions) >= 10 and len(set(usage.default_values)) > 1:
            self.inconsistencies.append({
                'type': 'widely_used_inconsistent',
                'arg_name': arg_name,
                'usage_count': len(usage.functions),
                'different_defaults': usage.default_values,
                'suggestion': f"Consider standardizing default value",
                'severity': 'medium'
            })
    
    def _find_similar_argument_names(self, arg_name: str) -> List[str]:
        """Find similar argument names that might be inconsistent"""
        similar = []
        
        # Check for common variations
        variations = [
            (r'num_(.+)', r'number_of_\1', r'n_\1'),  # num_threads vs number_of_threads
            (r'(.+)_flag', r'enable_\1', r'use_\1'),  # debug_flag vs enable_debug
            (r'show_(.+)', r'\1_progress', r'display_\1'),  # show_progress vs progress_bar
        ]
        
        for usage_arg in self.argument_usage:
            if usage_arg != arg_name:
                # Check edit distance and semantic similarity
                if self._are_similar_args(arg_name, usage_arg):
                    similar.append(usage_arg)
        
        return similar[:5]  # Limit to avoid noise
    
    def _are_similar_args(self, arg1: str, arg2: str) -> bool:
        """Check if two argument names are semantically similar"""
        # Simple heuristic - could be improved
        words1 = set(re.split(r'[_-]', arg1.lower()))
        words2 = set(re.split(r'[_-]', arg2.lower()))
        
        # Check for shared words
        shared = words1.intersection(words2)
        if len(shared) >= 1 and (len(words1) <= 3 or len(words2) <= 3):
            return True
            
        # Check for common patterns
        patterns = [
            ('num', 'number'), ('show', 'display'), ('use', 'enable'),
            ('prog', 'progress'), ('temp', 'temporary'), ('max', 'maximum')
        ]
        
        for short, long in patterns:
            if (short in words1 and long in words2) or (long in words1 and short in words2):
                return True
                
        return False
    
    def generate_argument_conventions_db(self, output_path: str):
        """Generate comprehensive argument conventions database"""
        db = {
            'metadata': {
                'total_functions_analyzed': len(self.function_args),
                'total_unique_arguments': len(self.argument_usage),
                'standard_arguments': list(self.standard_args.keys()),
                'inconsistencies_found': len(self.inconsistencies)
            },
            'standard_arguments': self.standard_args,
            'argument_usage': {},
            'inconsistencies': self.inconsistencies,
            'recommendations': self._generate_recommendations()
        }
        
        # Convert ArgumentUsage objects to dicts
        for arg_name, usage in self.argument_usage.items():
            db['argument_usage'][arg_name] = {
                'arg_name': usage.arg_name,
                'usage_count': len(usage.functions),
                'sample_functions': usage.functions[:10],
                'types_seen': list(usage.types),
                'default_values': usage.default_values,
                'common_patterns': usage.common_patterns,
                'is_standard': arg_name in self.standard_args
            }
        
        with open(output_path, 'w') as f:
            json.dump(db, f, indent=2, default=str)
        
        print(f"Argument conventions database saved to: {output_path}")
        return db
    
    def _generate_recommendations(self) -> List[Dict]:
        """Generate recommendations for improving argument consistency"""
        recommendations = []
        
        # Find arguments that should be standardized
        for arg_name, usage in self.argument_usage.items():
            if len(usage.functions) >= 5 and arg_name not in self.standard_args:
                # Check if it follows a standard pattern
                if any(pattern in arg_name for pattern in ['progress', 'cache', 'thread', 'strict']):
                    recommendations.append({
                        'type': 'candidate_for_standardization',
                        'arg_name': arg_name,
                        'usage_count': len(usage.functions),
                        'current_defaults': usage.default_values,
                        'recommendation': f'Consider adding {arg_name} to standard arguments'
                    })
        
        # Find missing standard arguments
        for func_name, args_info in self.function_args.items():
            func_arg_names = [arg['name'] for arg in args_info]
            
            # Check if function could benefit from standard arguments
            if self._function_could_use_standard_args(func_name, func_arg_names):
                missing_standards = []
                for std_arg in self.standard_args:
                    if std_arg not in func_arg_names:
                        if self._should_have_standard_arg(func_name, std_arg):
                            missing_standards.append(std_arg)
                
                if missing_standards:
                    recommendations.append({
                        'type': 'missing_standard_arguments',
                        'function': func_name,
                        'missing_args': missing_standards,
                        'recommendation': f'Consider adding standard arguments: {", ".join(missing_standards)}'
                    })
        
        return recommendations
    
    def _function_could_use_standard_args(self, func_name: str, args: List[str]) -> bool:
        """Check if function could benefit from standard arguments"""
        # Functions that load/process data could use strict, use_cache, show_progress
        if any(pattern in func_name for pattern in ['load_', 'save_', 'process_', 'download_']):
            return True
        return False
    
    def _should_have_standard_arg(self, func_name: str, std_arg: str) -> bool:
        """Check if specific function should have a specific standard argument"""
        if std_arg == 'strict' and any(pattern in func_name for pattern in ['load_', 'process_']):
            return True
        elif std_arg == 'show_progress' and any(pattern in func_name for pattern in ['load_', 'download_', 'process_']):
            return True
        elif std_arg == 'use_cache' and any(pattern in func_name for pattern in ['load_', 'get_']):
            return True
        return False
    
    def generate_inconsistency_report(self) -> str:
        """Generate human-readable inconsistency report"""
        report = "=== RP Argument Consistency Report ===\n\n"
        
        # Summary
        report += f"Functions analyzed: {len(self.function_args)}\n"
        report += f"Unique arguments found: {len(self.argument_usage)}\n"
        report += f"Inconsistencies detected: {len(self.inconsistencies)}\n\n"
        
        # Standard argument usage
        report += "=== Standard Argument Usage ===\n"
        for std_arg in self.standard_args:
            if std_arg in self.argument_usage:
                usage = self.argument_usage[std_arg]
                report += f"{std_arg}: used in {len(usage.functions)} functions\n"
                if usage.default_values:
                    report += f"  Default values: {usage.default_values}\n"
            else:
                report += f"{std_arg}: NOT USED in any function\n"
        report += "\n"
        
        # Top inconsistencies
        high_severity = [i for i in self.inconsistencies if i.get('severity') == 'high']
        if high_severity:
            report += "=== High Priority Inconsistencies ===\n"
            for issue in high_severity[:10]:
                report += f"{issue['arg_name']} ({issue['type']}):\n"
                if 'expected' in issue:
                    report += f"  Expected: {issue['expected']}\n"
                if 'found' in issue:
                    report += f"  Found: {issue['found']}\n"
                if 'functions' in issue:
                    report += f"  Sample functions: {', '.join(issue['functions'][:3])}\n"
                report += "\n"
        
        # Most used arguments
        report += "=== Most Frequently Used Arguments ===\n"
        sorted_args = sorted(self.argument_usage.items(), 
                           key=lambda x: len(x[1].functions), reverse=True)
        
        for arg_name, usage in sorted_args[:15]:
            report += f"{arg_name}: {len(usage.functions)} functions\n"
            if usage.default_values:
                report += f"  Common defaults: {usage.default_values[:3]}\n"
        
        return report

def main():
    tracker = RPArgumentTracker()
    tracker.analyze_all_arguments()
    
    # Generate databases and reports
    db = tracker.generate_argument_conventions_db(
        "/opt/homebrew/lib/python3.10/site-packages/rp/management/consistency/argument_conventions.json"
    )
    
    report = tracker.generate_inconsistency_report()
    print(report)
    
    # Save report
    with open("/opt/homebrew/lib/python3.10/site-packages/rp/management/consistency/argument_report.txt", 'w') as f:
        f.write(report)
    
    print(f"\nDatabase saved with {db['metadata']['total_unique_arguments']} arguments analyzed")

if __name__ == "__main__":
    main()