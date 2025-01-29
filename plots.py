import pandas as pd
import matplotlib.pyplot as plt
import os
import re


def analyze_camera_performances(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Load the CSV file
    data = pd.read_csv(file_path)

    # Identify the number of cameras dynamically based on column names
    camera_columns = [col for col in data.columns if re.match(r"Camera\d+_Performance", col)]
    num_cameras = len(camera_columns)

    if num_cameras == 0:
        print("Error: No camera performance data found in the file.")
        return

    # Initialize a dictionary to store performance stats
    performance_stats = {
        "Camera": [],
        "Best_Performance": [],
        "Worst_Performance": [],
        "Average_Performance": []
    }

    # Analyze performance for each camera
    for camera in camera_columns:
        performance_stats["Camera"].append(camera)
        performance_stats["Best_Performance"].append(data[camera].max())
        performance_stats["Worst_Performance"].append(data[camera].min())
        performance_stats["Average_Performance"].append(data[camera].mean())

        # Plot individual camera performance
        plt.figure(figsize=(8, 5))
        plt.plot(data["Rank"], data[camera], label=camera, marker="o", linestyle="-", color="b")
        plt.xlabel("Rank")
        plt.ylabel("Performance (%)")
        plt.title(f"Performance for {camera}")
        plt.legend()
        plt.grid(True)
        output_path = f"output/{camera}_performance_plot.png"
        os.makedirs("output", exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        print(f"Plot saved for {camera}: {output_path}")

    # Convert performance stats to a DataFrame for easy visualization
    stats_df = pd.DataFrame(performance_stats)
    print("\nCamera Performance Statistics:")
    print(stats_df)

    # Plot combined performance
    plt.figure(figsize=(12, 6))
    for camera in camera_columns:
        plt.plot(data["Rank"], data[camera], label=camera, marker="o", linestyle="--")
    plt.xlabel("Rank")
    plt.ylabel("Performance (%)")
    plt.title("Combined Camera Performances")
    plt.legend()
    plt.grid(True)
    combined_output_path = "output/combined_camera_performance_plot.png"
    plt.savefig(combined_output_path)
    plt.close()
    print(f"Combined plot saved: {combined_output_path}")


if __name__ == "__main__":
    # Replace this with the path to your CSV file
    csv_file_path = "output/base_model_morning_camera_performances.csv"

    # Analyze performances and generate plots
    analyze_camera_performances(csv_file_path)
