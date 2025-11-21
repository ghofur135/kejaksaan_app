import sys
import os

if getattr(sys, 'frozen', False):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pdfplumber
import pandas as pd
import os
from datetime import datetime
import re

class PDFtoCSVConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to CSV Converter - Multi Format")
        self.root.geometry("950x700")
        self.root.resizable(True, True)
        self.pdf_path = None
        self.output_path = None
        self.pdf_format = "auto"
        self.setup_ui()
    
    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(
            title_frame, 
            text="PDF to CSV Converter - Multi Format", 
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        format_frame = tk.LabelFrame(main_frame, text="Format PDF", font=("Arial", 10, "bold"), padx=10, pady=10)
        format_frame.pack(fill=tk.X, pady=(0, 15))
        self.format_var = tk.StringVar(value="auto")
        tk.Radiobutton(format_frame, text="Auto Detect", variable=self.format_var, value="auto", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(format_frame, text="Register SPDP (Penerimaan)", variable=self.format_var, value="spdp", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(format_frame, text="Register Penuntutan", variable=self.format_var, value="penuntutan", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(format_frame, text="Register Upaya Hukum (RP-11)", variable=self.format_var, value="rp11", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        pdf_frame = tk.LabelFrame(main_frame, text="1. Pilih File PDF", font=("Arial", 10, "bold"), padx=10, pady=10)
        pdf_frame.pack(fill=tk.X, pady=(0, 15))
        self.pdf_entry = tk.Entry(pdf_frame, font=("Arial", 10), state="readonly")
        self.pdf_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        browse_btn = tk.Button(pdf_frame, text="Browse PDF", command=self.browse_pdf,
            bg="#3498db", fg="white", font=("Arial", 10, "bold"), padx=20, cursor="hand2")
        browse_btn.pack(side=tk.RIGHT)
        
        output_frame = tk.LabelFrame(main_frame, text="2. Lokasi Penyimpanan CSV", font=("Arial", 10, "bold"), padx=10, pady=10)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        self.output_entry = tk.Entry(output_frame, font=("Arial", 10), state="readonly")
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        output_btn = tk.Button(output_frame, text="Pilih Lokasi", command=self.browse_output, bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), padx=20, cursor="hand2")
        output_btn.pack(side=tk.RIGHT)
        
        self.convert_btn = tk.Button(main_frame, text="🔄 CONVERT PDF TO CSV", command=self.convert_pdf, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), padx=30, pady=15, cursor="hand2", state=tk.DISABLED)
        self.convert_btn.pack(pady=20)
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=400)
        self.progress.pack(pady=(0, 15))
        
        log_frame = tk.LabelFrame(main_frame, text="Log Aktivitas", font=("Arial", 10, "bold"), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text = tk.Text(log_frame, height=12, font=("Consolas", 9), yscrollcommand=scrollbar.set, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        self.status_bar = tk.Label(self.root, text="Status: Siap", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.add_log("Aplikasi siap digunakan")
        self.add_log("Mendukung format: Register SPDP, Register Penuntutan, dan Register Upaya Hukum (RP-11)")
    
    def browse_pdf(self):
        filename = filedialog.askopenfilename(title="Pilih File PDF", filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
        if filename:
            self.pdf_path = filename
            self.pdf_entry.config(state=tk.NORMAL)
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, filename)
            self.pdf_entry.config(state="readonly")
            base_name = os.path.splitext(os.path.basename(filename))[0]
            output_dir = os.path.dirname(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_output = os.path.join(output_dir, f"{base_name}_extracted_{timestamp}.csv")
            self.output_path = default_output
            self.output_entry.config(state=tk.NORMAL)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, default_output)
            self.output_entry.config(state="readonly")
            self.convert_btn.config(state=tk.NORMAL)
            self.status_bar.config(text=f"Status: File PDF siap untuk dikonversi")
            self.add_log(f"✓ PDF dipilih: {os.path.basename(filename)}")
    
    def browse_output(self):
        if not self.pdf_path:
            messagebox.showwarning("Peringatan", "Pilih file PDF terlebih dahulu!")
            return
        filename = filedialog.asksaveasfilename(title="Simpan CSV Sebagai", defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if filename:
            self.output_path = filename
            self.output_entry.config(state=tk.NORMAL)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)
            self.output_entry.config(state="readonly")
            self.add_log(f"✓ Lokasi output: {os.path.basename(filename)}")
    
    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update()
    
    def detect_pdf_format(self, text_content):
        text_lower = text_content.lower()
        if "register penerimaan spdp" in text_lower or "pemberitahuan dimulainya penyidikan" in text_lower:
            return "spdp"
        elif "register penuntutan" in text_lower:
            return "penuntutan"
        elif "register upaya hukum" in text_lower or "rp-11" in text_lower:
            return "rp11"
        else:
            return "penuntutan"
    
    def extract_spdp_format(self, pdf):
        """
        Extract data dari Register SPDP (Penerimaan)
        Hanya mengambil 3 kolom:
        - No (nomor urut)
        - Tgl_Nomor (dari kolom 3: Tgl. diterima di Kejaksaan)
        - Pasal_yang_Disangkakan (dari kolom 7)
        """
        extracted_data = []
        total_pages = len(pdf.pages)
        self.add_log(f"Format: Register SPDP (Penerimaan)")
        
        for page_num, page in enumerate(pdf.pages, 1):
            self.add_log(f"Memproses halaman {page_num}/{total_pages}...")
            
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "intersection_tolerance": 10,
                "snap_tolerance": 5
            }
            
            tables = page.extract_tables(table_settings)
            
            if not tables:
                self.add_log(f"  - Tidak ada tabel di halaman {page_num}")
                continue
            
            for table_idx, table in enumerate(tables):
                self.add_log(f"  - Tabel {table_idx + 1}: {len(table)} baris, {len(table[0]) if table else 0} kolom")
                
                for row_idx, row in enumerate(table):
                    if row_idx < 2 or not row or len(row) < 8:
                        continue
                    
                    try:
                        # Kolom 0: No urut
                        no_urut = str(row[0]).strip() if row[0] else ''
                        
                        if not no_urut.isdigit():
                            continue
                        
                        # Kolom 3: Tgl. diterima di Kejaksaan
                        tgl_diterima = str(row[3]).strip() if len(row) > 3 and row[3] else ''
                        
                        # Kolom 7: Pasal yang disangkakan
                        pasal = str(row[7]).strip() if len(row) > 7 and row[7] else ''
                        
                        # Clean data
                        tgl_diterima = ' '.join(tgl_diterima.split())
                        pasal = ' '.join(pasal.split())
                        
                        # Skip jika tidak ada data tanggal dan pasal
                        if not tgl_diterima and not pasal:
                            continue
                        
                        record = {
                            'No': no_urut,
                            'Tgl_Nomor': tgl_diterima,
                            'Pasal_yang_Disangkakan': pasal
                        }
                        
                        extracted_data.append(record)
                        
                        tgl_preview = tgl_diterima[:30] + "..." if len(tgl_diterima) > 30 else tgl_diterima
                        pasal_preview = pasal[:50] + "..." if len(pasal) > 50 else pasal
                        self.add_log(f"    ✓ [{no_urut}] Tgl: {tgl_preview}")
                        if pasal:
                            self.add_log(f"       Pasal: {pasal_preview}")
                    
                    except Exception as e:
                        self.add_log(f"    ! Error pada baris {row_idx}: {str(e)}")
                        continue
        
        return extracted_data

    def extract_penuntutan_format(self, pdf):
        """Extract data dari Register Penuntutan"""
        extracted_data = []
        total_pages = len(pdf.pages)
        self.add_log(f"Format: Register Penuntutan")
        
        for page_num, page in enumerate(pdf.pages, 1):
            self.add_log(f"Memproses halaman {page_num}/{total_pages}...")
            
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "intersection_tolerance": 10
            }
            
            tables = page.extract_tables(table_settings)
            
            if not tables:
                continue
            
            for table in tables:
                for row_idx, row in enumerate(table):
                    if row_idx < 2 or not row or len(row) < 5:
                        continue
                    
                    try:
                        no_urut = str(row[0]).strip() if row[0] else ''
                        
                        if not no_urut.isdigit():
                            continue
                        
                        record = {
                            'No': no_urut,
                            'No_Tanggal_Register_Perkara': ' '.join(str(row[1]).split()) if len(row) > 1 and row[1] else '',
                            'Identitas_Tersangka': ' '.join(str(row[2]).split()) if len(row) > 2 and row[2] else '',
                            'Tindak_Pidana_Didakwakan': ' '.join(str(row[3]).split()) if len(row) > 3 and row[3] else '',
                            'Jaksa_Penuntut_Umum': ' '.join(str(row[4]).split()) if len(row) > 4 and row[4] else ''
                        }
                        
                        if record['Identitas_Tersangka'] or record['Tindak_Pidana_Didakwakan']:
                            extracted_data.append(record)
                            self.add_log(f"    ✓ [{no_urut}] {record['Identitas_Tersangka'][:40]}...")
                    except:
                        continue
        
        return extracted_data

    def extract_upayahukum_format(self, pdf):
        """
        Extract data dari Register Upaya Hukum (RP-11)
        Fokus pada kolom 10 (Banding), 15 (Kasasi), dan 22 (PK)
        """
        extracted_data = []
        total_pages = len(pdf.pages)
        self.add_log(f"Format: Register Upaya Hukum (RP-11)")
        
        for page_num, page in enumerate(pdf.pages, 1):
            self.add_log(f"Memproses halaman {page_num}/{total_pages}...")
            
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "intersection_tolerance": 10,
                "snap_tolerance": 5
            }
            
            tables = page.extract_tables(table_settings)
            
            if not tables:
                self.add_log(f"  - Tidak ada tabel di halaman {page_num}")
                continue
            
            for table_idx, table in enumerate(tables):
                total_cols = len(table[0]) if table else 0
                self.add_log(f"  - Tabel {table_idx + 1}: {len(table)} baris, {total_cols} kolom")
                
                for row_idx, row in enumerate(table):
                    # Skip header (2 baris pertama)
                    if row_idx < 2:
                        continue
                    
                    # Skip jika row kosong
                    if not row or len(row) < 3:
                        continue
                    
                    try:
                        # Kolom utama (kotak merah kiri)
                        no_urut = str(row[0]).strip() if row[0] else ''
                        
                        # Validasi nomor urut
                        if not no_urut.isdigit():
                            continue
                        
                        terdakwa = str(row[1]).strip() if row[1] else ''
                        no_rp9 = str(row[2]).strip() if row[2] else ''
                        
                        # Clean data
                        terdakwa = ' '.join(terdakwa.split())
                        no_rp9 = ' '.join(no_rp9.split())
                        
                        # Skip jika tidak ada data terdakwa
                        if not terdakwa:
                            continue
                        
                        # FOKUS EKSTRAK KOLOM 10, 15, 22 (dengan toleransi +/- 1 kolom)
                        
                        # Kolom 10: Banding - No. & Tgl. Akte Permohonan banding
                        banding_akte = ''
                        for col_idx in [9, 10, 11]:  # Toleransi kolom 9-11
                            if len(row) > col_idx:
                                cell = str(row[col_idx]).strip() if row[col_idx] else ''
                                if cell and cell not in ['-', '.', ''] and len(cell) > 3:
                                    banding_akte = ' '.join(cell.split())
                                    self.add_log(f"      [Banding] Kolom {col_idx}: {banding_akte[:40]}")
                                    break
                        
                        # Kolom 15: Kasasi - No. Tgl. Akte permohonan Kasasi
                        kasasi_akte = ''
                        for col_idx in [14, 15, 16]:  # Toleransi kolom 14-16
                            if len(row) > col_idx:
                                cell = str(row[col_idx]).strip() if row[col_idx] else ''
                                if cell and cell not in ['-', '.', ''] and len(cell) > 3:
                                    kasasi_akte = ' '.join(cell.split())
                                    self.add_log(f"      [Kasasi] Kolom {col_idx}: {kasasi_akte[:40]}")
                                    break
                        
                        # Kolom 22: PK - Tanggal Diajukan oleh Terpidana
                        pk_tanggal = ''
                        for col_idx in [21, 22, 23]:  # Toleransi kolom 21-23
                            if len(row) > col_idx:
                                cell = str(row[col_idx]).strip() if row[col_idx] else ''
                                if cell and cell not in ['-', '.', ''] and len(cell) > 3:
                                    pk_tanggal = ' '.join(cell.split())
                                    self.add_log(f"      [PK] Kolom {col_idx}: {pk_tanggal[:40]}")
                                    break
                        
                        # Tentukan jenis upaya hukum dan tanggal transaksi
                        jenis_upaya_hukum = ''
                        tanggal_transaksi = ''
                        
                        # Priority: Banding > Kasasi > PK
                        if banding_akte:
                            jenis_upaya_hukum = 'Banding'
                            tanggal_transaksi = banding_akte
                        elif kasasi_akte:
                            jenis_upaya_hukum = 'Kasasi'
                            tanggal_transaksi = kasasi_akte
                        elif pk_tanggal:
                            jenis_upaya_hukum = 'PK'
                            tanggal_transaksi = pk_tanggal
                        
                        # Buat record
                        record = {
                            'No': no_urut,
                            'Terdakwa_Terpidana': terdakwa,
                            'No_Tanggal_RP9': no_rp9,
                            'Jenis_Upaya_Hukum': jenis_upaya_hukum,
                            'Tanggal_Transaksi': tanggal_transaksi,
                            'Banding_Akte': banding_akte,
                            'Kasasi_Akte': kasasi_akte,
                            'PK_Tanggal': pk_tanggal
                        }
                        
                        extracted_data.append(record)
                        
                        # Log hasil
                        terdakwa_preview = terdakwa[:35] + "..." if len(terdakwa) > 35 else terdakwa
                        if jenis_upaya_hukum:
                            self.add_log(f"    ✓ [{no_urut}] {terdakwa_preview}")
                            self.add_log(f"       {jenis_upaya_hukum}: {tanggal_transaksi[:50]}")
                        else:
                            self.add_log(f"    ○ [{no_urut}] {terdakwa_preview} (Tidak ada upaya hukum)")
                    
                    except Exception as e:
                        self.add_log(f"    ! Error pada baris {row_idx}: {str(e)}")
                        continue
        
        return extracted_data

    def extract_pdf_data(self):
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                selected_format = self.format_var.get()
                
                if selected_format == "auto":
                    first_page_text = pdf.pages[0].extract_text() if pdf.pages else ""
                    detected_format = self.detect_pdf_format(first_page_text)
                    self.add_log(f"Auto detect: Format {detected_format.upper()} terdeteksi")
                else:
                    detected_format = selected_format
                    self.add_log(f"Format dipilih: {detected_format.upper()}")
                
                if detected_format == "spdp":
                    data = self.extract_spdp_format(pdf)
                elif detected_format == "penuntutan":
                    data = self.extract_penuntutan_format(pdf)
                elif detected_format == "rp11":
                    data = self.extract_upayahukum_format(pdf)
                else:
                    data = self.extract_penuntutan_format(pdf)
                
                self.add_log(f"✓ Ekstraksi selesai. Total data: {len(data)} baris")
                return data
        
        except Exception as e:
            self.add_log(f"✗ Error: {str(e)}")
            raise e
    
    def convert_pdf(self):
        if not self.pdf_path or not self.output_path:
            messagebox.showerror("Error", "Pilih file PDF dan lokasi output terlebih dahulu!")
            return
        
        self.convert_btn.config(state=tk.DISABLED)
        self.progress.start(10)
        self.status_bar.config(text="Status: Sedang mengkonversi...")
        
        try:
            self.add_log("=" * 60)
            self.add_log("Memulai proses konversi...")
            
            data = self.extract_pdf_data()
            
            if not data:
                messagebox.showwarning("Peringatan", "Tidak ada data yang berhasil diekstrak dari PDF!")
                self.add_log("✗ Tidak ada data yang ditemukan")
                return
            
            self.add_log("Membuat CSV file...")
            df = pd.DataFrame(data)
            
            # Remove duplicates
            df_clean = df.drop_duplicates()
            
            if len(df) != len(df_clean):
                self.add_log(f"Data sebelum cleaning: {len(df)} baris")
                self.add_log(f"Data setelah cleaning: {len(df_clean)} baris")
            
            # Save to CSV
            df_clean.to_csv(self.output_path, index=False, encoding='utf-8-sig')
            
            self.add_log(f"✓ File CSV berhasil disimpan!")
            self.add_log(f"✓ Lokasi: {self.output_path}")
            self.add_log(f"✓ Total baris data: {len(df_clean)}")
            self.add_log(f"✓ Kolom: {', '.join(df_clean.columns.tolist())}")
            self.add_log("=" * 60)
            
            result = messagebox.askyesno(
                "Konversi Berhasil!", 
                f"File CSV berhasil dibuat!\n\n"
                f"Total data: {len(df_clean)} baris\n"
                f"Kolom: {len(df_clean.columns)}\n"
                f"Lokasi: {self.output_path}\n\n"
                f"Apakah ingin membuka folder output?"
            )
            
            if result:
                os.startfile(os.path.dirname(self.output_path))
            
            self.status_bar.config(text=f"Status: Konversi berhasil - {len(df_clean)} data diekstrak")
        
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan:\n{str(e)}")
            self.add_log(f"✗ Error: {str(e)}")
            self.status_bar.config(text="Status: Konversi gagal")
        
        finally:
            self.progress.stop()
            self.convert_btn.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = PDFtoCSVConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
