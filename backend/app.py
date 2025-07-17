from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
from scipy.integrate import solve_ivp
import os

# Import the physics model from our data generator script
from generate_data import ode_system, G, M_CENTRAL, DT

# --- App Setup ---
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app) # Allow cross-origin requests

# --- Load Model and Scaler ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'orbital_model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'data_scaler.pkl')

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Model and scaler loaded successfully.")
except FileNotFoundError:
    print("Error: Model or scaler not found. Please run train_model.py first.")
    model = None
    scaler = None

# --- API Routes ---
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not scaler:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.json
    initial_state = np.array([data['x'], data['y'], data['vx'], data['vy']])
    n_steps = data.get('steps', 365)

    # 1. Generate ML Trajectory
    ml_path = [initial_state[:2].tolist()]
    current_state = initial_state.reshape(1, -1)
    
    for _ in range(n_steps):
        scaled_state = scaler.transform(current_state)
        next_state = model.predict(scaled_state)
        ml_path.append(next_state[0][:2].tolist())
        current_state = next_state

    # 2. Generate Physics Trajectory (Ground Truth)
    t_span = [0, n_steps * DT]
    t_eval = np.linspace(t_span[0], t_span[1], n_steps + 1)
    sol = solve_ivp(
        ode_system,
        t_span,
        initial_state,
        args=(M_CENTRAL,),
        t_eval=t_eval,
        method='RK45'
    )
    physics_path = sol.y.T[:, :2].tolist()

    return jsonify({
        'ml_path': ml_path,
        'physics_path': physics_path
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
