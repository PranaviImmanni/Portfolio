# Dataset Information

## EV Sensors: Driving Pattern Diagnostics (2020-24)

### Dataset Source
**Kaggle Dataset**: [EV Sensors: Driving Pattern Diagnostics (2020-24)](https://www.kaggle.com/datasets/...)

### Overview
This dataset contains detailed hourly electric vehicle (EV) telemetry data collected from four unique EVs driven under distinct usage profiles:
- **Rare User**: Minimal usage patterns
- **Moderate User**: Average usage patterns
- **Heavy User**: Intensive usage patterns
- **Regular User**: Consistent usage patterns

### Dataset Details
- **Time Period**: January 1, 2020 to December 31, 2024
- **Resolution**: Hourly data
- **Records per Vehicle**: 43,200 time-stamped entries
- **Total Records**: 172,800 entries (4 vehicles × 43,200)

### Files Included
1. `rare_user.csv` - Rare user telemetry data
2. `moderate_user.csv` - Moderate user telemetry data
3. `heavy_user.csv` - Heavy user telemetry data
4. `regular_user.csv` - Regular user telemetry data

### Dataset Purpose
The goal of this dataset is to:
- Analyze driving patterns across different usage profiles
- Detect early warning signs of system faults
- Forecast upcoming Diagnostic Trouble Codes (DTCs) using sensor-based historical data
- Enable predictive maintenance for EV components

### Sensor Data Features
The dataset includes various EV sensor readings such as:
- Battery voltage and temperature
- Motor temperature
- Charging current
- Vehicle speed and mileage
- State of charge (SOC)
- Cooling system temperature
- And other telemetry metrics

### Usage in This Project

#### Loading the Dataset
```python
from data.data_loader import EVDatasetLoader

# Initialize loader
loader = EVDatasetLoader(data_dir="data/raw")

# Load all user types
df = loader.load_and_preprocess()

# Or load specific user type
df_rare = loader.load_dataset(user_type="rare_user")
```

#### Preprocessing
The dataset loader automatically:
- Converts timestamps to datetime format
- Standardizes column names
- Maps common column variations
- Creates vehicle IDs if missing
- Handles missing values

#### Creating Training Data
```python
# Create training data with failure labels
training_df = loader.create_training_data(df)
```

### Integration with Project

The real dataset can be used instead of synthetic data by:

1. **Download the dataset from Kaggle**
   ```bash
   # Place the CSV files in data/raw/
   data/raw/rare_user.csv
   data/raw/moderate_user.csv
   data/raw/heavy_user.csv
   data/raw/regular_user.csv
   ```

2. **Run with real data flag**
   ```bash
   # Train models with real data
   python main.py --mode train --use-real-data
   
   # Run analytics with real data
   python main.py --mode analytics --use-real-data
   ```

3. **Or use the data loader directly**
   ```bash
   python data/data_loader.py
   ```

### Dataset Citation
If using this dataset, please cite the original Kaggle dataset source:
```
EV Sensors: Driving Pattern Diagnostics (2020-24)
Kaggle Dataset
https://www.kaggle.com/datasets/...
```

### Synthetic Data Fallback
If the real dataset is not available, the project will automatically fall back to synthetic data generation using the `SampleDataGenerator` class.

### Data Privacy
This dataset contains simulated telemetry data and does not contain personally identifiable information (PII) or real vehicle identification numbers.

