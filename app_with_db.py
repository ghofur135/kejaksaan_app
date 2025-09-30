from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, jsonify
import pandas as pd
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from database import (
    init_database, insert_pidum_data, insert_pidsus_data,
    get_all_pidum_data, get_all_pidsus_data,
    get_pidum_data_for_export, get_pidsus_data_for_export,
    get_database_stats, get_pidum_report_data
)
from import_helper import process_import_file, get_jenis_perkara_suggestions, prepare_import_data

def generate_pidum_chart(report_data):
    """Generate chart data for PIDUM report"""
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Prepare data for chart - show all jenis perkara including those with value 0
    jenis_perkara = [item['jenis_perkara'] for item in report_data]
    jumlah_data = [item['JUMLAH'] for item in report_data]
    
    if not jenis_perkara:  # If no data at all, create empty chart with all categories
        jenis_perkara = ['NARKOBA', 'PERKARA ANAK', 'KESUSILAAN', 'JUDI', 'KDRT', 'OHARDA', 'PERKARA LAINNYA']
        jumlah_data = [0] * 7
    
    # Create bar chart
    bars = plt.bar(range(len(jenis_perkara)), jumlah_data, color='#4472C4')
    
    # Customize chart
    plt.title('Grafik PIDUM', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Jenis Perkara', fontsize=12)
    plt.ylabel('Jumlah', fontsize=12)
    
    # Set x-axis labels
    plt.xticks(range(len(jenis_perkara)), jenis_perkara, rotation=45, ha='right')
    
    # Add value labels on bars (show all values, including 0)
    for i, (bar, value) in enumerate(zip(bars, jumlah_data)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(value), ha='center', va='bottom', fontweight='bold')
    
    # Set y-axis to start from 0 and add some padding
    max_value = max(jumlah_data) if jumlah_data and max(jumlah_data) > 0 else 5
    plt.ylim(0, max_value + 1)
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Convert to base64 string
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    chart_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return chart_base64

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

# Initialize database on startup
init_database()

# Custom Jinja2 filter for summing numeric strings
@app.template_filter('sum_numeric')
def sum_numeric(data_list, attribute):
    """Sum numeric values from a list of dictionaries, converting strings to integers"""
    try:
        total = 0
        for item in data_list:
            value = item.get(attribute, 0)
            # Convert to int, handle both string and int types
            if isinstance(value, str):
                total += int(value) if value.isdigit() else 0
            else:
                total += int(value)
        return total
    except (ValueError, TypeError):
        return 0

@app.route('/')
def index():
    stats = get_database_stats()
    return render_template('index.html', stats=stats)

@app.route('/input_pidum', methods=['GET', 'POST'])
def input_pidum():
    # Redirect langsung ke halaman pilihan import data PIDUM
    # Bisa pilih dari dropdown import tahapan penanganan
    if request.method == 'GET':
        return render_template('pilihan_import_pidum.html')
    
    # Jika POST, proses input manual
    if request.method == 'POST':
        try:
            # Get form data
            data = {
                'NO': request.form['no'],
                'PERIODE': request.form['periode'],
                'TANGGAL': request.form['tanggal'],
                'JENIS PERKARA': request.form['jenis_perkara'],
                'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',  # Default value for manual input
                'KETERANGAN': ''  # Default empty for manual input
            }
            
            # Insert to database
            insert_pidum_data(data)
            
            flash('Data PIDUM berhasil ditambahkan!', 'success')
            return redirect(url_for('input_pidum'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
    
    # Get data from database untuk fallback
    data = get_pidum_data_for_export()
    return render_template('pilihan_import_pidum.html', data=data)

@app.route('/manual_input_pidum', methods=['GET', 'POST'])
def manual_input_pidum():
    """Route untuk input manual data PIDUM (form asli)"""
    if request.method == 'POST':
        try:
            # Get form data
            data = {
                'NO': request.form['no'],
                'PERIODE': request.form['periode'],
                'TANGGAL': request.form['tanggal'],
                'JENIS PERKARA': request.form['jenis_perkara'],
                'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',  # Default value for manual input
                'KETERANGAN': request.form.get('keterangan', '')  # Get keterangan from form
            }
            
            # Insert to database
            insert_pidum_data(data)
            
            flash('Data PIDUM berhasil ditambahkan!', 'success')
            return redirect(url_for('manual_input_pidum'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
    
    # Get data from database
    data = get_pidum_data_for_export()
    return render_template('input_pidum.html', data=data)

@app.route('/input_pidsus', methods=['GET', 'POST'])
def input_pidsus():
    if request.method == 'POST':
        try:
            # Get form data
            data = {
                'NO': request.form['no'],
                'PERIODE': request.form['periode'],
                'TANGGAL': request.form['tanggal'],
                'JENIS PERKARA': request.form['jenis_perkara'],
                'PENYIDIKAN': request.form['penyidikan'],
                'PENUNTUTAN': request.form['penuntutan'],
                'KETERANGAN': request.form['keterangan']
            }
            
            # Insert to database
            insert_pidsus_data(data)
            
            flash('Data PIDSUS berhasil ditambahkan!', 'success')
            return redirect(url_for('input_pidsus'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
    
    # Get data from database
    data = get_pidsus_data_for_export()
    return render_template('input_pidsus.html', data=data)

@app.route('/view_pidum')
def view_pidum():
    data = get_pidum_data_for_export()
    return render_template('view_pidum.html', data=data)

@app.route('/view_pidsus')
def view_pidsus():
    data = get_pidsus_data_for_export()
    return render_template('view_pidsus.html', data=data)

@app.route('/laporan_pidum')
def laporan_pidum():
    # Get filter parameters
    bulan = request.args.get('bulan', type=int)
    tahun = request.args.get('tahun', type=int)
    
    # Default to current month/year if not specified
    from datetime import datetime
    if not bulan:
        bulan = datetime.now().month
    if not tahun:
        tahun = datetime.now().year
    
    # Get report data
    report_data = get_pidum_report_data(bulan, tahun)
    
    # Calculate totals
    total_pra_penuntutan = sum(item['PRA PENUNTUTAN'] for item in report_data)
    total_penuntutan = sum(item['PENUNTUTAN'] for item in report_data)
    total_upaya_hukum = sum(item['UPAYA HUKUM'] for item in report_data)
    total_keseluruhan = sum(item['JUMLAH'] for item in report_data)
    
    # Generate chart data
    chart_data = generate_pidum_chart(report_data)
    
    # Month names for display
    month_names = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    
    return render_template('laporan_pidum.html', 
                         report_data=report_data,
                         bulan=bulan, 
                         tahun=tahun,
                         bulan_nama=month_names.get(bulan, 'Tidak diketahui'),
                         total_pra_penuntutan=total_pra_penuntutan,
                         total_penuntutan=total_penuntutan,
                         total_upaya_hukum=total_upaya_hukum,
                         total_keseluruhan=total_keseluruhan,
                         chart_data=chart_data)

@app.route('/export_pidum_excel')
def export_pidum_excel():
    data = get_pidum_data_for_export()
    if not data:
        flash('Tidak ada data PIDUM untuk diekspor', 'warning')
        return redirect(url_for('view_pidum'))
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data PIDUM', index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Data PIDUM']
        
        # Style the header
        header_font = Font(bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid')
        header_alignment = Alignment(horizontal='center', vertical='center')
        
        for cell in worksheet[1]:  # First row
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
        
        # Auto-adjust column width
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_pidum_{timestamp}.xlsx"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

@app.route('/export_pidsus_excel')
def export_pidsus_excel():
    data = get_pidsus_data_for_export()
    if not data:
        flash('Tidak ada data PIDSUS untuk diekspor', 'warning')
        return redirect(url_for('view_pidsus'))
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data PIDSUS', index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Data PIDSUS']
        
        # Style the header
        header_font = Font(bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid')
        header_alignment = Alignment(horizontal='center', vertical='center')
        
        for cell in worksheet[1]:  # First row
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
        
        # Auto-adjust column width
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_pidsus_{timestamp}.xlsx"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

@app.route('/pidum_charts')
def pidum_charts():
    data = get_pidum_data_for_export()
    if not data:
        flash('Tidak ada data PIDUM untuk ditampilkan dalam grafik', 'warning')
        return redirect(url_for('view_pidum'))
    
    # Create charts
    charts = {}
    
    # Chart by Jenis Perkara
    df = pd.DataFrame(data)
    jenis_perkara_counts = df['JENIS PERKARA'].value_counts()
    
    plt.figure(figsize=(10, 6))
    jenis_perkara_counts.plot(kind='bar', color='skyblue')
    plt.title('Jumlah Kasus Berdasarkan Jenis Perkara (PIDUM)')
    plt.xlabel('Jenis Perkara')
    plt.ylabel('Jumlah Kasus')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    charts['jenis_perkara'] = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    
    # Chart by Upaya Hukum
    upaya_hukum_counts = df['UPAYA HUKUM'].value_counts()
    
    plt.figure(figsize=(8, 6))
    upaya_hukum_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightcoral', 'lightgreen', 'lightblue', 'lightyellow'])
    plt.title('Distribusi Upaya Hukum (PIDUM)')
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    charts['upaya_hukum'] = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    
    return render_template('pidum_charts.html', charts=charts)

@app.route('/pidsus_charts')
def pidsus_charts():
    data = get_pidsus_data_for_export()
    if not data:
        flash('Tidak ada data PIDSUS untuk ditampilkan dalam grafik', 'warning')
        return redirect(url_for('view_pidsus'))
    
    # Create charts
    charts = {}
    
    # Chart by Jenis Perkara
    df = pd.DataFrame(data)
    jenis_perkara_counts = df['JENIS PERKARA'].value_counts()
    
    plt.figure(figsize=(10, 6))
    jenis_perkara_counts.plot(kind='bar', color='skyblue')
    plt.title('Jumlah Kasus Berdasarkan Jenis Perkara (PIDSUS)')
    plt.xlabel('Jenis Perkara')
    plt.ylabel('Jumlah Kasus')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    charts['jenis_perkara'] = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    
    # Chart by Penyidikan
    penyidikan_counts = df['PENYIDIKAN'].value_counts()
    
    plt.figure(figsize=(8, 6))
    penyidikan_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightcoral', 'lightgreen', 'lightblue', 'lightyellow'])
    plt.title('Distribusi Penyidikan (PIDSUS)')
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    charts['penyidikan'] = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    
    return render_template('pidsus_charts.html', charts=charts)

@app.route('/database_info')
def database_info():
    """Route untuk melihat informasi database"""
    stats = get_database_stats()
    return f"""
    <h2>Database Information</h2>
    <p><strong>Database Path:</strong> {stats['database_path']}</p>
    <p><strong>PIDUM Records:</strong> {stats['pidum_count']}</p>
    <p><strong>PIDSUS Records:</strong> {stats['pidsus_count']}</p>
    <p><strong>Total Records:</strong> {stats['pidum_count'] + stats['pidsus_count']}</p>
    <p><a href="/">Back to Home</a></p>
    """

@app.route('/import_tahapan/<tahapan>', methods=['GET', 'POST'])
def import_tahapan(tahapan):
    """Route untuk import data berdasarkan tahapan penanganan perkara"""
    # Map tahapan URL ke tahapan database
    tahapan_mapping = {
        'pra_penuntutan': 'PRA PENUNTUTAN',
        'penuntutan': 'PENUNTUTAN', 
        'upaya_hukum': 'UPAYA HUKUM'
    }
    
    if tahapan not in tahapan_mapping:
        flash('Tahapan tidak valid', 'error')
        return redirect(url_for('input_pidum'))
    
    tahapan_penanganan = tahapan_mapping[tahapan]
    
    if request.method == 'POST':
        # Check if file is uploaded
        if 'file' not in request.files:
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(request.url)
        
        if file:
            # Process the uploaded file with tahapan
            result = process_import_file(file, tahapan_penanganan)
            
            if result['success']:
                # Store import data in session for preview
                session['import_data'] = result['data']
                session['import_filename'] = file.filename
                session['import_tahapan'] = tahapan_penanganan
                
                # Add suggestions for jenis perkara
                for i, row in enumerate(result['data']):
                    original_jenis = row.get('JENIS_PERKARA_ORIGINAL', '')
                    suggestion = get_jenis_perkara_suggestions(original_jenis)
                    result['data'][i]['SUGGESTED_JENIS_PERKARA'] = suggestion
                
                return render_template('import_tahapan_preview.html', 
                                     import_data=result['data'],
                                     filename=file.filename,
                                     total_rows=result['total_rows'],
                                     tahapan_penanganan=tahapan_penanganan)
            else:
                flash(f'Error memproses file: {result["error"]}', 'error')
                return redirect(request.url)
    
    # Render template berdasarkan tahapan
    template_mapping = {
        'pra_penuntutan': 'import_pra_penuntutan.html',
        'penuntutan': 'import_penuntutan.html',
        'upaya_hukum': 'import_upaya_hukum.html'
    }
    
    return render_template(template_mapping[tahapan])

@app.route('/confirm_import_tahapan', methods=['POST'])
def confirm_import_tahapan():
    """Confirm and process import with selected jenis perkara for specific tahapan"""
    import_data = session.get('import_data', [])
    tahapan_penanganan = session.get('import_tahapan', 'PRA PENUNTUTAN')
    
    if not import_data:
        flash('Tidak ada data import yang tersedia', 'error')
        return redirect(url_for('input_pidum'))
    
    try:
        # Get data from form
        prepared_data = []
        
        for i, original_row in enumerate(import_data):
            # Check if this row should be included (not removed)
            jenis_perkara_key = f'jenis_perkara_{i}'
            if jenis_perkara_key not in request.form:
                continue  # Skip removed rows
            
            # Get form data for this row
            periode = request.form.get(f'periode_{i}', '1')
            tanggal = request.form.get(f'tanggal_{i}', datetime.now().strftime('%Y-%m-%d'))
            jenis_perkara = request.form.get(jenis_perkara_key, 'PERKARA LAINNYA')
            keterangan = request.form.get(f'keterangan_{i}', '')
            
            # Prepare data for database insertion
            prepared_row = {
                'NO': str(original_row.get('NO', i + 1)),
                'PERIODE': str(periode),
                'TANGGAL': tanggal,
                'JENIS PERKARA': jenis_perkara,
                'TAHAPAN_PENANGANAN': tahapan_penanganan,
                'KETERANGAN': str(keterangan)
            }
            
            prepared_data.append(prepared_row)
        
        # Insert data to database
        success_count = 0
        error_count = 0
        error_details = []
        
        for data in prepared_data:
            try:
                insert_pidum_data(data)
                success_count += 1
            except Exception as e:
                error_count += 1
                error_details.append(f"Baris {data.get('NO', '?')}: {str(e)}")
                print(f"Error inserting row {data.get('NO', '?')}: {e}")
        
        # Clear session data
        session.pop('import_data', None)
        session.pop('import_filename', None)
        session.pop('import_tahapan', None)
        
        # Show results
        if success_count > 0:
            flash(f'Berhasil import {success_count} data {tahapan_penanganan}', 'success')
            if error_count > 0:
                flash(f'{error_count} data gagal diimport', 'warning')
                # Optionally show error details
                for error in error_details[:5]:  # Show max 5 errors
                    flash(error, 'warning')
        else:
            flash('Tidak ada data yang berhasil diimport', 'error')
            if error_details:
                for error in error_details[:3]:  # Show max 3 errors
                    flash(error, 'error')
            
    except Exception as e:
        flash(f'Error saat import data: {str(e)}', 'error')
    
    return redirect(url_for('view_pidum'))

@app.route('/import_pidum', methods=['GET', 'POST'])
def import_pidum():
    """Route untuk import data PIDUM dari file Excel/CSV"""
    if request.method == 'POST':
        # Check if file is uploaded
        if 'file' not in request.files:
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(request.url)
        
        if file:
            # Process the uploaded file
            result = process_import_file(file)
            
            if result['success']:
                # Store import data in session for preview
                session['import_data'] = result['data']
                session['import_filename'] = file.filename
                
                # Add suggestions for jenis perkara
                for i, row in enumerate(result['data']):
                    original_jenis = row.get('JENIS_PERKARA_ORIGINAL', '')
                    suggestion = get_jenis_perkara_suggestions(original_jenis)
                    result['data'][i]['SUGGESTED_JENIS_PERKARA'] = suggestion
                
                return render_template('import_preview.html', 
                                     import_data=result['data'],
                                     filename=file.filename,
                                     total_rows=result['total_rows'],
                                     data_type='PIDUM')
            else:
                flash(f'Error memproses file: {result["error"]}', 'error')
                return redirect(request.url)
    
    return render_template('import_pidum.html')

@app.route('/confirm_import_pidum', methods=['POST'])
def confirm_import_pidum():
    """Confirm and process PIDUM import with selected jenis perkara"""
    import_data = session.get('import_data', [])
    
    if not import_data:
        flash('Tidak ada data import yang tersedia', 'error')
        return redirect(url_for('import_pidum'))
    
    try:
        # Get data from form
        prepared_data = []
        
        for i, original_row in enumerate(import_data):
            # Check if this row should be included (not removed)
            jenis_perkara_key = f'jenis_perkara_{i}'
            if jenis_perkara_key not in request.form:
                continue  # Skip removed rows
            
            # Get form data for this row
            periode = request.form.get(f'periode_{i}', '1')
            tanggal = request.form.get(f'tanggal_{i}', datetime.now().strftime('%Y-%m-%d'))
            jenis_perkara = request.form.get(jenis_perkara_key, 'PERKARA LAINNYA')
            
            # Prepare data for database insertion
            prepared_row = {
                'NO': str(original_row.get('NO', i + 1)),
                'PERIODE': str(periode),
                'TANGGAL': tanggal,
                'JENIS PERKARA': jenis_perkara
            }
            
            prepared_data.append(prepared_row)
        
        # Insert data to database
        success_count = 0
        error_count = 0
        error_details = []
        
        for data in prepared_data:
            try:
                insert_pidum_data(data)
                success_count += 1
            except Exception as e:
                error_count += 1
                error_details.append(f"Baris {data.get('NO', '?')}: {str(e)}")
                print(f"Error inserting row {data.get('NO', '?')}: {e}")
        
        # Clear session data
        session.pop('import_data', None)
        session.pop('import_filename', None)
        
        # Show results
        if success_count > 0:
            flash(f'Berhasil import {success_count} data PIDUM', 'success')
            if error_count > 0:
                flash(f'{error_count} data gagal diimport', 'warning')
                # Optionally show error details
                for error in error_details[:5]:  # Show max 5 errors
                    flash(error, 'warning')
        else:
            flash('Tidak ada data yang berhasil diimport', 'error')
            if error_details:
                for error in error_details[:3]:  # Show max 3 errors
                    flash(error, 'error')
            
    except Exception as e:
        flash(f'Error saat import data: {str(e)}', 'error')
    
    return redirect(url_for('view_pidum'))

# Register PDF conversion routes
try:
    from pdf_routes import register_pdf_routes
    register_pdf_routes(app)
    print("PDF conversion routes registered successfully")
except ImportError as e:
    print(f"Warning: Could not register PDF routes: {e}")

if __name__ == '__main__':
    print(f"Database initialized at: {get_database_stats()['database_path']}")
    app.run(debug=True, port=5001)