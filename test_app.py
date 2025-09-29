#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("Flask app imported successfully")
    
    with app.test_client() as client:
        # Test all routes
        routes = [
            '/',
            '/input_pidum',
            '/input_pidsus',
            '/view_pidum',
            '/view_pidsus',
            '/pidum_charts',
            '/pidsus_charts'
        ]
        
        print("\nTesting Flask Application Routes:")
        print("=" * 40)
        
        for route in routes:
            try:
                response = client.get(route)
                status = "✓ PASS" if response.status_code == 200 else "✗ FAIL"
                print(f"{route:<20} {status} ({response.status_code})")
            except Exception as e:
                print(f"{route:<20} ✗ ERROR: {str(e)}")
        
        print("\nApplication is ready!")
        print("Run 'python3 app.py' to start the server")
        print("Then visit http://localhost:5000 in your browser")
        
except Exception as e:
    print(f"Error importing app: {e}")
    print("Please check if all dependencies are installed correctly")