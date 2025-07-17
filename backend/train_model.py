import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import joblib
import os

def train_model():
    print("Starting model training...")
    
    # --- File Paths ---
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, 'data', 'orbital_data.csv')
    models_dir = os.path.join(base_dir, 'models')
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    # --- Load Data ---
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        print("Please run `generate_data.py` first.")
        return

    # --- Feature and Target Selection ---
    features = ['x', 'y', 'vx', 'vy']
    targets = ['next_x', 'next_y', 'next_vx', 'next_vy']

    X = df[features]
    y = df[targets]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Scaling ---
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Data scaled.")

    # --- Model Training ---
    # MLPRegressor is a Neural Network, great for complex non-linear problems
    model = MLPRegressor(
        hidden_layer_sizes=(128, 128, 64),
        activation='relu',
        solver='adam',
        max_iter=500,
        random_state=42,
        early_stopping=True, # Stop training when validation score is not improving
        verbose=True
    )

    print("Training MLP Regressor...")
    model.fit(X_train_scaled, y_train)

    # --- Evaluation ---
    score = model.score(X_test_scaled, y_test)
    print(f"\nModel training complete. R^2 score on test set: {score:.4f}")

    # --- Save Model and Scaler ---
    joblib.dump(model, os.path.join(models_dir, 'orbital_model.pkl'))
    joblib.dump(scaler, os.path.join(models_dir, 'data_scaler.pkl'))
    print(f"Model and scaler saved to {models_dir}")

if __name__ == "__main__":
    train_model()
