#!/usr/bin/env python3
"""
PDF to CSV Converter for PIDUM data
Mengkonversi tabel dari file PDF menjadi format CSV yang siap di-import
"""

import pandas as pd
import os
from datetime import datetime

try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False

try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

def check_dependencies():
    """Check which PDF processing libraries are available"""
    available = []
    if TABULA_AVAILABLE:
        available.append("tabula-py")
    if CAMELOT_AVAILABLE:
        available.append("camelot-py")
    if PDFPLUMBER_AVAILABLE:
        available.append("pdfplumber")
    
    return available

def convert_pdf_to_csv_tabula(pdf_path, output_path=None, pages="all"):
    """
    Convert PDF table to CSV using tabula-py
    
    Args:
        pdf_path (str): Path to PDF file
        output_path (str): Output CSV path (optional)
        pages (str): Pages to extract ("all" or "1,2,3")
    
    Returns:
        list: List of DataFrames extracted from PDF
    """
    if not TABULA_AVAILABLE:
        raise ImportError("tabula-py is not installed. Install with: pip install tabula-py")
    
    try:
        # Extract tables from PDF
        print(f"🔄 Extracting tables from {pdf_path} using tabula-py...")
        tables = tabula.read_pdf(pdf_path, pages=pages, multiple_tables=True)
        
        if not tables:
            print("❌ No tables found in PDF")
            return []
        
        print(f"✅ Found {len(tables)} table(s)")
        
        # Process each table
        processed_tables = []
        for i, table in enumerate(tables):
            # Clean table data
            cleaned_table = clean_pidum_table(table)
            processed_tables.append(cleaned_table)
            
            # Save to CSV if output path provided
            if output_path:
                if len(tables) > 1:
                    csv_path = output_path.replace('.csv', f'_table_{i+1}.csv')
                else:
                    csv_path = output_path
                
                cleaned_table.to_csv(csv_path, index=False)
                print(f"💾 Saved table {i+1} to {csv_path}")
        
        return processed_tables
        
    except Exception as e:
        print(f"❌ Error with tabula-py: {e}")
        return []

def convert_pdf_to_csv_camelot(pdf_path, output_path=None):
    """
    Convert PDF table to CSV using camelot-py
    
    Args:
        pdf_path (str): Path to PDF file
        output_path (str): Output CSV path (optional)
    
    Returns:
        list: List of DataFrames extracted from PDF
    """
    if not CAMELOT_AVAILABLE:
        raise ImportError("camelot-py is not installed. Install with: pip install camelot-py[cv]")
    
    try:
        print(f"🔄 Extracting tables from {pdf_path} using camelot-py...")
        tables = camelot.read_pdf(pdf_path)
        
        if not tables:
            print("❌ No tables found in PDF")
            return []
        
        print(f"✅ Found {len(tables)} table(s)")
        
        processed_tables = []
        for i, table in enumerate(tables):
            # Convert to DataFrame
            df = table.df
            
            # Clean table data
            cleaned_table = clean_pidum_table(df)
            processed_tables.append(cleaned_table)
            
            # Save to CSV if output path provided
            if output_path:
                if len(tables) > 1:
                    csv_path = output_path.replace('.csv', f'_table_{i+1}.csv')
                else:
                    csv_path = output_path
                
                cleaned_table.to_csv(csv_path, index=False)
                print(f"💾 Saved table {i+1} to {csv_path}")
        
        return processed_tables
        
    except Exception as e:
        print(f"❌ Error with camelot-py: {e}")
        return []

def convert_pdf_to_csv_pdfplumber(pdf_path, output_path=None):
    """
    Convert PDF table to CSV using pdfplumber
    
    Args:
        pdf_path (str): Path to PDF file
        output_path (str): Output CSV path (optional)
    
    Returns:
        list: List of DataFrames extracted from PDF
    """
    if not PDFPLUMBER_AVAILABLE:
        raise ImportError("pdfplumber is not installed. Install with: pip install pdfplumber")
    
    try:
        print(f"🔄 Extracting tables from {pdf_path} using pdfplumber...")
        processed_tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            table_count = 0
            
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                
                for table in tables:
                    if table and len(table) > 1:  # Must have header + data
                        # Convert to DataFrame
                        headers = table[0]
                        data = table[1:]
                        df = pd.DataFrame(data, columns=headers)
                        
                        # Clean table data
                        cleaned_table = clean_pidum_table(df)
                        processed_tables.append(cleaned_table)
                        table_count += 1
                        
                        # Save to CSV if output path provided
                        if output_path:
                            if table_count > 1:
                                csv_path = output_path.replace('.csv', f'_page_{page_num+1}_table_{table_count}.csv')
                            else:
                                csv_path = output_path
                            
                            cleaned_table.to_csv(csv_path, index=False)
                            print(f"💾 Saved table from page {page_num+1} to {csv_path}")
        
        print(f"✅ Found {len(processed_tables)} table(s)")
        return processed_tables
        
    except Exception as e:
        print(f"❌ Error with pdfplumber: {e}")
        return []

def clean_pidum_table(df):
    """
    Clean and standardize PIDUM table data
    
    Args:
        df (DataFrame): Raw table data
    
    Returns:
        DataFrame: Cleaned table data
    """
    # Copy dataframe
    cleaned_df = df.copy()
    
    # Remove empty rows and columns
    cleaned_df = cleaned_df.dropna(how='all')  # Remove completely empty rows
    cleaned_df = cleaned_df.loc[:, ~cleaned_df.isnull().all()]  # Remove empty columns
    
    # Clean column names
    if not cleaned_df.empty:
        # Standardize column names
        column_mapping = {
            'no': 'NO',
            'nomor': 'NO',
            'periode': 'PERIODE',
            'tanggal': 'TANGGAL',
            'tgl': 'TANGGAL',
            'date': 'TANGGAL',
            'jenis_perkara': 'JENIS PERKARA',
            'jenis perkara': 'JENIS PERKARA',
            'kategori': 'JENIS PERKARA',
            'keterangan': 'KETERANGAN',
            'pasal': 'KETERANGAN',
            'description': 'KETERANGAN'
        }
        
        # Apply column mapping
        new_columns = []
        for col in cleaned_df.columns:
            col_lower = str(col).lower().strip()
            mapped_col = column_mapping.get(col_lower, col)
            new_columns.append(mapped_col)
        
        cleaned_df.columns = new_columns
    
    # Clean data values
    for col in cleaned_df.columns:
        if col in cleaned_df.columns:
            # Remove extra whitespace
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            
            # Replace empty strings with proper values
            cleaned_df[col] = cleaned_df[col].replace('', None)
            cleaned_df[col] = cleaned_df[col].replace('nan', None)
    
    # Ensure required columns exist
    required_columns = ['NO', 'PERIODE', 'TANGGAL', 'JENIS PERKARA', 'KETERANGAN']
    for col in required_columns:
        if col not in cleaned_df.columns:
            cleaned_df[col] = ''
    
    # Reorder columns
    available_columns = [col for col in required_columns if col in cleaned_df.columns]
    extra_columns = [col for col in cleaned_df.columns if col not in required_columns]
    final_columns = available_columns + extra_columns
    
    cleaned_df = cleaned_df[final_columns]
    
    return cleaned_df

def auto_convert_pdf_to_csv(pdf_path, output_path=None, method="auto"):
    """
    Automatically convert PDF to CSV using best available method
    
    Args:
        pdf_path (str): Path to PDF file
        output_path (str): Output CSV path (optional)
        method (str): "auto", "tabula", "camelot", or "pdfplumber"
    
    Returns:
        list: List of DataFrames extracted from PDF
    """
    # Generate output path if not provided
    if not output_path:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"{base_name}_converted.csv"
    
    print(f"🚀 Starting PDF to CSV conversion...")
    print(f"📄 Input: {pdf_path}")
    print(f"💾 Output: {output_path}")
    
    # Check available libraries
    available_libs = check_dependencies()
    print(f"📚 Available libraries: {available_libs}")
    
    if not available_libs:
        print("❌ No PDF processing libraries available!")
        print("Install one of: pip install tabula-py, pip install camelot-py[cv], pip install pdfplumber")
        return []
    
    # Choose method
    if method == "auto":
        if "tabula-py" in available_libs:
            method = "tabula"
        elif "camelot-py" in available_libs:
            method = "camelot"
        elif "pdfplumber" in available_libs:
            method = "pdfplumber"
    
    # Convert based on method
    try:
        if method == "tabula" and TABULA_AVAILABLE:
            return convert_pdf_to_csv_tabula(pdf_path, output_path)
        elif method == "camelot" and CAMELOT_AVAILABLE:
            return convert_pdf_to_csv_camelot(pdf_path, output_path)
        elif method == "pdfplumber" and PDFPLUMBER_AVAILABLE:
            return convert_pdf_to_csv_pdfplumber(pdf_path, output_path)
        else:
            print(f"❌ Method '{method}' not available")
            return []
            
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return []

def main():
    """Demo function"""
    print("🔧 PDF to CSV Converter for PIDUM Data")
    print("=" * 50)
    
    # Check dependencies
    available = check_dependencies()
    print(f"Available libraries: {available}")
    
    if not available:
        print("\n❌ No PDF libraries installed!")
        print("Install with:")
        print("  pip install tabula-py  # Most popular")
        print("  pip install camelot-py[cv]  # High quality")
        print("  pip install pdfplumber  # Detailed control")
        return
    
    # Example usage (uncomment to test)
    # pdf_file = "sample_pidum_report.pdf"
    # if os.path.exists(pdf_file):
    #     tables = auto_convert_pdf_to_csv(pdf_file)
    #     if tables:
    #         print(f"\n✅ Successfully converted {len(tables)} table(s)")
    #         for i, table in enumerate(tables):
    #             print(f"Table {i+1} shape: {table.shape}")
    #             print(f"Columns: {list(table.columns)}")
    # else:
    #     print(f"\n⚠️  Sample file {pdf_file} not found")

if __name__ == "__main__":
    main()