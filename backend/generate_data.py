import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import os

# --- Constants ---
G = 6.67430e-11  # Gravitational constant
M_CENTRAL = 1.989e30  # Mass of a central body like the Sun
DT = 3600 * 24 # Time step (1 day in seconds)
N_STEPS = 365 * 2 # Number of steps to simulate (2 years)
N_SIMULATIONS = 200 # Number of different orbits to generate

# --- Physics Model ---
def ode_system(t, state, M):
    """Defines the differential equations for the two-body problem."""
    x, y, vx, vy = state
    r = np.sqrt(x**2 + y**2)
    
    # Acceleration components
    ax = -G * M * x / r**3
    ay = -G * M * y / r**3
    
    return [vx, vy, ax, ay]

# --- Main Data Generation Logic ---
def generate_data():
    print("Starting data generation...")
    all_trajectories = []

    for i in range(N_SIMULATIONS):
        # Random initial conditions for stable-ish orbits
        r0 = np.random.uniform(0.5e11, 2.5e11) # Initial distance (meters)
        angle0 = np.random.uniform(0, 2 * np.pi) # Initial angle
        x0 = r0 * np.cos(angle0)
        y0 = r0 * np.sin(angle0)

        # Velocity for a circular orbit, with some noise
        v_circ = np.sqrt(G * M_CENTRAL / r0) * np.random.uniform(0.8, 1.2)
        vx0 = -v_circ * np.sin(angle0)
        vy0 = v_circ * np.cos(angle0)
        
        initial_state = [x0, y0, vx0, vy0]
        t_span = [0, N_STEPS * DT]
        t_eval = np.linspace(t_span[0], t_span[1], N_STEPS)

        # Solve the ODE
        sol = solve_ivp(
            ode_system, 
            t_span, 
            initial_state, 
            args=(M_CENTRAL,), 
            t_eval=t_eval,
            method='RK45'
        )

        # Process the results into (current_state, next_state) pairs
        states = sol.y.T
        for j in range(len(states) - 1):
            current_state = states[j]
            next_state = states[j+1]
            all_trajectories.append({
                'x': current_state[0], 'y': current_state[1], 'vx': current_state[2], 'vy': current_state[3],
                'next_x': next_state[0], 'next_y': next_state[1], 'next_vx': next_state[2], 'next_vy': next_state[3]
            })
        print(f"  Generated simulation {i+1}/{N_SIMULATIONS}")

    df = pd.DataFrame(all_trajectories)
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    output_path = os.path.join(data_dir, 'orbital_data.csv')
    df.to_csv(output_path, index=False)
    print(f"\nData generation complete. Saved to {output_path}")

if __name__ == "__main__":
    generate_data()
