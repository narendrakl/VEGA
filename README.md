# VEGA - Tally P&L Automation with Kannada Translation

## 📋 Project Overview

VEGA is an automated solution for processing Tally Profit & Loss (P&L) statements and generating formatted Excel reports with Kannada translations. The project automates the conversion of Tally XML exports into professionally formatted bilingual (English-Kannada) financial reports.

## ✨ Features

- **XML Parsing**: Automatically extracts income and expense data from Tally P&L XML exports
- **Kannada Translation**: Translates English ledger names to Kannada using a configurable mapping file
- **Excel Generation**: Creates formatted Excel reports with proper styling and formatting
- **Dynamic Report Assembly**: Merges header, body, and footer templates into a complete P&L statement
- **Month/Year Localization**: Automatically inserts current month and year in Kannada format
- **Style Preservation**: Maintains Excel formatting, cell styles, and merged ranges during processing

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
    ├── automate.py              # Main script: XML parsing and body generation
    └── merge-header-footer.py   # Script: Merges header, body, and footer
```

## 🔧 Requirements

### Python Packages
- `openpyxl` - Excel file manipulation
- `pandas` - Data processing and Excel reading
- `xml.etree.ElementTree` - XML parsing (built-in)

### Installation
```bash
pip install openpyxl pandas
```

## 🚀 Usage

### Step 1: Prepare Input Files

1. **Export P&L from Tally**: Export your Profit & Loss statement as XML and save it as `exports/PandL.xml`
2. **Update Ledger Mapping**: Ensure `config/ledger_mapping.xlsx` contains all required English-to-Kannada mappings with columns:
   - `EnglishLedger`: English ledger names from Tally
   - `KannadaLedger`: Corresponding Kannada translations

### Step 2: Generate Body Section

Run the main automation script to parse XML and generate the body section:

```bash
python scripts/automate.py
```

This script:
- Parses the Tally XML file
- Extracts income and expense entries
- Translates ledger names to Kannada
- Generates `output/body_PnL.xlsx` with formatted data

### Step 3: Merge Header, Body, and Footer

Combine all sections into the final report:

```bash
python scripts/merge-header-footer.py
```

This script:
- Inserts current month/year in Kannada into the header
- Merges header, body, and footer templates
- Generates `output/final_PnL.xlsx` as the complete report

## 📊 Workflow

```
Tally P&L Export (XML)
         ↓
    [automate.py]
    - Parse XML
    - Extract Income/Expense
    - Translate to Kannada
    - Generate body_PnL.xlsx
         ↓
[merge-header-footer.py]
    - Insert month/year
    - Merge header + body + footer
         ↓
    Final P&L Report (Excel)
```

## 🎯 Key Functionality

### XML Parsing
- Identifies section headers (Direct/Indirect Incomes and Expenses)
- Extracts ledger names and amounts
- Filters out zero-amount entries

### Translation System
- Case-insensitive matching of English ledger names
- Configurable mapping via Excel file
- Only includes ledgers present in the mapping file

### Excel Formatting
- Preserves cell styles, fonts, borders, and fills
- Maintains merged cell ranges
- Applies Indian Rupee (₹) number formatting
- Copies column widths and alignment

### Month/Year Localization
Automatically converts current date to Kannada:
- January → ಜನವರಿ
- February → ಫೆಬ್ರವರಿ
- March → ಮಾರ್ಚ್
- ... and so on

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

## 📌 Notes

- The script only processes ledgers that exist in the mapping file
- Zero-amount entries are automatically filtered out
- All file paths are relative to the project root directory
- Output files are generated in the `output/` directory

## 👤 Author

Narendra KL

## 📄 License

This project is for internal use and automation of Tally P&L reporting with Kannada translation support.

