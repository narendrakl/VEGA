import xml.etree.ElementTree as ET
from openpyxl import load_workbook
from openpyxl.styles import numbers
from copy import copy
from datetime import datetime
import pandas as pd
from pathlib import Path

# --- File paths ---
base_dir = Path(__file__).parent.parent
xml_file = base_dir / "exports" / "PandL.xml"
template_file = base_dir / "config" / "template_kannada.xlsx"
mapping_file = base_dir / "config" / "ledger_mapping.xlsx"
output_file = base_dir / "output" / "body_PnL.xlsx"

# ==========================================================
# 1️⃣ Parse the Tally P&L XML section-wise
# ==========================================================
tree = ET.parse(xml_file)
root = tree.getroot()

income, expense = [], []
current_section = None
last_ledger = None

for elem in root.iter():
    tag = elem.tag.upper()

    # Identify section headers
    if tag == "DSPDISPNAME":
        name_text = elem.text.strip() if elem.text else ""
        if name_text in ["Direct Incomes", "Indirect Incomes"]:
            current_section = "income"
            last_ledger = None
        elif name_text in ["Direct Expenses", "Indirect Expenses"]:
            current_section = "expense"
            last_ledger = None
        else:
            last_ledger = name_text  # ledger candidate

    elif tag == "BSSUBAMT" and last_ledger and current_section:
        amt_text = elem.text.strip() if elem.text else ""
        try:
            amt = float(amt_text)
        except:
            amt = 0.0
        if amt != 0:
            if current_section == "income":
                income.append((last_ledger, amt))
            elif current_section == "expense":
                expense.append((last_ledger, amt))
        last_ledger = None

# ==========================================================
# 2️⃣ Load English→Kannada mapping and filter
# ==========================================================
mapping_df = pd.read_excel(mapping_file)
mapping_df.columns = mapping_df.columns.str.strip()

mapping_dict = {
    str(row["EnglishLedger"]).strip().lower(): str(row["KannadaLedger"]).strip()
    for _, row in mapping_df.iterrows()
    if pd.notna(row["EnglishLedger"]) and pd.notna(row["KannadaLedger"])
}

def translate_and_filter(data):
    translated = []
    for name, amt in data:
        key = name.strip().lower()
        if key in mapping_dict and amt != 0:
            translated.append((mapping_dict[key], amt))
    return translated

income = translate_and_filter(income)
expense = translate_and_filter(expense)

# ==========================================================
# 3️⃣ Month-year in Kannada
# ==========================================================
MONTHS_KN = {
    1:"ಜನವರಿ",2:"ಫೆಬ್ರವರಿ",3:"ಮಾರ್ಚ್",4:"ಏಪ್ರಿಲ್",5:"ಮೇ",6:"ಜೂನ್",
    7:"ಜುಲೈ",8:"ಆಗಸ್ಟ್",9:"ಸೆಪ್ಟೆಂಬರ್",10:"ಅಕ್ಟೋಬರ್",11:"ನವೆಂಬರ್",12:"ಡಿಸೆಂಬರ್"
}
now = datetime.now()
month_year_kn = f"{MONTHS_KN[now.month]} {now.year}"

# ==========================================================
# 4️⃣ Load template and utilities
# ==========================================================
wb = load_workbook(template_file)
ws = wb.active

def copy_style(src, dst):
    if src.has_style:
        dst.font = copy(src.font)
        dst.border = copy(src.border)
        dst.fill = copy(src.fill)
        dst.number_format = copy(src.number_format)
        dst.protection = copy(src.protection)
        dst.alignment = copy(src.alignment)

# Replace $$monthYear$$ if found
for row in ws.iter_rows():
    for cell in row:
        if str(cell.value).strip() == "$$monthYear$$":
            cell.value = month_year_kn

# ==========================================================
# 5️⃣ Write income / expense with dynamic row insertion
# ==========================================================
start_row = 2
exp_name_col, exp_amt_col = 2, 3   # B, C
inc_name_col, inc_amt_col = 5, 6   # E, F

# reference styles (top-left non-merged cells)
ref_exp_name = ws.cell(start_row, exp_name_col)
ref_exp_amt  = ws.cell(start_row, exp_amt_col)
ref_inc_name = ws.cell(start_row, inc_name_col)
ref_inc_amt  = ws.cell(start_row, inc_amt_col)

def insert_data(data, start_row, col_name, col_amt, ref_name, ref_amt):
    """
    Dynamically insert rows from start_row based on data length.
    Keeps header/footer intact.
    """
    if not data:
        return

    # Insert blank rows equal to data length
    #ws.insert_rows(start_row, amount=len(data))

    # Write data
    for i, (name_kn, amt) in enumerate(data):
        row = start_row + i
        c1 = ws.cell(row, col_name)
        c1.value = name_kn
        c2 = ws.cell(row, col_amt)
        c2.value = amt
        # copy styles
        copy_style(ref_name, c1)
        copy_style(ref_amt, c2)
        c2.number_format = u'₹ #,##0.00'

# Insert expense side (B-C)
insert_data(expense, start_row, exp_name_col, exp_amt_col, ref_exp_name, ref_exp_amt)

# Insert income side (E-F)
insert_data(income, start_row, inc_name_col, inc_amt_col, ref_inc_name, ref_inc_amt)

# ==========================================================
# 6️⃣ Save output
# ==========================================================
wb.save(output_file)
print("✅ Kannada Profit & Loss generated successfully →", output_file)
print(f"   Income Ledgers: {len(income)} | Expense Ledgers: {len(expense)}")
