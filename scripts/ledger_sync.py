# ledger_sync.py
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path

TALLY_URL = "http://localhost:9000"
LEDGER_MAPPING_FILE = Path("../config/ledger_mapping.xlsx")
OUTPUT_LOG_FILE = Path("../output/updated_mapping_log.txt")

def sync_ledgers_from_tally():
    """
    Fetch all ledgers from Tally, update ledger_mapping.xlsx,
    and return a pandas DataFrame of mappings.
    KannadaLedger defaults to EnglishLedger for new entries.
    """
    print("Syncing ledgers from Tally...")

    ledger_request_xml = """<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>EXPORT</TALLYREQUEST>
        <TYPE>DATA</TYPE>
        <ID>SimpleLedgerList</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <REPORT NAME="SimpleLedgerList">
                        <FORMS>SimpleLedgerForm</FORMS>
                    </REPORT>
                    <FORM NAME="SimpleLedgerForm">
                        <TOPPARTS>SimpleLedgerPart</TOPPARTS>
                        <XMLTAG>"LEDGERLIST"</XMLTAG>
                    </FORM>
                    <PART NAME="SimpleLedgerPart">
                        <LINES>SimpleLedgerLine</LINES>
                        <REPEAT>SimpleLedgerLine : SimpleLedgerCollection</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE NAME="SimpleLedgerLine">
                        <FIELDS>LedgerNameField</FIELDS>
                        <XMLTAG>"LEDGER"</XMLTAG>
                    </LINE>
                    <FIELD NAME="LedgerNameField">
                        <SET>$Name</SET>
                        <XMLTAG>"NAME"</XMLTAG>
                    </FIELD>
                    <COLLECTION NAME="SimpleLedgerCollection">
                        <TYPE>Ledger</TYPE>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""


    try:
        res = requests.post(TALLY_URL, data=ledger_request_xml)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to connect to Tally: {e}")
        return None

    root = ET.fromstring(res.content)
    ledger_names = [elem.text.strip() for elem in root.iter("NAME") if elem.text]

    print(f"✅ Received {len(ledger_names)} ledgers from Tally.")

    # Load or create mapping file
    if LEDGER_MAPPING_FILE.exists():
        df = pd.read_excel(LEDGER_MAPPING_FILE)
        if "EnglishLedger" not in df.columns or "KannadaLedger" not in df.columns:
            print("⚠️ Mapping file missing columns. Recreating headers.")
            df = pd.DataFrame(columns=["EnglishLedger", "KannadaLedger"])
    else:
        df = pd.DataFrame(columns=["EnglishLedger", "KannadaLedger"])

    existing_ledgers = set(str(x).strip().lower() for x in df["EnglishLedger"].dropna())
    new_ledgers = [l for l in ledger_names if l.lower() not in existing_ledgers]

    if not new_ledgers:
        print("✅ No new ledgers — mapping file already up-to-date.")
    else:
        print(f"➕ Found {len(new_ledgers)} new ledgers. Updating mapping file.")
        new_entries = pd.DataFrame({
            "EnglishLedger": new_ledgers,
            "KannadaLedger": new_ledgers  # fallback = English
        })
        df = pd.concat([df, new_entries], ignore_index=True)
        df = df.sort_values(by="EnglishLedger").reset_index(drop=True)

        LEDGER_MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(LEDGER_MAPPING_FILE, index=False)

        OUTPUT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n--- Sync Run ---\nAdded {len(new_ledgers)} ledgers:\n")
            for name in new_ledgers:
                f.write(f"  {name}\n")

        print(f"✅ Mapping updated → {LEDGER_MAPPING_FILE}")

    return df
