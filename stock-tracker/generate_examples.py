#!/usr/bin/env python3
"""
Example Plot Generator for Stock Tracker
This script generates sample plots to demonstrate the project's capabilities.
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from stock_data import StockDataManager
from plotter import StockPlotter
from utils import StockUtils
import os

def generate_example_plots():
    """Generate example plots and save them to a single file"""
    
    print("Generating example plots...")
    
    # Initialize components
    data_manager = StockDataManager()
    plotter = StockPlotter()
    utils = StockUtils()
    
    # Sample stocks for demonstration
    sample_stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
    
    # Download data
    print("Downloading sample data...")
    stock_data = data_manager.get_multiple_stocks(sample_stocks, period="6mo")
    
    if not stock_data:
        print("Failed to download data. Please check your internet connection.")
        return
    
    # Create a comprehensive example file
    create_comprehensive_example(stock_data, plotter, utils)
    
    print("Example plots generated successfully!")
    print("Check 'stock_tracker_examples.png' for all visualizations")

def create_comprehensive_example(stock_data, plotter, utils):
    """Create a comprehensive example with multiple plot types"""
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 24))
    gs = gridspec.GridSpec(4, 2, figure=fig, height_ratios=[1, 1, 1, 1])
    
    # 1. Basic Price Comparison
    ax1 = fig.add_subplot(gs[0, :])
    for symbol, data in stock_data.items():
        if data is not None and not data.empty:
            ax1.plot(data.index, data['Close'], label=symbol, linewidth=2)
    ax1.set_title('Stock Price Comparison (6 Months)', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Closing Price ($)', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Performance Comparison (Normalized)
    ax2 = fig.add_subplot(gs[1, 0])
    for symbol, data in stock_data.items():
        if data is not None and not data.empty:
            normalized = (data['Close'] / data['Close'].iloc[0]) * 100
            ax2.plot(data.index, normalized, label=symbol, linewidth=2)
    ax2.set_title('Performance Comparison (Base=100)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Performance (%)', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=100, color='black', linestyle='--', alpha=0.5)
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Volume Analysis (First stock)
    ax3 = fig.add_subplot(gs[1, 1])
    first_symbol = list(stock_data.keys())[0]
    first_data = stock_data[first_symbol]
    if first_data is not None and not first_data.empty:
        ax3.bar(first_data.index, first_data['Volume'], alpha=0.6, color='blue')
        ax3.set_title(f'Volume Analysis - {first_symbol}', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Volume', fontsize=12)
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
    
    # 4. Price Distribution
    ax4 = fig.add_subplot(gs[2, 0])
    for symbol, data in stock_data.items():
        if data is not None and not data.empty:
            ax4.hist(data['Close'], bins=20, alpha=0.6, label=symbol)
    ax4.set_title('Price Distribution', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Price ($)', fontsize=12)
    ax4.set_ylabel('Frequency', fontsize=12)
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    # 5. Statistics Table (Text)
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.axis('off')
    
    # Create statistics text
    stats_text = "STOCK STATISTICS\n"
    stats_text += "=" * 50 + "\n"
    stats_text += f"{'Symbol':<8} {'Current':<10} {'Change%':<8} {'Volatility':<10}\n"
    stats_text += "-" * 50 + "\n"
    
    for symbol, data in stock_data.items():
        stats = utils.calculate_stats(data)
        if stats:
            change_indicator = "+" if stats['change'] >= 0 else "-"
            stats_text += f"{symbol:<8} ${stats['current']:<9.2f} {change_indicator}{stats['change_pct']:<6.1f}% {stats['volatility']:<9.1f}%\n"
    
    stats_text += "=" * 50 + "\n"
    stats_text += "\nKey Metrics:\n"
    stats_text += "• Current: Latest closing price\n"
    stats_text += "• Change%: Total return over period\n"
    stats_text += "• Volatility: Price variation (std/mean)\n"
    
    ax5.text(0.05, 0.95, stats_text, transform=ax5.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    
    # 6. Feature Overview
    ax6 = fig.add_subplot(gs[3, :])
    ax6.axis('off')
    
    features_text = "ENHANCED STOCK TRACKER - FEATURES\n"
    features_text += "=" * 60 + "\n\n"
    features_text += "Core Features:\n"
    features_text += "• Multi-stock tracking and comparison\n"
    features_text += "• Real-time data from Yahoo Finance\n"
    features_text += "• Interactive plots with matplotlib\n"
    features_text += "• Comprehensive statistics and analysis\n\n"
    features_text += "Advanced Features:\n"
    features_text += "• Local data caching (CSV files)\n"
    features_text += "• Custom date range selection\n"
    features_text += "• Favorite stocks management\n"
    features_text += "• High-quality plot export\n"
    features_text += "• Modular, maintainable architecture\n\n"
    features_text += "Usage Examples:\n"
    features_text += "• Interactive: python main.py\n"
    features_text += "• Quick analysis: python main.py --symbols AAPL MSFT --stats --plot\n"
    features_text += "• Export: python main.py --symbols TSLA --export analysis.png\n"
    features_text += "• Custom dates: python main.py --symbols AAPL --start 2023-01-01 --end 2023-12-31\n"
    
    ax6.text(0.05, 0.95, features_text, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('stock_tracker_examples.png', dpi=300, bbox_inches='tight')
    print("Comprehensive example saved as 'stock_tracker_examples.png'")

def create_simple_examples():
    """Create simple individual example plots"""
    
    print("Creating simple example plots...")
    
    # Initialize components
    data_manager = StockDataManager()
    plotter = StockPlotter()
    
    # Sample data
    sample_stocks = ['AAPL', 'MSFT']
    stock_data = data_manager.get_multiple_stocks(sample_stocks, period="3mo")
    
    if not stock_data:
        print("Failed to download data.")
        return
    
    # 1. Basic price comparison
    fig1 = plotter.plot_stocks(stock_data, "Basic Stock Price Comparison")
    plotter.export_plot(fig1, "example_basic_comparison.png")
    
    # 2. Performance comparison
    fig2 = plotter.plot_performance_comparison(stock_data, "Performance Comparison")
    plotter.export_plot(fig2, "example_performance.png")
    
    # 3. Summary plot
    fig3 = plotter.create_summary_plot(stock_data, "Stock Summary")
    plotter.export_plot(fig3, "example_summary.png")
    
    print("Simple examples created:")
    print("- example_basic_comparison.png")
    print("- example_performance.png") 
    print("- example_summary.png")

if __name__ == "__main__":
    print("Stock Tracker - Example Plot Generator")
    print("=" * 50)
    
    # Create comprehensive example
    generate_example_plots()
    
    # Create simple examples
    create_simple_examples()
    
    print("\nAll example plots generated successfully!")
    print("Check the current directory for the generated PNG files.") 