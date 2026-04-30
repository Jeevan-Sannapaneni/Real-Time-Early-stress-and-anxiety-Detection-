# Testing Guide - Quick Start

## 🚀 Quick Access Links

**App URL:** http://localhost:5000

### Demo Credentials:
```
Username: demo     | Password: demo123
Username: test     | Password: test123
Username: admin    | Password: admin123
```

---

## 📊 Sample Test Data (Copy & Paste)

### 🟢 NORMAL STATE DATA
Copy this and paste into the dashboard to test NORMAL (Low Stress) prediction:

```
0.32, -0.15, 10.02, 0.18, 0.45, 9.95, -0.22, -0.08, 10.15, 0.41, -0.28, 9.88, 0.05, 0.12, 10.08, -0.33, 0.31, 9.92, 0.24, -0.19, 10.12, 0.38, 0.02, 9.85, -0.11, -0.42, 10.04, 0.29, 0.15, 9.98, 0.14, -0.25, 10.06, -0.27, 0.35, 9.89, 0.31, -0.05, 10.01, 0.22, 0.28, 9.93, -0.18, -0.14, 10.09, 0.35, -0.31, 9.87, 0.19, 0.42, 10.05, 0.28, 0.08, 9.96, -0.12, -0.38, 10.11, 0.33, 0.19, 9.91, 0.26, -0.22, 10.03, -0.29, 0.34, 9.94, 0.37, -0.09, 10.07, 0.21, 0.32, 9.86, -0.14, -0.18, 10.13, 0.32, 0.26, 9.99, 0.18, -0.35, 10.02, 0.31, 0.11, 9.97, -0.24, 0.39, 10.08, 0.25, 0.21, 9.90, 0.29, -0.16, 10.04, -0.32, 0.33, 9.95, 0.34, 0.22, 10.06, 0.17, -0.27, 9.88, 0.36, 0.04, 10.10, 0.23, 0.40, 9.92, 0.27, -0.13, 10.05, 0.30, 0.17, 9.98, -0.20, -0.36, 10.09, 0.35, -0.03, 9.87, 0.19, 0.43, 10.02, 0.28, 0.09, 9.96
```

**Expected Result:** 🟢 NORMAL (Stress Score: Low)

---

### 🔴 STRESSED STATE DATA
Copy this and paste into the dashboard to test STRESSED (High Stress) prediction:

```
2.15, 1.85, 10.45, 3.22, 2.41, 9.65, 1.82, 1.72, 11.25, 2.91, 2.15, 8.95, 1.65, 3.28, 10.15, 2.45, 1.92, 9.45, 3.18, 2.38, 11.08, 2.72, 1.85, 8.82, 1.95, 3.45, 10.32, 2.38, 2.22, 9.75, 1.72, 1.65, 11.15, 3.15, 2.58, 9.25, 2.35, 1.98, 10.05, 1.85, 3.32, 9.95, 2.45, 2.12, 10.85, 1.62, 1.78, 8.75, 3.28, 2.48, 10.45, 2.15, 1.92, 9.35, 1.95, 3.18, 11.02, 2.72, 2.35, 9.58, 1.85, 1.68, 10.28, 3.12, 2.52, 9.12, 2.28, 1.88, 10.92, 1.75, 3.42, 9.42, 2.58, 2.18, 10.62, 1.68, 1.82, 8.88, 3.22, 2.65, 10.15, 2.35, 1.95, 9.68, 1.92, 3.38, 10.95, 2.48, 2.28, 9.05, 1.82, 1.72, 10.42, 3.05, 2.55, 9.48, 2.18, 1.85, 10.78, 1.95, 3.25, 9.22, 2.42, 2.12, 10.32, 1.88, 1.98, 8.98, 3.18, 2.38, 10.68
```

**Expected Result:** 🔴 STRESSED (Stress Score: High)

---

## 🧪 How to Test

### Method 1: Using Sample Data Page (Recommended)
1. Go to http://localhost:5000/dashboard
2. Click "📊 Sample Data" button in navbar
3. Click "📋 Copy Data" on any sample
4. Go back to Dashboard
5. Data auto-loads, click "⚡ Analyze Stress Level"
6. View results

### Method 2: Manual Copy-Paste
1. Login at http://localhost:5000/login
2. Go to Dashboard
3. Copy sample data from above
4. Paste in the input field
5. Click "⚡ Analyze Stress Level"
6. View results

### Method 3: Using Python Script
```bash
cd c:\Users\tb266\nandini_project
python sample_data_generator.py
```

---

## ✅ What to Expect

### Normal Data:
- **Values around 0.0 for X, Y**
- **Values around 9.8 for Z (gravity)**
- **Low variance**
- **Result:** 🟢 NORMAL with stress score < 50%

### Stressed Data:
- **Values around 2.0 for X, Y**
- **Variable Z values (8-11 range)**
- **High variance**
- **Result:** 🔴 STRESSED with stress score > 50%

---

## 🎯 Navigation

- **Login:** http://localhost:5000/login
- **Dashboard:** http://localhost:5000/dashboard
- **Sample Data:** http://localhost:5000/samples
- **Logout:** http://localhost:5000/logout

---

## 🐛 Troubleshooting

**Error: "Expected 360 values"**
- Make sure you copied all the data
- Count should be 120 timesteps × 3 features = 360 values

**Model not loading?**
- Check that `models/wesad_final_model.h5` exists
- Restart the Flask app

**Still Running?**
- Check terminal for app status
- Should see: "Running on http://127.0.0.1:5000"

---

Enjoy testing! 🚀
