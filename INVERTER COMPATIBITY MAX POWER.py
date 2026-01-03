# Notes: Program designed to calcualte tipover and slidign risk. Mass and com are calculaed based on case design as of fall 2025 major iterations
#        Will result is inacuate resuslts. Sliding risk is depenedent on user imputed coefiant of static friction. This value should be deterimed 
#        experimentaly and will very dependign of soil charecteristics. program includes saftey factor of 1.5.

# produced Fall 2025 
# author Eoin Graham graha308@purdue.edu 

# Import statements
import pandas as pd
import os

# Battery parameters
num_batteries = 2  # Number of batteries in parallel
amp_hours_rated = 100  # Rated amp hours per battery
discharge_time = 20  # Discharge time in hours
resting_voltage = 13.1  # Resting voltage in volts (adjustable)

# Inverter parameters
inverter_max_power = 1100  # Maximum power in watts
inverter_min_voltage = 10  # Minimum voltage in volts
inverter_max_voltage = 15  # Maximum voltage in volts

# Battery voltage table (State of Charge)
voltage_table = [
    (100, 13.1),
    (90, 12.7),
    (80, 12.5),
    (70, 12.3),
    (60, 12.1),
    (50, 12.0),
    (40, 11.7),
    (20, 11.3),
    (0, 10.5)
]

# Function for calculating adjusted amp hours based on resting voltage
def adjust_amp_hours(Resting_voltage, Amp_hours_rated):
    # Find state of charge from voltage table
    soc_percent = 100
    for soc, voltage in voltage_table:
        if Resting_voltage >= voltage:
            soc_percent = soc
            break
    
    # Adjust amp hours proportionally
    adjusted_ah = Amp_hours_rated * (soc_percent / 100.0)
    return adjusted_ah, soc_percent

# Function for calculating max power draw from batteries
def power_draw_calc(Amp_hours, Discharge_time, Num_batteries, Voltage):
    # Current per battery
    current_per_battery = Amp_hours / Discharge_time
    # Total current from parallel batteries
    total_current = current_per_battery * Num_batteries
    # Max power draw
    max_power = Voltage * total_current
    return max_power, total_current

# Function for checking inverter compatibility
def compatibility_check(Max_power_draw, Voltage, Inverter_max_power, Inverter_min_voltage, Inverter_max_voltage):
    if Voltage < Inverter_min_voltage:
        return "Battery is not compatible - Voltage too low"
    elif Voltage > Inverter_max_voltage:
        return "Battery is not compatible - Voltage too high"
    elif Max_power_draw > Inverter_max_power:
        return "Battery is not compatible - Power draw exceeds inverter rating"
    else:
        return "Battery is compatible"

# Function for creating and saving results
def save_results(results):
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "inverter_compatibility_results.csv")
    
    df = pd.DataFrame([results])
    df.to_csv(csv_path, index=False)
    print(f"Results saved to: {csv_path}")
    
    return csv_path

def main():
    # Adjust amp hours based on resting voltage
    adjusted_ah, soc_percent = adjust_amp_hours(resting_voltage, amp_hours_rated)
    
    # Calculate max power draw
    max_power_draw, total_current = power_draw_calc(adjusted_ah, discharge_time, num_batteries, resting_voltage)
    
    # Check compatibility
    compatibility = compatibility_check(max_power_draw, resting_voltage, inverter_max_power, inverter_min_voltage, inverter_max_voltage)
    
    # Create results dictionary
    results = {
        "Resting Voltage (V)": resting_voltage,
        "State of Charge (%)": soc_percent,
        "Rated Amp Hours": amp_hours_rated,
        "Adjusted Amp Hours": round(adjusted_ah, 2),
        "Discharge Time (hours)": discharge_time,
        "Number of Batteries": num_batteries,
        "Total Current (A)": round(total_current, 2),
        "Max Power Draw (W)": round(max_power_draw, 2),
        "Inverter Max Power (W)": inverter_max_power,
        "Inverter Voltage Range": f"{inverter_min_voltage}-{inverter_max_voltage} V",
        "Compatibility": compatibility
    }
    
    # Save results
    save_results(results)
    
    # Print statements
    print("Battery configuration: {} batteries in parallel".format(num_batteries))
    print("Resting voltage: {} V".format(resting_voltage))
    print("Percentage of Original Capacity: {}%".format(soc_percent))
    print("Rated amp hours per battery: {} Ah".format(amp_hours_rated))
    print("Adjusted amp hours per battery: {:.2f} Ah".format(adjusted_ah))
    print("Discharge time: {} hours".format(discharge_time))
    print("Total current available: {:.2f} A".format(total_current))
    print("Max power draw from batteries: {:.2f} W".format(max_power_draw))
    print("Inverter rating: {} W ({}-{} V)".format(inverter_max_power, inverter_min_voltage, inverter_max_voltage))
    print("Compatibility status: {}".format(compatibility))

if __name__ == "__main__":

    main()
