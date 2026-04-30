"""
Fix for TensorFlow/Keras Model Loading Issues
Converts model from H5 to SavedModel format or fixes compatibility issues
"""

import os
import sys
import json
import shutil
import tensorflow as tf
from tensorflow import keras

def try_load_with_safe_mode():
    """Attempt to load model with safe mode to handle version mismatches"""
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'wesad_final_model.h5')
    
    print(f"🔧 Attempting to fix model: {model_path}\n")
    
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
    
    # Create backup
    backup_path = model_path + '.backup_fix'
    if not os.path.exists(model_path + '.backup'):
        shutil.copy2(model_path, model_path + '.backup')
        print(f"✓ Backup created: {model_path}.backup\n")
    
    try:
        print("📥 Attempting to load model...")
        
        # Try loading with compile=False first
        print("  • Trying with compile=False...")
        model = keras.models.load_model(model_path, compile=False)
        print("  ✓ Model loaded with compile=False\n")
        
        # Compile with default settings
        print("  • Compiling model...")
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        print("  ✓ Model compiled successfully\n")
        
        # Save in SavedModel format (TF 2.x native format)
        saved_model_path = os.path.join(os.path.dirname(__file__), 'models', 'wesad_final_model')
        print(f"💾 Saving to SavedModel format: {saved_model_path}")
        model.save(saved_model_path, save_format='tf')
        print(f"✓ Model saved successfully\n")
        
        # Update app.py to use SavedModel
        update_app_to_use_saved_model()
        
        print("="*60)
        print("✅ MODEL FIX SUCCESSFUL!")
        print("="*60)
        print(f"Original H5 model: {model_path} (backup: {model_path}.backup)")
        print(f"New SavedModel format: {saved_model_path}")
        print("\n📝 app.py has been updated to use the SavedModel format")
        print("🚀 Ready to run: python app.py\n")
        return True
        
    except Exception as e:
        print(f"❌ Error during model loading: {str(e)}\n")
        print("Troubleshooting steps:")
        print("1. Check TensorFlow version compatibility")
        print("2. Ensure h5py is installed: pip install h5py")
        print("3. Try with a fresh model file")
        print("4. Contact model developer\n")
        return False

def update_app_to_use_saved_model():
    """Update app.py to load SavedModel instead of H5"""
    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    
    try:
        with open(app_path, 'r') as f:
            app_content = f.read()
        
        # Replace H5 loading with SavedModel loading
        old_load = """    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'wesad_final_model.h5')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    
    # Load model with compile=False to skip compilation step
    model = load_model(model_path, compile=False)"""
        
        new_load = """    # Try SavedModel format first (recommended), fallback to H5
    saved_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'wesad_final_model')
    h5_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'wesad_final_model.h5')
    
    if os.path.exists(saved_model_path):
        # Load SavedModel format
        model_path = saved_model_path
        model = keras.models.load_model(model_path)
    elif os.path.exists(h5_model_path):
        # Load H5 format as fallback
        model_path = h5_model_path
        model = load_model(model_path, compile=False)
    else:
        raise FileNotFoundError(f"Model not found at: {saved_model_path} or {h5_model_path}")"""
        
        if old_load in app_content:
            app_content = app_content.replace(old_load, new_load)
            with open(app_path, 'w') as f:
                f.write(app_content)
            print("✓ app.py updated to use SavedModel format\n")
        else:
            print("⚠️  Could not auto-update app.py - please update manually\n")
    except Exception as e:
        print(f"⚠️  Could not update app.py: {str(e)}\n")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔧 WESAD Model Compatibility Fixer")
    print("="*60 + "\n")
    
    success = try_load_with_safe_mode()
    sys.exit(0 if success else 1)
