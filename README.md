# ShopSense AI prototype v0.1

A beginner-friendly Streamlit demo for small-shop inventory, sales, expenses, low-stock alerts, and a basic customer credit ledger.

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Internet connection for the initial package installation

## Run on Windows
1. Install Python from https://www.python.org/downloads/windows/
   - During installation, tick **Add python.exe to PATH**.
2. Install VS Code from https://code.visualstudio.com/Download (optional but recommended).
3. Extract this ZIP to a folder, e.g. `C:\ShopSense`.
4. Open Command Prompt in that folder.
5. Run:

   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   py -m pip install -r requirements.txt
   py -m streamlit run app.py
   ```

6. The app should open in your browser. If not, open the local URL shown in the terminal (usually http://localhost:8501).

## Test on your phone
Your laptop and phone should be on the same Wi-Fi network. Start Streamlit with:

```bat
py -m streamlit run app.py --server.address 0.0.0.0
```

Then find your laptop's local IPv4 address with `ipconfig` in Command Prompt and open `http://LAPTOP-IP:8501` on your phone. Windows Firewall may ask permission; allow private-network access only if you trust the Wi-Fi. If this is confusing, first test on the laptop.

## Current limitations
- Data is stored in Streamlit session memory and may reset; there is no database yet.
- Sales cost is not configured, so the displayed profit is only a rough estimate and should not be treated as actual profit.
- No authentication, backups, multi-user support, cloud hosting, or production-grade accounting.
- Voice commands and AI parsing are not included in v0.1; add them after the basic workflow is tested.
- Use sample/fake data only. Do not enter real customer personal or financial information.
