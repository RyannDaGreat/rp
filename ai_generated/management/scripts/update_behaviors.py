#!/opt/homebrew/opt/python@3.10/bin/python3.10
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
