#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script untuk cek data pasal di database"""

import sys
sys.path.insert(0, 'src')

from models.mysql_database import MySQLDatabase
import json

def check_pidum_data():
    """Check PIDUM data with pasal information"""
    db = MySQLDatabase()

    try:
        with db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)

            # Get sample data
            query = """
                SELECT
                    id,
                    no,
                    identitas_tersangka,
                    jenis_perkara,
                    tahapan_penanganan,
                    tanggal,
                    keterangan,
                    periode
                FROM pidum_data
                ORDER BY created_at DESC
                LIMIT 20
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            print("=" * 100)
            print("SAMPLE DATA PIDUM (20 rows terbaru)")
            print("=" * 100)
            print(f"Total rows di database: {len(rows)}")
            print()

            if not rows:
                print("[!] Tidak ada data di tabel pidum_data")
                return

            # Print in table format
            print(f"{'ID':<5} {'No':<10} {'Nama Tersangka':<25} {'Jenis Perkara':<20} {'Tahapan':<15} {'Tanggal':<12} {'Pasal/Keterangan':<30}")
            print("-" * 135)

            for row in rows:
                print(f"{row['id']:<5} "
                      f"{str(row['no'])[:10]:<10} "
                      f"{str(row.get('identitas_tersangka', '-'))[:25]:<25} "
                      f"{str(row['jenis_perkara'])[:20]:<20} "
                      f"{str(row['tahapan_penanganan'])[:15]:<15} "
                      f"{str(row['tanggal'])[:12]:<12} "
                      f"{str(row.get('keterangan', '-'))[:30]:<30}")

            print()
            print("=" * 100)
            print("ANALISA FIELD KETERANGAN (PASAL)")
            print("=" * 100)

            # Analyze keterangan field
            cursor.execute("""
                SELECT
                    keterangan,
                    COUNT(*) as count
                FROM pidum_data
                WHERE keterangan IS NOT NULL AND keterangan != ''
                GROUP BY keterangan
                ORDER BY count DESC
                LIMIT 10
            """)

            keterangan_stats = cursor.fetchall()

            print("\nTop 10 nilai di field 'keterangan':")
            print(f"{'Keterangan':<50} {'Jumlah':<10}")
            print("-" * 60)
            for stat in keterangan_stats:
                print(f"{str(stat['keterangan'])[:50]:<50} {stat['count']:<10}")

            # Check for pasal patterns
            print("\n" + "=" * 100)
            print("CEK PATTERN PASAL")
            print("=" * 100)

            cursor.execute("""
                SELECT
                    identitas_tersangka,
                    jenis_perkara,
                    tahapan_penanganan,
                    keterangan,
                    tanggal
                FROM pidum_data
                WHERE keterangan IS NOT NULL AND keterangan != ''
                LIMIT 5
            """)

            samples = cursor.fetchall()
            print("\nSample data dengan keterangan:")
            for i, sample in enumerate(samples, 1):
                print(f"\nSample {i}:")
                print(f"  Nama: {sample.get('identitas_tersangka', '-')}")
                print(f"  Jenis: {sample['jenis_perkara']}")
                print(f"  Tahapan: {sample['tahapan_penanganan']}")
                print(f"  Tanggal: {sample['tanggal']}")
                print(f"  Keterangan (Pasal): {sample['keterangan']}")

            # Check data structure for report
            print("\n" + "=" * 100)
            print("SIMULASI DATA UNTUK LAPORAN PELACAKAN")
            print("=" * 100)

            cursor.execute("""
                SELECT
                    identitas_tersangka as nama_tersangka,
                    MAX(keterangan) as pasal,
                    jenis_perkara,
                    MAX(CASE WHEN tahapan_penanganan = 'PRA PENUNTUTAN'
                        THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as pra_penuntutan,
                    MAX(CASE WHEN tahapan_penanganan = 'PENUNTUTAN'
                        THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as penuntutan,
                    MAX(CASE WHEN tahapan_penanganan = 'UPAYA HUKUM'
                        THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as upaya_hukum
                FROM pidum_data
                WHERE identitas_tersangka IS NOT NULL AND identitas_tersangka != ''
                GROUP BY identitas_tersangka, jenis_perkara
                LIMIT 5
            """)

            report_preview = cursor.fetchall()

            print("\nPreview Laporan (Format seperti gambar):")
            print(f"{'No':<5} {'Nama Tersangka':<25} {'Pasal':<15} {'Jenis Perkara':<20} {'Pra Penuntutan':<15} {'Penuntutan':<15} {'Upaya Hukum':<15}")
            print("-" * 125)

            for i, row in enumerate(report_preview, 1):
                print(f"{i:<5} "
                      f"{str(row.get('nama_tersangka', '-'))[:25]:<25} "
                      f"{str(row.get('pasal', '-'))[:15]:<15} "
                      f"{str(row['jenis_perkara'])[:20]:<20} "
                      f"{str(row.get('pra_penuntutan', '-'))[:15]:<15} "
                      f"{str(row.get('penuntutan', '-'))[:15]:<15} "
                      f"{str(row.get('upaya_hukum', '-'))[:15]:<15}")

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

def check_pidsus_data():
    """Check PIDSUS data with pasal information"""
    db = MySQLDatabase()

    try:
        with db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT COUNT(*) as count FROM pidsus_data
            """)
            count = cursor.fetchone()['count']

            print("\n" + "=" * 100)
            print(f"DATA PIDSUS: Total {count} rows")
            print("=" * 100)

            if count > 0:
                cursor.execute("""
                    SELECT
                        id, no, nama_tersangka, jenis_perkara,
                        tanggal, keterangan
                    FROM pidsus_data
                    LIMIT 5
                """)
                rows = cursor.fetchall()

                print(f"\n{'ID':<5} {'No':<10} {'Nama':<25} {'Jenis':<20} {'Keterangan (Pasal)':<30}")
                print("-" * 95)
                for row in rows:
                    print(f"{row['id']:<5} "
                          f"{str(row['no'])[:10]:<10} "
                          f"{str(row.get('nama_tersangka', '-'))[:25]:<25} "
                          f"{str(row['jenis_perkara'])[:20]:<20} "
                          f"{str(row.get('keterangan', '-'))[:30]:<30}")

    except Exception as e:
        print(f"[ERROR] Error checking PIDSUS: {e}")

if __name__ == '__main__':
    print("\n=== CEK DATA PASAL DI DATABASE KEJAKSAAN APP ===\n")
    check_pidum_data()
    check_pidsus_data()
    print("\n=== Selesai ===\n")
