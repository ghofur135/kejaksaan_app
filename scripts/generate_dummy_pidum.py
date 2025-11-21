#!/usr/bin/env python3
"""
Script untuk generate dummy data PIDUM
Periode: Agustus - Oktober 2025
"""

import random
from datetime import datetime, date, timedelta
from src.models.database import insert_pidum_data, get_database_stats

# Data dummy untuk generate
JENIS_PERKARA_LIST = [
    'NARKOTIKA',
    'KORUPSI', 
    'PENCURIAN',
    'PENIPUAN',
    'PENGANIAYAAN',
    'PEMBUNUHAN',
    'PERKOSAAN',
    'PENGELAPAN',
    'PERKARA LAINNYA'
]

TAHAPAN_PENANGANAN_LIST = [
    'PRA PENUNTUTAN',
    'PENUNTUTAN', 
    'UPAYA HUKUM'
]

# Template keterangan berdasarkan jenis perkara
KETERANGAN_TEMPLATES = {
    'NARKOTIKA': [
        'Kepemilikan sabu-sabu seberat {} gram',
        'Penyalahgunaan narkotika jenis {}',
        'Pengedar narkoba di wilayah {}',
        'Kepemilikan ganja seberat {} gram',
        'Pemakai narkotika jenis methamphetamine'
    ],
    'KORUPSI': [
        'Korupsi dana {} sebesar Rp {} juta',
        'Gratifikasi dalam proyek {}',
        'Penyuapan untuk tender {}',
        'Penggelapan dana bantuan sosial',
        'Korupsi pengadaan barang dan jasa'
    ],
    'PENCURIAN': [
        'Pencurian {} di {}',
        'Pencurian kendaraan bermotor {}',
        'Pencurian dengan kekerasan',
        'Pencurian dalam rumah tinggal',
        'Pencurian di tempat umum'
    ],
    'PENIPUAN': [
        'Penipuan online sebesar Rp {} juta',
        'Penipuan investasi bodong',
        'Penipuan berkedok arisan',
        'Penipuan jual beli {}',
        'Penipuan via media sosial'
    ],
    'PENGANIAYAAN': [
        'Penganiayaan ringan akibat {}',
        'Penganiayaan berat menggunakan {}',
        'Kekerasan dalam rumah tangga',
        'Penganiayaan di tempat kerja',
        'Perkelahian antar warga'
    ],
    'PEMBUNUHAN': [
        'Pembunuhan berencana menggunakan {}',
        'Pembunuhan akibat konflik {}',
        'Pembunuhan dalam perampokan',
        'Pembunuhan berencana',
        'Pembunuhan karena dendam'
    ],
    'PERKOSAAN': [
        'Perkosaan terhadap anak di bawah umur',
        'Perkosaan dengan kekerasan',
        'Perkosaan dalam keluarga',
        'Perkosaan berencana',
        'Pencabulan terhadap anak'
    ],
    'PENGELAPAN': [
        'Pengelapan dana {} sebesar Rp {} juta',
        'Pengelapan oleh pegawai {}',
        'Pengelapan kendaraan dinas',
        'Pengelapan barang inventaris',
        'Pengelapan uang kas {}'
    ],
    'PERKARA LAINNYA': [
        'Pelanggaran {} sesuai pasal {}',
        'Tindak pidana {} lainnya',
        'Kasus {} yang memerlukan penanganan khusus',
        'Pelanggaran aturan {}',
        'Tindakan {} melanggar hukum'
    ]
}

# Data untuk variasi template
VARIASI_DATA = {
    'berat': ['0.5', '1.2', '2.5', '5.0', '10.5', '25.0'],
    'narkotika_jenis': ['sabu-sabu', 'ganja', 'ekstasi', 'kokain', 'heroin'],
    'lokasi': ['Jakarta Utara', 'Jakarta Selatan', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Pusat'],
    'dana': ['bantuan sosial', 'APBD', 'proyek jalan', 'pengadaan', 'dana desa'],
    'nominal': ['50', '100', '250', '500', '750', '1000', '2500'],
    'proyek': ['pembangunan jalan', 'pengadaan komputer', 'renovasi gedung', 'pembangunan jembatan'],
    'barang': ['sepeda motor', 'handphone', 'laptop', 'perhiasan', 'uang tunai'],
    'tempat': ['mall', 'pasar', 'stasiun', 'terminal', 'bandara'],
    'senjata': ['pisau', 'parang', 'benda tumpul', 'senjata tajam'],
    'konflik': ['warisan', 'tanah', 'hutang piutang', 'percintaan', 'bisnis'],
    'instansi': ['dinas pendidikan', 'puskesmas', 'kelurahan', 'kecamatan', 'dinas sosial'],
    'pasal': ['362 KUHP', '378 KUHP', '340 KUHP', '351 KUHP', '372 KUHP']
}

def generate_keterangan(jenis_perkara):
    """Generate keterangan berdasarkan jenis perkara"""
    templates = KETERANGAN_TEMPLATES.get(jenis_perkara, KETERANGAN_TEMPLATES['PERKARA LAINNYA'])
    template = random.choice(templates)
    
    # Replace placeholders with random data
    if '{}' in template:
        if jenis_perkara == 'NARKOTIKA':
            if 'seberat' in template:
                return template.format(random.choice(VARIASI_DATA['berat']))
            elif 'jenis' in template:
                return template.format(random.choice(VARIASI_DATA['narkotika_jenis']))
            elif 'wilayah' in template:
                return template.format(random.choice(VARIASI_DATA['lokasi']))
        elif jenis_perkara == 'KORUPSI':
            if 'sebesar' in template:
                return template.format(random.choice(VARIASI_DATA['dana']), random.choice(VARIASI_DATA['nominal']))
            else:
                return template.format(random.choice(VARIASI_DATA['proyek']))
        elif jenis_perkara == 'PENCURIAN':
            return template.format(random.choice(VARIASI_DATA['barang']), random.choice(VARIASI_DATA['tempat']))
        elif jenis_perkara == 'PENIPUAN':
            if 'sebesar' in template:
                return template.format(random.choice(VARIASI_DATA['nominal']))
            else:
                return template.format(random.choice(VARIASI_DATA['barang']))
        elif jenis_perkara == 'PENGANIAYAAN':
            if 'menggunakan' in template:
                return template.format(random.choice(VARIASI_DATA['senjata']))
            else:
                return template.format(random.choice(VARIASI_DATA['konflik']))
        elif jenis_perkara == 'PEMBUNUHAN':
            if 'menggunakan' in template:
                return template.format(random.choice(VARIASI_DATA['senjata']))
            else:
                return template.format(random.choice(VARIASI_DATA['konflik']))
        elif jenis_perkara == 'PENGELAPAN':
            if 'sebesar' in template:
                return template.format(random.choice(VARIASI_DATA['dana']), random.choice(VARIASI_DATA['nominal']))
            elif 'oleh pegawai' in template:
                return template.format(random.choice(VARIASI_DATA['instansi']))
            else:
                return template.format(random.choice(VARIASI_DATA['instansi']))
        elif jenis_perkara == 'PERKARA LAINNYA':
            if 'pasal' in template:
                return template.format(random.choice(VARIASI_DATA['barang']), random.choice(VARIASI_DATA['pasal']))
            else:
                return template.format(random.choice(VARIASI_DATA['barang']))
    
    return template

def generate_date_range(start_month, start_year, end_month, end_year):
    """Generate list of random dates within range"""
    start_date = date(start_year, start_month, 1)
    
    # Get last day of end month
    if end_month == 12:
        end_date = date(end_year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(end_year, end_month + 1, 1) - timedelta(days=1)
    
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    
    return dates

def generate_dummy_data():
    """Generate dummy PIDUM data"""
    print("🚀 Generating Dummy Data PIDUM...")
    print("📅 Periode: Agustus - Oktober 2025")
    
    # Get date range
    available_dates = generate_date_range(8, 2025, 10, 2025)  # Aug-Oct 2025
    
    dummy_data = []
    
    # Generate 150 dummy records (50 per month approximately)
    for i in range(1, 151):
        # Random date from available dates
        random_date = random.choice(available_dates)
        
        # Determine periode based on month
        periode_map = {8: "Agustus 2025", 9: "September 2025", 10: "Oktober 2025"}
        periode = periode_map[random_date.month]
        
        # Random jenis perkara and tahapan
        jenis_perkara = random.choice(JENIS_PERKARA_LIST)
        tahapan_penanganan = random.choice(TAHAPAN_PENANGANAN_LIST)
        
        # Generate keterangan
        keterangan = generate_keterangan(jenis_perkara)
        
        # Create data record
        data = {
            'NO': str(i),
            'PERIODE': periode,
            'TANGGAL': random_date.strftime('%Y-%m-%d'),
            'JENIS PERKARA': jenis_perkara,
            'TAHAPAN_PENANGANAN': tahapan_penanganan,
            'KETERANGAN': keterangan
        }
        
        dummy_data.append(data)
    
    return dummy_data

def insert_dummy_data(data_list):
    """Insert dummy data to database"""
    print(f"\n📝 Inserting {len(data_list)} records to database...")
    
    success_count = 0
    error_count = 0
    
    for i, data in enumerate(data_list, 1):
        try:
            insert_pidum_data(data)
            success_count += 1
            
            # Progress indicator
            if i % 10 == 0:
                print(f"  ✅ Inserted {i}/{len(data_list)} records...")
                
        except Exception as e:
            error_count += 1
            print(f"  ❌ Error inserting record {i}: {e}")
    
    print(f"\n📊 Results:")
    print(f"  ✅ Successfully inserted: {success_count} records")
    print(f"  ❌ Failed: {error_count} records")
    
    return success_count, error_count

def main():
    """Main function"""
    print("=" * 60)
    print("🏛️  DUMMY DATA GENERATOR PIDUM")
    print("=" * 60)
    
    # Show current database stats
    stats = get_database_stats()
    print(f"📊 Current database stats:")
    print(f"  - PIDUM records: {stats['pidum_count']}")
    print(f"  - PIDSUS records: {stats['pidsus_count']}")
    
    # Confirm before proceeding
    print(f"\n🎯 Will generate dummy data for:")
    print(f"  - Period: Agustus - Oktober 2025")
    print(f"  - Records: ~150 dummy records")
    print(f"  - Jenis Perkara: {len(JENIS_PERKARA_LIST)} types")
    print(f"  - Tahapan: {len(TAHAPAN_PENANGANAN_LIST)} stages")
    
    confirm = input(f"\n❓ Proceed with dummy data generation? (y/N): ")
    
    if confirm.lower() != 'y':
        print("❌ Operation cancelled.")
        return
    
    try:
        # Generate dummy data
        dummy_data = generate_dummy_data()
        
        # Show sample data
        print(f"\n📋 Sample generated data:")
        for i, sample in enumerate(dummy_data[:3], 1):
            print(f"  {i}. NO: {sample['NO']}, Periode: {sample['PERIODE']}")
            print(f"     Jenis: {sample['JENIS PERKARA']}, Tahapan: {sample['TAHAPAN_PENANGANAN']}")
            print(f"     Keterangan: {sample['KETERANGAN'][:60]}...")
            print()
        
        # Insert to database
        success_count, error_count = insert_dummy_data(dummy_data)
        
        # Show final stats
        final_stats = get_database_stats()
        print(f"\n📊 Final database stats:")
        print(f"  - PIDUM records: {final_stats['pidum_count']} (+{final_stats['pidum_count'] - stats['pidum_count']})")
        print(f"  - PIDSUS records: {final_stats['pidsus_count']}")
        
        print(f"\n🎉 Dummy data generation completed!")
        print(f"📍 You can now view the data at: http://localhost:5001/view_pidum")
        
    except Exception as e:
        print(f"\n❌ Error during dummy data generation: {e}")
        return

if __name__ == "__main__":
    main()