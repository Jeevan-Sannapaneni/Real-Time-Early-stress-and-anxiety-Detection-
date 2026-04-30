"""
Sample Data Generator for WESAD Stress Detection Model
Generates 360 random sensor values (120 timesteps × 3 features)
Use this to test the model predictions
"""

import random
import numpy as np

def generate_sample_data(stressed=False):
    """
    Generate sample sensor data for testing
    
    Args:
        stressed (bool): If True, generate data patterns similar to stressed state
                        If False, generate normal state data
    
    Returns:
        list: 360 comma-separated sensor values
    """
    
    if stressed:
        # Generate data with higher variance (stressed pattern)
        base_values = []
        for _ in range(120):
            # 3 features (e.g., accelerometer X, Y, Z)
            x = np.random.normal(2.0, 1.5)  # Higher mean and variance
            y = np.random.normal(2.0, 1.5)
            z = np.random.normal(9.5, 1.5)  # Gravity + higher variation
            base_values.extend([round(x, 2), round(y, 2), round(z, 2)])
    else:
        # Generate data with lower variance (normal pattern)
        base_values = []
        for _ in range(120):
            # 3 features (e.g., accelerometer X, Y, Z)
            x = np.random.normal(0.2, 0.3)  # Lower mean and variance
            y = np.random.normal(0.2, 0.3)
            z = np.random.normal(9.8, 0.5)  # Gravity mostly stable
            base_values.extend([round(x, 2), round(y, 2), round(z, 2)])
    
    return ', '.join(str(v) for v in base_values)


def generate_custom_data(mean_x=0.2, mean_y=0.2, mean_z=9.8, std_dev=0.3):
    """
    Generate custom sensor data with specified parameters
    
    Args:
        mean_x, mean_y, mean_z (float): Mean values for each feature
        std_dev (float): Standard deviation
    
    Returns:
        list: 360 comma-separated sensor values
    """
    base_values = []
    for _ in range(120):
        x = np.random.normal(mean_x, std_dev)
        y = np.random.normal(mean_y, std_dev)
        z = np.random.normal(mean_z, std_dev)
        base_values.extend([round(x, 2), round(y, 2), round(z, 2)])
    
    return ', '.join(str(v) for v in base_values)


if __name__ == "__main__":
    print("WESAD Stress Detection - Sample Data Generator\n")
    print("=" * 60)
    
    # Generate normal state data
    print("\n🟢 NORMAL STATE DATA (Copy & Paste to Test):")
    print("-" * 60)
    normal_data = generate_sample_data(stressed=False)
    print(normal_data[:100] + "...")  # Print first 100 chars
    print("\n✓ Full data has 360 values (120 timesteps × 3 features)")
    
    # Generate stressed state data
    print("\n\n🔴 STRESSED STATE DATA (Copy & Paste to Test):")
    print("-" * 60)
    stressed_data = generate_sample_data(stressed=True)
    print(stressed_data[:100] + "...")  # Print first 100 chars
    print("\n✓ Full data has 360 values (120 timesteps × 3 features)")
    
    print("\n" + "=" * 60)
    print("\n📝 USAGE:")
    print("1. Copy either the NORMAL or STRESSED data above")
    print("2. Go to http://localhost:5000/dashboard")
    print("3. Paste the data in the input field")
    print("4. Click 'Analyze Stress Level'")
    print("5. View the prediction results")
