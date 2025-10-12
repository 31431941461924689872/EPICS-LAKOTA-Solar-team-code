# Import statements
import numpy as np
import pandas as pd
import os

# Charge controller parameters
output_voltage = 12  # Fixed output voltage in volts
max_power = 200  # Maximum power in watts (variable)

# Function for calculating output current from power
def current_calc(Power_values, Output_voltage):
    current_list = []
    if isinstance(Power_values, (int, float)):
        Power_values = [Power_values]
    for power_number in Power_values:
        current_list.append(power_number / Output_voltage)
    if len(current_list) == 1:
        return current_list[0]
    else:
        return current_list

# Function for generating power and current data
def generate_data():
    data = []
    Power_values = list(range(1, max_power + 1))
    current_list = current_calc(Power_values, output_voltage)
    
    for i in range(len(Power_values)):
        data.append((Power_values[i], output_voltage, round(current_list[i], 3)))
    
    return data

# Function for creating and saving CSV files
def save_csv_files(df):
    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Save main CSV
    csv_path = os.path.join(output_dir, "charge_controller_output_calculations.csv")
    df.to_csv(csv_path, index=False)
    print(f"CSV saved to: {csv_path}")
    
    return csv_path

def main():
    # Generate data for power range
    data = generate_data()
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=["Power (W)", "Voltage (V)", "Current (A)"])
    
    # Save CSV file
    save_csv_files(df)
    
    # Print statements
    print("Charge controller output voltage: {} V".format(output_voltage))
    print("Power range: 1 W to {} W".format(max_power))
    print("Current range: {:.3f} A to {:.3f} A".format(df["Current (A)"].min(), df["Current (A)"].max()))

if __name__ == "__main__":
    main()