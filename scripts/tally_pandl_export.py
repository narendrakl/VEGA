# tally_pandl_export.py
import requests
from datetime import datetime
from pathlib import Path

TALLY_URL = "http://localhost:9000"
EXPORT_FILE = Path("../exports/PandL.xml")

def is_tally_running():
    """
    Checks if Tally HTTP XML server is running and reachable.
    Returns True if reachable, False otherwise.
    """
    try:
        res = requests.get(TALLY_URL, timeout=5)
        # Some Tally builds respond with plain text, others with XML
        return res.status_code == 200
    except Exception:
        return False


def export_pandl_from_tally():
    
    """
    Checks connection to Tally, prompts user for date range (DD-MM-YYYY),
    requests Profit & Loss XML from Tally, and saves it to exports/PandL.xml.
    """

    print("Checking connection to Tally...")

    if not is_tally_running():
        print("Unable to connect to Tally.")
        print("Please ensure Tally is open and HTTP XML Server is enabled (F1 > Advanced Configuration > Enable HTTP Server = Yes).")
        print("Default port: 9000")
        return None

    print("Tally connection successful!\n")

    """
    Ask user for From/To dates (DD-MM-YYYY),
    request Profit & Loss report from Tally,
    and save as exports/PandL.xml.
    """

    # --- Get user input ---
    print("Please enter the date range for Profit & Loss export:")
    from_date_str = input("   From date (DD-MM-YYYY): ")
    to_date_str = input("   To date   (DD-MM-YYYY): ")

    # --- Validate dates ---
    try:
        from_date = datetime.strptime(from_date_str, "%d-%m-%Y")
        to_date = datetime.strptime(to_date_str, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format! Use DD-MM-YYYY.")
        return None

    # --- Convert to Tally format (YYYYMMDD) ---
    tally_from = from_date.strftime("%Y%m%d")
    tally_to = to_date.strftime("%Y%m%d")

    # --- Build XML request ---
    xml_request = f"""<ENVELOPE>
      <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
      </HEADER>
      <BODY>
        <EXPORTDATA>
          <REQUESTDESC>
            <REPORTNAME>Profit and Loss</REPORTNAME>
            <STATICVARIABLES>
              <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
              <EXPLODEFLAG>Yes</EXPLODEFLAG>
              <SVFROMDATE>{tally_from}</SVFROMDATE>
              <SVTODATE>{tally_to}</SVTODATE>
            </STATICVARIABLES>
          </REQUESTDESC>
        </EXPORTDATA>
      </BODY>
    </ENVELOPE>"""

    # --- Send to Tally ---
    print(f"Requesting Profit & Loss from {from_date_str} to {to_date_str} ...")

    try:
        response = requests.post(TALLY_URL, data=xml_request)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to connect to Tally: {e}")
        return None

    # --- Save XML to file ---
    EXPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EXPORT_FILE, "wb") as f:
        f.write(response.content)

    print(f"Profit & Loss XML saved → {EXPORT_FILE}")
    return (EXPORT_FILE, to_date)
