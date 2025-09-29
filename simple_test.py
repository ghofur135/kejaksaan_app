#!/usr/bin/env python3
print("Testing Flask app import...")
try:
    from app import app
    print("✓ Flask app imported successfully")
    print("✓ App name:", app.name)
    print("✓ App routes:", [rule.rule for rule in app.url_map.iter_rules()])
except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()