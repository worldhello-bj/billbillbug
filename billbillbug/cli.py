"""
Command line interface for BillBillBug
"""

import argparse
import sys
import os
from .scraper import BilibiliScraper
from .exporter import DataExporter


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="BillBillBug - Bilibili UP master video scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --uid 123456                    # Scrape all videos for UID 123456
  %(prog)s --uid 123456 --max-videos 50    # Scrape first 50 videos
  %(prog)s --uid 123456 --format json      # Export to JSON format
  %(prog)s --uid 123456 --output ./data/   # Save to specific directory
  %(prog)s --uid 123456 --delay 2          # Add 2-second delay between requests
        """
    )
    
    parser.add_argument(
        '--uid', 
        required=True,
        help='Bilibili UP master UID (required)'
    )
    
    parser.add_argument(
        '--max-videos',
        type=int,
        help='Maximum number of videos to scrape (default: all videos)'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'csv', 'both'],
        default='both',
        help='Output format (default: both)'
    )
    
    parser.add_argument(
        '--output',
        default='./output/',
        help='Output directory (default: ./output/)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between API requests in seconds (default: 1.0)'
    )
    
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Generate a summary report in addition to data export'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Reduce output verbosity'
    )
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    if not args.quiet:
        print("=== BillBillBug - Bilibili Video Scraper ===")
        print(f"Target UID: {args.uid}")
        print(f"Max videos: {args.max_videos if args.max_videos else 'All'}")
        print(f"Output format: {args.format}")
        print(f"Output directory: {args.output}")
        print(f"Request delay: {args.delay}s")
        print("=" * 50)
    
    # Initialize scraper
    scraper = BilibiliScraper(delay=args.delay)
    
    # Scrape data
    try:
        data = scraper.scrape_up_master(args.uid, args.max_videos)
        
        if not data:
            print("Failed to scrape data. Please check the UID and try again.")
            sys.exit(1)
            
        # Export data
        exporter = DataExporter()
        exported_files = []
        
        if args.format in ['json', 'both']:
            json_file = os.path.join(args.output, f"videos_{args.uid}.json")
            exporter.export_to_json(data, json_file)
            exported_files.append(json_file)
        
        if args.format in ['csv', 'both']:
            csv_file = os.path.join(args.output, f"videos_{args.uid}.csv")
            exporter.export_to_csv(data, csv_file)
            exported_files.append(csv_file)
            
            # Also export user info
            user_csv_file = os.path.join(args.output, f"user_{args.uid}.csv")
            exporter.export_user_info_csv(data, user_csv_file)
            exported_files.append(user_csv_file)
        
        if args.summary:
            summary_file = os.path.join(args.output, f"summary_{args.uid}.txt")
            exporter.export_summary_txt(data, summary_file)
            exported_files.append(summary_file)
        
        if not args.quiet:
            print("\n=== Scraping Complete ===")
            print(f"UP Master: {data.get('user_info', {}).get('name', 'Unknown')}")
            print(f"Total videos scraped: {data.get('total_videos', 0)}")
            print("Files created:")
            for file in exported_files:
                print(f"  - {file}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()