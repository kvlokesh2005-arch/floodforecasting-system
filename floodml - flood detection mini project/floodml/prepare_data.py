import os
import numpy as np
import rasterio
from sklearn.model_selection import train_test_split
import joblib

# Define paths
S1_DIR = 'data/input/S1'
S2_DIR = 'data/input/S2'
LABELS_DIR = 'data/input/labels'
OUTPUT_DIR = 'data/processed'

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Starting data preparation...")

# Get all file names
s1_files = sorted([f for f in os.listdir(S1_DIR) if f.endswith('.tif')])
print(f"Found {len(s1_files)} files to process")

# Initialize lists for data
X_s1_list = []
X_s2_list = []
y_list = []

# Process each file
for i, filename in enumerate(s1_files):

    if i % 50 == 0:
        print(f"Processing file {i+1}/{len(s1_files)}")

    # Extract ID from filename (e.g., "Bolivia_103757")
    file_id = filename.replace('_S1Hand.tif', '')

    # Read S1 image
    s1_path = os.path.join(S1_DIR, filename)
    with rasterio.open(s1_path) as src:
        s1_data = src.read()  # Shape: (bands, height, width)

    # Read S2 image
    s2_filename = f"{file_id}_S2Hand.tif"
    s2_path = os.path.join(S2_DIR, s2_filename)
    with rasterio.open(s2_path) as src:
        s2_data = src.read()

    # Read Label
    label_filename = f"{file_id}_LabelHand.tif"
    label_path = os.path.join(LABELS_DIR, label_filename)
    with rasterio.open(label_path) as src:
        label_data = src.read(1)  # Read first band only

    # Flatten and combine
    X_s1_list.append(s1_data.reshape(s1_data.shape[0], -1).T)  # (pixels, bands)
    X_s2_list.append(s2_data.reshape(s2_data.shape[0], -1).T)
    y_list.append(label_data.flatten())

print("Concatenating all data...")

# Concatenate all samples
X_s1 = np.vstack(X_s1_list)
X_s2 = np.vstack(X_s2_list)
y = np.hstack(y_list)

# Combine S1 and S2 features
X = np.hstack([X_s1, X_s2])

print(f"Final dataset shape: X={X.shape}, y={y.shape}")

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Train set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Save processed data
print("Saving processed data...")
np.save(os.path.join(OUTPUT_DIR, 'X_train.npy'), X_train)
np.save(os.path.join(OUTPUT_DIR, 'X_test.npy'), X_test)
np.save(os.path.join(OUTPUT_DIR, 'y_train.npy'), y_train)
np.save(os.path.join(OUTPUT_DIR, 'y_test.npy'), y_test)

print("Data preparation complete!")
print(f"Files saved to {OUTPUT_DIR}/")
