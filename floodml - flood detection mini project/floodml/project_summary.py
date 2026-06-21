import joblib
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load model
model = joblib.load('models/flood_model.pkl')

# Load test data
y_test = np.load('data/processed/y_test.npy')
X_test = np.load('data/processed/X_test.npy')

# Make predictions
y_pred = model.predict(X_test)

# Print results
print("=" * 60)
print("FLOOD DETECTION PROJECT - RESULTS SUMMARY")
print("=" * 60)

print("\nModel: Random Forest Classifier")
print(f"Number of trees: {model.n_estimators}")

print(f"Test samples: {len(X_test)}")
print("\nPerformance Metrics:")

print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"  Precision: {precision_score(y_test, y_pred, average='weighted', zero_division=0):.4f}")
print(f"  Recall:    {recall_score(y_test, y_pred, average='weighted', zero_division=0):.4f}")
print(f"  F1-Score:  {f1_score(y_test, y_pred, average='weighted', zero_division=0):.4f}")

print("\n" + "=" * 60)
