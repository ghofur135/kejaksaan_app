"""
Routes untuk fitur konversi PDF ke CSV
Menangani upload PDF, konversi, dan integrasi dengan sistem import
"""

import os
import logging
from io import StringIO
from flask import render_template, request, flash, redirect, url_for, session, Response
import pandas as pd
from pdf_to_csv_converter import PDFToCSVConverter

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_pdf_routes(app):
    """Register semua routes untuk PDF conversion"""
    
    @app.route('/convert_pdf_to_csv', methods=['GET', 'POST'])
    def convert_pdf_to_csv():
        """Halaman utama untuk konversi PDF ke CSV"""
        if request.method == 'GET':
            # Check available libraries
            converter = PDFToCSVConverter()
            available_libs = []
            for lib, available in converter.available_libraries.items():
                if available:
                    if lib == 'tabula':
                        available_libs.append('tabula-py')
                    elif lib == 'camelot':
                        available_libs.append('camelot-py')
                    elif lib == 'pdfplumber':
                        available_libs.append('pdfplumber')
            
            return render_template('convert_pdf_to_csv.html', available_libs=available_libs)
        
        try:
            # Check if file was uploaded
            if 'pdf_file' not in request.files:
                flash('Tidak ada file yang dipilih', 'error')
                return redirect(request.url)
            
            file = request.files['pdf_file']
            if file.filename == '':
                flash('Tidak ada file yang dipilih', 'error')
                return redirect(request.url)
            
            if not file.filename.lower().endswith('.pdf'):
                flash('File harus berformat PDF', 'error')
                return redirect(request.url)
            
            # Get conversion options
            library_choice = request.form.get('method', 'auto')  # Changed from 'library_choice' to 'method'
            pages = request.form.get('pages', 'all')
            
            # Save uploaded file temporarily
            upload_folder = '/tmp'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)
            
            # Initialize converter
            converter = PDFToCSVConverter()
            
            # Convert PDF to tables
            tables = converter.convert_pdf_to_dataframes(
                pdf_path=file_path,
                library_choice=library_choice,
                pages=pages
            )
            
            if not tables:
                flash('Tidak ada tabel yang ditemukan dalam PDF', 'warning')
                return redirect(request.url)
            
            # Clean up temporary file
            os.remove(file_path)
            
            # Store results in session
            session['converted_tables'] = [df.to_json(orient='records') for df in tables]
            session['original_filename'] = file.filename
            
            flash(f'Berhasil mengonversi PDF! Ditemukan {len(tables)} tabel.', 'success')
            return redirect(url_for('pdf_conversion_result'))
            
        except Exception as e:
            logger.error(f"Error converting PDF: {e}")
            flash(f'Error saat konversi PDF: {str(e)}', 'error')
            return redirect(request.url)
    
    @app.route('/pdf_conversion_result')
    def pdf_conversion_result():
        """Tampilkan hasil konversi PDF"""
        tables = session.get('converted_tables', [])
        original_filename = session.get('original_filename', 'unknown.pdf')
        
        if not tables:
            flash('Tidak ada data konversi ditemukan', 'error')
            return redirect(url_for('convert_pdf_to_csv'))
        
        # Convert JSON back to DataFrame for display
        tables_df = []
        for table_json in tables:
            df = pd.read_json(StringIO(table_json), orient='records')
            tables_df.append(df)
        
        return render_template('pdf_conversion_result.html', 
                             tables=tables_df, 
                             original_filename=original_filename)
    
    @app.route('/download_converted_csv')
    def download_converted_csv():
        """Download hasil konversi PDF sebagai file CSV"""
        try:
            tables = session.get('converted_tables', [])
            original_filename = session.get('original_filename', 'converted.pdf')
            
            if not tables:
                flash('Tidak ada data untuk didownload', 'error')
                return redirect(url_for('convert_pdf_to_csv'))
            
            # Gabungkan semua tabel jika ada lebih dari satu
            all_dataframes = []
            for table_json in tables:
                df = pd.read_json(StringIO(table_json), orient='records')
                all_dataframes.append(df)
            
            # Jika hanya satu tabel, gunakan langsung
            if len(all_dataframes) == 1:
                combined_df = all_dataframes[0]
            else:
                # Jika beberapa tabel, tambahkan separator
                combined_df = pd.DataFrame()
                for i, df in enumerate(all_dataframes):
                    if i > 0:
                        # Tambah baris kosong sebagai pemisah
                        separator = pd.DataFrame([[''] * len(df.columns)], columns=df.columns)
                        combined_df = pd.concat([combined_df, separator], ignore_index=True)
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
            
            # Buat nama file output
            base_name = os.path.splitext(original_filename)[0]
            csv_filename = f"{base_name}_converted.csv"
            
            # Buat response untuk download
            output = StringIO()
            combined_df.to_csv(output, index=False, encoding='utf-8')
            output.seek(0)
            
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename={csv_filename}'}
            )
            
        except Exception as e:
            logger.error(f"Error downloading converted CSV: {e}")
            flash(f'Error saat download: {str(e)}', 'error')
            return redirect(url_for('pdf_conversion_result'))
    
    @app.route('/import_from_converted_csv/<tahapan>')
    def import_from_converted_csv(tahapan):
        """Import hasil konversi langsung ke tahapan tertentu"""
        try:
            tables = session.get('converted_tables', [])
            
            if not tables:
                flash('Tidak ada data untuk diimport', 'error')
                return redirect(url_for('convert_pdf_to_csv'))
            
            # Validasi tahapan
            valid_tahapan = ['pra_penuntutan', 'penuntutan', 'upaya_hukum']
            if tahapan not in valid_tahapan:
                flash('Tahapan tidak valid', 'error')
                return redirect(url_for('pdf_conversion_result'))
            
            # Convert JSON back to DataFrame
            all_dataframes = []
            for table_json in tables:
                df = pd.read_json(StringIO(table_json), orient='records')
                all_dataframes.append(df)
            
            # Gabungkan semua tabel
            if len(all_dataframes) == 1:
                combined_df = all_dataframes[0]
            else:
                combined_df = pd.concat(all_dataframes, ignore_index=True)
            
            # Simpan DataFrame ke session untuk preview import
            session['import_preview_data'] = combined_df.to_json(orient='records')
            session['import_tahapan'] = tahapan
            session['import_source'] = 'pdf_conversion'
            
            # Redirect ke halaman preview import
            return redirect(url_for('import_tahapan_preview', tahapan=tahapan))
            
        except Exception as e:
            logger.error(f"Error importing from converted CSV: {e}")
            flash(f'Error saat import: {str(e)}', 'error')
            return redirect(url_for('pdf_conversion_result'))
    
    @app.route('/check_pdf_libraries')
    def check_pdf_libraries():
        """Check status instalasi library PDF"""
        converter = PDFToCSVConverter()
        status = converter.check_library_availability()
        return {'libraries': status}