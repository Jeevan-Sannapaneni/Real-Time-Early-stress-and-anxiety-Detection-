from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
from tensorflow.keras.models import load_model
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Load model
def load_model_safe():
    """Load model with proper error handling"""
    try:
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'wesad_final_model.h5')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        
        # Try loading with compile=False
        print(f"📥 Loading model from: {model_path}")
        loaded_model = load_model(model_path, compile=False)
        print(f"✅ Model loaded successfully!")
        return loaded_model
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)[:200]}")
        print(f"\n🔧 SOLUTION: Run these commands:")
        print(f"   pip uninstall tensorflow -y")
        print(f"   pip install tensorflow==2.16.1 numpy==1.24.3 h5py==3.10.0")
        print(f"\nℹ️ Your model uses Keras 3 format (newer)")
        print(f"   TensorFlow 2.16+ includes full Keras 3 support")
        return None

model = load_model_safe()

# Routes
def create_demo_users():
    """Create demo users if they don't exist"""
    demo_users = [
        {'username': 'demo', 'email': 'demo@example.com', 'password': 'demo123'},
        {'username': 'test', 'email': 'test@example.com', 'password': 'test123'},
        {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin123'}
    ]
    
    for user_data in demo_users:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(username=user_data['username'], email=user_data['email'])
            user.set_password(user_data['password'])
            db.session.add(user)
    
    db.session.commit()
    print("✓ Demo users created successfully!")
    print("\n" + "="*50)
    print("DEMO LOGIN CREDENTIALS")
    print("="*50)
    for user_data in demo_users:
        print(f"Username: {user_data['username']} | Password: {user_data['password']}")
    print("="*50 + "\n")

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match'}), 400

        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already exists'}), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Registration successful! Please login.'}), 201

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'success': True, 'message': 'Login successful'}), 200
        
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/samples')
def samples():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('samples.html', username=session.get('username'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    if model is None:
        return jsonify({'success': False, 'message': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        input_data = data.get('input_data')
        
        # Model expects shape (1, 120, 3) - 120 timesteps with 3 features
        if len(input_data) != 360:  # 120 * 3
            return jsonify({
                'success': False, 
                'message': f'Expected 360 values (120 timesteps × 3 features), got {len(input_data)}'
            }), 400
        
        # Reshape to (1, 120, 3)
        input_array = np.array(input_data, dtype=np.float32).reshape(1, 120, 3)
        
        # Make prediction
        prediction = model.predict(input_array, verbose=0)
        confidence = float(prediction[0][0])
        # Model logic: LOW value (< 0.5) = Normal, HIGH value (> 0.5) = Stressed
        predicted_class = 1 if confidence > 0.5 else 0
        
        # Map classes: 0 = Normal, 1 = Stressed
        class_names = {0: 'Normal', 1: 'Stressed'}
        # Calculate stress_score: direct confidence (higher confidence = higher stress)
        stress_score = round(confidence * 100, 2)

        return jsonify({
            'success': True,
            'prediction': int(predicted_class),
            'prediction_label': class_names[predicted_class],
            'confidence': round(confidence * 100, 2),
            'stress_score': stress_score
        }), 200

    except ValueError as e:
        return jsonify({'success': False, 'message': f'Invalid input format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('reports.html', username=session.get('username'))

@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('about.html', username=session.get('username'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_demo_users()
    print("\n" + "="*50)
    print("🚀 Flask App Started Successfully!")
    print("="*50)
    print("📱 Frontend Access: http://localhost:5000")
    print("🔓 Login Page: http://localhost:5000/login")
    print("📝 Register Page: http://localhost:5000/register")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
