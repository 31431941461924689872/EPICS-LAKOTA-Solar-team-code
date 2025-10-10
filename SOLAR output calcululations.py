# Import statements
import numpy as np
import pandas as pd

# Single panel parameters
Voc = 21.9
Isc = 6.13
a = 2
Pmax = 100
Vmpp = 18
Impp = Pmax / Vmpp
num_panels = 2  # panels in parallel

# Function for calculating current as function of voltage for single panel
def I_of_V(V):
    V = np.array(V)
    I = Isc * (1 - (V / Voc)**a)
    I[V < 0] = Isc
    I[V > Voc] = 0
    return I

# Function for calculating power as function of voltage for single panel
def P_of_V(V):
    return V * I_of_V(V)

# Function for finding voltage for given total power from parallel panels
def V_from_P(P):
    P_single = P / num_panels
    if P_single <= 0:
        return 0.0
    if P_single >= Pmax:
        return Vmpp
    V_values = np.linspace(0, Voc, 2000)
    P_values = P_of_V(V_values)
    idx = np.argmin(np.abs(P_values - P_single))
    return V_values[idx]

# Function for generating power, voltage, and current data
def generate_data():
    data = []
    for P in range(1, 201):  
        V = V_from_P(P)
        I = P / V if V != 0 else 0
        data.append((P, round(V, 3), round(I, 3)))
    return data

# Function for creating and saving CSV files
def save_csv_files(df):
    # Save main CSV
    csv_path = "/mnt/data/solar_pannel_parallel_output_calculations.csv"
    df.to_csv(csv_path, index=False)
    print(f"Main CSV saved to: {csv_path}")
    
    # Check for currents below 25mA (0.025 A)
    low_current_df = df[df["Current (A)"] < 0.025]
    
    # Save second CSV if low current values found
    if not low_current_df.empty:
        no_charge_csv = "/mnt/data/Power_resulting_in_no_charging.csv"
        low_current_df.to_csv(no_charge_csv, index=False)
        print(f"No charging CSV saved to: {no_charge_csv}")
        print(f"Found {len(low_current_df)} power levels with current < 25mA")
        print(f"Power range with insufficient current: {low_current_df['Power (W)'].min()}W - {low_current_df['Power (W)'].max()}W")
    else:
        print("No power levels found with current below 25mA")
    
    return csv_path

def main():
    # Generate data for power range
    data = generate_data()
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=["Power (W)", "Voltage (V)", "Current (A)"])
    
    # Save CSV files and check for low current values
    save_csv_files(df)

if __name__ == "__main__":
    main()