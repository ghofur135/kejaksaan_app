#!/usr/bin/env python3
"""
PDF to CSV Converter for PIDUM data
Mengkonversi tabel dari file PDF menjadi format CSV yang siap di-import
"""

import pandas as pd
import os
import logging
from datetime import datetime
from io import StringIO

# Import PDF processing libraries with error handling
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

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFToCSVConverter:
    """
    Main class for converting PDF tables to CSV format
    Supports multiple PDF processing libraries with automatic fallback
    """
    
    def __init__(self):
        self.available_libraries = self.check_library_availability()
        logger.info(f"Available PDF libraries: {self.available_libraries}")
    
    def check_library_availability(self):
        """Check which PDF processing libraries are available"""
        available = {}
        
        if TABULA_AVAILABLE:
            try:
                # Test tabula functionality
                available['tabula'] = True
            except Exception as e:
                available['tabula'] = False
                logger.warning(f"Tabula test failed: {e}")
        else:
            available['tabula'] = False
        
        if CAMELOT_AVAILABLE:
            try:
                # Test camelot functionality
                available['camelot'] = True
            except Exception as e:
                available['camelot'] = False
                logger.warning(f"Camelot test failed: {e}")
        else:
            available['camelot'] = False
        
        if PDFPLUMBER_AVAILABLE:
            available['pdfplumber'] = True
        else:
            available['pdfplumber'] = False
        
        return available
    
    def convert_pdf_to_dataframes(self, pdf_path, library_choice='auto', pages='all'):
        """
        Convert PDF tables to list of DataFrames
        
        Args:
            pdf_path (str): Path to PDF file
            library_choice (str): 'auto', 'tabula', 'camelot', or 'pdfplumber'
            pages (str): Pages to extract ('all' or '1,2,3')
        
        Returns:
            list: List of pandas DataFrames
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Determine which library to use
        if library_choice == 'auto':
            # Try libraries in order of preference
            if self.available_libraries.get('tabula', False):
                library_choice = 'tabula'
            elif self.available_libraries.get('camelot', False):
                library_choice = 'camelot'
            elif self.available_libraries.get('pdfplumber', False):
                library_choice = 'pdfplumber'
            else:
                raise RuntimeError("No PDF processing libraries available")
        
        logger.info(f"Using {library_choice} to process PDF: {pdf_path}")
        
        # Extract tables based on chosen library
        if library_choice == 'tabula' and self.available_libraries.get('tabula', False):
            return self._extract_with_tabula(pdf_path, pages)
        elif library_choice == 'camelot' and self.available_libraries.get('camelot', False):
            return self._extract_with_camelot(pdf_path, pages)
        elif library_choice == 'pdfplumber' and self.available_libraries.get('pdfplumber', False):
            return self._extract_with_pdfplumber(pdf_path)
        else:
            raise RuntimeError(f"Library {library_choice} not available")
    
    def _extract_with_tabula(self, pdf_path, pages='all'):
        """Extract tables using tabula-py"""
        try:
            # Extract all tables from PDF
            tables = tabula.read_pdf(pdf_path, pages=pages, multiple_tables=True)
            
            # Convert to list of DataFrames and clean
            dataframes = []
            for table in tables:
                if not table.empty:
                    cleaned_df = self._clean_dataframe(table)
                    if not cleaned_df.empty:
                        dataframes.append(cleaned_df)
            
            return dataframes
            
        except Exception as e:
            logger.error(f"Tabula extraction failed: {e}")
            return []
    
    def _extract_with_camelot(self, pdf_path, pages='all'):
        """Extract tables using camelot-py"""
        try:
            # Parse pages
            if pages == 'all':
                pages_param = 'all'
            else:
                pages_param = pages
            
            # Extract tables
            tables = camelot.read_pdf(pdf_path, pages=pages_param)
            
            # Convert to DataFrames
            dataframes = []
            for table in tables:
                df = table.df
                if not df.empty:
                    cleaned_df = self._clean_dataframe(df)
                    if not cleaned_df.empty:
                        dataframes.append(cleaned_df)
            
            return dataframes
            
        except Exception as e:
            logger.error(f"Camelot extraction failed: {e}")
            return []
    
    def _extract_with_pdfplumber(self, pdf_path):
        """Extract tables using pdfplumber"""
        try:
            dataframes = []
            
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract tables from page
                    tables = page.extract_tables()
                    
                    for table in tables:
                        if table and len(table) > 1:  # Must have header + data
                            # Convert to DataFrame
                            df = pd.DataFrame(table[1:], columns=table[0])
                            
                            # Clean and validate
                            cleaned_df = self._clean_dataframe(df)
                            if not cleaned_df.empty:
                                dataframes.append(cleaned_df)
            
            return dataframes
            
        except Exception as e:
            logger.error(f"PDFPlumber extraction failed: {e}")
            return []
    
    def _clean_dataframe(self, df):
        """Clean and standardize DataFrame"""
        try:
            # Remove completely empty rows and columns
            df = df.dropna(how='all').dropna(axis=1, how='all')
            
            if df.empty:
                return df
            
            # Clean column names
            df.columns = [str(col).strip().upper() for col in df.columns]
            
            # Remove rows where all values are NaN or empty strings
            df = df[~df.apply(lambda row: row.astype(str).str.strip().eq('').all(), axis=1)]
            
            # Clean data values
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.strip()
                    df[col] = df[col].replace(['nan', 'NaN', 'None', ''], pd.NA)
            
            # Try to standardize common column names for PIDUM data
            column_mapping = {
                'NOMOR': 'NO',
                'NUMBER': 'NO',
                'NUM': 'NO',
                'TGL': 'TANGGAL',
                'DATE': 'TANGGAL',
                'JENIS_PERKARA': 'JENIS PERKARA',
                'JENIS': 'JENIS PERKARA',
                'TYPE': 'JENIS PERKARA',
                'PERKARA': 'JENIS PERKARA',
                'KETERANGAN': 'KETERANGAN',
                'DESCRIPTION': 'KETERANGAN',
                'NOTES': 'KETERANGAN',
                'CATATAN': 'KETERANGAN'
            }
            
            # Apply column mapping
            df = df.rename(columns=column_mapping)
            
            # Ensure minimum required data
            if len(df) < 1:
                return pd.DataFrame()
            
            logger.info(f"Cleaned DataFrame: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except Exception as e:
            logger.error(f"DataFrame cleaning failed: {e}")
            return pd.DataFrame()
    
    def convert_pdf_to_csv(self, pdf_path, output_path=None, library_choice='auto', pages='all'):
        """
        Convert PDF to CSV file
        
        Args:
            pdf_path (str): Path to PDF file
            output_path (str): Output CSV path (optional)
            library_choice (str): Library to use
            pages (str): Pages to extract
        
        Returns:
            str: CSV content as string
        """
        try:
            # Extract DataFrames
            dataframes = self.convert_pdf_to_dataframes(pdf_path, library_choice, pages)
            
            if not dataframes:
                return None
            
            # Combine all DataFrames
            if len(dataframes) == 1:
                combined_df = dataframes[0]
            else:
                # Add separator between tables
                combined_df = pd.DataFrame()
                for i, df in enumerate(dataframes):
                    if i > 0:
                        # Add empty row as separator
                        separator = pd.DataFrame([[''] * len(df.columns)], columns=df.columns)
                        combined_df = pd.concat([combined_df, separator], ignore_index=True)
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
            
            # Convert to CSV
            csv_content = combined_df.to_csv(index=False)
            
            # Save to file if output path provided
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(csv_content)
                logger.info(f"CSV saved to: {output_path}")
            
            return csv_content
            
        except Exception as e:
            logger.error(f"PDF to CSV conversion failed: {e}")
            return None
    
    def get_conversion_info(self, pdf_path):
        """Get information about PDF conversion capabilities"""
        info = {
            'file_exists': os.path.exists(pdf_path),
            'available_libraries': self.available_libraries,
            'recommended_library': 'tabula' if self.available_libraries.get('tabula') else 
                                  'camelot' if self.available_libraries.get('camelot') else
                                  'pdfplumber' if self.available_libraries.get('pdfplumber') else None
        }
        
        if info['file_exists']:
            try:
                # Get basic PDF info using pdfplumber if available
                if PDFPLUMBER_AVAILABLE:
                    with pdfplumber.open(pdf_path) as pdf:
                        info['total_pages'] = len(pdf.pages)
                        info['has_tables'] = any(page.extract_tables() for page in pdf.pages[:3])  # Check first 3 pages
                else:
                    info['total_pages'] = 'unknown'
                    info['has_tables'] = 'unknown'
            except Exception as e:
                info['error'] = str(e)
        
        return info


# Standalone functions for backward compatibility
def check_library_availability():
    """Check which PDF processing libraries are available"""
    converter = PDFToCSVConverter()
    return converter.available_libraries


def convert_pdf_to_csv(pdf_path, output_path=None, library_choice='auto', pages='all'):
    """Convert PDF to CSV using best available library"""
    converter = PDFToCSVConverter()
    return converter.convert_pdf_to_csv(pdf_path, output_path, library_choice, pages)


# Main execution for testing
if __name__ == "__main__":
    print("PDF to CSV Converter")
    print("=" * 50)
    
    # Check available libraries
    converter = PDFToCSVConverter()
    print("Available libraries:")
    for lib, available in converter.available_libraries.items():
        status = "✅" if available else "❌"
        print(f"  {status} {lib}")
    
    # Example usage
    if converter.available_libraries:
        print("\nReady to convert PDF files!")
        print("Usage:")
        print("  converter = PDFToCSVConverter()")
        print("  dataframes = converter.convert_pdf_to_dataframes('file.pdf')")
        print("  csv_content = converter.convert_pdf_to_csv('file.pdf')")
    else:
        print("\n❌ No PDF processing libraries available!")
        print("Install at least one: pip install pdfplumber tabula-py camelot-py[cv]")