#!/usr/bin/env python3
"""
Script to insert sample PIDUM data for testing the report system
"""

from database import insert_pidum_data
from datetime import datetime

def insert_sample_data():
    """Insert sample PIDUM data matching the report structure in the image"""
    
    sample_data = [
        # Narkoba - 4 total (1 Pra Penuntutan, 3 Penuntutan)
        {
            'NO': '1',
            'PERIODE': '1',
            'TANGGAL': '2025-09-01',
            'JENIS PERKARA': 'NARKOBA',
            'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
            'KETERANGAN': 'Pasal 112 UU No. 35 Tahun 2009'
        },
        {
            'NO': '2',
            'PERIODE': '1',
            'TANGGAL': '2025-09-02',
            'JENIS PERKARA': 'NARKOBA',
            'TAHAPAN_PENANGANAN': 'PENUNTUTAN',
            'KETERANGAN': 'Pasal 114 UU No. 35 Tahun 2009'
        },
        {
            'NO': '3',
            'PERIODE': '1',
            'TANGGAL': '2025-09-03',
            'JENIS PERKARA': 'NARKOBA',
            'TAHAPAN_PENANGANAN': 'PENUNTUTAN',
            'KETERANGAN': 'Pasal 112 UU No. 35 Tahun 2009'
        },
        {
            'NO': '4',
            'PERIODE': '1',
            'TANGGAL': '2025-09-04',
            'JENIS PERKARA': 'NARKOBA',
            'TAHAPAN_PENANGANAN': 'PENUNTUTAN',
            'KETERANGAN': 'Pasal 112 UU No. 35 Tahun 2009'
        },
        
        # Perkara Anak - 2 total (2 Pra Penuntutan)
        {
            'NO': '5',
            'PERIODE': '1',
            'TANGGAL': '2025-09-05',
            'JENIS PERKARA': 'PERKARA ANAK',
            'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
            'KETERANGAN': 'Pasal 76C UU No. 35 Tahun 2014'
        },
        {
            'NO': '6',
            'PERIODE': '1',
            'TANGGAL': '2025-09-06',
            'JENIS PERKARA': 'PERKARA ANAK',
            'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
            'KETERANGAN': 'Pasal 81 UU No. 35 Tahun 2014'
        },
        
        # OHARDA - 4 total (3 Pra Penuntutan, 1 Penuntutan)
        {
            'NO': '7',
            'PERIODE': '1',
            'TANGGAL': '2025-09-07',
            'JENIS PERKARA': 'OHARDA',
            'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
            'KETERANGAN': 'Pasal 372 KUHP'
        },
        {
            'NO': '8',
            'PERIODE': '1',
            'TANGGAL': '2025-09-08',
            'JENIS PERKARA': 'OHARDA',
            'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
            'KETERANGAN': 'Pasal 378 KUHP'
        },
        {
            'NO': '9',
            'PERIODE': '1',
            'TANGGAL': '2025-09-09',
            'JENIS PERKARA': 'OHARDA',
            'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
            'KETERANGAN': 'Pasal 362 KUHP'
        },
        {
            'NO': '10',
            'PERIODE': '1',
            'TANGGAL': '2025-09-10',
            'JENIS PERKARA': 'OHARDA',
            'TAHAPAN_PENANGANAN': 'PENUNTUTAN',
            'KETERANGAN': 'Pasal 372 KUHP'
        },
        
        # Perkara Lainnya - 2 total (1 Pra Penuntutan, 1 Penuntutan)
        {
            'NO': '11',
            'PERIODE': '1',
            'TANGGAL': '2025-09-11',
            'JENIS PERKARA': 'PERKARA LAINNYA',
            'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
            'KETERANGAN': 'Pasal 351 KUHP'
        },
        {
            'NO': '12',
            'PERIODE': '1',
            'TANGGAL': '2025-09-12',
            'JENIS PERKARA': 'PERKARA LAINNYA',
            'TAHAPAN_PENANGANAN': 'PENUNTUTAN',
            'KETERANGAN': 'Pasal 335 KUHP'
        }
    ]
    
    success_count = 0
    for data in sample_data:
        try:
            insert_pidum_data(data)
            success_count += 1
            print(f"✅ Inserted: {data['JENIS PERKARA']} - {data['TAHAPAN_PENANGANAN']}")
        except Exception as e:
            print(f"❌ Error inserting {data['JENIS PERKARA']}: {e}")
    
    print(f"\n🎉 Successfully inserted {success_count} sample records!")

if __name__ == "__main__":
    print("🚀 Inserting sample PIDUM data...")
    insert_sample_data()
    print("✅ Sample data insertion completed!")