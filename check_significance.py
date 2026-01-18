import pandas as pd
from sqlalchemy import create_engine
from scipy.stats import norm

def check_results():
    # 1. Connect to the Data Warehouse (Directly)
    db_url = 'postgresql://user:password@localhost:5432/warehouse'
    engine = create_engine(db_url)
    
    # 2. Get the Aggregated Data
    print("Fetching A/B Test Results from dbt mart...")
    query = "SELECT * FROM mart_ab_test"
    df = pd.read_sql(query, engine)
    
    # 3. Separate Control vs Treatment
    control = df[df['experiment_group'] == 'Control'].iloc[0]
    treatment = df[df['experiment_group'] == 'Treatment'].iloc[0]
    
    print(f"\n--- RESULTS ---")
    print(f"Control (A):   {control['conversion_rate']*100:.2f}% (N={control['total_users']})")
    print(f"Treatment (B): {treatment['conversion_rate']*100:.2f}% (N={treatment['total_users']})")
    
    # 4. Calculate Z-Score and P-Value
    # Formula: (p_treatment - p_control) / sqrt(SE_treatment^2 + SE_control^2)
    uplift = treatment['conversion_rate'] - control['conversion_rate']
    pooled_se = (control['std_error']**2 + treatment['std_error']**2)**0.5
    
    z_score = uplift / pooled_se
    p_value = (1 - norm.cdf(abs(z_score))) * 2  # Two-tailed test
    
    print(f"\n--- STATISTICS ---")
    print(f"Uplift:        {uplift*100:.2f}% points")
    print(f"P-Value:       {p_value:.5f}")
    
    # 5. The Decision
    if p_value < 0.05:
        print("✅ RESULT: SIGNIFICANT! Roll out the new feature.")
    else:
        print("❌ RESULT: NOT SIGNIFICANT. Do not launch.")

if __name__ == "__main__":
    check_results()