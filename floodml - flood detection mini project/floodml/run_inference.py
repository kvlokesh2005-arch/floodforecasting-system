import numpy as np
import rasterio
import joblib
import matplotlib.pyplot as plt
import os

# Define paths
MODEL_PATH = 'models/flood_model.pkl'
TEST_IMAGE_S1 = 'data/input/S1/Bolivia_103757_S1Hand.tif'   # Change this
TEST_IMAGE_S2 = 'data/input/S2/Bolivia_103757_S2Hand.tif'
OUTPUT_DIR = 'results'

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading trained model...")
model = joblib.load(MODEL_PATH)

print("Loading test images...")

# Read S1 image
with rasterio.open(TEST_IMAGE_S1) as src:
    s1_data = src.read()
    s1_meta = src.meta

# Read S2 image
with rasterio.open(TEST_IMAGE_S2) as src:
    s2_data = src.read()

print(f"S1 shape: {s1_data.shape}")
print(f"S2 shape: {s2_data.shape}")

# Reshape for prediction
height, width = s1_data.shape[1], s1_data.shape[2]

X_s1 = s1_data.reshape(s1_data.shape[0], -1).T
X_s2 = s2_data.reshape(s2_data.shape[0], -1).T

# Combine bands
X = np.hstack([X_s1, X_s2])

print("Predicting flood areas...")
y_pred = model.predict(X)

# Reshape prediction back to image
flood_map = y_pred.reshape(height, width)

print("Prediction complete!")

# Save result as GeoTIFF
output_path = os.path.join(OUTPUT_DIR, 'flood_prediction.tif')

with rasterio.open(
    output_path,
    'w',
    driver='GTiff',
    height=height,
    width=width,
    count=1,
    dtype=flood_map.dtype,
    crs=s1_meta['crs'],
    transform=s1_meta['transform']
) as dst:
    dst.write(flood_map, 1)

print(f"Saved prediction to: {output_path}")

# Visualize result
plt.figure(figsize=(12, 8))
plt.imshow(flood_map, cmap='Blues')
plt.colorbar(label='Flood Classification')
plt.title('Flood Prediction Map')
plt.savefig(os.path.join(OUTPUT_DIR, 'flood_prediction.png'), dpi=300)
print(f"Saved visualization to: {OUTPUT_DIR}/flood_prediction.png")

plt.show()

print("\nInference complete!")
