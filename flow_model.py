import json
import math
from datetime import datetime

# Define pipe roughness values based on material (Hazen-Williams Coefficients)
ROUGHNESS_COEFFICIENTS = {
    "Cast Iron": 100,
    "Ductile Iron": 110,
    "Steel": 120,
    "Galvanized Steel": 110,
    "Stainless Steel": 140,
    "Copper": 150,
    "PVC/Plastic": 155,
    "Concrete": 120
}

# Corrosion rates (mm/year)
CORROSION_RATES = {
    "Cast Iron": 0.1,
    "Ductile Iron": 0.05,
    "Steel": 0.2,
    "Galvanized Steel": 0.15,
    "Stainless Steel": 0.02,
    "Copper": 0.01,
    "PVC/Plastic": 0.0,
    "Concrete": 0.005
}

def calculate_velocity(diameter, slope, roughness):
    """Uses the Hazen-Williams equation to estimate velocity."""
    C = roughness
    D_m = diameter  # Diameter in meters
    S = slope  # Slope as a decimal

    if S == 0:
        return 0  # Prevent division by zero (no flow)

    # Compute flow rate using Hazen-Williams formula
    Q = (C * (D_m ** 2.63) * (S ** 0.54)) / 278.5  # Flow rate in m³/s

    # Compute velocity
    A = math.pi * (D_m / 2) ** 2  # Cross-sectional area in m²
    V = Q / A  # Velocity in m/s

    return round(V, 2)

def calculate_pipe_diameter_reduction(material, age, initial_diameter):
    """Reduces pipe diameter due to corrosion over time."""
    corrosion_rate = CORROSION_RATES.get(material, 0.1) / 1000  # Convert mm/year to meters/year
    diameter_loss = 2 * (corrosion_rate * age)  # Total reduction in diameter
    reduced_diameter = max(initial_diameter - diameter_loss, 0.01)  # Ensure pipe isn't fully closed

    return round(reduced_diameter, 4)

def calculate_friction_loss(diameter, length, velocity, material):
    """Calculates head loss due to pipe friction using the Darcy-Weisbach equation."""
    f = 0.02  # Approximate friction factor (could be refined)
    g = 9.81  # Gravity (m/s^2)
    head_loss = (f * length / diameter) * (velocity ** 2 / (2 * g))
    return round(head_loss, 4)

def get_user_input():
    """Prompts user for required inputs."""
    print("\n💧 **Enhanced Water Travel Time Estimation** 💧")

    material = input(f"Enter pipe material ({', '.join(ROUGHNESS_COEFFICIENTS.keys())}): ")
    if material not in ROUGHNESS_COEFFICIENTS:
        print("⚠️ Invalid material. Defaulting to 'Cast Iron'.")
        material = "Cast Iron"

    age = int(input("Enter pipe age (years): "))
    initial_diameter = float(input("Enter initial pipe diameter (meters): "))
    total_distance = float(input("Enter total travel distance (meters): "))

    num_reductions = int(input("Enter number of pipe diameter reductions over distance: "))
    reductions = []
    for i in range(num_reductions):
        new_diameter = float(input(f"Enter reduced diameter after reduction {i+1} (meters): "))
        reduction_distance = float(input(f"Enter distance (meters) covered after reduction {i+1}: "))
        reductions.append((new_diameter, reduction_distance))

    num_slope_changes = int(input("Enter number of slope changes: "))
    slopes = []
    for i in range(num_slope_changes):
        slope_value = float(input(f"Enter slope (decimal, e.g., 0.01 for 1%) for section {i+1}: "))
        slope_distance = float(input(f"Enter distance (meters) for slope {i+1}: "))
        slopes.append((slope_value, slope_distance))

    num_pumps = int(input("Enter number of pumps along the pipeline: "))
    pumps = []
    for i in range(num_pumps):
        pump_flowrate = float(input(f"Enter flowrate of pump {i+1} (m³/s): "))
        pump_position = float(input(f"Enter distance (meters) from start where pump {i+1} is located: "))
        pumps.append((pump_flowrate, pump_position))

    return material, age, initial_diameter, total_distance, reductions, slopes, pumps

def main():
    """Main function to calculate water travel time."""
    material, age, initial_diameter, total_distance, reductions, slopes, pumps = get_user_input()
    reduced_diameter = calculate_pipe_diameter_reduction(material, age, initial_diameter)
    roughness = ROUGHNESS_COEFFICIENTS.get(material, 100)

    total_time = 0
    remaining_distance = total_distance
    current_diameter = reduced_diameter
    current_velocity = calculate_velocity(current_diameter, slopes[0][0], roughness)

    for slope, slope_distance in slopes:
        velocity = calculate_velocity(current_diameter, slope, roughness)
        section_time = slope_distance / velocity if velocity > 0 else float('inf')
        total_time += section_time
        remaining_distance -= slope_distance

    for pump_flowrate, pump_position in pumps:
        total_time -= pump_flowrate  # Adjust travel time for pump boost

    print("\n🔹 **Travel Time Calculation Results** 🔹")
    print(f"Pipe Material: {material}")
    print(f"Pipe Age: {age} years")
    print(f"Initial Diameter: {initial_diameter} meters")
    print(f"Reduced Diameter (after corrosion): {reduced_diameter} meters")
    print(f"Estimated Travel Time: {total_time:.2f} seconds ({total_time / 60:.2f} minutes)\n")

    data = {
        "timestamp": datetime.now().isoformat(),
        "pipe_material": material,
        "pipe_age": age,
        "initial_diameter_meters": initial_diameter,
        "reduced_diameter_meters": reduced_diameter,
        "total_distance_meters": total_distance,
        "travel_time_seconds": total_time
    }

    with open("water_travel_time.json", "a") as file:
        json.dump(data, file)
        file.write("\n")

if __name__ == "__main__":
    main()
