import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load CSV File
def load_data(file):
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

# Box plot for performance distribution
def plot_boxplot(df, cameras, plot_dir):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df[cameras].replace(0, np.nan), showfliers=False)
    
    # Remove "_Performance" from x-axis labels
    plt.xticks(ticks=range(len(cameras)), labels=[cam.replace("_Performance", "") for cam in cameras], rotation=-45)
    
    plt.xlabel("Cameras")
    plt.ylabel("Performance (%)")
    plt.title("Camera Performance Distribution")
    plt.savefig(os.path.join(plot_dir, "camera_performance_boxplot.png"))
    plt.show()

# Histogram plot for performance distribution per camera
def plot_histograms(df, cameras, plot_dir):
    for cam in cameras:
        plt.figure(figsize=(8, 5))
        plt.hist(df[cam].replace(0, np.nan), bins=30, alpha=0.6, color='blue', edgecolor='black', density=True, label="Histogram")
        sns.kdeplot(df[cam].replace(0, np.nan), color='red', linewidth=2, label="Curve")
        
        # Remove "_Performance" from the title
        plt.xlabel("Performance (%)")
        plt.ylabel("Density")
        plt.title(f"Histogram & Distribution of {cam.replace('_Performance', '')}")
        plt.legend()
        plt.savefig(os.path.join(plot_dir, f"histogram_{cam.replace('_Performance', '')}.png"))
        plt.show()

# Combined histogram for all cameras
def plot_combined_histogram(df, cameras, plot_dir):
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
    plt.savefig(os.path.join(plot_dir, "combined_camera_histogram.png"))
    plt.show()

# Correlation heatmap
def plot_correlation_heatmap(df, cameras, plot_dir):
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
    plt.savefig(os.path.join(plot_dir, "camera_performance_correlation_heatmap.png"))
    plt.show()

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
    
    # Create a directory for plots
    plot_dir = os.path.join("plots", model_type)
    os.makedirs(plot_dir, exist_ok=True)
    
    # Single file per model
    file = f"output/{model_type}_camera_performances.csv"
    print(f"\nLoading file: {file}")
    
    # Check if file exists
    if not os.path.exists(file):
        print(f"Error: File not found -> {file}")
        return
    
    df = load_data(file)
    summary, cameras = process_data(df)
    
    # Print summary table
    summary_df = pd.DataFrame(summary).T
    print("\nSummary of Camera Performances:")
    print(summary_df)
    
    # Generate plots
    plot_boxplot(df, cameras, plot_dir)
    plot_histograms(df, cameras, plot_dir)
    plot_combined_histogram(df, cameras, plot_dir)
    plot_correlation_heatmap(df, cameras, plot_dir)

if __name__ == "__main__":
    main()
