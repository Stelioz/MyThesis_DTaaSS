import pandas as pd
import numpy as np
import os

# Load and combine CSV file (since only one file per model)
def load_csv(file):
    df = pd.read_csv(file)
    return df

# Process data to remove zero values and compute summary
def process_data(df):
    cameras = [col for col in df.columns if "Performance" in col]
    summary = {}
    for cam in cameras:
        valid_values = df[cam].replace(0, np.nan).dropna()
        summary[cam] = {
            "Best": valid_values.max(),
            "Worst": valid_values.min(),
            "Average": valid_values.mean()
        }
    return summary, cameras

# Save combined performance data
def save_combined_performance(df, output_file):
    df.to_csv(output_file, index=False)
    print(f"Combined data saved to {output_file}")

# Generate boxplot summary statistics (Min, Q1, Median, Q3, Max)
def generate_boxplot_summary(df, cameras):
    summary_data = []
    for cam in cameras:
        valid_values = df[cam].replace(0, np.nan).dropna()
        summary_data.append({
            "Camera": cam,
            "Min": valid_values.min(),
            "Q1 (25%)": valid_values.quantile(0.25),
            "Median (50%)": valid_values.median(),
            "Q3 (75%)": valid_values.quantile(0.75),
            "Max": valid_values.max()
        })

    summary_df = pd.DataFrame(summary_data)
    return summary_df

# Generate histogram frequency table
def generate_histogram_summary(df, cameras):
    all_values = df[cameras].replace(0, np.nan).values.flatten()
    all_values = all_values[~np.isnan(all_values)]

    # Define bins (e.g., 0-10%, 10-20%, ...)
    bins = np.arange(0, 101, 10)
    hist, bin_edges = np.histogram(all_values, bins=bins)

    histogram_df = pd.DataFrame({
        "Range": [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}%" for i in range(len(hist))],
        "Frequency": hist
    })

    return histogram_df

# Generate correlation matrix for cameras
def generate_correlation_matrix(df, cameras):
    correlation_matrix = df[cameras].replace(0, np.nan).corr()
    return correlation_matrix

# Generate best, worst, and average performance summary
def generate_performance_summary(df, cameras):
    summary = []
    for cam in cameras:
        valid_values = df[cam].replace(0, np.nan).dropna()
        summary.append({
            "Camera": cam,
            "Best Performance": valid_values.max(),
            "Worst Performance": valid_values.min(),
            "Average Performance": valid_values.mean()
        })

    summary_df = pd.DataFrame(summary)
    return summary_df

# Main execution
def main():
    print("\nPlease choose the model you want to analyze:")
    print("1: Scaled_Base_Model")
    print("2: Scaled_Model_7")
    print("3: Scaled_Model_9")
    print("4: Scaled_Model_11")
    print("5: Enhanced_Base_Model")
    print("6: Enhanced_Model_7")
    print("7: Enhanced_Model_9")
    print("8: Enhanced_Model_11")

    model_choice = input("\nEnter your choice (1 to 8): ").strip()
    
    model_map = {
        "1": "scaled_base_model",
        "2": "scaled_model_7",
        "3": "scaled_model_9",
        "4": "scaled_model_11",
        "5": "enhanced_base_model",
        "6": "enhanced_model_7",
        "7": "enhanced_model_9",
        "8": "enhanced_model_11"
    }
    
    if model_choice not in model_map:
        print("\nInvalid choice. Exiting...")
        return
    
    model_type = model_map[model_choice]
    print(f"\nYou selected: {model_type}")
    
    # Define the file path for the selected model
    file = f"output/{model_type}_camera_performances.csv"
    
    if not os.path.exists(file):
        print(f"Error: The file {file} does not exist.")
        return
    
    # Create directory for statistics if it doesn't exist
    os.makedirs("stats", exist_ok=True)

    # Load and process data
    df = load_csv(file)
    summary, cameras = process_data(df)
    
    # Generate summary data
    boxplot_summary = generate_boxplot_summary(df, cameras)
    histogram_summary = generate_histogram_summary(df, cameras)
    correlation_matrix = generate_correlation_matrix(df, cameras)
    performance_summary = generate_performance_summary(df, cameras)

    # Combine all summary data into one DataFrame
    combined_summary_df = pd.concat([
        boxplot_summary.set_index("Camera").add_prefix("Boxplot_"),
        performance_summary.set_index("Camera").add_prefix("Performance_")
    ], axis=1)
    
    combined_summary_df = combined_summary_df.reset_index()

    # Save combined performance data and summary data to CSV
    combined_file = f"stats/{model_type}_combined_camera_performance.csv"
    combined_summary_df.to_csv(combined_file, index=False)
    
    # Save histogram summary to CSV
    histogram_file = f"stats/{model_type}_histogram_summary.csv"
    histogram_summary.to_csv(histogram_file, index=False)
    print(f"📊 Histogram summary saved to {histogram_file}")

    print(f"📊 Combined summary saved to {combined_file}")

    # Optionally print the full summary to terminal
    print("\n📊 Full Camera Performance Summary:\n", combined_summary_df)
    print("\n📊 Histogram Frequency Summary:\n", histogram_summary)

if __name__ == "__main__":
    main()
