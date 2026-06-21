import matplotlib.pyplot as plt
import rasterio
import os

# Make sure results folder exists
os.makedirs("results", exist_ok=True)

# Load prediction
with rasterio.open('results/flood_prediction.tif') as src:
    flood_map = src.read(1)

# Load original S1 image for comparison
with rasterio.open('data/input/S1/Bolivia_103757_S1Hand.tif') as src:
    s1_image = src.read(1)

# Create side-by-side comparison
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

axes[0].imshow(s1_image, cmap='gray')
axes[0].set_title('Sentinel-1 SAR Image')
axes[0].axis('off')

axes[1].imshow(flood_map, cmap='Blues')
axes[1].set_title('Flood Prediction')
axes[1].axis('off')

plt.tight_layout()

# Save visualization
plt.savefig('results/comparison.png', dpi=300, bbox_inches='tight')
plt.show()

print("Comparison saved to results/comparison.png")
