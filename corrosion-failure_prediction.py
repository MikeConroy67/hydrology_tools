import json
import math
import matplotlib.pyplot as plt
from datetime import datetime

# Corrosion rates (mm/year) based on pipe material in standard environments
CORROSION_RATES = {
    "Cast Iron": 0.1,   # Includes graphitization & tuberculation
    "Ductile Iron": 0.05,  # Lower due to improved alloy composition
    "Steel": 0.2,  # Rusting occurs faster in steel pipes
    "Galvanized Steel": 0.15,  # Zinc layer slows but does not prevent corrosion
    "Stainless Steel": 0.02,  # Resistant except in chloride environments
    "Copper": 0.01,  # Pitting corrosion possible in acidic water
    "PVC/Plastic": 0.0,  # No metallic corrosion, but may degrade from UV/chemicals
    "Concrete": 0.005  # Low corrosion, but sulfate attack is possible
}

def calculate_corrosion_rate(material, age):
    """Adjusts the corrosion rate based on pipe material and age factor"""
    base_rate = CORROSION_RATES.get(material, 0.1)  # Default if material is unknown
    age_factor = 1 + (0.02 * age)  # Corrosion accelerates over time (2% increase per year)
    return round(base_rate * age_factor, 4)

def estimate_remaining_life(initial_thickness, min_thickness, corrosion_rate):
    """Calculates remaining pipe lifespan before failure"""
    if corrosion_rate <= 0:
        return "Unlimited"  # No corrosion for plastic pipes
    remaining_life = (initial_thickness - min_thickness) / corrosion_rate
    return max(round(remaining_life, 2), 0)  # Ensure non-negative values

def get_user_input():
    """Prompts user for required inputs"""
    print("\n📌 **Pipe Corrosion & Failure Prediction Tool**")
    
    material = input(f"Enter pipe material ({', '.join(CORROSION_RATES.keys())}): ")
    if material not in CORROSION_RATES:
        print("⚠️ Invalid material. Defaulting to 'Cast Iron'.")
        material = "Cast Iron"

    age = int(input("Enter pipe age (years): "))
    initial_thickness = float(input("Enter initial pipe wall thickness (mm): "))
    min_thickness = float(input("Enter minimum safe wall thickness before failure (mm): "))
    
    return material, age, initial_thickness, min_thickness

def plot_corrosion_trend(material, initial_thickness, min_thickness, corrosion_rate):
    """Plots corrosion trends over time"""
    years = list(range(0, 51))  # Project for 50 years
    thicknesses = [initial_thickness - (corrosion_rate * y) for y in years]
    
    plt.figure(figsize=(8, 5))
    plt.plot(years, thicknesses, label=f"{material} Corrosion Trend", color='red')
    plt.axhline(y=min_thickness, color='blue', linestyle='--', label="Minimum Safe Thickness")
    plt.xlabel("Years")
    plt.ylabel("Wall Thickness (mm)")
    plt.title(f"Projected Corrosion Trend for {material}")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    """Main execution of the program"""
    material, age, initial_thickness, min_thickness = get_user_input()
    
    # Calculate corrosion rate
    corrosion_rate = calculate_corrosion_rate(material, age)
    
    # Estimate remaining life
    remaining_life = estimate_remaining_life(initial_thickness, min_thickness, corrosion_rate)

    # Display results
    print("\n🔹 **Corrosion Analysis Results** 🔹")
    print(f"Pipe Material: {material}")
    print(f"Pipe Age: {age} years")
    print(f"Corrosion Rate: {corrosion_rate} mm/year")
    print(f"Estimated Remaining Life: {remaining_life} years")
    
    # Save to JSON
    data = {
        "timestamp": datetime.now().isoformat(),
        "pipe_material": material,
        "pipe_age": age,
        "corrosion_rate_mm_per_year": corrosion_rate,
        "initial_thickness_mm": initial_thickness,
        "min_thickness_mm": min_thickness,
        "remaining_life_years": remaining_life
    }
    
    with open("pipe_corrosion_data.json", "a") as file:
        json.dump(data, file)
        file.write("\n")

    print(f"✅ Data successfully written to pipe_corrosion_data.json")

    # Plot corrosion trend
    plot_corrosion_trend(material, initial_thickness, min_thickness, corrosion_rate)

if __name__ == "__main__":
    main()
