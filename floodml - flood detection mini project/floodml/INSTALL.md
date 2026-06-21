# 📦 FloodML Dashboard - Installation Guide

## Complete Setup Instructions

### Prerequisites
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 8GB recommended
- **Disk**: 20GB available (for data and models)
- **Internet**: For downloading dependencies

---

## Installation Methods

### Method 1: Automated Installation (Recommended)

#### Windows
```cmd
run_dashboard.bat
```

#### Linux/macOS
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

**What it does:**
- Checks Python installation
- Installs missing dependencies
- Starts the dashboard automatically
- Opens browser to localhost:8501

---

### Method 2: Manual Installation

#### Step 1: Verify Python Installation
```bash
python --version
python -m pip --version
```

**Expected output**: Python 3.8 or higher

If not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: `brew install python3`
- **Linux (Ubuntu/Debian)**: `sudo apt-get install python3 python3-pip`

#### Step 2: Upgrade pip
```bash
python -m pip install --upgrade pip
```

#### Step 3: Create Virtual Environment (Optional but Recommended)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements-dashboard.txt
```

**Installation time**: ~5-10 minutes depending on internet speed

#### Step 5: Verify Installation
```bash
python verify_setup.py
```

**Expected**: All checks should pass ✅

#### Step 6: Run Dashboard
```bash
streamlit run app.py
```

**Expected**: Dashboard opens at http://localhost:8501

---

### Method 3: Conda Installation (For RAPIDS Users)

If you already have the main FloodML conda environment:

```bash
# Activate existing environment
conda activate rapids-0.21.08

# Install dashboard dependencies
pip install -r requirements-dashboard.txt

# Run dashboard
streamlit run app.py
```

---

## Troubleshooting Installation

### "Python not found" or "python: command not found"

**Windows:**
1. Download Python from python.org
2. **Important**: Check "Add Python to PATH" during installation
3. Restart terminal
4. Try again: `python --version`

**macOS:**
```bash
# If using Homebrew
brew install python3

# Add to PATH
export PATH="/usr/local/bin:$PATH"
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### "pip: command not found"

```bash
# Try with python module
python -m pip install -r requirements-dashboard.txt

# Or upgrade pip first
python -m pip install --upgrade pip
```

### "Permission denied" (Linux/macOS)

```bash
# Make scripts executable
chmod +x run_dashboard.sh verify_setup.py

# Or run with sudo if needed
sudo pip install -r requirements-dashboard.txt
```

### "Address already in use" (Port 8501 occupied)

```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing Streamlit process
# Windows: taskkill /IM streamlit.exe
# Linux/Mac: pkill -f streamlit
```

### "ModuleNotFoundError" during installation

This usually means pip couldn't download the package. Try:

```bash
# Clear pip cache
pip cache purge

# Retry installation
pip install -r requirements-dashboard.txt --no-cache-dir

# If still failing, try specific versions
pip install streamlit==1.28.0 plotly==5.14.0 pandas==1.5.0
```

### Installation hangs or is very slow

This might be due to network issues:

```bash
# Use different PyPI mirror
pip install -r requirements-dashboard.txt -i https://pypi.tsinghua.edu.cn/simple

# Or increase timeout
pip install -r requirements-dashboard.txt --default-timeout=1000
```

### "No module named 'streamlit'" after installation

Virtual environment might not be activated:

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Then verify
python -c "import streamlit; print(streamlit.__version__)"
```

---

## Post-Installation Setup

### 1. Create Required Directories
```bash
mkdir -p models
mkdir -p data/archive
mkdir -p data/input
mkdir -p data/processed
```

### 2. Place Model File
```bash
# Copy trained model
cp /path/to/flood_model.pkl models/flood_model.pkl
```

### 3. Configure Dashboard
Edit `dashboard_config.json` to match your setup:
```json
{
  "model": {
    "path": "models/flood_model.pkl"
  },
  "dem": {
    "copernicus_dir": "/path/to/copernicus_dem",
    "merit_dir": "/path/to/merit_dem"
  },
  "data": {
    "archive_path": "data/archive"
  }
}
```

### 4. Test Installation
```bash
python verify_setup.py
```

All checks should show ✅

---

## Advanced Configuration

### Using GPU Acceleration

If you have NVIDIA GPU and RAPIDS installed:

```bash
# Install cuML (GPU-accelerated ML)
pip install cuml-cu11

# In dashboard_config.json
{
  "processing": {
    "use_gpu": true
  }
}
```

### Using Conda with RAPIDS

```bash
# Create environment with RAPIDS
conda create -n floodml-rapids rapids-21.08 python=3.8 cudatoolkit=11.0
conda activate floodml-rapids

# Install dashboard dependencies
pip install -r requirements-dashboard.txt

# Run dashboard
streamlit run app.py
```

### Custom Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[client]
showErrorDetails = true

[server]
maxUploadSize = 200
port = 8501
headless = true

[theme]
primaryColor = "#00ff88"
backgroundColor = "#0a0a0a"
secondaryBackgroundColor = "#1a0033"
textColor = "#00ff88"

[logger]
level = "info"
```

---

## System Requirements Details

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 2 GB
- **Storage**: 10 GB
- **GPU**: Not required (CPU mode slower)

### Recommended Requirements
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Storage**: 50+ GB
- **GPU**: NVIDIA with CUDA 11.0+

### High-Performance Setup
- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Storage**: 500+ GB
- **GPU**: NVIDIA RTX 3090 or better with CUDA 11.0+

---

## Docker Installation (Advanced)

For containerized deployment:

```bash
# Build image
docker build -f Dockerfile.dashboard -t floodml-dashboard .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  floodml-dashboard

# Access at http://localhost:8501
```

Create `Dockerfile.dashboard`:
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements-dashboard.txt .
RUN pip install -r requirements-dashboard.txt

COPY app.py .
COPY dashboard_config.json .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.headless", "true"]
```

---

## Verification Checklist

After installation, verify:

- [ ] `python --version` shows 3.8+
- [ ] `python verify_setup.py` shows all ✅
- [ ] `models/flood_model.pkl` exists
- [ ] `data/` directory structure created
- [ ] `dashboard_config.json` configured
- [ ] `streamlit run app.py` launches without errors
- [ ] Browser opens to http://localhost:8501
- [ ] All dashboard tabs load without errors
- [ ] Can interact with controls (sliders, dropdowns)
- [ ] Visualizations render properly

---

## Uninstallation

### Remove Virtual Environment
```bash
# Windows
rmdir /s venv

# Linux/macOS
rm -rf venv
```

### Remove Dependencies
```bash
pip uninstall -r requirements-dashboard.txt -y
```

### Remove Dashboard Files
Keep only the files you created:
```bash
rm app.py
rm dashboard_config.json
rm requirements-dashboard.txt
rm verify_setup.py
rm run_dashboard.bat run_dashboard.sh
```

---

## Getting Help

### Check Logs
```bash
streamlit logs
```

### Debug Mode
```bash
streamlit run app.py --logger.level=debug
```

### Test Installation
```bash
python -c "import streamlit; print('✅ Streamlit OK')"
python -c "import plotly; print('✅ Plotly OK')"
python -c "import pandas; print('✅ Pandas OK')"
python -c "import joblib; print('✅ Joblib OK')"
```

### System Information
```bash
# Get system info for bug reports
python -c "import platform, sys; print(f'{platform.system()} {platform.release()}, Python {sys.version}')"
```

---

## Next Steps

After successful installation:

1. **Run Dashboard**: `streamlit run app.py`
2. **Read Quick Start**: See `QUICKSTART.md`
3. **Explore Dashboard**: Start with Overview tab
4. **Configure Settings**: Adjust in sidebar and Configuration tab
5. **Run Live Monitoring**: Analyze real scenes
6. **Check Analytics**: View historical performance

---

## Support & Issues

For problems:
1. Check this guide's Troubleshooting section
2. Run `python verify_setup.py` to diagnose
3. Check `streamlit logs` for errors
4. Try in debug mode: `streamlit run app.py --logger.level=debug`
5. Check system has minimum requirements

---

## Version Information

- **Dashboard Version**: 1.0.0
- **Python**: 3.8, 3.9, 3.10, 3.11 (tested)
- **Streamlit**: 1.28.0+
- **Last Updated**: November 2024

**Happy Flood Detecting! 🌊**
