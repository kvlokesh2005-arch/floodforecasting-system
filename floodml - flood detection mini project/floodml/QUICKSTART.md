# 🚀 FloodML Dashboard - Quick Start Guide

## 30-Second Setup

### Windows
```bash
run_dashboard.bat
```

### Linux/Mac
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

**That's it!** The dashboard will open at `http://localhost:8501`

---

## Detailed Setup (5 Minutes)

### Step 1: Install Python
- **Windows**: Download from [python.org](https://python.org)
- **macOS**: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

### Step 2: Install Dependencies
```bash
pip install -r requirements-dashboard.txt
```

### Step 3: Run Dashboard
```bash
streamlit run app.py
```

### Step 4: Access
Open browser to: `http://localhost:8501`

---

## First Time User Guide

### 1. **Explore the Overview**
   - See system metrics and recent detections
   - Check system health status
   - Monitor model accuracy

### 2. **View Live Monitoring**
   - Select a satellite source (default: Sentinel-2)
   - See real-time flood detection maps
   - Adjust confidence threshold to see different results

### 3. **Check Analytics**
   - View 30-day performance history
   - See which satellites perform best
   - Understand model metrics

### 4. **Understand Satellites**
   - Compare different satellite sources
   - Learn resolution and revisit frequencies
   - Check data availability

### 5. **Configure Settings**
   - Adjust model parameters
   - Configure post-processing
   - Set confidence thresholds

---

## Common Tasks

### Change Satellite Source
1. Open sidebar (click ☰ if collapsed)
2. Select satellite in **"Select Satellite Source"** dropdown
3. Choose from:
   - 🛰️ Sentinel-1 (all-weather SAR)
   - 🛰️ Sentinel-2 (high-quality optical)
   - 🛰️ Landsat 8/9 (wider coverage)
   - 🛰️ TerraSAR-X (high-res SAR)

### Adjust Detection Sensitivity
1. Go to sidebar
2. Adjust **"Confidence Threshold"** slider (0.5 - 0.99)
   - Lower = more sensitive (catch more floods, some false positives)
   - Higher = more selective (fewer false positives, might miss floods)
3. Results update instantly

### Filter Small Detections
1. Go to sidebar
2. Adjust **"Minimum Flood Area (pixels)"** slider
3. Remove noise from small false positives

### Change Date Range
1. Go to sidebar
2. Click **"Analysis Period"** date picker
3. Select custom date range for historical analysis

### View Different Bands
1. Go to **Live Monitoring** tab
2. Scroll to "Band Visualization" section
3. Select band from dropdown:
   - RGB Composite: Natural color
   - NDVI: Vegetation index
   - MNDWI: Water-specific index
   - SAR VV/VH: Radar polarizations

---

## Understanding Dashboard Sections

### 🏠 Overview Tab
**What**: System dashboard with key metrics
**Shows**: Accuracy, processed scenes, detected floods, system health
**Use When**: Want quick system status

### 🗺️ Live Monitoring Tab
**What**: Real-time flood detection visualization
**Shows**: Interactive heatmaps, scene statistics, band data
**Use When**: Analyzing specific satellite scene

### 📊 Analytics Tab
**What**: Historical analysis and performance metrics
**Shows**: 30-day trends, confusion matrix, classification metrics
**Use When**: Tracking model improvement or comparing results

### 🛰️ Satellites Tab
**What**: Satellite capabilities comparison
**Shows**: Resolution, accuracy, processing time, availability
**Use When**: Choosing best satellite for a region

### ⚙️ Configuration Tab
**What**: Advanced system settings
**Shows**: Model parameters, processing pipeline, storage, tuning
**Use When**: Fine-tuning for specific use cases

---

## Interpreting Results

### Flood Probability Heatmap Colors
```
🔵 Blue      → High probability of water/flood
🟢 Green     → Low flood risk
🟡 Yellow    → Medium flood risk
🟠 Orange    → High flood risk
🔴 Red       → Critical - Flood detected
⚪ Gray      → Cloud, shadow, or no data
```

### Key Metrics

| Metric | Range | Meaning |
|--------|-------|---------|
| **Accuracy** | 0-100% | Overall correctness of predictions |
| **Precision** | 0-100% | Of detected floods, how many real? |
| **Recall** | 0-100% | Of actual floods, how many found? |
| **F1-Score** | 0-100% | Balance of precision & recall |
| **Coverage** | 0-100% | % of scene with valid data (no clouds) |
| **Confidence** | 0-100% | Model confidence in prediction |

---

## Troubleshooting

### "Streamlit not found"
```bash
pip install streamlit
streamlit run app.py
```

### "Address already in use"
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### "Slow performance"
1. Reduce batch size in Configuration tab
2. Lower map resolution
3. Use GPU (if available) - set in Configuration

### "No data displayed"
1. Check satellite selection
2. Change date range
3. Lower confidence threshold
4. Try different satellite

### "Missing model file"
1. Verify `models/flood_model.pkl` exists
2. Check file permissions
3. Ensure model trained successfully

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Stop dashboard |
| `R` | Refresh data |
| `C` | Clear cache |
| `?` | Show help |
| `Ctrl+L` | Clear log |

---

## Tips & Tricks

### 🎯 For Better Detections
1. Use **Sentinel-2** for high accuracy
2. Use **Sentinel-1** when clouds present
3. Combine multiple satellites
4. Adjust confidence based on region

### ⚡ For Faster Performance
1. Reduce analysis period
2. Use single satellite
3. Enable GPU acceleration
4. Increase batch size

### 🔍 For Better Analysis
1. Start with low confidence threshold
2. Gradually increase to find optimal level
3. Compare multiple satellites
4. Check historical trends

### 🎨 For Better Visualization
1. Zoom in on areas of interest
2. Hover over map for exact values
3. Click legend items to hide/show
4. Export charts for presentations

---

## Next Steps

### Intermediate
- [ ] Learn about DEM configuration
- [ ] Understand post-processing options
- [ ] Explore performance tuning
- [ ] Try different satellite combinations

### Advanced
- [ ] Export custom reports
- [ ] Integrate with external APIs
- [ ] Set up email alerts
- [ ] Deploy to cloud (AWS/GCP)

### Mastery
- [ ] Fine-tune model for region
- [ ] Create custom training dataset
- [ ] Deploy on HPC cluster
- [ ] Develop plugins/extensions

---

## Getting Help

### Documentation
- Full guide: `DASHBOARD_README.md`
- Repo info: `.zencoder/rules/repo.md`
- License: `LICENSE.md`

### Common Issues
See Troubleshooting section above

### Report Issues
Check Streamlit logs:
```bash
streamlit logs
```

---

## Resources

### Learning
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Visualization](https://plotly.com/)
- [Random Forest ML](https://scikit-learn.org/stable/modules/ensemble.html#random-forests)
- [Flood Detection Basics](https://www.usgs.gov/faqs)

### Satellite Data
- [Sentinel Hub](https://scihub.copernicus.eu/)
- [USGS EarthExplorer](https://earthexplorer.usgs.gov/)
- [NASA EOSDIS](https://earthdata.nasa.gov/)

---

## Version Info
- **Dashboard**: 1.0.0
- **Python**: 3.8+
- **Status**: Production Ready ✅

**Ready to detect floods?** 🌊 Start the dashboard and explore! 🚀
