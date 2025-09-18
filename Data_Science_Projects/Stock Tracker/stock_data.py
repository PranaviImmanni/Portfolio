import yfinance as yf
import pandas as pd
import os
from datetime import datetime

class StockDataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_stock_data(self, symbol, period="6mo", start_date=None, end_date=None):
        """Download stock data with caching"""
        symbol = symbol.upper()
        cache_file = os.path.join(self.data_dir, f"{symbol}.csv")
        
        # Check if cached data exists
        if os.path.exists(cache_file):
            try:
                cached_data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
                if not cached_data.empty:
                    return cached_data
            except Exception:
                pass  # If cache is corrupted, download fresh data
        
        # Download fresh data
        try:
            stock = yf.Ticker(symbol)
            if start_date and end_date:
                data = stock.history(start=start_date, end=end_date)
            else:
                data = stock.history(period=period)
            
            if not data.empty:
                # Save to cache
                data.to_csv(cache_file)
                return data
            else:
                print(f"No data found for {symbol}")
                return None
        except Exception as e:
            print(f"Error downloading data for {symbol}: {e}")
            return None
    
    def get_multiple_stocks(self, symbols, period="6mo", start_date=None, end_date=None):
        """Download data for multiple stocks"""
        stock_data = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol, period, start_date, end_date)
            if data is not None:
                stock_data[symbol] = data
        return stock_data
    
    def clear_cache(self):
        """Clear all cached data"""
        if os.path.exists(self.data_dir):
            files = os.listdir(self.data_dir)
            csv_files = [f for f in files if f.endswith('.csv')]
            for file in csv_files:
                os.remove(os.path.join(self.data_dir, file))
            return len(csv_files)
        return 0
    
    def get_cache_info(self):
        """Get information about cached files"""
        if not os.path.exists(self.data_dir):
            return []
        
        cache_info = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.csv'):
                symbol = file.replace('.csv', '')
                file_path = os.path.join(self.data_dir, file)
                size = os.path.getsize(file_path)
                modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                cache_info.append({
                    'symbol': symbol,
                    'size': size,
                    'modified': modified
                })
        return cache_info 