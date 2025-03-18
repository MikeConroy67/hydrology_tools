import json
from datetime import datetime

def calculate_flow_rate(diameter, velocity, specific_gravity=1.0):
    """Calculates the volumetric flow rate considering specific gravity."""
    pi = 3.1416
    radius = diameter / 2
    area = pi * (radius ** 2)  # Cross-sectional area of the pipe
    flow_rate = area * velocity  # Q = A * V

    # Adjusting flow rate for fluids with different specific gravities
    adjusted_flow_rate = flow_rate / (specific_gravity ** 0.5)

    return round(flow_rate, 2), round(adjusted_flow_rate, 2)

def calculate_travel_time(pipe_length, velocity):
    """Calculates the time required for water to travel through a pipe length."""
    if velocity > 0:
        travel_time = pipe_length / velocity  # Time = Distance / Speed
        return round(travel_time, 2)  # Time in seconds
    else:
        return None  # Prevent division by zero error

def get_positive_float(prompt):
    """Helper function to safely get a positive floating-point number from the user."""
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def main():
    print("💧 Pipe Flow Rate & Travel Time Calculator 💧")

    # User input
    diameter = get_positive_float("Enter the pipe diameter (meters): ")
    velocity = get_positive_float("Enter the velocity of water (m/s): ")
    specific_gravity = get_positive_float("Enter the specific gravity of the fluid (1 for water): ")
    pipe_length = get_positive_float("Enter the pipe length for travel time calculation (meters): ")

    # Perform calculations
    flow_rate, adjusted_flow_rate = calculate_flow_rate(diameter, velocity, specific_gravity)
    travel_time = calculate_travel_time(pipe_length, velocity)

    # Display results
    print("\n🔹 **Calculation Results** 🔹")
    print(f"Pipe Diameter: {diameter} meters")
    print(f"Velocity: {velocity} m/s")
    print(f"Specific Gravity: {specific_gravity}")
    print(f"Flow Rate (for water): {flow_rate} cubic meters per second (m³/s)")
    print(f"Adjusted Flow Rate (for SG={specific_gravity}): {adjusted_flow_rate} cubic meters per second (m³/s)")
    print(f"Time to travel {pipe_length} meters: {travel_time} seconds\n")

    # Prepare data for JSON file
    data = {
        "timestamp": datetime.now().isoformat(),
        "pipe_diameter_meters": diameter,
        "velocity_mps": velocity,
        "specific_gravity": specific_gravity,
        "flow_rate_m3_per_s": flow_rate,
        "adjusted_flow_rate_m3_per_s": adjusted_flow_rate,
        "pipe_length_meters": pipe_length,
        "travel_time_seconds": travel_time
    }

    # Write results to JSON file
    filename = "pipe_flow_data.json"
    try:
        with open(filename, "a") as file:
            json.dump(data, file)
            file.write("\n")
        print(f"✅ Data successfully written to {filename}")
    except Exception as e:
        print(f"❌ Error writing to file: {e}")

if __name__ == "__main__":
    main()
