# 📡 Data Upload Tab - Quick Reference

## 60-Second Setup

1. **Navigate**: Click **📡 Data Upload** tab in sidebar
2. **Upload**: Select satellite files (.tif, .jp2, .nc)
3. **Configure**: Set population source & confidence (optional)
4. **Process**: Click **🔍 Process & Analyze**
5. **Review**: Check map, stats, and alerts

## Risk Levels at a Glance

| Level | Color | Flood Prob | Population | Action |
|-------|-------|-----------|------------|--------|
| 🟢 Low | Green | <25% | Remote | Monitor |
| 🟡 Medium | Yellow | 25-50% | Mixed | Check |
| 🟠 High | Orange | 50-75% | Populated | Alert |
| 🔴 Critical | Red/Pink | >75% | Urban | Emergency |

## Supported Formats

```
Sentinel-1: .tif, .jp2, .nc (VV/VH bands)
Sentinel-2: .tif, .jp2, .nc (multispectral)
Landsat 8/9: .tif, .jp2, .nc
```

## Key Metrics

- **Flood Coverage**: % of pixels with detection
- **Avg Probability**: Mean flood likelihood
- **Affected Pixels**: Count of detected areas
- **Detection Confidence**: Threshold setting

## Confidence Threshold Guide

```
0.3-0.4: Maximum sensitivity (emergency response)
0.5:     Balanced (default - recommended)
0.7-0.8: High specificity (verification)
```

## Population Data Sources

- **Worldpop**: Global population density (default)
- **GHSL**: Human settlement patterns
- **None**: Auto-estimate from scene characteristics

## Color-Coded Map Legend

```
Dark Green (#003a00):  Safe - No flood risk
Neon Green (#00ff88):  Low - <30% probability
Yellow (#ffff00):      Medium - 30-50% probability
Orange (#ff6600):      High - 50-70% probability
Hot Pink (#ff0080):    Critical - >70% probability

Blue Contours: Areas with >50% flood probability
```

## Processing Tips

✅ **Best Practices**
- Use cloud-free scenes when available
- Combine S1 + S2 for accuracy
- Start with default confidence (0.5)
- Check upload history for trends

❌ **Avoid**
- Corrupted or incomplete files
- Mixed spatial resolutions (if possible)
- Extremely large scenes (>1GB) without GPU

## Common Workflows

### Emergency Response
1. Upload high-resolution S1 data
2. Set confidence to 0.3 (max sensitivity)
3. Use Worldpop for population data
4. Review critical areas immediately

### Operational Monitoring
1. Upload routine S1 + S2 files
2. Use default confidence (0.5)
3. Select GHSL for better granularity
4. Track trends in history log

### Verification Analysis
1. Upload specific region S2 data
2. Set confidence to 0.8 (high specificity)
3. Cross-reference with ground truth
4. Export statistics for reports

## Interpreting the Flood Map

- **Hover over pixels**: See exact probability %
- **Darker colors**: Lower risk
- **Brighter colors**: Higher risk
- **Blue outlines**: Flood detected (prob > 50%)
- **Gaps in data**: Cloud cover or missing data

## Export & Sharing

Save analysis results:
1. Take screenshot of flood map
2. Download statistics CSV (if available)
3. Copy risk assessment to reports
4. Reference upload timestamp for archiving

## Processing Time Estimates

- Single small file: 5-15 sec
- Single large file: 30-60 sec
- Batch (5 files): 2-5 minutes
- Large scene with GPU: 10-30 sec

## Troubleshooting

| Problem | Solution |
|---------|----------|
| File won't upload | Check format (.tif, .jp2, .nc) |
| Analysis stuck | Refresh page, try smaller file |
| No map displayed | Verify file has geospatial metadata |
| Unexpected results | Check confidence threshold, review QA flags |

## Integration Points

| Dashboard Tab | Connection |
|---|---|
| 🏠 Overview | Upload count in metrics |
| 🗺️ Live Monitoring | Compare with live detections |
| 📊 Analytics | Include in 30-day history |
| 🛰️ Satellites | Reference sensor specs |

---

**Pro Tip**: Bookmark this page for quick access to upload features!
