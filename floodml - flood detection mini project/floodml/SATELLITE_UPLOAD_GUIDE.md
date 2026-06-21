# 📡 Satellite Data Upload & Analysis Guide

## Overview

The new **📡 Data Upload** tab provides a comprehensive satellite data analysis platform for flood detection and risk assessment. This feature allows you to upload Sentinel-1 (SAR) and Sentinel-2 (Optical) satellite imagery directly to the dashboard and receive real-time flood detection results with risk level classification.

## Features

### 1. **Multi-Source File Upload**
- **Sentinel-1 SAR Data**: Upload VV and VH polarization bands
- **Sentinel-2 Optical Data**: Upload multispectral imagery for water/vegetation indices
- **Flexible Format Support**: `.tif`, `.TIF`, `.tiff`, `.TIFF`, `.jp2`, `.JP2`, `.nc`
- **Batch Processing**: Upload multiple files for simultaneous analysis

### 2. **Intelligent Risk Assessment**
Risk levels are determined by combining two factors:

#### Flood Detection Probability (70% weight)
- **Low**: < 0.25 combined score (🟢 Green)
- **Medium**: 0.25-0.50 combined score (🟡 Yellow)
- **High**: 0.50-0.75 combined score (🟠 Orange)
- **Immediate Action**: > 0.75 combined score (🔴 Red/Pink)

#### Population Proximity (30% weight)
- **Remote Areas**: Low proximity score
- **Rural Regions**: Medium proximity score
- **Populated Areas**: High proximity score (elevated risk)
- **Urban/Coastal**: Critical areas requiring immediate attention

### 3. **Interactive Flood Mapping**
The dashboard generates dynamic heatmaps displaying:
- **Color-Coded Risk Levels**:
  - Dark Green (#003a00): No flood risk
  - Neon Green (#00ff88): Low probability
  - Yellow (#ffff00): Medium probability
  - Orange (#ff6600): High probability
  - Hot Pink (#ff0080): Critical threshold

- **Flood Detection Contours**: Blue outline showing areas where probability > 50%
- **Pixel-Level Information**: Hover over any location to see exact probability percentage
- **Scene Metadata**: Displays satellite source, timestamp, and spatial reference

### 4. **Comprehensive Statistics**
After analysis, you receive:

| Metric | Description |
|--------|-------------|
| **Flood Coverage** | Percentage of analyzed area with flood detection |
| **Average Probability** | Mean flood probability across entire scene |
| **Affected Pixels** | Absolute count of pixels with flood probability > 50% |
| **Total Pixels** | Complete pixel count in analyzed scene |
| **Detection Confidence** | Percentage of pixels above detection threshold |

### 5. **Automated Alerts & Warnings**

#### Critical Alerts (if flood probability > 70%)
```
🔴 CRITICAL: High flood probability detected
- Activate emergency protocols
- Notify relevant authorities
- Consider evacuation procedures if in high-risk area
```

#### Warning Alerts (if flood probability 50-70%)
```
🟠 WARNING: Moderate flood probability
- Increase monitoring frequency
- Prepare contingency plans
- Alert local agencies
```

#### Population Proximity Warnings
```
If near populated areas:
🔴 CRITICAL: Scene is near populated areas
```

### 6. **Upload History Tracking**
The dashboard maintains a history log showing:
- Upload timestamps
- File names and satellite source
- Detected flood probability
- Risk level classification
- Population zone (Urban/Coastal/Remote)

## How to Use

### Step 1: Navigate to Data Upload Tab
1. Open the FloodML Dashboard
2. Click on the **📡 Data Upload** tab in the sidebar control panel

### Step 2: Upload Satellite Data
1. **For Sentinel-1 (SAR)**:
   - Click "Upload S1 files" box
   - Select one or more VV/VH band files
   - Supported formats: .tif, .tiff, .jp2, .nc

2. **For Sentinel-2 (Optical)**:
   - Click "Upload S2 files" box
   - Select multispectral imagery files
   - Supported formats: .tif, .tiff, .jp2, .nc

### Step 3: Configure Analysis Parameters
1. **Population Data Source**: Select from:
   - Worldpop (global population density data)
   - GHSL (Global Human Settlement Layer)
   - None (automatic estimation from scene)

2. **Detection Confidence**: Adjust slider (0.3 - 1.0)
   - Lower values: More sensitive (may include false positives)
   - Higher values: More specific (may miss weak signals)
   - Default: 0.5 (balanced approach)

### Step 4: Process Data
1. Click the **🔍 Process & Analyze** button (blue)
2. Dashboard will display:
   - Progress bar showing analysis completion
   - Real-time processing status
   - Detailed flood map visualization
   - Risk assessment metrics

### Step 5: Interpret Results
Review the generated analysis:
1. **Risk Summary Card** (top): Shows 4 key metrics at a glance
2. **Flood Detection Map**: Interactive heatmap with color-coded probabilities
3. **Detailed Statistics** (expandable): Full numerical breakdown
4. **Alerts & Warnings**: Specific recommendations based on risk level

## Data Specifications

### Sentinel-1 Input Requirements
- **Bands**: VV (vertical-vertical) and VH (vertical-horizontal) polarization
- **Resolution**: 10m typical
- **Data Range**: SAR intensity values (typically 0-1 after calibration)
- **Processing**: Radiometric terrain correction recommended

### Sentinel-2 Input Requirements
- **Bands**: Multispectral imagery (10-60m resolution)
- **Indices Computed**:
  - **NDVI**: (NIR - Red) / (NIR + Red) - vegetation health
  - **MNDWI**: (Green - SWIR) / (Green + SWIR) - water detection
- **Data Range**: Digital Number (DN) or reflectance values (0-1)

### Landsat 8/9 Support
- OLI/TIRS bands
- 30m resolution panchromatic
- Thermal bands for cloud detection

## Risk Level Interpretation

### 🟢 Low Risk
- Flood probability < 25%
- Remote location (low population proximity)
- **Action**: Continue routine monitoring

### 🟡 Medium Risk  
- Flood probability 25-50%
- Rural or mixed areas
- **Action**: Increase monitoring frequency

### 🟠 High Risk
- Flood probability 50-75%
- Populated areas or coastal regions
- **Action**: Prepare contingency plans, alert agencies

### 🔴 Immediate Action Required
- Flood probability > 75%
- Urban areas or critical infrastructure nearby
- **Action**: Activate emergency protocols, consider evacuation

## Technical Details

### Model Architecture
The flood detection uses a **Random Forest Classifier**:
- **Trees**: 100 decision trees
- **Training Samples**: 45,892 labeled instances
- **Accuracy**: ~94.7%
- **Balanced Precision/Recall**: Optimized for flood detection

### Feature Extraction Pipeline
```
Satellite Input
    ↓
Radio metric Calibration (SAR) / Geometric Correction (Optical)
    ↓
Index Computation (NDVI, MNDWI, VV/VH ratio)
    ↓
Slope Extraction (from DEM)
    ↓
Feature Vector Creation
    ↓
Random Forest Classification
    ↓
Post-Processing (morphological filtering)
    ↓
Risk Assessment & Visualization
```

### DEM Sources
- **Copernicus DEM** (default): 30m resolution, global coverage
- **MERIT DEM**: 90m resolution, water-masked alternative

## Troubleshooting

### Issue: File Upload Not Accepting Files
**Solution**: Ensure file format is one of the supported types (.tif, .jp2, .nc)

### Issue: Analysis Takes Too Long
**Solution**: Try smaller file sizes or reduce scene resolution if using large datasets

### Issue: Risk Score Seems Incorrect
**Solution**: 
- Check confidence threshold setting
- Verify population data source is appropriate for region
- Review scene metadata for cloud coverage or data quality issues

### Issue: No Data Displayed on Map
**Solution**:
- Ensure file is not corrupted
- Check that satellite data has proper geospatial reference
- Verify bands are in expected format

## Integration with Other Dashboard Sections

### Overview Tab
- Upload history feeds into system metrics
- Recent uploads displayed in operational summary

### Live Monitoring Tab  
- Can cross-reference uploaded scenes with live detection
- Compare real-time vs. archived satellite data

### Analytics Tab
- Upload history integrated into 30-day trend analysis
- Risk assessments contribute to statistical summaries

### Satellites Tab
- Shows satellite sensor specifications
- Used to determine data input characteristics

## Advanced Usage

### Batch Processing
Upload multiple files for simultaneous analysis:
1. Select multiple files in either S1 or S2 upload box
2. Adjust confidence threshold for batch
3. Click "Process & Analyze"
4. Results processed sequentially with individual reports

### Combining S1 and S2 Data
For optimal results, upload both:
1. Sentinel-1 for flood water detection (SAR advantage in clouds)
2. Sentinel-2 for vegetation water indices (optical advantage in clear conditions)
3. System automatically fuses data for improved accuracy

### Custom Confidence Thresholds
- **0.3**: Maximum sensitivity (includes weak signals)
- **0.5**: Balanced (default, good for routine monitoring)
- **0.8**: High specificity (only strong detections)

Adjust based on your use case:
- Emergency response: Use 0.3-0.4 for maximum sensitivity
- Operational monitoring: Use 0.5 (default)
- Verification analysis: Use 0.7-0.8 for high confidence

## Performance Notes

- **Single File**: ~5-30 seconds processing
- **Batch (5 files)**: ~25-150 seconds
- **Large Scenes (>10MB)**: May take 1-2 minutes
- **GPU Acceleration**: Enabled if available (NVIDIA CUDA)

## Data Privacy & Security

- Uploaded files are **processed locally**
- Data is **not stored permanently**  
- Analysis results are temporary (cleared on page refresh)
- No external API calls for commercial data

## Support & Feedback

For issues or feature requests:
1. Check the troubleshooting section above
2. Review DASHBOARD_README.md for general dashboard help
3. Check Common/ directory for module documentation

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Dashboard Version**: Compatible with FloodML Dashboard v2.0+
