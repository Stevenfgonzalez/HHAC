import pandas as pd
import matplotlib.pyplot as plt

# --- Simulation Parameters ---
hours = list(range(24))  # 24 hours in a day
fire_station_power_needed = 10  # kWh needed per hour
home_power_needed = 1  # kWh per home per hour
num_homes = 10
generator_output = 50  # kWh per hour when on
battery_capacity = 100  # kWh, fully charged at start

# --- Initialize Tracking ---
fire_station_power_supplied = []
battery_level = battery_capacity
generator_on = False
battery_ran_out = False

# --- Simulate Each Hour ---
for hour in hours:
    # Outage from 6 PM (18) to 10 PM (22, exclusive)
    grid_outage = 18 <= hour < 22

    # Default: grid is up, all loads met
    if not grid_outage:
        fire_station_power_supplied.append(fire_station_power_needed)
        # Battery recharges if grid is up (optional, not specified)
        continue

    # During outage: homes get no power, only fire station is priority
    if battery_level >= fire_station_power_needed:
        # Use battery first
        fire_station_power_supplied.append(fire_station_power_needed)
        battery_level -= fire_station_power_needed
    else:
        # Battery empty, use generator if available
        if battery_level > 0:
            # Use remaining battery, then generator for the rest
            fire_station_power_supplied.append(battery_level)
            battery_level = 0
            generator_on = True
        else:
            generator_on = True
            if generator_output >= fire_station_power_needed:
                fire_station_power_supplied.append(fire_station_power_needed)
            else:
                # Generator can't supply enough (shouldn't happen in this scenario)
                fire_station_power_supplied.append(generator_output)

    # Warn if battery runs out
    if battery_level == 0 and not battery_ran_out:
        print(f"WARNING: Battery ran out at hour {hour} (time: {hour}:00). Generator started.")
        battery_ran_out = True

# --- Results DataFrame ---
df = pd.DataFrame({
    'Hour': hours,
    'Fire Station Power Supplied (kWh)': fire_station_power_supplied
})

# --- Plotting ---
plt.figure(figsize=(10, 5))
plt.plot(df['Hour'], df['Fire Station Power Supplied (kWh)'], marker='o', label='Fire Station Power')
plt.axhline(y=fire_station_power_needed, color='green', linestyle='--', label='Required Power (10 kWh)')
plt.axvspan(18, 22, color='orange', alpha=0.2, label='Grid Outage (6-10 PM)')
plt.title('Fire Station Power Supply Over 24 Hours')
plt.xlabel('Hour of Day')
plt.ylabel('Power Supplied (kWh)')
plt.xticks(range(0, 24))
plt.legend()
plt.grid(True)

# --- Check for "Going Dark" ---
for hour, power in enumerate(fire_station_power_supplied):
    if power < fire_station_power_needed:
        print(f'ALERT: Fire station risks going dark at hour {hour} (power supplied: {power} kWh)')

plt.tight_layout()
plt.show()
