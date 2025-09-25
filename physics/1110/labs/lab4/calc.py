import math

# Constants
g = 9.81  # acceleration due to gravity (m/s²)

def calculate_initial_velocity(height, horizontal_range):
    """Calculate initial velocity from horizontal launch height and range."""
    flight_time = math.sqrt(2 * height / g)
    initial_velocity = horizontal_range / flight_time
    return initial_velocity

def calculate_projectile_height(v0, angle_deg, initial_height, target_distance):
    """Calculate height at target distance for angled launch."""
    # Convert angle to radians
    theta = math.radians(angle_deg)
    
    # Calculate velocity components
    vx0 = v0 * math.cos(theta)
    vy0 = v0 * math.sin(theta)
    
    # Calculate time to reach target distance
    time_to_target = target_distance / vx0
    
    # Calculate height at target distance
    height = initial_height + vy0 * time_to_target - 0.5 * g * time_to_target**2
    
    return height

# Example usage:
if __name__ == "__main__":
    # a) Calculate initial velocity from height input
    launch_height = 0.85  # meters
    range_measurement = 1.46  # meters
    v0 = calculate_initial_velocity(launch_height, range_measurement)
    print(f"Initial velocity: {v0:.2f} m/s")
    
    # b) Calculate height at target for angled launch
    launch_angle = 30  # degrees
    initial_height = 0.1  # meters above table
    target_distance = 1.5  # meters
    
    predicted_height = calculate_projectile_height(v0, launch_angle, initial_height, target_distance)
    print(f"Predicted height at {target_distance}m: {predicted_height:.3f} m ({predicted_height*100:.1f} cm)")
