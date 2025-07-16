#!/usr/bin/env python3
"""
Enhanced Stock Tracker - Main Application
A modular stock tracking application with data visualization and analysis.
"""

import argparse
import sys
from stock_data import StockDataManager
from plotter import StockPlotter
from utils import StockUtils

class StockTrackerApp:
    def __init__(self):
        self.data_manager = StockDataManager()
        self.plotter = StockPlotter()
        self.utils = StockUtils()
    
    def run_interactive(self):
        """Run the interactive CLI application"""
        while True:
            self.show_main_menu()
            choice = input("Select an option (1-8): ").strip()
            
            if choice == "1":
                self.track_stocks_6months()
            elif choice == "2":
                self.track_stocks_custom_range()
            elif choice == "3":
                self.manage_favorites()
            elif choice == "4":
                self.view_statistics()
            elif choice == "5":
                self.export_plot()
            elif choice == "6":
                self.clear_cache()
            elif choice == "7":
                self.show_help()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
    
    def show_main_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("ENHANCED STOCK TRACKER")
        print("="*60)
        print("1. Track Stocks (6 months)")
        print("2. Track Stocks (Custom Date Range)")
        print("3. Manage Favorite Stocks")
        print("4. View Statistics")
        print("5. Export Plot")
        print("6. Clear Cached Data")
        print("7. Help")
        print("8. Exit")
        print("="*60)
    
    def track_stocks_6months(self):
        """Track stocks with 6-month data"""
        print("\nSTOCK TRACKING (6 months)")
        print("-" * 40)
        
        symbols = self.utils.get_user_input_symbols()
        if not symbols:
            return
        
        self.process_stock_data(symbols, period="6mo", title="6-Month Stock Price Comparison")
    
    def track_stocks_custom_range(self):
        """Track stocks with custom date range"""
        print("\nCUSTOM DATE RANGE TRACKING")
        print("-" * 40)
        
        start_date, end_date = self.utils.get_date_range()
        if not start_date or not end_date:
            return
        
        symbols = self.utils.get_user_input_symbols()
        if not symbols:
            return
        
        title = f"Stock Price Comparison ({start_date} to {end_date})"
        self.process_stock_data(symbols, start_date=start_date, end_date=end_date, title=title)
    
    def process_stock_data(self, symbols, period="6mo", start_date=None, end_date=None, title="Stock Price Comparison"):
        """Process stock data and display results"""
        print(f"\nDownloading data for {len(symbols)} stocks...")
        
        # Download data
        stock_data = self.data_manager.get_multiple_stocks(symbols, period, start_date, end_date)
        
        if not stock_data:
            print("No data could be downloaded for any stocks.")
            return
        
        # Show download status
        for symbol in symbols:
            status = "OK" if symbol in stock_data else "FAILED"
            print(f"  {status} {symbol}")
        
        # Display statistics
        self.utils.display_stats_table(stock_data)
        
        # Create and show plot
        fig = self.plotter.plot_stocks(stock_data, title)
        
        # Ask if user wants to save
        save_choice = input("\nSave plot as image? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = input("Enter filename (or press Enter for auto-name): ").strip()
            if not filename:
                filename = None
            self.plotter.export_plot(fig, filename)
        
        # Show plot
        try:
            import matplotlib.pyplot as plt
            plt.show()
        except Exception as e:
            print(f"Could not display plot: {e}")
            print("Use --export option to save plots without display")
    
    def manage_favorites(self):
        """Manage favorite stocks"""
        while True:
            favorites = self.utils.get_favorites()
            print(f"\nFAVORITE STOCKS ({len(favorites)} total)")
            print("-" * 40)
            
            if favorites:
                for i, symbol in enumerate(favorites, 1):
                    print(f"{i}. {symbol}")
            else:
                print("No favorite stocks yet.")
            
            print("\n1. Add Favorite")
            print("2. Remove Favorite")
            print("3. Track Favorites")
            print("4. Back to Main Menu")
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == "1":
                symbol = input("Enter stock symbol: ").strip().upper()
                if self.utils.validate_symbol(symbol):
                    if self.utils.add_favorite(symbol):
                        print(f"{symbol} added to favorites")
                    else:
                        print(f"{symbol} is already in favorites")
                else:
                    print("Invalid symbol format")
            
            elif choice == "2":
                if favorites:
                    try:
                        idx = int(input("Enter number to remove: ")) - 1
                        if 0 <= idx < len(favorites):
                            removed = favorites[idx]
                            if self.utils.remove_favorite(removed):
                                print(f"{removed} removed from favorites")
                        else:
                            print("Invalid number")
                    except ValueError:
                        print("Please enter a valid number")
            
            elif choice == "3":
                if favorites:
                    self.process_stock_data(favorites, period="6mo", title="Favorite Stocks - 6-Month Comparison")
                else:
                    print("No favorites to track")
            
            elif choice == "4":
                break
    
    def view_statistics(self):
        """View statistics for specific stocks"""
        print("\nVIEW STATISTICS")
        print("-" * 30)
        
        symbols = self.utils.get_user_input_symbols()
        if not symbols:
            return
        
        stock_data = self.data_manager.get_multiple_stocks(symbols, period="6mo")
        if stock_data:
            self.utils.display_stats_table(stock_data)
            self.utils.create_summary_report(stock_data)
    
    def export_plot(self):
        """Export plot for specific stocks"""
        print("\nEXPORT PLOT")
        print("-" * 20)
        
        symbols = self.utils.get_user_input_symbols()
        if not symbols:
            return
        
        stock_data = self.data_manager.get_multiple_stocks(symbols, period="6mo")
        if stock_data:
            filename = input("Enter filename (without extension): ").strip()
            if not filename:
                filename = None
            
            fig = self.plotter.plot_stocks(stock_data, "Stock Price Comparison")
            self.plotter.export_plot(fig, filename)
    
    def clear_cache(self):
        """Clear all cached data"""
        count = self.data_manager.clear_cache()
        print(f"Cleared {count} cached files")
    
    def show_help(self):
        """Show help information"""
        print("\nHELP & USAGE")
        print("=" * 50)
        print("Stock Tracking:")
        print("  - Enter stock symbols (e.g., AAPL, MSFT, GOOGL)")
        print("  - Data is cached locally for faster future loads")
        print("  - 6-month default period, or custom date range")
        print()
        print("Features:")
        print("  - Real-time stock data from Yahoo Finance")
        print("  - Interactive plots with matplotlib")
        print("  - Comprehensive statistics and analysis")
        print("  - Export plots as high-quality images")
        print("  - Save favorite stocks for quick access")
        print()
        print("Tips:")
        print("  - Use 'done' to finish entering symbols")
        print("  - Dates should be in YYYY-MM-DD format")
        print("  - Cached data speeds up repeated analysis")
        print("  - Use Ctrl+C to cancel any operation")
        print("=" * 50)

def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(
        description="Enhanced Stock Tracker - Analyze and visualize stock data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode
  python main.py --symbols AAPL MSFT --plot
  python main.py --symbols GOOGL --stats
  python main.py --symbols TSLA --export tesla_analysis.png
        """
    )
    
    parser.add_argument("--symbols", nargs="+", help="Stock symbols to analyze")
    parser.add_argument("--period", default="6mo", help="Time period (default: 6mo)")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--plot", action="store_true", help="Show plot")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--export", help="Export plot to file")
    parser.add_argument("--favorites", action="store_true", help="Use favorite stocks")
    
    args = parser.parse_args()
    
    app = StockTrackerApp()
    
    if args.symbols or args.favorites:
        # Command line mode
        if args.favorites:
            symbols = app.utils.get_favorites()
            if not symbols:
                print("No favorite stocks found. Add some in interactive mode first.")
                return
        else:
            symbols = args.symbols
        
        # Validate symbols
        invalid_symbols = [s for s in symbols if not app.utils.validate_symbol(s)]
        if invalid_symbols:
            print(f"Invalid symbols: {', '.join(invalid_symbols)}")
            return
        
        # Get data
        stock_data = app.data_manager.get_multiple_stocks(
            symbols, args.period, args.start, args.end
        )
        
        if not stock_data:
            print("No data could be downloaded.")
            return
        
        # Display results
        if args.stats:
            app.utils.display_stats_table(stock_data)
            app.utils.create_summary_report(stock_data, args.period)
        
        if args.plot or args.export:
            title = f"Stock Price Comparison ({args.period})"
            if args.start and args.end:
                title = f"Stock Price Comparison ({args.start} to {args.end})"
            
            fig = app.plotter.plot_stocks(stock_data, title)
            
            if args.export:
                app.plotter.export_plot(fig, args.export)
            else:
                try:
                    import matplotlib.pyplot as plt
                    plt.show()
                except Exception as e:
                    print(f"Could not display plot: {e}")
                    print("Use --export option to save plots without display")
    else:
        # Interactive mode
        try:
            app.run_interactive()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
