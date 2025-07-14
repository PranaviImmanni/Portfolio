import json
import os
from datetime import datetime
import pandas as pd

class StockUtils:
    def __init__(self, favorites_file="favorites.json"):
        self.favorites_file = favorites_file
        self.favorites = self.load_favorites()
    
    def load_favorites(self):
        """Load favorite stocks from JSON file"""
        try:
            with open(self.favorites_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_favorites(self):
        """Save favorite stocks to JSON file"""
        with open(self.favorites_file, 'w') as f:
            json.dump(self.favorites, f, indent=2)
    
    def add_favorite(self, symbol):
        """Add a stock to favorites"""
        symbol = symbol.upper()
        if symbol not in self.favorites:
            self.favorites.append(symbol)
            self.save_favorites()
            return True
        return False
    
    def remove_favorite(self, symbol):
        """Remove a stock from favorites"""
        symbol = symbol.upper()
        if symbol in self.favorites:
            self.favorites.remove(symbol)
            self.save_favorites()
            return True
        return False
    
    def get_favorites(self):
        """Get list of favorite stocks"""
        return self.favorites.copy()
    
    def calculate_stats(self, data):
        """Calculate comprehensive statistics for stock data"""
        if data is None or data.empty:
            return None
        
        close_prices = data['Close']
        volume = data['Volume'] if 'Volume' in data.columns else None
        
        stats = {
            'current': close_prices.iloc[-1],
            'max': close_prices.max(),
            'min': close_prices.min(),
            'avg': close_prices.mean(),
            'std': close_prices.std(),
            'change': close_prices.iloc[-1] - close_prices.iloc[0],
            'change_pct': ((close_prices.iloc[-1] - close_prices.iloc[0]) / close_prices.iloc[0]) * 100,
            'days': len(close_prices),
            'volatility': close_prices.std() / close_prices.mean() * 100
        }
        
        if volume is not None:
            stats['avg_volume'] = volume.mean()
            stats['max_volume'] = volume.max()
        
        return stats
    
    def display_stats_table(self, stock_data_dict):
        """Display formatted statistics table"""
        print("\n" + "="*100)
        print("STOCK STATISTICS")
        print("="*100)
        print(f"{'Symbol':<8} {'Current':<10} {'Max':<10} {'Min':<10} {'Avg':<10} "
              f"{'Change':<10} {'Change%':<8} {'Volatility':<10}")
        print("-"*100)
        
        for symbol, data in stock_data_dict.items():
            stats = self.calculate_stats(data)
            if stats:
                change_indicator = "+" if stats['change'] >= 0 else "-"
                print(f"{symbol:<8} ${stats['current']:<9.2f} ${stats['max']:<9.2f} "
                      f"${stats['min']:<9.2f} ${stats['avg']:<9.2f} "
                      f"${stats['change']:<9.2f} {change_indicator}{stats['change_pct']:<6.1f}% "
                      f"{stats['volatility']:<9.1f}%")
        
        print("="*100)
    
    def validate_symbol(self, symbol):
        """Basic validation for stock symbols"""
        if not symbol or len(symbol) > 10:
            return False
        # Check if symbol contains only letters and dots
        return symbol.replace('.', '').isalpha()
    
    def validate_date(self, date_str):
        """Validate date string format YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def format_currency(self, amount):
        """Format currency with proper formatting"""
        if amount >= 1_000_000:
            return f"${amount/1_000_000:.2f}M"
        elif amount >= 1_000:
            return f"${amount/1_000:.2f}K"
        else:
            return f"${amount:.2f}"
    
    def format_percentage(self, value):
        """Format percentage with indicators"""
        if value >= 0:
            return f"+{value:.2f}%"
        else:
            return f"{value:.2f}%"
    
    def get_user_input_symbols(self):
        """Get stock symbols from user input"""
        symbols = []
        print("Enter stock symbols (one per line, or 'done' to finish):")
        print("Examples: AAPL, MSFT, GOOGL")
        
        while True:
            symbol = input("Symbol: ").strip().upper()
            if symbol.lower() == 'done':
                break
            if symbol:
                if self.validate_symbol(symbol):
                    symbols.append(symbol)
                else:
                    print("Invalid symbol format. Use letters only (e.g., AAPL)")
        
        return symbols
    
    def get_date_range(self):
        """Get custom date range from user"""
        print("\nEnter date range (YYYY-MM-DD format):")
        
        while True:
            start_date = input("Start date: ").strip()
            if not start_date:
                return None, None
            
            if not self.validate_date(start_date):
                print("Invalid date format. Use YYYY-MM-DD")
                continue
            
            end_date = input("End date: ").strip()
            if not self.validate_date(end_date):
                print("Invalid date format. Use YYYY-MM-DD")
                continue
            
            # Check if start is before end
            if datetime.strptime(start_date, "%Y-%m-%d") >= datetime.strptime(end_date, "%Y-%m-%d"):
                print("Start date must be before end date")
                continue
            
            return start_date, end_date
    
    def create_summary_report(self, stock_data_dict, period="6 months"):
        """Create a comprehensive summary report"""
        print(f"\nSTOCK ANALYSIS REPORT - {period.upper()}")
        print("="*60)
        
        total_stocks = len(stock_data_dict)
        successful_downloads = len([d for d in stock_data_dict.values() if d is not None])
        
        print(f"Stocks analyzed: {successful_downloads}/{total_stocks}")
        print(f"Analysis period: {period}")
        print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Calculate overall statistics
        all_changes = []
        for data in stock_data_dict.values():
            if data is not None and not data.empty:
                change_pct = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                all_changes.append(change_pct)
        
        if all_changes:
            avg_change = sum(all_changes) / len(all_changes)
            best_performer = max(all_changes)
            worst_performer = min(all_changes)
            
            print(f"Average performance: {self.format_percentage(avg_change)}")
            print(f"Best performer: {self.format_percentage(best_performer)}")
            print(f"Worst performer: {self.format_percentage(worst_performer)}")
        
        print("="*60) 