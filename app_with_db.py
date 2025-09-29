from flask import Flask, render_template, request, redirect, url_for, flash, send_file
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
    get_database_stats
)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
    if request.method == 'POST':
        try:
            # Get form data
            data = {
                'NO': request.form['no'],
                'PERIODE': request.form['periode'],
                'TANGGAL': request.form['tanggal'],
                'JENIS PERKARA': request.form['jenis_perkara'],
                'PRA PENUTUTAN': request.form['pra_penututan'],
                'PENUNTUTAN': request.form['penuntutan'],
                'UPAYA HUKUM': request.form['upaya_hukum']
            }
            
            # Insert to database
            insert_pidum_data(data)
            
            flash('Data PIDUM berhasil ditambahkan!', 'success')
            return redirect(url_for('input_pidum'))
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

if __name__ == '__main__':
    print(f"Database initialized at: {get_database_stats()['database_path']}")
    app.run(debug=True, port=5001)