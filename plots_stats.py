import pandas as pd
import numpy as np
import os

# Load and combine CSV files
def load_and_combine(files):
    dataframes = [pd.read_csv(file) for file in files]
    df_combined = pd.concat(dataframes, axis=0, ignore_index=True)
    return df_combined

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
    # summary_df.to_csv("plots/base/boxplot_summary.csv", index=False)
    print("\n📊 Boxplot Summary:\n", summary_df)
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

    # histogram_df.to_csv("plots/base/histogram_summary.csv", index=False)
    print("\n📊 Histogram Frequency Summary:\n", histogram_df)
    return histogram_df

# Generate correlation matrix for cameras
def generate_correlation_matrix(df, cameras):
    correlation_matrix = df[cameras].replace(0, np.nan).corr()
    # correlation_matrix.to_csv("plots/base/correlation_matrix.csv")
    print("\n🔗 Correlation Matrix:\n", correlation_matrix)
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
    # summary_df.to_csv("plots/base/camera_performance_summary.csv", index=False)
    print("\n📊 Camera Performance Summary:\n", summary_df)
    return summary_df

# Main execution
def main():
    os.makedirs("statistics", exist_ok=True)  # Ensure statistics directory exists
    files = [
        "output/a11c_model_morning_camera_performances.csv",
        "output/a11c_model_noon_camera_performances.csv",
        "output/a11c_model_afternoon_camera_performances.csv"
    ]
    
    # Load and process data
    df = load_and_combine(files)
    summary, cameras = process_data(df)
    
    # Save combined data
    # save_combined_performance(df, "statistics/combined_camera_performance.csv")

    # Generate and save numerical summaries
    generate_boxplot_summary(df, cameras)
    generate_histogram_summary(df, cameras)
    generate_correlation_matrix(df, cameras)
    generate_performance_summary(df, cameras)

if __name__ == "__main__":
    main()
