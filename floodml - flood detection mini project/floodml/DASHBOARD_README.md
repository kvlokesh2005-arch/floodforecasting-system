# 🌊 FloodML Dashboard

## Real-Time Flood Detection & Monitoring System

### Overview

The FloodML Dashboard is a comprehensive web-based monitoring and analysis platform for real-time flood detection using satellite imagery and machine learning. It provides an intuitive, neon-themed interface for viewing flood detection results, analyzing model performance, and managing satellite data processing.

---

## 🎨 Features

### Dashboard Views

#### 1. **🏠 Overview Dashboard**
- **System Status Metrics**: Real-time display of model accuracy, processed scenes, detected floods, and processing time
- **Recent Detections**: Last 7 days of flood detections with confidence scores and affected areas
- **System Health Monitoring**: Component status, uptime, and system load visualization

#### 2. **🗺️ Live Monitoring**
- **Interactive Flood Detection Maps**: Real-time heatmaps showing flood probability by pixel
- **Scene Statistics**: Flood coverage percentage, detection confidence, processing time
- **Scene Information**: Satellite type, tile ID, timestamp, projection, resolution, cloud cover
- **Band Visualization**: Select and view different satellite bands (RGB, NDVI, MNDWI, SAR)
- **Classification Legend**: Color-coded flood risk levels and classification information
- **Processing Pipeline**: Step-by-step visualization of inference stages

#### 3. **📊 Analytics Dashboard**
- **Performance Metrics Over Time**: 30-day history of accuracy, precision, recall, F1-score
- **Confusion Matrix Breakdown**: True/False positives and negatives
- **Classification Metrics**: Precision, recall, F1-score, accuracy, specificity, sensitivity
- **Temporal Analysis**: Monthly activity showing scenes processed and floods detected

#### 4. **🛰️ Satellite Sources**
- **Comparative Analysis**: Coverage %, accuracy, and processing time by satellite
- **Satellite Capabilities**:
  - **Sentinel-1**: SAR, 10m resolution, 6-day revisit, 92% accuracy
  - **Sentinel-2**: Optical, 10m resolution, 5-day revisit, 95% accuracy
  - **Landsat 8/9**: Optical, 30m resolution, 8-day revisit, 88% accuracy
  - **TerraSAR-X**: SAR, 3m resolution, regular revisit, 87% accuracy
- **Data Availability Calendar**: Track satellite passes over 7-day period

#### 5. **⚙️ Configuration**
- **Model Configuration**: Random Forest classifier settings, training data statistics
- **Processing Pipeline**: Detailed configuration of each processing stage
- **Data Management**: Database, storage, and retention settings
- **Performance Tuning**: GPU/CPU optimization, batch processing, parallel processing
- **Advanced Settings**: Post-processing, cloud thresholds, DEM source selection

---

## 🎯 Key Metrics & Indicators

### Flood Detection Classification
- 🔴 **Critical - Flood Detected**: High flood probability (>0.7)
- 🟠 **High Risk**: Moderate flood probability (0.5-0.7)
- 🟡 **Medium Risk**: Elevated flood probability (0.3-0.5)
- 🟢 **Low Flood Risk**: Low probability (<0.3)
- ☁️ **Cloud/NoData**: No valid data available

### Model Performance Metrics
- **Accuracy**: Overall correctness of predictions
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **Specificity**: True negatives / (True negatives + False positives)
- **Sensitivity**: Same as recall (True positive rate)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda
- 2GB RAM minimum
- Internet connection (for satellite data)

### Quick Start

1. **Install Dependencies**
```bash
pip install -r requirements-dashboard.txt
```

2. **Run the Dashboard**
```bash
streamlit run app.py
```

3. **Access the Dashboard**
- Open your browser to: `http://localhost:8501`

### Advanced Setup with Virtual Environment

```bash
# Create virtual environment
conda create -n floodml-dashboard python=3.8
conda activate floodml-dashboard

# Install requirements
pip install -r requirements-dashboard.txt

# Run dashboard
streamlit run app.py
```

---

## 🎮 Control Panel Guide

### Sidebar Controls

#### Satellite Selection
- **Sentinel-1 (SAR)**: All-weather radar imaging, works through clouds
- **Sentinel-2 (Optical)**: Multispectral optical imaging, requires clear skies
- **Landsat 8/9**: Coarser resolution but wider coverage
- **TerraSAR-X (SAR)**: High-resolution SAR data

#### Region/Tile ID
- Input MGRS tile identifier (e.g., T30UUE)
- Defines geographic area of analysis

#### Analysis Period
- Select date range for historical analysis
- Affects analytics and performance metrics

#### Confidence Threshold
- **Range**: 0.5 - 0.99
- **Default**: 0.75
- **Effect**: Filters flood detections below threshold
- **Higher values**: More conservative (fewer false positives)
- **Lower values**: More sensitive (catches more floods, more false positives)

#### Minimum Flood Area
- **Range**: 10 - 1000 pixels
- **Default**: 100 pixels
- **Effect**: Removes noise (isolated small detections)
- **Higher values**: Focuses on large flood events

---

## 🔄 Data Processing Pipeline

### 1. **Input Processing**
- Satellite data ingestion from COPERNICUS Hub or USGS
- Validation of data integrity
- Cloud and shadow detection/masking
- Radiometric calibration

### 2. **Feature Extraction**
- Synthetic band generation:
  - **NDVI** (Normalized Difference Vegetation Index): From optical bands
  - **MNDWI** (Modified Normalized Difference Water Index): Specific for water detection
  - **SAR Backscatter**: From Sentinel-1 or TerraSAR-X
- **DEM-based features**: Slope calculation from topography
- Morphological filtering for noise reduction

### 3. **Classification (Random Forest)**
- Multi-tree ensemble voting
- 100 decision trees
- Two classes: Water/No-Water
- Per-pixel probability scoring

### 4. **Post-Processing**
- Majority filter (morphological cleaning)
- Connected component analysis
- Land cover overlay (ESA World Cover classification)
- Cloud/shadow masking

### 5. **Output Generation**
- Georeferenced GeoTIFF files
- Rapid mapping visualizations
- Statistical reports

---

## 📊 Understanding the Visualizations

### Flood Probability Heatmap
- **Color Scale**: Blue (water) → Green (low risk) → Yellow → Red (flood)
- **Interactive**: Hover for exact coordinates and probabilities
- **Zoom/Pan**: Standard Plotly controls

### Performance Metrics Charts
- **Line Charts**: Time-series tracking of model performance
- **Bar Charts**: Comparative analysis across satellites
- **Legends**: Click to toggle data series visibility

### Data Tables
- **Sortable Columns**: Click header to sort
- **Searchable**: Use browser find function (Ctrl+F)
- **Progress Bars**: Visual representation of percentages

---

## ⚙️ Configuration Details

### Model Settings
```
Algorithm: Random Forest Classifier
Number of Trees: 100
Max Depth: Auto (not limited)
Min Samples Split: 2
Min Samples Leaf: 1
Random State: 42
```

### Training Data
```
Total Samples: 45,892
Classes: 2 (Water/No-Water)
Training/Test Split: 70/30
Features: VV, VH/NDVI/MNDWI, Slope
```

### DEM Sources
- **Copernicus DEM**: 30m global coverage, recent
- **MERIT DEM**: 90m global coverage, research grade

### Processing Parameters
- **Post-Processing Radius**: 2-5 pixels (default: 2)
- **Cloud Threshold**: 0.0-1.0 (default: 0.3)
- **Nodata Value**: 255 (standard for uint8)
- **Compression**: LZW for output GeoTIFFs

---

## 🛠️ Troubleshooting

### Dashboard Not Loading
```bash
# Clear Streamlit cache
streamlit cache clear

# Run with verbose logging
streamlit run app.py --logger.level=debug
```

### Slow Performance
1. Check GPU availability: `nvidia-smi`
2. Reduce batch size in Advanced Settings
3. Clear temporary processing files
4. Check disk space (requires ~10GB for cache)

### Missing Satellite Data
- Verify internet connection
- Check COPERNICUS/USGS account credentials
- Verify date range has available data
- Try different satellite source

### Model Inference Errors
- Ensure model file exists: `models/flood_model.pkl`
- Check for corrupted cached files
- Verify input data format
- Check GPU memory availability

---

## 📈 API Integration

The dashboard can be integrated with external systems:

### Data Export
- Export configuration as JSON
- Save analysis reports as PDF (future version)
- Stream results to external databases

### Monitoring Integration
- Prometheus metrics endpoint
- Alert webhooks for critical detections
- REST API for programmatic access (planned)

---

## 🔐 Security & Privacy

- All processing runs locally (no data sent externally)
- Satellite data validated against known datasets
- User configurations stored locally
- No user tracking or analytics

---

## 📚 References & Resources

### Satellite Data
- [ESA Sentinel Hub](https://scihub.copernicus.eu/)
- [USGS EarthExplorer](https://earthexplorer.usgs.gov/)
- [Copernicus Open Access Hub](https://scihub.copernicus.eu/)

### Documentation
- [Sentinel-1 Documentation](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-1-sar)
- [Sentinel-2 Documentation](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi)
- [Landsat 8/9 Documentation](https://www.usgs.gov/landsat-missions)

### ML & GIS
- [Scikit-learn Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [GDAL Documentation](https://gdal.org/)
- [Plotly Interactive Visualizations](https://plotly.com/)

---

## 📞 Support & Feedback

For issues, feature requests, or feedback:
- Check the troubleshooting section above
- Review system logs: `streamlit logs`
- Consult CNES FloodML documentation

---

## 📄 License

Copyright (C) CNES - All Rights Reserved
This file is subject to the terms and conditions defined in LICENSE.md

---

## 🎓 Learning Resources

### Understanding Flood Detection
1. Start with **Overview** tab to see system metrics
2. Navigate to **Live Monitoring** to see real flood detection
3. Check **Analytics** for historical performance
4. Explore **Satellites** to understand data sources
5. Review **Configuration** to understand processing pipeline

### Tips for Best Results
- Use Sentinel-2 for precise detection (optical)
- Use Sentinel-1 for all-weather capability (SAR)
- Combine multiple satellites for improved accuracy
- Lower confidence threshold for sensitive areas (flood plains)
- Higher confidence threshold for urban areas (reduce false positives)

---

## 🚀 Future Enhancements

- [ ] Real-time streaming from satellite APIs
- [ ] Multi-temporal change detection
- [ ] Advanced anomaly detection
- [ ] Custom model training interface
- [ ] PDF report generation
- [ ] Email/SMS alerts for critical detections
- [ ] Mobile application
- [ ] Cloud deployment templates (AWS, GCP)

---

**Last Updated**: November 2024
**Version**: 1.0.0
**Status**: Production Ready ✅
