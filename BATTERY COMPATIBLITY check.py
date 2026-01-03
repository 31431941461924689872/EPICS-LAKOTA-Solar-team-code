# Notes: Program designed to calcualte tipover and slidign risk. Mass and com are calculaed based on case design as of fall 2025 major iterations
#        Will result is inacuate resuslts. Sliding risk is depenedent on user imputed coefiant of static friction. This value should be deterimed 
#        experimentaly and will very dependign of soil charecteristics. program includes saftey factor of 1.5.

# produced Fall 2025 
# author Eoin Graham graha308@purdue.edu 

# Import statements
import pandas as pd
import os

# Battery parameters
max_charging_current = 25  # Maximum charging current in amps
max_voltage = 11  # Maximum voltage in volts
num_batteries = 2  # Number of batteries in parallel

# Function for checking battery compatibility
def compatibility_check(Current_values, Voltage_values, Max_current, Max_voltage):
    compatible_list = []
    if isinstance(Current_values, (int, float)):
        Current_values = [Current_values]
        Voltage_values = [Voltage_values]
    for i in range(len(Current_values)):
        if Current_values[i] <= Max_current and Voltage_values[i] <= Max_voltage:
            compatible_list.append("Battery is compatible")
        else:
            compatible_list.append("Battery is not compatible")
    if len(compatible_list) == 1:
        return compatible_list[0]
    else:
        return compatible_list

# Function for importing charge controller data
def import_data():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    csv_path = os.path.join(input_dir, "charge_controller_output_calculations.csv")
    
    if not os.path.exists(csv_path):
        print("Error: Charge controller CSV file not found")
        return None
    
    df = pd.read_csv(csv_path)
    return df

# Function for creating and saving compatibility results
def save_results(df):
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "battery_compatibility_results.csv")
    df.to_csv(csv_path, index=False)
    print(f"Results saved to: {csv_path}")
    
    return csv_path

def main():
    # Import charge controller data
    df = import_data()
    
    if df is None:
        return
    
    # Extract voltage and current values
    Current_values = df["Current (A)"].tolist()
    Voltage_values = df["Voltage (V)"].tolist()
    Power_values = df["Power (W)"].tolist()
    
    # Calculate total current for parallel batteries (current per battery is divided)
    Current_per_battery = [i / num_batteries for i in Current_values]
    
    # Check compatibility
    compatibility_list = compatibility_check(Current_per_battery, Voltage_values, max_charging_current, max_voltage)
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        "Power (W)": Power_values,
        "Voltage (V)": Voltage_values,
        "Total Current (A)": Current_values,
        "Current per Battery (A)": [round(i, 3) for i in Current_per_battery],
        "Compatibility": compatibility_list
    })
    
    # Save results
    save_results(results_df)
    
    # Print statements
    print("Battery configuration: {} batteries in parallel".format(num_batteries))
    print("Max charging current per battery: {} A".format(max_charging_current))
    print("Max voltage: {} V".format(max_voltage))
    
    compatible_count = compatibility_list.count("Battery is compatible")
    incompatible_count = compatibility_list.count("Battery is not compatible")
    
    print("Compatible power levels: {}".format(compatible_count))
    print("Incompatible power levels: {}".format(incompatible_count))

if __name__ == "__main__":

    main()
