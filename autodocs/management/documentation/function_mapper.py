#!/opt/homebrew/opt/python@3.10/bin/python3.10
"""
RP Function Relationship Mapper
Analyzes r.py to extract function relationships, dependencies, and clusters.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter

class RPFunctionMapper:
    def __init__(self, rp_path: str = "/opt/homebrew/lib/python3.10/site-packages/rp/r.py"):
        self.rp_path = rp_path
        self.functions = {}  # function_name -> AST node
        self.function_calls = defaultdict(set)  # function_name -> set of called functions
        self.function_callers = defaultdict(set)  # function_name -> set of functions that call it
        self.aliases = defaultdict(set)  # function_name -> set of alias names
        self.via_variants = defaultdict(set)  # base_function -> set of _via_ variants
        self.multiplexing_patterns = {}  # base_function -> list of implementations
        
    def analyze_rp_file(self):
        """Parse r.py and extract all function relationships"""
        with open(self.rp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse AST
        tree = ast.parse(content)
        
        # Extract all function definitions
        self._extract_functions(tree)
        
        # Analyze function calls within each function
        self._analyze_function_calls(tree)
        
        # Detect aliases and patterns
        self._detect_aliases(content)
        self._detect_via_variants()
        self._detect_multiplexing_patterns()
        
        return self._generate_analysis_report()
    
    def _extract_functions(self, tree):
        """Extract all function definitions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.functions[node.name] = node
    
    def _analyze_function_calls(self, tree):
        """Analyze which functions call which other functions"""
        for func_name, func_node in self.functions.items():
            called_functions = set()
            
            # Walk through function body looking for function calls
            for node in ast.walk(func_node):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        # Direct function call: func()
                        called_func = node.func.id
                        if called_func in self.functions:
                            called_functions.add(called_func)
                    elif isinstance(node.func, ast.Attribute):
                        # Method call or module.func(): obj.method() or rp.func()
                        if hasattr(node.func, 'attr'):
                            called_func = node.func.attr
                            if called_func in self.functions:
                                called_functions.add(called_func)
            
            self.function_calls[func_name] = called_functions
            
            # Build reverse mapping (callers)
            for called_func in called_functions:
                self.function_callers[called_func].add(func_name)
    
    def _detect_aliases(self, content):
        """Detect function aliases (func_name = other_func)"""
        # Pattern: function_name = other_function_name
        alias_pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*$'
        
        for line in content.split('\n'):
            line = line.strip()
            match = re.match(alias_pattern, line)
            if match:
                alias_name, original_name = match.groups()
                if original_name in self.functions:
                    self.aliases[original_name].add(alias_name)
    
    def _detect_via_variants(self):
        """Detect _via_ implementation variants"""
        for func_name in self.functions:
            if '_via_' in func_name:
                # Extract base function name
                base_name = func_name.split('_via_')[0]
                if base_name.startswith('_'):
                    base_name = base_name[1:]  # Remove leading underscore
                
                self.via_variants[base_name].add(func_name)
    
    def _detect_multiplexing_patterns(self):
        """Detect multiplexing patterns where base functions dispatch to specific ones"""
        for func_name, func_node in self.functions.items():
            # Look for functions that have multiple if/elif chains calling other functions
            if_chains = self._find_if_chains(func_node)
            
            if len(if_chains) >= 3:  # Multiplexing pattern likely
                self.multiplexing_patterns[func_name] = if_chains
    
    def _find_if_chains(self, func_node):
        """Find if/elif chains that call different functions"""
        called_functions = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.If):
                # Extract function calls in if/elif branches
                for child in ast.walk(node):
                    if isinstance(child, ast.Return) and isinstance(child.value, ast.Call):
                        if isinstance(child.value.func, ast.Name):
                            called_functions.append(child.value.func.id)
        
        return called_functions
    
    def get_function_cluster(self, func_name: str, depth: int = 2) -> Set[str]:
        """Get all related functions within depth levels"""
        cluster = {func_name}
        to_explore = {func_name}
        
        for _ in range(depth):
            new_functions = set()
            for f in to_explore:
                # Add functions this one calls
                new_functions.update(self.function_calls.get(f, set()))
                # Add functions that call this one
                new_functions.update(self.function_callers.get(f, set()))
                # Add aliases
                new_functions.update(self.aliases.get(f, set()))
                # Add _via_ variants
                new_functions.update(self.via_variants.get(f, set()))
            
            to_explore = new_functions - cluster
            cluster.update(new_functions)
        
        return cluster
    
    def get_function_context(self, func_name: str) -> Dict:
        """Get complete context for a function for minion documentation"""
        return {
            'function_name': func_name,
            'calls': list(self.function_calls.get(func_name, set())),
            'called_by': list(self.function_callers.get(func_name, set())),
            'aliases': list(self.aliases.get(func_name, set())),
            'via_variants': list(self.via_variants.get(func_name, set())),
            'cluster': list(self.get_function_cluster(func_name, depth=1)),
            'multiplexing': self.multiplexing_patterns.get(func_name, []),
            'is_via_variant': '_via_' in func_name,
            'is_private': func_name.startswith('_')
        }
    
    def _generate_analysis_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        return {
            'total_functions': len(self.functions),
            'functions_with_calls': len([f for f in self.function_calls if self.function_calls[f]]),
            'total_aliases': sum(len(aliases) for aliases in self.aliases.values()),
            'via_variants': len([f for f in self.functions if '_via_' in f]),
            'multiplexing_functions': len(self.multiplexing_patterns),
            'most_called_functions': Counter(
                func for calls in self.function_calls.values() for func in calls
            ).most_common(10),
            'most_calling_functions': Counter(
                func for func, calls in self.function_calls.items() if calls
            ).most_common(10)
        }

def generate_minion_work_packages(mapper: RPFunctionMapper, package_size: int = 10) -> List[Dict]:
    """Generate work packages for minion agents with full context"""
    all_functions = list(mapper.functions.keys())
    packages = []
    
    # Group functions into clusters
    processed = set()
    
    for func_name in all_functions:
        if func_name in processed:
            continue
            
        # Get function cluster
        cluster = mapper.get_function_cluster(func_name, depth=1)
        cluster = cluster - processed  # Remove already processed
        
        if len(cluster) == 0:
            continue
            
        # Limit cluster size to package_size
        cluster_list = list(cluster)[:package_size]
        processed.update(cluster_list)
        
        # Create work package with context
        package = {
            'package_id': len(packages) + 1,
            'functions': cluster_list,
            'context': {func: mapper.get_function_context(func) for func in cluster_list},
            'priority': _calculate_priority(cluster_list, mapper),
            'estimated_work_hours': len(cluster_list) * 0.5  # 30 min per function
        }
        
        packages.append(package)
    
    # Sort by priority
    packages.sort(key=lambda x: x['priority'], reverse=True)
    return packages

def _calculate_priority(functions: List[str], mapper: RPFunctionMapper) -> int:
    """Calculate priority score for a function cluster"""
    score = 0
    
    for func in functions:
        # High priority for functions called by many others
        score += len(mapper.function_callers.get(func, set())) * 3
        
        # High priority for public functions
        if not func.startswith('_'):
            score += 10
            
        # High priority for multiplexing base functions
        if func in mapper.multiplexing_patterns:
            score += 20
            
        # Medium priority for _via_ variants
        if '_via_' in func:
            score += 5
            
        # High priority for functions with aliases (popular)
        score += len(mapper.aliases.get(func, set())) * 2
    
    return score

if __name__ == "__main__":
    mapper = RPFunctionMapper()
    analysis = mapper.analyze_rp_file()
    
    print("=== RP Function Analysis ===")
    print(f"Total functions: {analysis['total_functions']}")
    print(f"Functions with calls: {analysis['functions_with_calls']}")
    print(f"Total aliases: {analysis['total_aliases']}")
    print(f"_via_ variants: {analysis['via_variants']}")
    print(f"Multiplexing functions: {analysis['multiplexing_functions']}")
    
    print("\n=== Most Called Functions ===")
    for func, count in analysis['most_called_functions']:
        print(f"  {func}: {count} calls")
    
    # Generate work packages
    packages = generate_minion_work_packages(mapper)
    print(f"\n=== Generated {len(packages)} Work Packages ===")
    
    # Show first few packages
    for i, package in enumerate(packages[:3]):
        print(f"\nPackage {package['package_id']} (Priority: {package['priority']}):")
        print(f"  Functions: {package['functions'][:5]}{'...' if len(package['functions']) > 5 else ''}")
        print(f"  Estimated hours: {package['estimated_work_hours']}")