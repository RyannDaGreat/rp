#!/opt/homebrew/opt/python@3.10/bin/python3.10
"""
Minion Work Package Generator
Creates comprehensive work packages for minion agents with full context and documentation status
"""

import json
from typing import Dict, List, Set, Tuple
from pathlib import Path
from function_mapper import RPFunctionMapper
from docstring_analyzer import RPDocstringAnalyzer, DocQuality

class MinionPackager:
    def __init__(self, rp_path: str = "/opt/homebrew/lib/python3.10/site-packages/rp/r.py"):
        self.mapper = RPFunctionMapper(rp_path)
        self.doc_analyzer = RPDocstringAnalyzer(rp_path)
        self.packages = []
        
    def generate_comprehensive_packages(self, package_size: int = 8) -> List[Dict]:
        """Generate work packages with full context and documentation analysis"""
        # Analyze the codebase
        print("Analyzing function relationships...")
        self.mapper.analyze_rp_file()
        
        print("Analyzing documentation quality...")  
        self.doc_analyzer.analyze_all_docstrings()
        
        print("Generating contextualized work packages...")
        
        # Get high-priority functions based on importance and documentation gaps
        priority_functions = self._identify_priority_functions()
        
        # Create packages with related function clusters
        self.packages = self._create_contextualized_packages(priority_functions, package_size)
        
        return self.packages
    
    def _identify_priority_functions(self) -> List[Tuple[str, int]]:
        """Identify functions by priority score"""
        priorities = []
        
        for func_name in self.mapper.functions.keys():
            score = self._calculate_comprehensive_priority(func_name)
            priorities.append((func_name, score))
        
        # Sort by priority score (highest first)
        priorities.sort(key=lambda x: x[1], reverse=True)
        return priorities
    
    def _calculate_comprehensive_priority(self, func_name: str) -> int:
        """Calculate comprehensive priority considering multiple factors"""
        score = 0
        
        # Documentation urgency (highest priority)
        doc_analysis = self.doc_analyzer.analyses.get(func_name)
        if doc_analysis:
            if doc_analysis.quality == DocQuality.MISSING:
                score += 100
            elif doc_analysis.quality == DocQuality.BASIC:
                score += 50
            elif doc_analysis.quality == DocQuality.GOOD:
                score += 10
        
        # Function importance (how many functions call this one)
        callers = len(self.mapper.function_callers.get(func_name, set()))
        score += callers * 5
        
        # Public API functions get higher priority
        if not func_name.startswith('_'):
            score += 20
            
        # Core RP pattern functions get maximum priority
        core_patterns = ['fog', 'seq', 'scoop', 'par', 'pip_import', '_omni_load']
        if func_name in core_patterns:
            score += 200
            
        # Multiplexing base functions
        if func_name in self.mapper.multiplexing_patterns:
            score += 30
            
        # Functions with many aliases (popular functions)
        aliases = len(self.mapper.aliases.get(func_name, set()))
        score += aliases * 10
        
        # _via_ variants get medium priority (important but implementation details)
        if '_via_' in func_name:
            score += 15
        
        return score
    
    def _create_contextualized_packages(self, priority_functions: List[Tuple[str, int]], 
                                      package_size: int) -> List[Dict]:
        """Create work packages with full context"""
        packages = []
        processed = set()
        
        for func_name, priority_score in priority_functions:
            if func_name in processed:
                continue
                
            # Get function cluster (related functions)
            cluster = self.mapper.get_function_cluster(func_name, depth=1)
            
            # Filter out already processed functions
            cluster = cluster - processed
            
            if not cluster:
                continue
                
            # Limit cluster size and prioritize within cluster
            cluster_list = list(cluster)
            cluster_priorities = [(f, self._calculate_comprehensive_priority(f)) for f in cluster_list]
            cluster_priorities.sort(key=lambda x: x[1], reverse=True)
            
            # Take top functions from cluster up to package_size
            package_functions = [f for f, _ in cluster_priorities[:package_size]]
            processed.update(package_functions)
            
            # Create comprehensive work package
            package = self._create_work_package(package_functions, len(packages) + 1)
            packages.append(package)
        
        return packages
    
    def _create_work_package(self, functions: List[str], package_id: int) -> Dict:
        """Create a comprehensive work package with all context"""
        package = {
            'package_id': package_id,
            'functions': functions,
            'total_functions': len(functions),
            'estimated_hours': len(functions) * 0.75,  # 45 min per function with context
            'priority_score': sum(self._calculate_comprehensive_priority(f) for f in functions),
            'context': {},
            'documentation_status': {},
            'work_instructions': self._generate_work_instructions(functions),
            'quality_checklist': self._generate_quality_checklist(),
        }
        
        # Add detailed context for each function
        for func_name in functions:
            package['context'][func_name] = self.mapper.get_function_context(func_name)
            
            doc_analysis = self.doc_analyzer.analyses.get(func_name)
            if doc_analysis:
                package['documentation_status'][func_name] = {
                    'current_quality': doc_analysis.quality.value,
                    'current_docstring': doc_analysis.docstring_text[:200] + '...' if len(doc_analysis.docstring_text) > 200 else doc_analysis.docstring_text,
                    'suggestions': doc_analysis.suggestions,
                    'has_examples': doc_analysis.has_examples,
                    'has_parameters': doc_analysis.has_parameters,
                    'has_return_info': doc_analysis.has_return_info,
                }
        
        return package
    
    def _generate_work_instructions(self, functions: List[str]) -> List[str]:
        """Generate specific work instructions for the function cluster"""
        instructions = [
            "For each function in this package:",
            "1. Read the existing docstring (if any) and understand the function's purpose",
            "2. Examine the function's implementation to understand its behavior",
            "3. Check related functions (in context) to understand how they work together",
            "4. ENHANCE (don't replace) the docstring following the template:",
            "   - Keep original docstring if it exists",
            "   - Add 'Enhanced Documentation:' section with usage patterns",
            "   - Include concrete examples with >>> syntax", 
            "   - Document parameters and return values",
            "   - Note related functions and when to use vs alternatives",
            "   - Add relevant tags for searchability",
            "5. Test your examples to ensure they work",
            "6. Update the appropriate tag files in documentation/tags/",
        ]
        
        # Add specific instructions based on function patterns
        has_via_variants = any('_via_' in f for f in functions)
        has_multiplexing = any(f in self.mapper.multiplexing_patterns for f in functions)
        has_core_patterns = any(f in ['fog', 'seq', 'scoop', 'par'] for f in functions)
        
        if has_core_patterns:
            instructions.append("7. SPECIAL: These are core RP pattern functions - provide extensive examples showing how they enable RP's functional programming style")
            
        if has_via_variants:
            instructions.append("7. SPECIAL: Document backend-specific behavior and when to use each _via_ variant")
            
        if has_multiplexing:
            instructions.append("7. SPECIAL: Document the multiplexing pattern - how the base function dispatches to specific implementations")
            
        return instructions
    
    def _generate_quality_checklist(self) -> List[str]:
        """Generate quality assurance checklist"""
        return [
            "☐ Each function has enhanced docstring with purpose clearly explained",
            "☐ All parameters are documented with types and descriptions", 
            "☐ Return values are documented with types and descriptions",
            "☐ At least one concrete example with >>> syntax that actually runs",
            "☐ Related functions are mentioned with explanations",
            "☐ Usage patterns and common scenarios are described",
            "☐ Relevant tags added for searchability",
            "☐ Function added to appropriate tag files in documentation/tags/",
            "☐ Examples tested and confirmed working",
            "☐ Cross-references to multiplexing patterns or _via_ variants documented"
        ]
    
    def save_packages(self, output_dir: str = "/opt/homebrew/lib/python3.10/site-packages/rp/documentation/work_packages"):
        """Save work packages to individual JSON files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save summary
        summary = {
            'total_packages': len(self.packages),
            'total_functions': sum(len(p['functions']) for p in self.packages),
            'estimated_total_hours': sum(p['estimated_hours'] for p in self.packages),
            'packages_by_priority': sorted(self.packages, key=lambda x: x['priority_score'], reverse=True)[:10]
        }
        
        with open(output_path / 'summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save individual packages
        for package in self.packages:
            filename = f"package_{package['package_id']:03d}_priority_{package['priority_score']}.json"
            with open(output_path / filename, 'w') as f:
                json.dump(package, f, indent=2)
        
        print(f"Saved {len(self.packages)} work packages to {output_path}")
        print(f"Total estimated work: {summary['estimated_total_hours']:.1f} hours")
        
        return summary

def main():
    packager = MinionPackager()
    packages = packager.generate_comprehensive_packages(package_size=8)
    summary = packager.save_packages()
    
    print("\n=== Top Priority Packages ===")
    for i, package in enumerate(packages[:5]):
        print(f"\nPackage {package['package_id']} (Score: {package['priority_score']}):")
        print(f"Functions: {', '.join(package['functions'][:4])}{'...' if len(package['functions']) > 4 else ''}")
        print(f"Estimated hours: {package['estimated_hours']:.1f}")
        
        # Show documentation status
        missing_docs = sum(1 for f in package['functions'] 
                          if package['documentation_status'].get(f, {}).get('current_quality') == 'missing')
        print(f"Functions without docs: {missing_docs}/{len(package['functions'])}")

if __name__ == "__main__":
    main()