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
    """
    Calculates water velocity using the Hazen-Williams equation.
    Q = (C * D^2.63 * S^0.54) / 278.5 (for metric units)
    V = Q / A
    """
    C = roughness
    D_m = diameter  # Diameter in meters
    S = slope  # Slope as a decimal

    # Compute flow rate using Hazen-Williams formula
    Q = (C * (D_m ** 2.63) * (S ** 0.54)) / 278.5  # Flow rate in m³/s

    # Compute velocity
    A = math.pi * (D_m / 2) ** 2  # Cross-sectional area in m²
    V = Q / A  # Velocity in m/s

    return round(V, 2)

def calculate_pipe_diameter_reduction(material, age, initial_diameter):
    """
    Reduces pipe diameter over time due to corrosion.
    """
    corrosion_rate = CORROSION_RATES.get(material, 0.1) / 1000  # Convert mm/year to meters/year
    diameter_loss = 2 * (corrosion_rate * age)  # Total reduction in diameter
    reduced_diameter = max(initial_diameter - diameter_loss, 0.01)  # Ensure pipe isn't fully closed

    return round(reduced_diameter, 4)

def calculate_travel_time(distance, velocity):
    """
    Time = Distance / Velocity
    """
    if velocity > 0:
        travel_time = distance / velocity  # Time in seconds
        return round(travel_time, 2)
    else:
        return None  # Prevent division by zero

def get_user_input():
    """
    Gets user input for pipe characteristics and environment.
    """
    print("\n💧 **Water Travel Time Estimation** 💧")

    material = input(f"Enter pipe material ({', '.join(ROUGHNESS_COEFFICIENTS.keys())}): ")
    if material not in ROUGHNESS_COEFFICIENTS:
        print("⚠️ Invalid material. Defaulting to 'Cast Iron'.")
        material = "Cast Iron"

    age = int(input("Enter pipe age (years): "))
    initial_diameter = float(input("Enter initial pipe diameter (meters): "))
    distance = float(input("Enter total travel distance (meters): "))
    slope = float(input("Enter slope of the pipe (as decimal, e.g., 0.01 for 1% slope): "))

    return material, age, initial_diameter, distance, slope

def main():
    """
    Main function to calculate water travel time.
    """
    material, age, initial_diameter, distance, slope = get_user_input()

    # Adjust pipe diameter for corrosion
    reduced_diameter = calculate_pipe_diameter_reduction(material, age, initial_diameter)

    # Get roughness coefficient
    roughness = ROUGHNESS_COEFFICIENTS.get(material, 100)

    # Calculate velocity
    velocity = calculate_velocity(reduced_diameter, slope, roughness)

    # Calculate travel time
    travel_time = calculate_travel_time(distance, velocity)

    # Display results
    print("\n🔹 **Travel Time Calculation Results** 🔹")
    print(f"Pipe Material: {material}")
    print(f"Pipe Age: {age} years")
    print(f"Initial Diameter: {initial_diameter} meters")
    print(f"Reduced Diameter (after corrosion): {reduced_diameter} meters")
    print(f"Velocity: {velocity} m/s")
    print(f"Total Distance: {distance} meters")
    print(f"Estimated Travel Time: {travel_time} seconds ({travel_time / 60:.2f} minutes)\n")

    # Save results to JSON
    data = {
        "timestamp": datetime.now().isoformat(),
        "pipe_material": material,
        "pipe_age": age,
        "initial_diameter_meters": initial_diameter,
        "reduced_diameter_meters": reduced_diameter,
        "velocity_mps": velocity,
        "travel_distance_meters": distance,
        "slope": slope,
        "travel_time_seconds": travel_time
    }

    with open("water_travel_time.json", "a") as file:
        json.dump(data, file)
        file.write("\n")

    print(f"✅ Data successfully written to water_travel_time.json")

if __name__ == "__main__":
    main()
