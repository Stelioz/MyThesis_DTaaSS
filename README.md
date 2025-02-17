# [Public Space Security Management Using Digital Twin Technologies] ![version](https://img.shields.io/badge/version-1.0.0-blue.svg)

## Overview
This repository contains the code and resources for **Public Space Security Management Using Digital Twin Technologies** (MSc Thesis). The goal of the project is to create a Digital Twin model for the security management of public spaces, focusing on preventing terrorist attacks. The project uses FlexSim simulation software to model the M2 "Agios Ioannis" metro station in Athens, integrating performance data from security cameras and generating statistical summaries.

## Features
- **Digital Twin Model**: A simulated representation of M2 "Agios Ioannis" metro station in Athens for security management.
- **Camera Data Simulation**: Analysis of security camera performance for detecting unusual behavior.
- **Data Processing**: Clean and analyze performance data (e.g., histogram, correlation matrix, camera performance).
- **Statistical Analysis**: Generate key statistics (e.g., best/worst performance, correlation, histogram) for camera performance.

## Requirements
- **Python 3.12.7** (or compatible version)
- **Pandas**: For data manipulation and analysis
- **NumPy**: For numerical computations
- **Seaborn**: For statistical plots and visualization
- **Matplotlib**: For general plotting and data visualization

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Stelioz/MyThesis_DTaaSS.git
   cd MyThesis_DTaaSS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Data Collection**: Run the scripts to load and combine CSV files of camera performance data.
2. **Data Processing**: The project processes this data to clean up zero values and generate statistical summaries.
3. **Visualizations**: It includes generating:
   - **Boxplots**
   - **Histograms**
   - **Correlation matrices**
4. The final output includes:
   - **Combined Performance Data**
   - **Summary Statistics**
   - **Visualizations** stored in the `plots` directory.

## Contributing
If you would like to contribute, please fork the repository, make changes, and create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
