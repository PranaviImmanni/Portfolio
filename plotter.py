import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class StockPlotter:
    def __init__(self):
        self.setup_style()
    
    def setup_style(self):
        """Setup matplotlib style for better looking plots"""
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
    
    def plot_stocks(self, stock_data_dict, title="Stock Price Comparison", 
                   show_volume=False, save_path=None):
        """Plot multiple stocks on one graph"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Plot each stock
        for symbol, data in stock_data_dict.items():
            if data is not None and not data.empty:
                ax.plot(data.index, data['Close'], label=symbol, linewidth=2)
        
        # Customize the plot
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Closing Price ($)', fontsize=12)
        ax.legend(fontsize=10, loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved as {save_path}")
        
        return fig
    
    def plot_with_volume(self, stock_data_dict, title="Stock Price with Volume"):
        """Plot stocks with volume bars"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), 
                                      gridspec_kw={'height_ratios': [3, 1]})
        
        # Plot price data
        for symbol, data in stock_data_dict.items():
            if data is not None and not data.empty:
                ax1.plot(data.index, data['Close'], label=symbol, linewidth=2)
        
        ax1.set_title(title, fontsize=16, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=12)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Plot volume data (use first stock's volume)
        first_symbol = list(stock_data_dict.keys())[0]
        first_data = stock_data_dict[first_symbol]
        if first_data is not None and not first_data.empty:
            ax2.bar(first_data.index, first_data['Volume'], alpha=0.6, color='gray')
            ax2.set_xlabel('Date', fontsize=12)
            ax2.set_ylabel('Volume', fontsize=12)
            ax2.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def plot_performance_comparison(self, stock_data_dict, title="Performance Comparison"):
        """Plot normalized performance comparison (starting at 100)"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for symbol, data in stock_data_dict.items():
            if data is not None and not data.empty:
                # Normalize to starting price
                normalized = (data['Close'] / data['Close'].iloc[0]) * 100
                ax.plot(data.index, normalized, label=symbol, linewidth=2)
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Performance (Base=100)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=100, color='black', linestyle='--', alpha=0.5)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def create_summary_plot(self, stock_data_dict, title="Stock Summary"):
        """Create a comprehensive summary plot with multiple subplots"""
        num_stocks = len(stock_data_dict)
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # Price comparison
        ax1 = axes[0, 0]
        for symbol, data in stock_data_dict.items():
            if data is not None and not data.empty:
                ax1.plot(data.index, data['Close'], label=symbol, linewidth=2)
        ax1.set_title('Price Comparison')
        ax1.set_ylabel('Price ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Performance comparison
        ax2 = axes[0, 1]
        for symbol, data in stock_data_dict.items():
            if data is not None and not data.empty:
                normalized = (data['Close'] / data['Close'].iloc[0]) * 100
                ax2.plot(data.index, normalized, label=symbol, linewidth=2)
        ax2.set_title('Performance Comparison (Base=100)')
        ax2.set_ylabel('Performance')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=100, color='black', linestyle='--', alpha=0.5)
        
        # Volume (first stock only)
        ax3 = axes[1, 0]
        first_symbol = list(stock_data_dict.keys())[0]
        first_data = stock_data_dict[first_symbol]
        if first_data is not None and not first_data.empty:
            ax3.bar(first_data.index, first_data['Volume'], alpha=0.6, color='blue')
            ax3.set_title(f'Volume - {first_symbol}')
            ax3.set_ylabel('Volume')
            ax3.grid(True, alpha=0.3)
        
        # Price distribution
        ax4 = axes[1, 1]
        for symbol, data in stock_data_dict.items():
            if data is not None and not data.empty:
                ax4.hist(data['Close'], bins=20, alpha=0.6, label=symbol)
        ax4.set_title('Price Distribution')
        ax4.set_xlabel('Price ($)')
        ax4.set_ylabel('Frequency')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def export_plot(self, fig, filename=None, format='png', dpi=300):
        """Export plot to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"stock_plot_{timestamp}.{format}"
        
        fig.savefig(filename, dpi=dpi, bbox_inches='tight', format=format)
        print(f"Plot exported as {filename}")
        return filename 