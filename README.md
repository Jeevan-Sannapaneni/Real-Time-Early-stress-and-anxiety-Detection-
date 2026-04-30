# ML Model Web App with Login & Register

This is a complete web application with user authentication and ML model prediction capabilities.

## Project Structure

```
nandini_project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── models/
│   ├── model.weights.h5
│   └── wesad_final_model.h5
├── templates/
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── dashboard.html    # Main dashboard with predictions
└── users.db              # SQLite database (created automatically)
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The app will start on `http://localhost:5000`

### 3. Access the App

- **Home Page:** http://localhost:5000/
- **Register:** Create a new account at http://localhost:5000/register
- **Login:** Log in with your credentials at http://localhost:5000/login
- **Dashboard:** After login, you can make predictions at http://localhost:5000/dashboard

## Features

### Authentication
- User registration with email validation
- Secure login with password hashing
- Session management
- Logout functionality

### Model Prediction
- Load and run ML model (wesad_final_model.h5)
- Input feature values via web interface
- Get predictions with confidence scores
- View probability distributions

## How to Use

1. **Register:** Create a new account with username, email, and password
2. **Login:** Log in with your credentials
3. **Make Predictions:** 
   - Enter feature values separated by commas
   - Click "Predict" button
   - View results including predicted class and confidence score

## Customization

### Change Secret Key
Edit `app.py` and change the `SECRET_KEY`:
```python
app.config['SECRET_KEY'] = 'your-custom-secret-key'
```

### Modify Model Path
If your model is in a different location, update in `app.py`:
```python
model = load_model('path/to/your/model.h5')
```

### Database
- SQLite database is created automatically in the project folder as `users.db`
- To reset: Simply delete `users.db` and restart the app

## Troubleshooting

### Model Not Loading
**Solution:**
1. **Verify model file exists:**
   - Check that `models/wesad_final_model.h5` is in your project folder
   - File size should be several MB (not corrupted)

2. **Check TensorFlow/Keras compatibility:**
   - Run: `pip install --upgrade tensorflow`
   - Current requirement: `tensorflow==2.12.0`
   - Try: `pip install tensorflow==2.12.0 --force-reinstall`

3. **Install missing dependencies:**
   ```bash
   pip install h5py
   pip install -r requirements.txt
   ```

4. **Check console output:**
   - Look for specific error messages when starting `python app.py`
   - Common errors:
     - `FileNotFoundError`: Model file is missing or path is incorrect
     - `ImportError`: Missing tensorflow or h5py
     - `ValueError`: Model file is corrupted

5. **Regenerate if needed:**
   - Ensure you copied the model file from the original PC
   - File should be: `models/wesad_final_model.h5` (not in a subfolder)

### Port Already in Use
If port 5000 is in use, edit `app.py`:
```python
app.run(debug=True, port=5001)  # Change to different port
```

### Database Errors
- Delete `users.db` and restart the application
- The database will be recreated automatically

## Production Deployment

For production:
1. Change `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Use a proper database (PostgreSQL instead of SQLite)
4. Set a strong `SECRET_KEY`
5. Use HTTPS

```bash
pip install gunicorn
gunicorn app:app
```

## Technologies Used

- **Backend:** Flask (Python)
- **Database:** SQLAlchemy with SQLite
- **ML Framework:** TensorFlow/Keras
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Werkzeug (password hashing)

---

Questions or issues? Check the error messages in the console for debugging information.
