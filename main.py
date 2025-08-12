#!/usr/bin/env python3
"""
BillBillBug - Main entry point
A tool for scraping Bilibili UP master video information
"""

import sys
import os

# Add the package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from billbillbug.cli import main

if __name__ == '__main__':
    main()