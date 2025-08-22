#!/opt/homebrew/opt/python@3.10/bin/python3.10
"""
RP Docstring Quality Analyzer
Assesses the quality and completeness of function docstrings in r.py
"""

import ast
import re
from typing import Dict, List, Tuple, Set
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class DocQuality(Enum):
    EXCELLENT = "excellent"  # Comprehensive docstring with examples
    GOOD = "good"           # Decent docstring, could use enhancement  
    BASIC = "basic"         # Minimal docstring
    MISSING = "missing"     # No docstring
    STUB = "stub"          # Just """ placeholder

@dataclass
class DocAnalysis:
    function_name: str
    quality: DocQuality
    length: int
    has_examples: bool
    has_parameters: bool
    has_return_info: bool
    has_usage_notes: bool
    docstring_text: str
    suggestions: List[str]

class RPDocstringAnalyzer:
    def __init__(self, rp_path: str = "/opt/homebrew/lib/python3.10/site-packages/rp/r.py"):
        self.rp_path = rp_path
        self.analyses = {}  # function_name -> DocAnalysis
        
    def analyze_all_docstrings(self) -> Dict[str, DocAnalysis]:
        """Analyze docstring quality for all functions in r.py"""
        with open(self.rp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                analysis = self._analyze_function_docstring(node)
                self.analyses[node.name] = analysis
                
        return self.analyses
    
    def _analyze_function_docstring(self, func_node: ast.FunctionDef) -> DocAnalysis:
        """Analyze a single function's docstring"""
        docstring = ast.get_docstring(func_node)
        
        if not docstring:
            return DocAnalysis(
                function_name=func_node.name,
                quality=DocQuality.MISSING,
                length=0,
                has_examples=False,
                has_parameters=False,
                has_return_info=False,
                has_usage_notes=False,
                docstring_text="",
                suggestions=["Add comprehensive docstring with purpose, parameters, and examples"]
            )
        
        # Analyze docstring content
        length = len(docstring)
        has_examples = self._has_examples(docstring)
        has_parameters = self._has_parameter_info(docstring)
        has_return_info = self._has_return_info(docstring)
        has_usage_notes = self._has_usage_notes(docstring)
        
        # Determine quality
        quality = self._determine_quality(docstring, has_examples, has_parameters, has_return_info)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(
            func_node.name, docstring, has_examples, has_parameters, has_return_info, has_usage_notes
        )
        
        return DocAnalysis(
            function_name=func_node.name,
            quality=quality,
            length=length,
            has_examples=has_examples,
            has_parameters=has_parameters,
            has_return_info=has_return_info,
            has_usage_notes=has_usage_notes,
            docstring_text=docstring,
            suggestions=suggestions
        )
    
    def _has_examples(self, docstring: str) -> bool:
        """Check if docstring has usage examples"""
        example_indicators = [
            '>>>', 'Example:', 'Examples:', 'Usage:', 'e.g.',
            'For example', 'Example usage', '```'
        ]
        return any(indicator in docstring for indicator in example_indicators)
    
    def _has_parameter_info(self, docstring: str) -> bool:
        """Check if docstring documents parameters"""
        param_indicators = [
            'Args:', 'Arguments:', 'Parameters:', 'Params:',
            ':param', '@param', 'arg:', 'parameter:'
        ]
        return any(indicator in docstring for indicator in param_indicators)
    
    def _has_return_info(self, docstring: str) -> bool:
        """Check if docstring documents return value"""
        return_indicators = [
            'Returns:', 'Return:', ':return', '@return',
            'returns', 'output:', 'Output:'
        ]
        return any(indicator in docstring for indicator in return_indicators)
    
    def _has_usage_notes(self, docstring: str) -> bool:
        """Check if docstring has usage notes or warnings"""
        note_indicators = [
            'Note:', 'Warning:', 'Caution:', 'Important:',
            'TODO:', 'FIXME:', 'See also:', 'Related:'
        ]
        return any(indicator in docstring for indicator in note_indicators)
    
    def _determine_quality(self, docstring: str, has_examples: bool, 
                          has_parameters: bool, has_return_info: bool) -> DocQuality:
        """Determine overall docstring quality"""
        if len(docstring.strip()) <= 10 or docstring.strip() in ['"""', "'''"]:
            return DocQuality.STUB
            
        if len(docstring) < 50:
            return DocQuality.BASIC
            
        quality_score = 0
        if has_examples: quality_score += 3
        if has_parameters: quality_score += 2  
        if has_return_info: quality_score += 2
        if len(docstring) > 200: quality_score += 1
        
        if quality_score >= 6:
            return DocQuality.EXCELLENT
        elif quality_score >= 3:
            return DocQuality.GOOD
        else:
            return DocQuality.BASIC
    
    def _generate_suggestions(self, func_name: str, docstring: str,
                            has_examples: bool, has_parameters: bool, 
                            has_return_info: bool, has_usage_notes: bool) -> List[str]:
        """Generate specific improvement suggestions"""
        suggestions = []
        
        if not has_examples:
            suggestions.append("Add concrete usage examples with >>> syntax")
            
        if not has_parameters and self._likely_has_parameters(func_name):
            suggestions.append("Document function parameters and their types")
            
        if not has_return_info and not func_name.startswith('_') and 'print' not in func_name:
            suggestions.append("Document return value and type")
            
        if not has_usage_notes:
            if '_via_' in func_name:
                suggestions.append("Explain backend-specific behavior and when to use this variant")
            elif func_name.startswith('load_') or func_name.startswith('save_'):
                suggestions.append("Add supported file formats and common usage patterns")
            elif 'image' in func_name:
                suggestions.append("Document supported image types and formats")
                
        if len(docstring) < 100:
            suggestions.append("Expand description with more detail about purpose and behavior")
            
        return suggestions
    
    def _likely_has_parameters(self, func_name: str) -> bool:
        """Heuristic to determine if function likely has parameters worth documenting"""
        # Most functions have parameters except for very simple ones
        simple_patterns = ['get_', 'is_', 'has_', 'clear_', 'reset_']
        return not any(func_name.startswith(pattern) for pattern in simple_patterns)
    
    def get_documentation_priorities(self) -> Dict[DocQuality, List[str]]:
        """Get functions grouped by documentation priority"""
        priorities = {quality: [] for quality in DocQuality}
        
        for func_name, analysis in self.analyses.items():
            priorities[analysis.quality].append(func_name)
            
        return priorities
    
    def get_high_impact_functions(self, function_calls: Dict[str, Set[str]]) -> List[str]:
        """Get functions that are called frequently but poorly documented"""
        # Calculate call frequency
        call_frequency = {}
        for caller, called_funcs in function_calls.items():
            for func in called_funcs:
                call_frequency[func] = call_frequency.get(func, 0) + 1
        
        # Find high-impact functions with poor documentation
        high_impact = []
        for func_name, analysis in self.analyses.items():
            calls = call_frequency.get(func_name, 0)
            if calls >= 10 and analysis.quality in [DocQuality.MISSING, DocQuality.BASIC, DocQuality.STUB]:
                high_impact.append((func_name, calls, analysis.quality))
        
        # Sort by call frequency
        high_impact.sort(key=lambda x: x[1], reverse=True)
        return [func for func, _, _ in high_impact]
    
    def generate_documentation_report(self, function_calls: Dict[str, Set[str]] = None) -> str:
        """Generate comprehensive documentation status report"""
        if not self.analyses:
            self.analyze_all_docstrings()
            
        priorities = self.get_documentation_priorities()
        
        report = "=== RP Documentation Status Report ===\n\n"
        
        # Summary statistics
        total = len(self.analyses)
        report += f"Total Functions: {total}\n"
        for quality in DocQuality:
            count = len(priorities[quality])
            percentage = (count / total) * 100
            report += f"{quality.value.title()}: {count} ({percentage:.1f}%)\n"
        
        report += "\n=== High Priority Functions (Missing/Basic Documentation) ===\n"
        
        # Show functions that need immediate attention
        needs_work = priorities[DocQuality.MISSING] + priorities[DocQuality.STUB] + priorities[DocQuality.BASIC][:10]
        
        for func_name in needs_work[:20]:  # Top 20
            analysis = self.analyses[func_name]
            report += f"\n{func_name} [{analysis.quality.value}]:\n"
            for suggestion in analysis.suggestions[:2]:  # Top 2 suggestions
                report += f"  - {suggestion}\n"
        
        if function_calls:
            report += "\n=== High-Impact Functions Needing Documentation ===\n"
            high_impact = self.get_high_impact_functions(function_calls)
            for func in high_impact[:10]:
                calls = sum(1 for called_funcs in function_calls.values() if func in called_funcs)
                report += f"{func} ({calls} calls) - {self.analyses[func].quality.value}\n"
        
        return report

if __name__ == "__main__":
    analyzer = RPDocstringAnalyzer()
    analyzer.analyze_all_docstrings()
    
    # Generate report
    report = analyzer.generate_documentation_report()
    print(report)