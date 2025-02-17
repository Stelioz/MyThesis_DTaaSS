![banner](https://github.com/user-attachments/assets/c20177e8-4353-40f4-a46f-07faaedcb4c3)

# Public Space Security Management Using Digital Twin Technologies ![version](https://img.shields.io/badge/version-1.0.0-blue.svg)

## Overview
This repository contains the code and resources for **Public Space Security Management Using Digital Twin Technologies** (MSc Thesis). The goal of the project is to create a Digital Twin model for the security management of public spaces, focusing on preventing terrorist attacks. The project uses FlexSim simulation software to model the M2 "Agios Ioannis" metro station in Athens, integrating performance data from security cameras and generating statistical summaries.
<br/><br/>

## Features
- **Digital Twin Model**: A simulated representation of M2 "Agios Ioannis" metro station in Athens for security management.
- **Camera Data Simulation**: Analysis of security camera performance for detecting unusual behavior.
- **Data Processing**: Clean and analyze performance data (e.g., histogram, correlation matrix, camera performance).
- **Statistical Analysis**: Generate key statistics (e.g., best/worst performance, correlation, histogram) for camera performance.
<br/>

## Requirements
- **Python 3.12.7** (or compatible version)
- **Pandas**: For data manipulation and analysis
- **NumPy**: For numerical computations
- **Seaborn**: For statistical plots and visualization
- **Matplotlib**: For general plotting and data visualization
<br/>

## Installation
1. **Clone the repository**:  
   Open your terminal and run the following command to clone the repository to your local machine:
   ```bash
   git clone https://github.com/Stelioz/MyThesis_DTaaSS.git
   cd MyThesis_DTaaSS
   ```

2. **Create a Virtual Environment** (Recommended):  
   It is recommended to create a virtual environment to manage dependencies cleanly:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   .\venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**:  
   Install all required packages using the provided `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
   If you encounter issues, try upgrading pip:
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Verify Installation**:  
   Ensure all dependencies are correctly installed by running:
   ```bash
   python -c "import pandas as pd; import numpy as np; import seaborn as sns; import matplotlib.pyplot as plt; print('All dependencies are installed correctly!')"
   ```
<br/>

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
<br/>

## Contributing
If you would like to contribute, please fork the repository, make changes, and create a pull request.
<br/><br/>

## Special thanks
For the development of this project, we used [FlexSim](https://www.flexsim.com/) (Student License) from FlexSim Software Products, Inc. and we want to thank them for their support. Also we would like to thank Mr. Krystian Kogut, International Sales Director and Board Member of [InterMarium](https://www.flexsim.com/contacts/intermarium/) for their help in acquiring the License.
<br/><br/>

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
