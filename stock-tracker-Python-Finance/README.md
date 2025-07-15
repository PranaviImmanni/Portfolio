# Stock Tracker — Python Finance Project

A robust, modular Python application for tracking, analyzing, and visualizing stock market data.

## Motivation
Financial data analysis is essential for investors, analysts, and anyone interested in understanding market trends. This project was created to provide a user-friendly, extensible tool for fetching, analyzing, and visualizing stock data using Python. It is suitable for both beginners and professionals who want to explore, compare, and report on stock performance.

## Overview
Stock Tracker enables users to fetch historical stock prices for multiple companies, generate insightful visualizations, and compute detailed summary statistics. The tool is designed for finance enthusiasts, students, and data professionals interested in programmatic stock analysis.

## Key Features
- Fetch historical stock data for any number of companies (using Yahoo Finance)
- Visualize price trends, comparisons, and normalized performance charts
- Generate summary statistics: max, min, average, percent change, volatility, and more
- Export plots as high-quality PNG images for reports or presentations
- Interactive command-line interface (CLI) for easy use
- Modular, well-documented codebase for easy extension and customization
- Local data caching for faster repeated analysis

## Technologies Used
- **Python 3.7+**
- **pandas** — Data manipulation and analysis
- **matplotlib** — Data visualization
- **yfinance** — Stock data retrieval
- **numpy** — Numerical calculations

## Setup & Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/PranaviImmanni/Portfolio.git
   cd Portfolio/stock-tracker-Python-Finance
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python main.py
   ```

## Usage
- Use the interactive CLI to select stocks, date ranges, and view statistics.
- Visualizations and statistics are generated automatically and can be exported.
- Sample data is provided in the `data/` folder for demonstration.

### Example CLI Commands
- **Track multiple stocks for the last 6 months:**
  ```bash
  python main.py --symbols AAPL MSFT GOOGL
  ```
- **Show statistics only:**
  ```bash
  python main.py --symbols TSLA AMZN --stats
  ```
- **Export a plot to file:**
  ```bash
  python main.py --symbols AAPL MSFT --export my_plot.png
  ```
- **Custom date range:**
  ```bash
  python main.py --symbols AAPL --start 2023-01-01 --end 2023-12-31 --plot
  ```

## Workflow
1. **Select stocks and date range** via CLI or interactive menu.
2. **Fetch data** from Yahoo Finance (or load from cache if available).
3. **Analyze data**: compute statistics, trends, and comparisons.
4. **Visualize results**: generate plots and tables.
5. **Export**: save plots as images for reports or presentations.

## File Structure
- `main.py` — Application entry point and CLI
- `stock_data.py` — Stock data fetching and caching
- `plotter.py` — Visualization and plotting utilities
- `utils.py` — Helper functions
- `data/` — Sample CSV files with stock data
- `images/` — Generated plots and visualizations
- `requirements.txt` — Python dependencies

## Example Output
![Stock Analysis Example](images/stock_analysis.png)

---

## Extensibility & Contributing
- The codebase is modular and well-documented, making it easy to add new features (e.g., technical indicators, new data sources, or advanced visualizations).
- Contributions, suggestions, and bug reports are welcome! Please open an issue or submit a pull request.

<<<<<<< HEAD
## License
MIT License
=======
>>>>>>> 9540f8865315322c0881bc5e5e7fb82e0e93534c

---

**Questions or suggestions?**  
Email: pranavi@immanni.com  
[LinkedIn: Pranavi Immanni](https://www.linkedin.com/in/pranavi-immanni-ab04a823b)
