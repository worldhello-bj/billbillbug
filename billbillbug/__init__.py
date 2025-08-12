"""
BillBillBug - Bilibili data scraping toolkit
"""

__version__ = "0.1.0"
__author__ = "BillBillBug Team"
__description__ = "A toolkit for scraping Bilibili data"

from .scraper import BilibiliScraper
from .exporter import DataExporter

__all__ = ['BilibiliScraper', 'DataExporter']