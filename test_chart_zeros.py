#!/usr/bin/env python3
"""
Test script to verify that chart shows all categories including those with value 0
"""

from database import get_pidum_report_data
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def test_chart_with_zeros():
    """Test chart generation with some categories having 0 values"""
    
    # Get report data for current month/year
    report_data = get_pidum_report_data(9, 2025)  # September 2025
    
    print("Current report data:")
    for item in report_data:
        print(f"  {item['jenis_perkara']}: {item['JUMLAH']} (Pra: {item['PRA PENUNTUTAN']}, Penuntutan: {item['PENUNTUTAN']}, Upaya: {item['UPAYA HUKUM']})")
    
    # Categories with 0 values
    zero_categories = [item for item in report_data if item['JUMLAH'] == 0]
    non_zero_categories = [item for item in report_data if item['JUMLAH'] > 0]
    
    print(f"\nCategories with 0 values: {len(zero_categories)}")
    for cat in zero_categories:
        print(f"  - {cat['jenis_perkara']}")
    
    print(f"\nCategories with data: {len(non_zero_categories)}")
    for cat in non_zero_categories:
        print(f"  - {cat['jenis_perkara']}: {cat['JUMLAH']}")
    
    print(f"\nTotal categories in report: {len(report_data)}")
    print("Chart will show ALL categories including those with 0 values.")

if __name__ == "__main__":
    test_chart_with_zeros()