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
        
        # Format selection frame
        format_frame = tk.LabelFrame(main_frame, text="Format PDF", font=("Arial", 10, "bold"), padx=10, pady=10)
        format_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.format_var = tk.StringVar(value="auto")
        
        formats = [
            ("Auto Detect", "auto"),
            ("Register SPDP (Penerimaan)", "spdp"),
            ("Register Penuntutan", "penuntutan"),
            ("Register Upaya Hukum (RP-11)", "upaya_hukum")
        ]
        
        for text, value in formats:
            rb = tk.Radiobutton(
                format_frame,
                text=text,
                variable=self.format_var,
                value=value,
                font=("Arial", 10)
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # File selection frame
        file_frame = tk.LabelFrame(main_frame, text="File Selection", font=("Arial", 10, "bold"), padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # PDF file selection
        pdf_frame = tk.Frame(file_frame)
        pdf_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(pdf_frame, text="PDF File:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.pdf_entry = tk.Entry(pdf_frame, font=("Arial", 10))
        self.pdf_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Button(
            pdf_frame,
            text="Browse",
            command=self.browse_pdf,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        # Output file selection
        output_frame = tk.Frame(file_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(output_frame, text="Output CSV:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.output_entry = tk.Entry(output_frame, font=("Arial", 10))
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Button(
            output_frame,
            text="Browse",
            command=self.browse_output,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        # Convert button
        tk.Button(
            main_frame,
            text="Convert to CSV",
            command=self.convert_to_csv,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            height=2
        ).pack(fill=tk.X, pady=(0, 15))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 15))
        
        # Log area
        log_frame = tk.LabelFrame(main_frame, text="Log", font=("Arial", 10, "bold"), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=10, font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_pdf(self):
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.pdf_path = filename
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, filename)
            
            # Auto-suggest output filename
            base_name = os.path.splitext(os.path.basename(filename))[0]
            output_path = os.path.join(os.path.dirname(filename), f"{base_name}_output.csv")
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_path)
            
            self.log_message(f"Selected PDF: {filename}")

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save CSV as",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.output_path = filename
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)
            self.log_message(f"Output will be saved to: {filename}")

    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def detect_format(self, pdf_path):
        """Detect PDF format based on content"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                
                if text:
                    text_lower = text.lower()
                    if "register penerimaan spdp" in text_lower or "pemberitahuan dimulainya penyidikan" in text_lower:
                        return "spdp"
                    elif "register penuntutan" in text_lower:
                        return "penuntutan"
                    elif "upaya hukum" in text_lower or "rp-11" in text_lower:
                        return "upaya_hukum"
                
                return "spdp"  # Default
        except Exception as e:
            self.log_message(f"Error detecting format: {str(e)}")
            return "spdp"

    def extract_spdp_format(self, pdf_path):
        """
        Extract data from REGISTER PENERIMAAN SPDP format
        MODIFIKASI: Menambahkan kolom Identitas Tersangka (kolom 4)
        Mengambil 4 kolom: No, Tgl_Nomor, Identitas_Tersangka, Pasal_yang_Disangkakan
        """
        all_data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                self.log_message(f"Processing page {page_num}/{len(pdf.pages)}...")
                
                tables = page.extract_tables()
                
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    
                    for row in table[1:]:  # Skip header
                        if row and len(row) > 7:
                            # Kolom 0: No
                            no = row[0] if row[0] else ""
                            
                            # Kolom 3: Tgl_Nomor (kolom "Tgl." dan "Nomor" di PDF)
                            tgl_nomor = row[3] if len(row) > 3 and row[3] else ""
                            
                            # Kolom 4: Identitas Tersangka (BARU DITAMBAHKAN)
                            identitas_tersangka = row[4] if len(row) > 4 and row[4] else ""
                            
                            # Kolom 7: Pasal yang Disangkakan
                            pasal = row[7] if len(row) > 7 and row[7] else ""
                            
                            # Filter baris yang valid (minimal ada nomor atau pasal)
                            if no.strip() or pasal.strip():
                                all_data.append({
                                    'No': no.strip(),
                                    'Tgl_Nomor': tgl_nomor.strip(),
                                    'Identitas_Tersangka': identitas_tersangka.strip(),
                                    'Pasal_yang_Disangkakan': pasal.strip()
                                })
        
        return pd.DataFrame(all_data)

    def extract_penuntutan_format(self, pdf_path):
        """Extract data from REGISTER PENUNTUTAN format"""
        all_data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                self.log_message(f"Processing page {page_num}/{len(pdf.pages)}...")
                
                tables = page.extract_tables()
                
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    
                    for row in table[1:]:
                        if row and len(row) > 5:
                            no = row[0] if row[0] else ""
                            no_tgl_register = row[1] if len(row) > 1 and row[1] else ""
                            identitas = row[2] if len(row) > 2 and row[2] else ""
                            tindak_pidana = row[3] if len(row) > 3 and row[3] else ""
                            jaksa_penuntut = row[4] if len(row) > 4 and row[4] else ""
                            
                            if no.strip() or identitas.strip():
                                all_data.append({
                                    'No': no.strip(),
                                    'No_Tanggal_Register_Perkara': no_tgl_register.strip(),
                                    'Identitas_Tersangka': identitas.strip(),
                                    'Tindak_Pidana_Didakwakan': tindak_pidana.strip(),
                                    'Jaksa_Penuntut_Umum': jaksa_penuntut.strip()
                                })
        
        return pd.DataFrame(all_data)

    def extract_upaya_hukum_format(self, pdf_path):
        """Extract data from REGISTER UPAYA HUKUM (RP-11) format"""
        all_data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                self.log_message(f"Processing page {page_num}/{len(pdf.pages)}...")
                
                tables = page.extract_tables()
                
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    
                    for row in table[1:]:
                        if row and len(row) > 22:
                            no = row[0] if row[0] else ""
                            banding = row[10] if len(row) > 10 and row[10] else ""
                            kasasi = row[15] if len(row) > 15 and row[15] else ""
                            pk = row[22] if len(row) > 22 and row[22] else ""
                            
                            if no.strip():
                                all_data.append({
                                    'No': no.strip(),
                                    'Banding': banding.strip(),
                                    'Kasasi': kasasi.strip(),
                                    'PK': pk.strip()
                                })
        
        return pd.DataFrame(all_data)

    def convert_to_csv(self):
        if not self.pdf_entry.get():
            messagebox.showerror("Error", "Please select a PDF file!")
            return
        
        if not self.output_entry.get():
            messagebox.showerror("Error", "Please specify output CSV file!")
            return
        
        self.pdf_path = self.pdf_entry.get()
        self.output_path = self.output_entry.get()
        
        try:
            self.progress.start()
            self.status_bar.config(text="Converting...")
            self.log_message("Starting conversion...")
            
            # Detect or use selected format
            format_type = self.format_var.get()
            if format_type == "auto":
                format_type = self.detect_format(self.pdf_path)
                self.log_message(f"Auto-detected format: {format_type}")
            else:
                self.log_message(f"Using selected format: {format_type}")
            
            # Extract data based on format
            if format_type == "spdp":
                df = self.extract_spdp_format(self.pdf_path)
                self.log_message("MODIFIKASI: Mengekstrak dengan kolom Identitas Tersangka")
            elif format_type == "penuntutan":
                df = self.extract_penuntutan_format(self.pdf_path)
            elif format_type == "upaya_hukum":
                df = self.extract_upaya_hukum_format(self.pdf_path)
            else:
                raise ValueError(f"Unknown format: {format_type}")
            
            if df.empty:
                self.log_message("Warning: No data extracted!")
                messagebox.showwarning("Warning", "No data was extracted from the PDF!")
                return
            
            # Save to CSV
            df.to_csv(self.output_path, index=False, encoding='utf-8-sig')
            
            self.log_message(f"Successfully extracted {len(df)} rows")
            self.log_message(f"Saved to: {self.output_path}")
            
            self.status_bar.config(text=f"Conversion completed - {len(df)} rows extracted")
            
            messagebox.showinfo(
                "Success",
                f"Conversion completed successfully!\n\n"
                f"Rows extracted: {len(df)}\n"
                f"Columns: {', '.join(df.columns)}\n"
                f"Output saved to:\n{self.output_path}"
            )
            
        except Exception as e:
            error_msg = f"Error during conversion: {str(e)}"
            self.log_message(error_msg)
            self.status_bar.config(text="Error occurred")
            messagebox.showerror("Error", error_msg)
        
        finally:
            self.progress.stop()

def main():
    root = tk.Tk()
    app = PDFtoCSVConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()