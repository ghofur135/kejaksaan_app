#!/usr/bin/env python3
"""
Script untuk generate dummy data PIDUM berdasarkan format file CSV nyata
Periode: Agustus - Oktober 2025 (30 data per bulan = 90 total)
"""

import random
from datetime import datetime, date, timedelta
from src.models.database import insert_pidum_data, get_database_stats, delete_all_pidum_data

# Data dari file CSV nyata untuk template
PRA_PENUNTUTAN_TEMPLATES = [
    {
        "tgl_nomor": "2025-08-28 SPDP/63/VIII/RES.1.24/2025/Reskrim",
        "pasal": "Pasal 82 Undang-Undang Nomor 17 Tahun 2016 tentang penetapan Pepu Nomor 1 Tahun 2016 tentang Perubahan kedua atas Undang-Undang Nomor 23 Tahun 2002 tentang Perlindungan Anak",
        "jenis": "PERKARA ANAK"
    },
    {
        "tgl_nomor": "2025-09-02 B/SPDP/65/IX/RES.1.8/Reskrim",
        "pasal": "Pasal 365 KUHP Jo Pasal 55 ayat (1) ke-1 KUHP dan/atau pasal 368 KUHP jo pasal 55 ayat (1) ke-1 KUHP",
        "jenis": "PENCURIAN"
    },
    {
        "tgl_nomor": "2025-09-08 SPDP/24/IX/RES.4.2/2025/Resnarkoba",
        "pasal": "Pasal 114 ayat (1) atau Pasal 112 ayat (1) atau Pasal 127 ayal (1) huruf (a) UU Rl Nomor 35 Tahun 2009 tentang Narkotika",
        "jenis": "NARKOTIKA"
    },
    {
        "tgl_nomor": "2025-09-10 B/SPDP/69/IX/RES.1.24./2025/RESKRIM",
        "pasal": "Pasal 372 KUHP dan/atau Pasal 36 Jo Pasal 23 ayat (2) Undang - Undang Republik Indonesia Nomor 42 Tahun 1999 tentang jaminan Fidusia",
        "jenis": "PENGELAPAN"
    },
    {
        "tgl_nomor": "2025-09-21 B/SPDP/76/IX/RES.1.6./2025/Satreskrirn",
        "pasal": "Pasal 351 Ayat (3) KUHPidana",
        "jenis": "PENGANIAYAAN"
    },
    {
        "tgl_nomor": "2025-09-24 B/SPDP/75/IX/RES.1 .8./2025/Reskrim",
        "pasal": "Pasal 362 KUHP",
        "jenis": "PENCURIAN"
    }
]

PENUNTUTAN_TEMPLATES = [
    {
        "register": "PDM-22/PRBAL/Enz.2/09/2025",
        "tersangka": "IMRAN Bin IDRIS",
        "tindak_pidana": "UU NO. 36 TAHUN 2009,Pasal 196",
        "jaksa": "SATENO, S.H.M.H. | PANJI BANGUN INDRIYANTO, S.H.",
        "jenis": "NARKOTIKA"
    },
    {
        "register": "PDM-24/PRBAL/Eoh.2/09/2025",
        "tersangka": "HERNI LINDU SAPUTRA als LINDU bin SUHERI",
        "tindak_pidana": "KUHP,Pasal 362",
        "jaksa": "YESKY VERLANGGA WOHON, S.H., M.H. | MAULA PRIMANDA SUMAWIBAWA, S.H.",
        "jenis": "PENCURIAN"
    },
    {
        "register": "PDM-25/PRBAL/Enz.2/09/2025",
        "tersangka": "AIFAN GUSTI KURNIAWAN als. GUSTI bin KHOJIM",
        "tindak_pidana": "UU NO.35 TAHUN 2009,Pasal 114 (1) #Pasal 112 (1)",
        "jaksa": "PANJI BANGUN INDRIYANTO, S.H. | MAULA PRIMANDA SUMAWIBAWA, S.H.",
        "jenis": "NARKOTIKA"
    },
    {
        "register": "PDM-25/PRBAL/Eoh.2/09/2025",
        "tersangka": "SUWANDI Alias WANDI bin ENJANG SUTRISNA",
        "tindak_pidana": "KUHP,Pasal 378#Pasal 372",
        "jaksa": "PANJI BANGUN INDRIYANTO, S.H. | MAULA PRIMANDA SUMAWIBAWA, S.H.",
        "jenis": "PENIPUAN"
    },
    {
        "register": "PDM-26/PRBAL/Eoh.2/09/2025",
        "tersangka": "ABDUL QODIR Bin TARNUJI",
        "tindak_pidana": "KUHP,Pasal 351 Ayat (2)#Pasal 351 Ayat (1)",
        "jaksa": "PANJI BANGUN INDRIYANTO, S.H. | HIDAYAH ARUM KINANTI, S.H.",
        "jenis": "PENGANIAYAAN"
    },
    {
        "register": "PDM-32/PRBAL/Eku.2/09/2025",
        "tersangka": "RAHMAT SUKARMO Bin DARONI",
        "tindak_pidana": "UU NO.17 TAHUN 2016,Pasal 81 Ayat (2)",
        "jaksa": "YESKY VERLANGGA WOHON, S.H., M.H. | MAULA PRIMANDA SUMAWIBAWA, S.H.",
        "jenis": "PERKARA ANAK"
    }
]

UPAYA_HUKUM_TEMPLATES = [
    {
        "terdakwa": "FADELA TRI ANGGRAENI Alias DELA Binti PAIJO",
        "rp9": "PDM- 08/PRBAL/Eoh.2/06/2025",
        "jenis_upaya": "Banding",
        "tanggal_transaksi": "Terdakwa: 2025-09-08 0",
        "banding_akte": "Terdakwa: 2025-09-08 0",
        "jenis": "PERKARA LAINNYA"
    },
    {
        "terdakwa": "RENO ALI MUKHTAMAR Alias RENO Bin AHMAD SUBARNO",
        "rp9": "PDM- 11/PRBAL/Eoh.2/07/2025",
        "jenis_upaya": "Banding",
        "tanggal_transaksi": "Terdakwa: 2025-09-22 0",
        "banding_akte": "Terdakwa: 2025-09-22 0",
        "jenis": "PERKARA LAINNYA"
    },
    {
        "terdakwa": "ADITYA SETIAWAN bin WAHIDIN",
        "rp9": "PDM- 19/PRBAL/Enz.2/06/2025",
        "jenis_upaya": "Banding",
        "tanggal_transaksi": "Jaksa: 2025-09-01 0",
        "banding_akte": "Jaksa: 2025-09-01 0",
        "jenis": "PERKARA LAINNYA"
    }
]

# Jenis perkara yang tersedia
JENIS_PERKARA_LIST = [
    'NARKOTIKA', 'PERKARA ANAK', 'KESUSILAAN', 'JUDI', 'KDRT', 
    'OHARDA', 'PERKARA LAINNYA', 'PENCURIAN', 'PENIPUAN', 
    'PENGANIAYAAN', 'PENGELAPAN', 'KORUPSI'
]

# Nama-nama untuk variasi
NAMA_TEMPLATES = [
    "AHMAD BIN SULAIMAN", "BUDI SANTOSO", "CECEP RUHIAT", "DEDI KURNIAWAN",
    "EDI SUPRIADI", "FIRMAN HIDAYAT", "GUNAWAN SETIAWAN", "HENDRA WIJAYA",
    "INDRA KUSUMA", "JOKO WIDODO", "KURNIA SARI", "LINA MARLINA",
    "MAYA DEWI", "NANA SUPRIATNA", "OKKY RAHMAN", "PUTRI WULANDARI",
    "QOMAR ZAMAN", "RINI ASTUTI", "SARI INDAH", "TONO SURYADI",
    "UMI KALSUM", "VINA ANGGRAENI", "WAWAN SETIAWAN", "XENIA PUTRI",
    "YUNI SARI", "ZAENAL ABIDIN"
]

def generate_date_range(start_month, start_year, end_month, end_year):
    """Generate list of dates within range"""
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

def generate_keterangan_pra_penuntutan(template_data, date_obj):
    """Generate keterangan for PRA PENUNTUTAN based on template"""
    # Modify template dengan tanggal yang sesuai
    tgl_nomor = template_data["tgl_nomor"]
    # Replace tanggal dalam template dengan tanggal yang sesuai
    new_tgl_nomor = tgl_nomor.replace("2025-08-28", date_obj.strftime('%Y-%m-%d'))
    new_tgl_nomor = new_tgl_nomor.replace("2025-09-02", date_obj.strftime('%Y-%m-%d'))
    new_tgl_nomor = new_tgl_nomor.replace("2025-09-08", date_obj.strftime('%Y-%m-%d'))
    
    return f"SPDP: {new_tgl_nomor} | Pasal: {template_data['pasal'][:100]}..."

def generate_keterangan_penuntutan(template_data, date_obj):
    """Generate keterangan for PENUNTUTAN based on template"""
    register = template_data["register"].replace("09/2025", f"{date_obj.month:02d}/2025")
    return f"Register: {register} | Tersangka: {template_data['tersangka']} | Tindak Pidana: {template_data['tindak_pidana'][:50]}... | Jaksa: {template_data['jaksa'][:50]}..."

def generate_keterangan_upaya_hukum(template_data, date_obj):
    """Generate keterangan for UPAYA HUKUM based on template"""
    # Modify nama terdakwa dengan variasi
    nama_variasi = random.choice(NAMA_TEMPLATES)
    rp9 = template_data["rp9"].replace("06/2025", f"{date_obj.month:02d}/2025").replace("07/2025", f"{date_obj.month:02d}/2025")
    return f"Terdakwa: {nama_variasi} | Jenis: {template_data['jenis_upaya']} | RP9: {rp9} | Tanggal Transaksi: {date_obj.strftime('%Y-%m-%d')}"

def generate_dummy_data():
    """Generate 90 dummy PIDUM data (30 per month)"""
    print("🚀 Generating Realistic Dummy Data PIDUM...")
    print("📅 Periode: Agustus - Oktober 2025 (30 data per bulan)")
    
    dummy_data = []
    
    # Generate untuk setiap bulan
    months = [
        (8, "Agustus 2025"), 
        (9, "September 2025"), 
        (10, "Oktober 2025")
    ]
    
    record_counter = 1
    
    for month_num, periode_name in months:
        print(f"\n📆 Generating data untuk {periode_name}...")
        
        # Get dates for this month
        month_dates = generate_date_range(month_num, 2025, month_num, 2025)
        
        # Generate 30 data for this month
        for i in range(30):
            random_date = random.choice(month_dates)
            
            # Distribute data across tahapan (10 each)
            if i < 10:
                tahapan = "PRA PENUNTUTAN"
                template = random.choice(PRA_PENUNTUTAN_TEMPLATES)
                jenis_perkara = template["jenis"]
                keterangan = generate_keterangan_pra_penuntutan(template, random_date)
            elif i < 20:
                tahapan = "PENUNTUTAN"
                template = random.choice(PENUNTUTAN_TEMPLATES)
                jenis_perkara = template["jenis"]
                keterangan = generate_keterangan_penuntutan(template, random_date)
            else:
                tahapan = "UPAYA HUKUM"
                template = random.choice(UPAYA_HUKUM_TEMPLATES)
                jenis_perkara = template["jenis"]
                keterangan = generate_keterangan_upaya_hukum(template, random_date)
            
            # Create data record
            data = {
                'NO': str(record_counter),
                'PERIODE': periode_name,
                'TANGGAL': random_date.strftime('%Y-%m-%d'),
                'JENIS PERKARA': jenis_perkara,
                'TAHAPAN_PENANGANAN': tahapan,
                'KETERANGAN': keterangan
            }
            
            dummy_data.append(data)
            record_counter += 1
    
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
            if i % 15 == 0:
                print(f"  ✅ Inserted {i}/{len(data_list)} records...")
                
        except Exception as e:
            error_count += 1
            print(f"  ❌ Error inserting record {i}: {e}")
    
    print(f"\n📊 Results:")
    print(f"  ✅ Successfully inserted: {success_count} records")
    print(f"  ❌ Failed: {error_count} records")
    
    return success_count, error_count

def show_sample_data(dummy_data):
    """Show sample of generated data"""
    print(f"\n📋 Sample generated data:")
    
    # Show sample from each month and tahapan
    samples = [
        ("Agustus - PRA PENUNTUTAN", dummy_data[0]),
        ("Agustus - PENUNTUTAN", dummy_data[10]),
        ("Agustus - UPAYA HUKUM", dummy_data[20]),
        ("September - PRA PENUNTUTAN", dummy_data[30]),
        ("Oktober - UPAYA HUKUM", dummy_data[80])
    ]
    
    for label, sample in samples:
        print(f"\n  📌 {label}:")
        print(f"     NO: {sample['NO']}, Periode: {sample['PERIODE']}")
        print(f"     Tanggal: {sample['TANGGAL']}, Jenis: {sample['JENIS PERKARA']}")
        print(f"     Tahapan: {sample['TAHAPAN_PENANGANAN']}")
        print(f"     Keterangan: {sample['KETERANGAN'][:80]}...")

def main():
    """Main function"""
    print("=" * 70)
    print("🏛️  REALISTIC DUMMY DATA GENERATOR PIDUM")
    print("📋 Based on Real CSV Data Formats")
    print("=" * 70)
    
    # Show current database stats
    stats = get_database_stats()
    print(f"📊 Current database stats:")
    print(f"  - PIDUM records: {stats['pidum_count']}")
    print(f"  - PIDSUS records: {stats['pidsus_count']}")
    
    # Show what will be generated
    print(f"\n🎯 Will generate realistic dummy data:")
    print(f"  - Period: Agustus - Oktober 2025")
    print(f"  - Total Records: 90 (30 per month)")
    print(f"  - Distribution per month:")
    print(f"    • PRA PENUNTUTAN: 10 data (based on SPDP format)")
    print(f"    • PENUNTUTAN: 10 data (based on Register format)")
    print(f"    • UPAYA HUKUM: 10 data (based on RP9 format)")
    print(f"  - Jenis Perkara: {len(JENIS_PERKARA_LIST)} types")
    print(f"  - Data Templates: Real data from provided CSV files")
    
    # Ask for confirmation
    print(f"\n❓ Options:")
    print(f"  1. Generate new data (add to existing)")
    print(f"  2. Replace all data (delete all + generate new)")
    print(f"  3. Cancel")
    
    choice = input(f"\nSelect option (1/2/3): ").strip()
    
    if choice == "2":
        print(f"\n⚠️  WARNING: This will DELETE ALL existing PIDUM data!")
        confirm_delete = input(f"Are you sure? Type 'DELETE ALL' to confirm: ")
        if confirm_delete == "DELETE ALL":
            try:
                deleted_count = delete_all_pidum_data()
                print(f"🗑️  Deleted {deleted_count} existing records")
            except Exception as e:
                print(f"❌ Error deleting data: {e}")
                return
        else:
            print("❌ Operation cancelled.")
            return
    elif choice == "3":
        print("❌ Operation cancelled.")
        return
    elif choice != "1":
        print("❌ Invalid choice. Operation cancelled.")
        return
    
    try:
        # Generate dummy data
        dummy_data = generate_dummy_data()
        
        # Show sample data
        show_sample_data(dummy_data)
        
        # Final confirmation
        final_confirm = input(f"\n❓ Proceed with database insertion? (y/N): ")
        if final_confirm.lower() != 'y':
            print("❌ Operation cancelled.")
            return
        
        # Insert to database
        success_count, error_count = insert_dummy_data(dummy_data)
        
        # Show final stats
        final_stats = get_database_stats()
        print(f"\n📊 Final database stats:")
        print(f"  - PIDUM records: {final_stats['pidum_count']} (+{final_stats['pidum_count'] - stats['pidum_count']})")
        print(f"  - PIDSUS records: {final_stats['pidsus_count']}")
        
        print(f"\n🎉 Realistic dummy data generation completed!")
        print(f"📍 You can now view the data at: http://localhost:5001/view_pidum")
        print(f"🧪 Test import APIs with generated data patterns")
        
    except Exception as e:
        print(f"\n❌ Error during dummy data generation: {e}")
        return

if __name__ == "__main__":
    main()