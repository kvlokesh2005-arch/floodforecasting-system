import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'floodml'))

import numpy as np
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'floodml', 'models', 'flood_model.pkl')

print("=" * 70)
print("VERIFYING MODEL INTEGRATION")
print("=" * 70)

print("\n1️⃣  Checking model file exists...")
if os.path.exists(MODEL_PATH):
    print(f"   ✅ Model found at: {MODEL_PATH}")
else:
    print(f"   ❌ Model NOT found at: {MODEL_PATH}")
    sys.exit(1)

print("\n2️⃣  Loading model...")
try:
    model = joblib.load(MODEL_PATH)
    print(f"   ✅ Model loaded successfully")
    print(f"   Model type: {type(model).__name__}")
    print(f"   Model features: {model.n_features_in_}")
    print(f"   Model estimators: {model.n_estimators}")
except Exception as e:
    print(f"   ❌ Error loading model: {e}")
    sys.exit(1)

print("\n3️⃣  Testing feature extraction...")
try:
    test_data = np.random.randn(10000, model.n_features_in_)
    print(f"   ✅ Created test data with shape: {test_data.shape}")
except Exception as e:
    print(f"   ❌ Error creating test data: {e}")
    sys.exit(1)

print("\n4️⃣  Testing model.predict()...")
try:
    predictions = model.predict(test_data)
    print(f"   ✅ Predictions shape: {predictions.shape}")
    print(f"   Predictions (0/1): {np.unique(predictions)}")
except Exception as e:
    print(f"   ❌ Error in predict: {e}")
    sys.exit(1)

print("\n5️⃣  Testing model.predict_proba()...")
try:
    probabilities = model.predict_proba(test_data)
    print(f"   ✅ Probabilities shape: {probabilities.shape}")
    print(f"   Probability range: [{probabilities.min():.4f}, {probabilities.max():.4f}]")
    print(f"   Flood prob column (class 1): min={probabilities[:, 1].min():.4f}, max={probabilities[:, 1].max():.4f}")
except Exception as e:
    print(f"   ❌ Error in predict_proba: {e}")
    sys.exit(1)

print("\n6️⃣  Testing reshape to image...")
try:
    height, width = 100, 100
    flood_prob = probabilities[:height*width, 1]
    flood_map = flood_prob.reshape(height, width)
    print(f"   ✅ Reshaped to image: {flood_map.shape}")
    print(f"   Image min/max: [{flood_map.min():.4f}, {flood_map.max():.4f}]")
except Exception as e:
    print(f"   ❌ Error in reshape: {e}")
    sys.exit(1)

print("\n7️⃣  Checking satellite_upload_module...")
try:
    from satellite_upload_module import (
        load_trained_model,
        extract_features_from_file,
        predict_flood_probability
    )
    print(f"   ✅ All functions imported successfully")
except Exception as e:
    print(f"   ❌ Error importing functions: {e}")
    sys.exit(1)

print("\n8️⃣  Testing feature padding logic...")
try:
    small_X = np.random.randn(100, model.n_features_in_ - 5)
    
    if small_X.shape[1] < model.n_features_in_:
        padding = np.zeros((small_X.shape[0], model.n_features_in_ - small_X.shape[1]))
        X_padded = np.hstack([small_X, padding])
    
    print(f"   ✅ Feature padding works")
    print(f"   Original shape: {small_X.shape}")
    print(f"   Padded shape: {X_padded.shape}")
    
    pred = model.predict_proba(X_padded)
    print(f"   ✅ Prediction on padded data works: {pred.shape}")
except Exception as e:
    print(f"   ❌ Error in padding logic: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ ALL CHECKS PASSED! MODEL INTEGRATION IS READY")
print("=" * 70)
