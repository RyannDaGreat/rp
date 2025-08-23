#!/opt/homebrew/opt/python@3.10/bin/python3.10
"""
RP Diff-Aware Management Updater
Only updates analysis when specific parts of r.py change, making updates efficient.
"""

import os
import json
import hashlib
import ast
from typing import Dict, List, Set, Optional
from pathlib import Path

class RPDiffTracker:
    def __init__(self, rp_path: str = "/opt/homebrew/lib/python3.10/site-packages/rp/r.py"):
        self.rp_path = rp_path
        self.management_dir = Path(rp_path).parent / "management"
        self.state_file = self.management_dir / "scripts" / "last_update_state.json"
        
    def get_current_state(self) -> Dict:
        """Get current state of r.py for diff tracking"""
        with open(self.rp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse to extract functions
        tree = ast.parse(content)
        functions = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get function signature hash
                func_start = node.lineno
                func_end = node.end_lineno if hasattr(node, 'end_lineno') else func_start
                
                # Extract function source
                func_lines = content.split('\n')[func_start-1:func_end]
                func_source = '\n'.join(func_lines)
                
                functions[node.name] = {
                    'hash': hashlib.md5(func_source.encode()).hexdigest(),
                    'line_start': func_start,
                    'line_end': func_end,
                    'args': [arg.arg for arg in node.args.args],
                    'has_docstring': ast.get_docstring(node) is not None
                }
        
        return {
            'file_hash': hashlib.md5(content.encode()).hexdigest(),
            'total_functions': len(functions),
            'functions': functions,
            'timestamp': int(os.path.getmtime(self.rp_path))
        }
    
    def load_previous_state(self) -> Optional[Dict]:
        """Load previous state from disk"""
        if not self.state_file.exists():
            return None
            
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def save_current_state(self, state: Dict):
        """Save current state to disk"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def analyze_changes(self, old_state: Dict, new_state: Dict) -> Dict:
        """Analyze what changed between states"""
        if not old_state:
            return {
                'type': 'full_analysis_needed',
                'reason': 'No previous state found'
            }
            
        if old_state['file_hash'] == new_state['file_hash']:
            return {
                'type': 'no_changes',
                'reason': 'File unchanged since last analysis'
            }
        
        changes = {
            'type': 'incremental_update',
            'added_functions': [],
            'removed_functions': [],
            'modified_functions': [],
            'unchanged_functions': []
        }
        
        old_funcs = old_state.get('functions', {})
        new_funcs = new_state.get('functions', {})
        
        # Find added functions
        for func_name in new_funcs:
            if func_name not in old_funcs:
                changes['added_functions'].append(func_name)
        
        # Find removed functions  
        for func_name in old_funcs:
            if func_name not in new_funcs:
                changes['removed_functions'].append(func_name)
        
        # Find modified functions
        for func_name in new_funcs:
            if func_name in old_funcs:
                if old_funcs[func_name]['hash'] != new_funcs[func_name]['hash']:
                    changes['modified_functions'].append(func_name)
                else:
                    changes['unchanged_functions'].append(func_name)
        
        return changes
    
    def determine_required_updates(self, changes: Dict) -> Dict:
        """Determine which analysis tools need to be re-run based on changes"""
        if changes['type'] == 'no_changes':
            return {'updates_needed': []}
        
        if changes['type'] == 'full_analysis_needed':
            return {
                'updates_needed': [
                    'function_mapping',
                    'docstring_analysis', 
                    'consistency_analysis',
                    'argument_tracking',
                    'behavior_analysis',
                    'work_packages'
                ]
            }
        
        # Incremental updates
        updates_needed = []
        
        # Always update if functions added/removed
        if changes['added_functions'] or changes['removed_functions']:
            updates_needed.extend([
                'function_mapping',
                'consistency_analysis',
                'work_packages'
            ])
        
        # Update docstring analysis if any functions modified
        if changes['modified_functions']:
            updates_needed.append('docstring_analysis')
            
        # Update argument tracking if function signatures might have changed
        if changes['added_functions'] or changes['modified_functions']:
            updates_needed.extend([
                'argument_tracking',
                'behavior_analysis'
            ])
        
        return {
            'updates_needed': list(set(updates_needed)),
            'affected_functions': changes['added_functions'] + changes['modified_functions'],
            'unchanged_functions': changes['unchanged_functions']
        }

def run_selective_updates(updates_needed: List[str], affected_functions: List[str] = None):
    """Run only the analysis tools that need updating"""
    import sys
    management_dir = Path("/opt/homebrew/lib/python3.10/site-packages/rp/management")
    
    print(f"Running selective updates: {', '.join(updates_needed)}")
    
    if 'function_mapping' in updates_needed:
        print("→ Updating function relationship mapping...")
        exec(open(management_dir / "documentation" / "function_mapper.py").read())
    
    if 'docstring_analysis' in updates_needed:
        print("→ Updating docstring quality analysis...")
        exec(open(management_dir / "documentation" / "docstring_analyzer.py").read())
    
    if 'consistency_analysis' in updates_needed:
        print("→ Updating consistency analysis...")
        exec(open(management_dir / "consistency" / "consistency_tracker.py").read())
    
    if 'argument_tracking' in updates_needed:
        print("→ Updating argument consistency tracking...")
        exec(open(management_dir / "consistency" / "argument_tracker.py").read())
    
    if 'behavior_analysis' in updates_needed:
        print("→ Updating behavioral pattern analysis...")
        exec(open(management_dir / "consistency" / "behavior_tracker.py").read())
    
    if 'work_packages' in updates_needed:
        print("→ Regenerating work packages...")
        exec(open(management_dir / "documentation" / "minion_packager.py").read())
    
    print("✅ Selective updates completed!")

def main():
    """Main diff-aware update function"""
    print("🔍 RP Diff-Aware Updater")
    
    tracker = RPDiffTracker()
    
    # Get current and previous states
    current_state = tracker.get_current_state()
    previous_state = tracker.load_previous_state()
    
    print(f"Current r.py: {current_state['total_functions']} functions")
    
    # Analyze changes
    changes = tracker.analyze_changes(previous_state, current_state)
    
    if changes['type'] == 'no_changes':
        print("✅ No changes detected - all analysis is up to date")
        return
    
    print(f"📝 Changes detected: {changes['type']}")
    
    if changes['type'] == 'incremental_update':
        print(f"  Added: {len(changes['added_functions'])} functions")
        print(f"  Modified: {len(changes['modified_functions'])} functions") 
        print(f"  Removed: {len(changes['removed_functions'])} functions")
        print(f"  Unchanged: {len(changes['unchanged_functions'])} functions")
    
    # Determine what needs updating
    update_plan = tracker.determine_required_updates(changes)
    
    if not update_plan['updates_needed']:
        print("✅ No analysis updates required")
        return
    
    print(f"🔄 Updates needed: {', '.join(update_plan['updates_needed'])}")
    
    # Run selective updates
    run_selective_updates(
        update_plan['updates_needed'],
        update_plan.get('affected_functions')
    )
    
    # Save new state
    tracker.save_current_state(current_state)
    print("💾 Updated state saved")
    
    # Generate summary
    print("\n📊 Update Summary:")
    print(f"  Total functions: {current_state['total_functions']}")
    print(f"  Analysis tools run: {len(update_plan['updates_needed'])}")
    print(f"  Time saved by differential analysis: ~{5 * (6 - len(update_plan['updates_needed']))} minutes")

if __name__ == "__main__":
    main()