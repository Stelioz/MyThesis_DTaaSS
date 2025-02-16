import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

# Box plot for performance distribution
def plot_boxplot(df, cameras):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df[cameras].replace(0, np.nan), showfliers=False)
    
    # Remove "_Performance" from x-axis labels
    plt.xticks(ticks=range(len(cameras)), labels=[cam.replace("_Performance", "") for cam in cameras], rotation=-45)
    
    plt.xlabel("Cameras")
    plt.ylabel("Performance (%)")
    plt.title("Camera Performance Distribution")
    plt.savefig("plots/abase/camera_performance_boxplot.png")
    plt.show()

# Histogram plot for performance distribution per camera
def plot_histograms(df, cameras):
    for cam in cameras:
        plt.figure(figsize=(8, 5))
        plt.hist(df[cam].replace(0, np.nan), bins=30, alpha=0.6, color='blue', edgecolor='black', density=True, label="Histogram")
        sns.kdeplot(df[cam].replace(0, np.nan), color='red', linewidth=2, label="Curve")
        
        # Remove "_Performance" from the title
        plt.xlabel("Performance (%)")
        plt.ylabel("Density")
        plt.title(f"Histogram & Distribution of {cam.replace('_Performance', '')}")
        plt.legend()
        plt.savefig(f"plots/abase/histogram_{cam.replace('_Performance', '')}.png")
        plt.show()

# Correlation heatmap
def plot_correlation_heatmap(df, cameras):
    plt.figure(figsize=(10, 8))
    
    # Compute correlation matrix and replace NaN with 0
    correlation_matrix = df[cameras].replace(0, np.nan).corr()
    correlation_matrix = correlation_matrix.fillna(0)  # Replace NaN with 0
    
    # Plot heatmap
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        cbar_kws={"label": "Correlation"}
    )
    
    # Remove "_Performance" from the heatmap labels
    plt.xticks(ticks=range(len(cameras)), labels=[cam.replace("_Performance", "") for cam in cameras], rotation=45)
    plt.yticks(ticks=range(len(cameras)), labels=[cam.replace("_Performance", "") for cam in cameras], rotation=0)
    
    plt.title("Correlation Heatmap of Camera Performances")
    plt.savefig("plots/abase/camera_performance_correlation_heatmap.png")
    plt.show()

# Histogram for all cameras combined
def plot_combined_histogram(df, cameras):
    plt.figure(figsize=(10, 6))
    
    # Flatten all non-zero performance values
    all_values = df[cameras].replace(0, np.nan).values.flatten()
    all_values = all_values[~np.isnan(all_values)]  # Remove NaN values

    # Plot histogram (without density normalization)
    plt.hist(all_values, bins=50, alpha=0.6, color='purple', edgecolor='black', density=False, label="Histogram")
    
    plt.xlabel("Performance (%)")
    plt.ylabel("Frequency")  # Y-axis represents frequency (count)
    plt.title("Histogram of the Model")
    plt.legend()
    plt.savefig("plots/abase/combined_camera_histogram.png")
    plt.show()

# Combined distribution curves for all cameras
def plot_combined_distribution_curves(df, cameras):
    plt.figure(figsize=(10, 6))
    
    # Plot KDE for each camera
    for cam in cameras:
        sns.kdeplot(df[cam].replace(0, np.nan), label=cam.replace("_Performance", ""), linewidth=2)
    
    plt.xlabel("Performance (%)")
    plt.ylabel("Density")
    plt.title("Performance Distribution Curves for All Cameras")
    plt.legend(title="Cameras", bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.savefig("plots/abase/combined_camera_distribution_curves.png")
    plt.show()

# Main execution
def main():
    os.makedirs("plots/base", exist_ok=True)  # Ensure plots directory exists
    files = [
        "output/abase_model_morning_camera_performances.csv",
        "output/abase_model_noon_camera_performances.csv",
        "output/abase_model_afternoon_camera_performances.csv"
    ]
    df = load_and_combine(files)
    summary, cameras = process_data(df)
    save_combined_performance(df, "combined_camera_performance.csv")
    
    # Print summary table
    summary_df = pd.DataFrame(summary).T
    print(summary_df)
    
    # Generate plots
    plot_boxplot(df, cameras)
    plot_histograms(df, cameras)
    plot_correlation_heatmap(df, cameras)
    plot_combined_histogram(df, cameras)
    plot_combined_distribution_curves(df, cameras)  # Add this line

if __name__ == "__main__":
    main()