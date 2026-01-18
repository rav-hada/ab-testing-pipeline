import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# CONFIGURATION
NUM_ROWS = 500000
START_DATE = datetime(2024, 1, 1)

def generate_data():
    print(f"Generating {NUM_ROWS} rows of synthetic AdTech data...")
    
    # 1. User IDs (Simulate repeat users)
    # We create a pool of 100k unique users, so some appear multiple times
    user_ids = np.random.randint(100000, 200000, size=NUM_ROWS)
    
    # 2. Experiment Groups (A/B)
    # 50/50 split between Control (A) and Treatment (B)
    groups = np.random.choice(['Control', 'Treatment'], size=NUM_ROWS)
    
    # 3. Device Types (Desktop vs Mobile)
    devices = np.random.choice(['Mobile', 'Desktop'], size=NUM_ROWS, p=[0.7, 0.3])
    
    # 4. Generate Clicks (The "Effect")
    # Logic: Treatment group has a slightly higher click rate (CTR)
    # Control CTR: 15% | Treatment CTR: 18%
    click_probs = np.where(groups == 'Treatment', 0.18, 0.15)
    clicks = (np.random.rand(NUM_ROWS) < click_probs).astype(int)
    
    # 5. Generate Timestamps
    # Spread over 30 days
    time_deltas = np.random.randint(0, 30*24*60*60, size=NUM_ROWS) # Seconds in 30 days
    timestamps = [START_DATE + timedelta(seconds=int(d)) for d in time_deltas]
    
    # Create DataFrame
    df = pd.DataFrame({
        'user_id': user_ids,
        'timestamp': timestamps,
        'experiment_group': groups,
        'device_type': devices,
        'clicked': clicks
    })
    
    # Save to CSV
    filename = 'ad_clicks.csv'
    df.to_csv(filename, index=False)
    print(f"Success! Data saved to {filename} with {len(df)} rows.")

if __name__ == "__main__":
    generate_data()