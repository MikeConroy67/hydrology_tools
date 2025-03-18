import json
from datetime import datetime

def calculate_spherical_volume(diameter):
    """Calculates the volume of a spherical tank given its diameter."""
    pi = 3.1416
    radius = diameter / 2
    volume = (4/3) * pi * (radius ** 3)
    return volume

def calculate_cylindrical_volume(diameter, height):
    """Calculates the volume of a cylindrical tank given its diameter and height."""
    pi = 3.1416
    radius = diameter / 2
    volume = pi * (radius ** 2) * height
    return volume

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
    # Prompt user to choose the type of tank
    print("Select the type of water tank:")
    print("1. Spherical Tank")
    print("2. Cylindrical Tank")
    
    while True:
        choice = input("Enter 1 for Spherical or 2 for Cylindrical: ")
        if choice in ["1", "2"]:
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # Get user inputs and calculate volume based on tank type
    if choice == "1":
        # Spherical Tank Calculation
        diameter = get_positive_float("Enter the diameter of the spherical water tank (in meters): ")
        volume = calculate_spherical_volume(diameter)
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "tank_type": "Spherical",
            "diameter_meters": diameter,
            "radius_meters": diameter / 2,
            "volume_cubic_meters": round(volume, 2)
        }

        print("\nSpherical Tank Calculation:")
        print(f"Diameter: {diameter} meters")
        print(f"Radius: {diameter / 2} meters")
        print(f"Volumetric Capacity: {volume:.2f} cubic meters\n")

    else:
        # Cylindrical Tank Calculation
        diameter = get_positive_float("Enter the diameter of the cylindrical water tank (in meters): ")
        height = get_positive_float("Enter the height of the cylindrical water tank (in meters): ")
        volume = calculate_cylindrical_volume(diameter, height)

        data = {
            "timestamp": datetime.now().isoformat(),
            "tank_type": "Cylindrical",
            "diameter_meters": diameter,
            "radius_meters": diameter / 2,
            "height_meters": height,
            "volume_cubic_meters": round(volume, 2)
        }

        print("\nCylindrical Tank Calculation:")
        print(f"Diameter: {diameter} meters")
        print(f"Radius: {diameter / 2} meters")
        print(f"Height: {height} meters")
        print(f"Volumetric Capacity: {volume:.2f} cubic meters\n")

    # Write results to JSON file
    filename = "tank_volume_data.json"
    try:
        with open(filename, "a") as file:
            json.dump(data, file)
            file.write("\n")
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()
