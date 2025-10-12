# Import statements
import numpy as np
import pandas as pd
import os

# Single panel parameters
Voc = 21.9
Isc = 5.56
Pmax = 100
Vmpp = 18
Impp = Pmax / Vmpp
a = np.log(1 - Impp/Isc) / np.log(Vmpp/Voc)
num_panels = 2

# Function for calculating current as function of voltage for single panel
def I_of_V(V):
    V = np.atleast_1d(V)
    I = Isc * (1 - (V / Voc)**a)
    I = np.where(V < 0, Isc, I)
    I = np.where(V > Voc, 0, I)
    return I if len(I) > 1 else I[0]

# Function for calculating power as function of voltage for single panel
def P_of_V(V):
    return V * I_of_V(V)

# Function for generating voltage, current, and power data
def generate_data():
    data = []
    # Start from maximum power and work towards lower power (higher voltage, lower current)
    target_powers = range(int(Pmax * num_panels), 0, -1)  
    
    # Generate dense voltage points from Vmpp to Voc
    V_values = np.linspace(Vmpp, Voc, 5000)
    
    # Calculate power for each voltage
    P_lookup = []
    for V_single in V_values:
        I_single = I_of_V(V_single)
        I_total = I_single * num_panels
        P_total = V_single * I_total
        P_lookup.append(P_total)
    
    P_lookup = np.array(P_lookup)
    
    # For each target power, find closest voltage
    for P_target in target_powers:
        idx = np.argmin(np.abs(P_lookup - P_target))
        V_single = V_values[idx]
        I_single = I_of_V(V_single)
        I_total = I_single * num_panels
        P_total = V_single * I_total
        
        data.append((P_target, round(V_single, 3), round(I_total, 3)))
    
    return data

# Function for creating and saving CSV files
def save_csv_files(df):
    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Save main CSV
    csv_path = os.path.join(output_dir, "solar_pannel_parallel_output_calculations.csv")
    df.to_csv(csv_path, index=False)
    print(f"Main CSV saved to: {csv_path}")
    
    # Check for currents below 25mA (0.025 A)
    low_current_df = df[df["Current (A)"] < 0.025]
    
    # Save second CSV if low current values found
    if not low_current_df.empty:
        no_charge_csv = os.path.join(output_dir, "Power_resulting_in_no_charging.csv")
        low_current_df.to_csv(no_charge_csv, index=False)
        print(f"No charging CSV saved to: {no_charge_csv}")
        print(f"Found {len(low_current_df)} power levels with current < 25mA")
        print(f"Power range with insufficient current: {low_current_df['Power (W)'].min()}W - {low_current_df['Power (W)'].max()}W")
    else:
        print("No power levels found with current below 25mA")
    
    return csv_path

def main():
    # Generate data by sweeping voltage
    data = generate_data()
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=["Power (W)", "Voltage (V)", "Current (A)"])
    
    # Save CSV files and check for low current values
    save_csv_files(df)

if __name__ == "__main__":
    main()
