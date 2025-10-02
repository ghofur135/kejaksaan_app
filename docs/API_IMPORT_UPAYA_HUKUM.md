# API Import Upaya Hukum - Documentation

## Overview
API khusus untuk mengimport data tahapan **Upaya Hukum** dengan format CSV yang berisi data terdakwa/terpidana dan nomor RP9.

## Endpoint Details

### Upload dan Preview
- **URL**: `/import_upaya_hukum_api`
- **Method**: GET (form), POST (upload)
- **Content-Type**: multipart/form-data
- **Template**: `import_upaya_hukum.html`

### Konfirmasi Import
- **URL**: `/confirm_import_upaya_hukum`
- **Method**: POST
- **Content-Type**: application/x-www-form-urlencoded

## Expected CSV Format

### Required Columns
1. **No** - Nomor urut data
2. **Terdakwa_Terpidana** - Nama lengkap terdakwa/terpidana
3. **No_Tanggal_RP9** - Nomor dan tanggal RP9 (format: PDM- XX/PRBAL/Eoh.2/MM/YYYY)

### Sample CSV Data
```csv
No,Terdakwa_Terpidana,No_Tanggal_RP9
1,FADELA TRI ANGGRAENI Alias DELA Binti PAIJO,PDM- 08/PRBAL/Eoh.2/06/2025
2,RENO ALI MUKHTAMAR Alias RENO Bin AHMAD SUBARNO,PDM- 11/PRBAL/Eoh.2/07/2025
3,ADITYA SETIAWAN bin WAHIDIN,PDM- 19/PRBAL/Enz.2/06/2025
```

## Processing Flow

### 1. File Upload
```
POST /import_upaya_hukum_api
├── File validation (CSV, XLS, XLSX)
├── Column validation (No, Terdakwa_Terpidana, No_Tanggal_RP9)
├── Data processing and standardization
└── Session storage → Preview page
```

### 2. Data Processing (`process_upaya_hukum_import_file`)
- **Date Extraction**: Extract month/year from RP9 format
- **Jenis Perkara Analysis**: Analyze terdakwa name for case type suggestions
- **Data Standardization**: Convert to database format
- **Header Row Filtering**: Skip rows with "1,2,3" values

### 3. Preview and Confirmation
```
GET → Preview Template
├── Display processed data
├── Allow jenis perkara selection
├── Enable row removal/inclusion
└── Form submission → Confirm import
```

### 4. Database Insertion
```
POST /confirm_import_upaya_hukum
├── Form data processing
├── Database insertion (insert_pidum_data)
├── Success/error reporting
└── Redirect → /view_pidum
```

## Data Transformation

### Input to Database Mapping
| CSV Column | Database Field | Processing |
|------------|----------------|------------|
| No | NO | Direct mapping |
| Terdakwa_Terpidana | JENIS_PERKARA_ORIGINAL | For analysis only |
| No_Tanggal_RP9 | TANGGAL | Date extraction from RP9 |
| - | PERIODE | Default: "1" |
| - | TAHAPAN_PENANGANAN | Fixed: "UPAYA HUKUM" |
| - | JENIS PERKARA | User selection (dropdown) |
| - | KETERANGAN | Generated from CSV data |

### Date Extraction Logic
- Pattern: `PDM- XX/PRBAL/Eoh.2/MM/YYYY`
- Extract: Month (MM) and Year (YYYY)
- Output: `YYYY-MM-01` (1st day of month)
- Fallback: Current date if parsing fails

### Jenis Perkara Suggestions
Automatic analysis based on terdakwa name:
- **NARKOTIKA**: Contains "narkotika", "narkoba", "sabu", "ganja", etc.
- **KORUPSI**: Contains "korupsi", "gratifikasi", "suap", etc.
- **PENCURIAN**: Contains "curi", "pencurian", "theft"
- **PENIPUAN**: Contains "tipu", "penipuan", "fraud"
- **PENGANIAYAAN**: Contains "aniaya", "penganiayaan", "kekerasan"
- **PEMBUNUHAN**: Contains "bunuh", "pembunuhan", "murder"
- **PERKOSAAN**: Contains "perkosa", "pemerkosaan", "sexual"
- **PENGELAPAN**: Contains "gelap", "pengelapan", "embezzlement"
- **Default**: "PERKARA LAINNYA"

## API Response Examples

### Success Response (Preview Page)
```html
<!-- Rendered template: import_upaya_hukum_preview.html -->
<!-- Contains: -->
- Processed data table
- Jenis perkara dropdown selections
- Row removal functionality
- Confirmation form
```

### Error Responses
- **No file**: Flash message + redirect to upload form
- **Invalid format**: Flash message + redirect to upload form
- **Missing columns**: Flash message + redirect to upload form
- **Processing error**: Flash message + redirect to upload form

## Session Management
- **Key**: `import_data_upaya_hukum`
- **Content**: Processed import data array
- **Lifecycle**: Upload → Preview → Confirm (cleared after confirmation)

## Integration Points

### Route Redirects
- `/import_tahapan/upaya_hukum` → `/import_upaya_hukum_api`

### Database Functions
- `insert_pidum_data(data)` - Insert individual record
- Standard PIDUM table structure

### Helper Functions
- `allowed_file_upaya_hukum(filename)` - File validation
- `extract_date_from_rp9(rp9_string)` - Date parsing
- `get_jenis_perkara_suggestions_upaya_hukum(name)` - Case type analysis
- `prepare_upaya_hukum_data_for_db(data, form)` - Form processing

## Error Handling

### File Level Errors
- Invalid file extension
- Missing required columns
- Empty file
- Corrupted file

### Data Level Errors
- Invalid date format
- Empty terdakwa name
- Database insertion failures

### User Experience
- Flash messages for all error types
- Graceful fallbacks (default values)
- Detailed error logging
- Transaction rollback on failures

## Usage Example

1. **Access API**: `GET /import_upaya_hukum_api`
2. **Upload CSV**: POST with multipart form data
3. **Review Preview**: Adjust jenis perkara selections
4. **Confirm Import**: Submit form to `/confirm_import_upaya_hukum`
5. **View Results**: Redirected to `/view_pidum` with success messages

## Supported File Formats
- **.csv** - Comma-separated values (UTF-8 encoding)
- **.xlsx** - Excel 2007+ format
- **.xls** - Excel 97-2003 format

Maximum file size: 10MB (configurable)

## Security Considerations
- File extension validation
- Secure filename handling (`werkzeug.secure_filename`)
- Session-based data storage
- Input sanitization in form processing
- SQL injection prevention through parameterized queries

---

**Note**: This API follows the same pattern as `/import_pra_penuntutan_api` but is specifically designed for Upaya Hukum data with RP9 format processing.