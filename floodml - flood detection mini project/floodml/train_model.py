import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

# Define paths
DATA_DIR = 'data/processed'
MODEL_DIR = 'models'

# Create model directory
os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading processed data...")

# Load processed dataset
X_train = np.load(os.path.join(DATA_DIR, 'X_train.npy'))
X_test = np.load(os.path.join(DATA_DIR, 'X_test.npy'))
y_train = np.load(os.path.join(DATA_DIR, 'y_train.npy'))
y_test = np.load(os.path.join(DATA_DIR, 'y_test.npy'))

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# ------------------------------------------------------
#  DOWNSAMPLING TO AVOID MEMORY CRASH (IMPORTANT)
# ------------------------------------------------------
MAX_SAMPLES = 2_000_000  # Use 2 million samples

if len(X_train) > MAX_SAMPLES:
    print(f"\nReducing dataset from {len(X_train)} to {MAX_SAMPLES} samples...")
    idx = np.random.choice(len(X_train), MAX_SAMPLES, replace=False)
    X_train = X_train[idx]
    y_train = y_train[idx]

print("Final training set after downsampling:", X_train.shape)
# ------------------------------------------------------

# Initialize a smaller Random Forest (Low RAM mode)
print("\nInitializing Smaller Random Forest Classifier (Low RAM Mode)...")

model = RandomForestClassifier(
    n_estimators=20,       # Fewer trees to reduce memory
    max_depth=10,         # Smaller trees
    min_samples_leaf=10,  # Prevent over-splitting
    max_features="sqrt",  # Reduce feature usage
    n_jobs=4,             # Limit CPU threads to reduce RAM use
    random_state=42,
    verbose=2
)

# Train the model
print("\nTraining model... (should take 5–15 minutes)")
model.fit(X_train, y_train)
print("\nTraining complete!")

# Evaluate the model
print("\nEvaluating model...")
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save trained model
model_path = os.path.join(MODEL_DIR, 'flood_model.pkl')
print(f"\nSaving model to {model_path}...")
joblib.dump(model, model_path)

print("\nModel training and saving complete!")
