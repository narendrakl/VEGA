# VEGA - Offline Deployment Guide

This guide explains how to package and deploy VEGA on a Windows machine without internet connectivity.

## 📦 Packaging for Offline Deployment

### Step 1: Prepare Dependencies (On a machine with internet)

1. **Ensure Python is installed** on your development machine
   - Download from: https://www.python.org/downloads/
   - Version 3.8 or higher required
   - Check "Add Python to PATH" during installation

2. **Run the dependency download script:**
   ```batch
   download_dependencies.bat
   ```
   This will:
   - Download all required Python packages as wheel files
   - Save them in the `wheels` folder
   - Prepare everything for offline installation

3. **Verify the wheels folder was created:**
   - Check that `wheels` folder exists
   - It should contain `.whl` files for all dependencies

### Step 2: Package Everything

Create a ZIP file containing the entire VEGA folder with:

```
VEGA/
├── config/                    # All template files
├── exports/                   # (can be empty)
├── output/                    # (can be empty)
├── scripts/                   # All Python scripts
├── wheels/                    # All downloaded wheel files (IMPORTANT!)
├── requirements.txt           # Dependency list
├── setup.bat                  # Offline setup script
├── run.bat                    # Application launcher
├── download_dependencies.bat  # (optional, for future updates)
├── README.md                  # Documentation
└── DEPLOYMENT_GUIDE.md        # This file
```

**Important:** Make sure the `wheels` folder is included in the ZIP!

## 🚀 Deployment on Target Machine (No Internet)

### Step 1: Extract the Package

1. Extract the ZIP file to a location on the target Windows machine
   - Example: `C:\VEGA\` or `D:\VEGA\`

### Step 2: Install Python (If not already installed)

1. **If Python is not installed:**
   - You need to download Python installer separately (can be done on another machine)
   - Download Python 3.8+ from: https://www.python.org/downloads/
   - Copy the installer to the target machine via USB/external drive
   - Install Python and **check "Add Python to PATH"** during installation

2. **Verify Python installation:**
   - Open Command Prompt
   - Type: `python --version`
   - Should show Python version (e.g., Python 3.11.0)

### Step 3: Run Setup

1. **Navigate to the VEGA folder:**
   ```batch
   cd C:\VEGA
   ```

2. **Run the setup script:**
   ```batch
   setup.bat
   ```
   
   Or simply double-click `setup.bat` in Windows Explorer

3. **Wait for installation to complete:**
   - The script will install all Python packages from the `wheels` folder
   - This may take 2-5 minutes
   - You should see "Setup completed successfully!" message

### Step 4: Verify Installation

1. **Test Python packages:**
   ```batch
   python -c "import openpyxl; import pandas; import requests; print('All packages installed!')"
   ```

2. **If successful**, you're ready to use VEGA!

## 🎯 Running the Application

### Option 1: Using the Launcher (Recommended)

Simply double-click `run.bat` in the VEGA folder.

### Option 2: Using Command Line

```batch
cd C:\VEGA
python scripts\automate.py
```

## 📋 Prerequisites on Target Machine

- **Windows 7 or higher**
- **Python 3.8 or higher** (must be installed separately if not present)
- **Tally** (with HTTP Server enabled for automated features)

### Tally Configuration

Before using automated features, configure Tally:

1. Open Tally
2. Press `F1` to open Gateway of Tally
3. Go to **Advanced Configuration** (or press `F12`)
4. Enable **HTTP Server** = **Yes**
5. Default port is **9000**

## 🔧 Troubleshooting

### Issue: "Python is not recognized"

**Solution:**
- Python is not installed or not in PATH
- Install Python and check "Add Python to PATH" during installation
- Or manually add Python to system PATH

### Issue: "pip is not available"

**Solution:**
- Reinstall Python with pip included
- Or download get-pip.py and install pip manually

### Issue: "wheels directory not found"

**Solution:**
- The offline package is incomplete
- Ensure the `wheels` folder was included when creating the ZIP
- Re-download dependencies using `download_dependencies.bat` on a machine with internet

### Issue: "Module not found" errors

**Solution:**
- Run `setup.bat` again to reinstall packages
- Check that all `.whl` files are in the `wheels` folder
- Verify Python version compatibility (3.8+)

### Issue: "Cannot connect to Tally"

**Solution:**
- Ensure Tally is running
- Check that HTTP Server is enabled in Tally
- Verify Tally is listening on port 9000
- You can still use manual export workflow if Tally connection fails

## 📝 File Structure After Setup

```
VEGA/
├── config/                    # Template files
├── exports/                   # Input XML files
├── output/                    # Generated reports
├── scripts/                   # Python scripts
├── wheels/                    # Offline package files (keep this!)
├── requirements.txt
├── setup.bat
├── run.bat
└── README.md
```

## 🔄 Updating Dependencies (Future)

If you need to update packages in the future:

1. On a machine with internet, run `download_dependencies.bat`
2. Replace the `wheels` folder in your deployment package
3. On target machine, run `setup.bat` again

## ✅ Checklist for Deployment

- [ ] Python 3.8+ installed on target machine
- [ ] VEGA folder extracted to target machine
- [ ] `wheels` folder included in package
- [ ] `setup.bat` run successfully
- [ ] All packages installed without errors
- [ ] Tally configured with HTTP Server enabled
- [ ] Test run successful with `run.bat`

## 📞 Support

For issues or questions, refer to the main README.md file or contact the development team.

---

**Note:** This deployment method is designed for offline environments. All dependencies are packaged locally, so no internet connection is required after initial setup.
