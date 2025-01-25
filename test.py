import pandas as pd

# Define weights and max density
W_DISTANCE = 0.4
W_ANGLE = 0.4
W_DENSITY = 0.2
MAX_DENSITY = 20  # Maximum density threshold for normalization

def calculate_performance(angle, distance, density):
    """Calculate the performance for a single camera."""
    performance = (
        (W_DISTANCE * (distance / 10)) +
        (W_ANGLE * (angle / 10)) -
        (W_DENSITY * (density / MAX_DENSITY))
    )
    return max(0, min(1, performance)) * 100  # Ensure result is between 0 and 100%

def process_csv(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)

    # Extract the Rank, Name & Surname, and SSN columns
    result_data = data[["Rank", "Name & Surname", "SSN"]].copy()

    # Prepare performance columns
    for i in range(1, 7):  # Loop through Camera1 to Camera6
        performance_column = f"Camera{i}_Performance"
        result_data[performance_column] = data.apply(
            lambda row: calculate_performance(row[f"Angle{i}"], row[f"Distance{i}"], row[f"Density{i}"]),
            axis=1
        )

    # Group by Rank and keep the highest performance for each camera
    grouped_result = result_data.groupby("Rank").agg(
        {
            **{f"Camera{i}_Performance": "max" for i in range(1, 7)}  # Keep max performance for each camera
        }
    )

    return grouped_result

# Path to your CSV file
file_path = "output/flexsim_data_test_run.csv"

# Process the CSV file and calculate performances
result_data = process_csv(file_path)

# Save the result to a new CSV file
result_data.to_csv("output/camera_performances_test_run", index=False)

# Print all results for verification
print(result_data)
