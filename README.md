# VEGA - Tally P&L Automation with Kannada Translation

## 📋 Project Overview

VEGA is an automated solution for processing Tally Profit & Loss (P&L) statements and generating formatted Excel reports with Kannada translations. The project automates the conversion of Tally XML exports into professionally formatted bilingual (English-Kannada) financial reports.

## ✨ Features

- **Direct Tally Integration**: Automatically connects to Tally via HTTP XML API (no manual export needed)
- **Automated P&L Export**: Fetches Profit & Loss data directly from Tally with interactive date range selection
- **Ledger Synchronization**: Automatically syncs all ledgers from Tally and updates the mapping file
- **XML Parsing**: Automatically extracts income and expense data from Tally P&L XML exports
- **Kannada Translation**: Translates English ledger names to Kannada using a configurable mapping file
- **Excel Generation**: Creates formatted Excel reports with proper styling and formatting
- **Dynamic Report Assembly**: Merges header, body, and footer templates into a complete P&L statement
- **Month/Year Localization**: Automatically inserts current month and year in Kannada format
- **Style Preservation**: Maintains Excel formatting, cell styles, and merged ranges during processing
- **Unified Workflow**: Single command runs the entire process from export to final report generation
- **Connection Validation**: Checks Tally connectivity before attempting operations
- **Automatic Mapping Updates**: New ledgers are automatically added to mapping file with English as fallback
- **Sync Logging**: Maintains logs of ledger synchronization operations

## 📁 Project Structure

```
VEGA/
├── config/                      # Configuration and template files
│   ├── final_PnL.xlsx          # Final P&L template
│   ├── footer_template.xlsx     # Footer section template
│   ├── header_template.xlsx     # Header section template
│   ├── ledger_mapping.xlsx      # English to Kannada ledger mapping
│   └── template_kannada.xlsx    # Kannada template for body section
├── exports/                     # Input XML files from Tally
│   └── PandL.xml                # Tally P&L export (XML format)
├── output/                      # Generated output files
│   ├── body_PnL.xlsx           # Generated body section
│   ├── final_PnL.xlsx          # Final merged P&L report
│   └── header_with_month.xlsx  # Header with month/year inserted
└── scripts/                     # Python automation scripts
    ├── automate.py              # Main orchestration script: Complete end-to-end workflow
    ├── tally_pandl_export.py    # Automated P&L export from Tally via HTTP API
    ├── ledger_sync.py            # Synchronizes ledgers from Tally to mapping file
    └── merge_header_footer.py    # Merges header, body, and footer into final report
```

## 🔧 Requirements

### Python Packages
- `openpyxl` - Excel file manipulation
- `pandas` - Data processing and Excel reading
- `requests` - HTTP requests for Tally API communication
- `xml.etree.ElementTree` - XML parsing (built-in)

### Installation
```bash
pip install openpyxl pandas requests
```

### Tally Configuration
Before using the automated features, ensure Tally is configured:
1. Open Tally
2. Press `F1` to open Gateway of Tally
3. Go to **Advanced Configuration** (or press `F12`)
4. Enable **HTTP Server** = **Yes**
5. Default port is **9000** (can be changed in script if needed)

## 🚀 Usage

### Automated Workflow (Recommended)

Run the main automation script for a complete end-to-end process:

```bash
python scripts/automate.py
```

This single command automatically:
1. **Exports P&L from Tally**: Connects to Tally, prompts for date range, and exports P&L XML
2. **Syncs Ledgers**: Fetches all ledgers from Tally and updates the mapping file with any new entries
3. **Parses XML**: Extracts income and expense data from the exported XML
4. **Translates to Kannada**: Converts English ledger names to Kannada using the mapping file
5. **Generates Body**: Creates the formatted body section with Kannada translations
6. **Merges Report**: Combines header, body, and footer into the final P&L report

**Output**: `output/final_PnL.xlsx` - Complete bilingual P&L report ready for use

### Manual Workflow (Alternative)

If you prefer to export XML manually or work with existing files:

#### Step 1: Export P&L from Tally (Manual)
1. Export your Profit & Loss statement as XML from Tally
2. Save it as `exports/PandL.xml`

#### Step 2: Sync Ledgers (Optional)
Update the ledger mapping file with latest ledgers from Tally:

```bash
python scripts/ledger_sync.py
```

This will:
- Fetch all ledgers from Tally
- Add any new ledgers to `config/ledger_mapping.xlsx`
- Log updates to `output/updated_mapping_log.txt`

#### Step 3: Generate Report
Run the automation script (it will skip Tally export if XML already exists):

```bash
python scripts/automate.py
```

### Individual Script Usage

You can also run individual components separately:

**Export P&L from Tally:**
```bash
python scripts/tally_pandl_export.py
```

**Sync Ledgers:**
```bash
python scripts/ledger_sync.py
```

**Merge Header, Body, and Footer:**
```bash
python scripts/merge_header_footer.py
```

## 📊 Workflow

### Automated Workflow
```
Tally (HTTP API)
         ↓
[tally_pandl_export.py]
    - Connect to Tally
    - Get date range from user
    - Export P&L XML
         ↓
[ledger_sync.py]
    - Fetch all ledgers from Tally
    - Update mapping file
    - Log new entries
         ↓
[automate.py]
    - Parse XML
    - Extract Income/Expense
    - Translate to Kannada
    - Generate body_PnL.xlsx
         ↓
[merge_header_footer.py]
    - Insert month/year in Kannada
    - Merge header + body + footer
         ↓
    Final P&L Report (Excel)
```

### Manual Workflow
```
Manual Tally Export (XML)
         ↓
[automate.py]
    - Parse XML
    - Extract Income/Expense
    - Translate to Kannada
    - Generate body_PnL.xlsx
         ↓
[merge_header_footer.py]
    - Insert month/year
    - Merge header + body + footer
         ↓
    Final P&L Report (Excel)
```

## 🎯 Key Functionality

### Direct Tally Integration
- **HTTP API Communication**: Connects to Tally's built-in HTTP XML server (port 9000)
- **Connection Validation**: Checks if Tally is running and accessible before operations
- **Interactive Date Selection**: Prompts user for date range (DD-MM-YYYY format) for P&L export
- **Automatic Export**: Fetches P&L data directly from Tally without manual export steps

### Ledger Synchronization
- **Automatic Discovery**: Fetches all ledgers from Tally automatically
- **Smart Updates**: Only adds new ledgers that don't exist in mapping file
- **Fallback Translation**: New ledgers default to English name until manually translated
- **Sorted Mapping**: Maintains alphabetically sorted ledger list
- **Sync Logging**: Tracks all synchronization operations in `output/updated_mapping_log.txt`

### XML Parsing
- Identifies section headers (Direct/Indirect Incomes and Expenses)
- Extracts ledger names and amounts
- Filters out zero-amount entries

### Translation System
- Case-insensitive matching of English ledger names
- Configurable mapping via Excel file
- Only includes ledgers present in the mapping file
- Automatic mapping file updates when new ledgers are discovered

### Excel Formatting
- Preserves cell styles, fonts, borders, and fills
- Maintains merged cell ranges
- Applies Indian Rupee (₹) number formatting
- Copies column widths and alignment
- Dynamic row insertion based on data length

### Month/Year Localization
Automatically converts current date to Kannada:
- January → ಜನವರಿ
- February → ಫೆಬ್ರವರಿ
- March → ಮಾರ್ಚ್
- April → ಏಪ್ರಿಲ್
- May → ಮೇ
- June → ಜೂನ್
- July → ಜುಲೈ
- August → ಆಗಸ್ಟ್
- September → ಸೆಪ್ಟೆಂಬರ್
- October → ಅಕ್ಟೋಬರ್
- November → ನವೆಂಬರ್
- December → ಡಿಸೆಂಬರ್

## 📝 Configuration

### Ledger Mapping File (`config/ledger_mapping.xlsx`)
Required columns:
- **EnglishLedger**: Exact ledger names as they appear in Tally
- **KannadaLedger**: Kannada translations

### Template Files
- **header_template.xlsx**: Contains `$$monthYear$$` placeholder for dynamic date insertion
- **template_kannada.xlsx**: Body template with Kannada formatting
- **footer_template.xlsx**: Footer section with totals and summary

## 🔍 Output Files

- **body_PnL.xlsx**: Generated body section with income/expense data in Kannada
- **header_with_month.xlsx**: Header with current month/year in Kannada
- **final_PnL.xlsx**: Complete merged report ready for use
- **updated_mapping_log.txt**: Log file tracking ledger synchronization operations

## 📌 Notes

- **Tally Connection**: Ensure Tally is running with HTTP Server enabled before using automated features
- **Mapping File**: The script only processes ledgers that exist in the mapping file
- **Auto-Sync**: New ledgers are automatically added to mapping file during sync, but Kannada translation needs to be added manually
- **Zero-Amount Filtering**: Zero-amount entries are automatically filtered out
- **Date Format**: When prompted for dates, use DD-MM-YYYY format (e.g., 01-04-2024)
- **File Paths**: All file paths are relative to the project root directory
- **Output Directory**: All output files are generated in the `output/` directory
- **Error Handling**: Scripts gracefully handle connection failures and missing files

## 👤 Author

Narendra KL

## 📄 License

This project is for internal use and automation of Tally P&L reporting with Kannada translation support.

