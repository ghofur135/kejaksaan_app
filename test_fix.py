#!/usr/bin/env python3
"""
Test script untuk memastikan fix TypeError sudah benar
"""

def test_sum_numeric_filter():
    """Test custom Jinja2 filter sum_numeric"""
    from app_with_db import app
    from database import get_pidum_data_for_export
    
    # Get test data
    data = get_pidum_data_for_export()
    print(f"Testing with {len(data)} records:")
    for i, item in enumerate(data):
        print(f"  Record {i+1}: PRA_PENUTUTAN={item['PRA PENUTUTAN']} (type: {type(item['PRA PENUTUTAN'])})")
    
    # Test the custom filter
    with app.app_context():
        sum_filter = app.jinja_env.filters['sum_numeric']
        
        # Test each numeric field
        pra_penututan_sum = sum_filter(data, 'PRA PENUTUTAN')
        penuntutan_sum = sum_filter(data, 'PENUNTUTAN')
        upaya_hukum_sum = sum_filter(data, 'UPAYA HUKUM')
        
        print(f"\nResults:")
        print(f"  Total PRA PENUTUTAN: {pra_penututan_sum}")
        print(f"  Total PENUNTUTAN: {penuntutan_sum}")
        print(f"  Total UPAYA HUKUM: {upaya_hukum_sum}")
        
        # Verify with manual calculation
        manual_pra = sum(int(item['PRA PENUTUTAN']) for item in data)
        manual_pen = sum(int(item['PENUNTUTAN']) for item in data)
        manual_upaya = sum(int(item['UPAYA HUKUM']) for item in data)
        
        print(f"\nManual verification:")
        print(f"  Manual PRA PENUTUTAN: {manual_pra} ({'✅ MATCH' if manual_pra == pra_penututan_sum else '❌ MISMATCH'})")
        print(f"  Manual PENUNTUTAN: {manual_pen} ({'✅ MATCH' if manual_pen == penuntutan_sum else '❌ MISMATCH'})")
        print(f"  Manual UPAYA HUKUM: {manual_upaya} ({'✅ MATCH' if manual_upaya == upaya_hukum_sum else '❌ MISMATCH'})")
        
        return pra_penututan_sum == manual_pra and penuntutan_sum == manual_pen and upaya_hukum_sum == manual_upaya

def test_template_rendering():
    """Test template rendering with real data"""
    from app_with_db import app
    from flask import render_template_string
    from database import get_pidum_data_for_export
    
    data = get_pidum_data_for_export()
    
    # Test template snippet that was causing error
    template_snippet = """
    Total PRA PENUTUTAN: {{ data|sum_numeric('PRA PENUTUTAN') }}
    Total PENUNTUTAN: {{ data|sum_numeric('PENUNTUTAN') }}
    Total UPAYA HUKUM: {{ data|sum_numeric('UPAYA HUKUM') }}
    """
    
    with app.app_context():
        try:
            result = render_template_string(template_snippet, data=data)
            print(f"\nTemplate rendering test:")
            print(result)
            return True
        except Exception as e:
            print(f"\n❌ Template rendering failed: {e}")
            return False

if __name__ == "__main__":
    print("🧪 TESTING TypeError FIX")
    print("=" * 50)
    
    try:
        # Test custom filter
        filter_test = test_sum_numeric_filter()
        print(f"\n📊 Custom filter test: {'✅ PASSED' if filter_test else '❌ FAILED'}")
        
        # Test template rendering
        template_test = test_template_rendering()
        print(f"🎨 Template rendering test: {'✅ PASSED' if template_test else '❌ FAILED'}")
        
        # Overall result
        if filter_test and template_test:
            print(f"\n🎉 ALL TESTS PASSED! TypeError fix is working correctly.")
        else:
            print(f"\n⚠️  Some tests failed. Please check the errors above.")
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()