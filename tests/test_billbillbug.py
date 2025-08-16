#!/usr/bin/env python3
"""
Simple tests for BillBillBug functionality
"""

import os
import sys
import unittest
import tempfile
import json
from datetime import datetime

# Add the package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from billbillbug.exporter import DataExporter
from billbillbug.scraper import BilibiliScraper


class TestDataExporter(unittest.TestCase):
    """Test the DataExporter functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = {
            'user_info': {
                'mid': 123456,
                'name': 'Test UP Master',
                'level': 5,
                'fans': 10000
            },
            'videos': [
                {
                    'title': 'Test Video 1',
                    'bvid': 'BV1test001',
                    'aid': 1001,
                    'play': 5000,
                    'video_review': 100,
                    'favorites': 200,
                    'created': '2024-01-01 12:00:00'
                },
                {
                    'title': 'Test Video 2',
                    'bvid': 'BV1test002',
                    'aid': 1002,
                    'play': 3000,
                    'video_review': 50,
                    'favorites': 150,
                    'created': '2024-01-02 15:30:00'
                }
            ],
            'total_videos': 2,
            'scrape_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.exporter = DataExporter()
        
    def test_export_to_json(self):
        """Test JSON export functionality"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
            
        try:
            result_file = self.exporter.export_to_json(self.test_data, temp_file)
            
            # Check that file was created
            self.assertTrue(os.path.exists(result_file))
            self.assertEqual(result_file, temp_file)
            
            # Check file content
            with open(result_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                
            self.assertEqual(loaded_data['user_info']['name'], 'Test UP Master')
            self.assertEqual(len(loaded_data['videos']), 2)
            self.assertEqual(loaded_data['videos'][0]['title'], 'Test Video 1')
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_export_to_csv(self):
        """Test CSV export functionality"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
            
        try:
            result_file = self.exporter.export_to_csv(self.test_data, temp_file)
            
            # Check that file was created
            self.assertTrue(os.path.exists(result_file))
            self.assertEqual(result_file, temp_file)
            
            # Check file content
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.assertIn('Test Video 1', content)
            self.assertIn('Test Video 2', content)
            self.assertIn('BV1test001', content)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_export_summary_txt(self):
        """Test summary text export functionality"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name
            
        try:
            result_file = self.exporter.export_summary_txt(self.test_data, temp_file)
            
            # Check that file was created
            self.assertTrue(os.path.exists(result_file))
            
            # Check file content
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.assertIn('Bilibili UP Master Video Summary', content)
            self.assertIn('Test UP Master', content)
            self.assertIn('Total Videos: 2', content)
            self.assertIn('Test Video 1', content)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestBilibiliScraper(unittest.TestCase):
    """Test the BilibiliScraper functionality"""
    
    def test_scraper_initialization(self):
        """Test scraper initialization"""
        scraper = BilibiliScraper(delay=2.0)
        self.assertEqual(scraper.delay, 2.0)
        self.assertIsNotNone(scraper.session)
        
    def test_wbi_mixin_key_generation(self):
        """Test WBI mixin key generation"""
        scraper = BilibiliScraper()
        
        # Test data from official documentation
        img_key = "7cd084941338484aae1ad9425b84077c"
        sub_key = "4932caff0ff746eab6f01bf08b70ac45"
        expected_mixin = "ea1db124af3c7062474693fa704f4ff8"
        
        mixin_key = scraper._get_mixin_key(img_key, sub_key)
        self.assertEqual(mixin_key, expected_mixin)
        
    def test_wbi_params_signing(self):
        """Test WBI parameter signing"""
        scraper = BilibiliScraper()
        
        # Mock WBI keys
        img_key = "7cd084941338484aae1ad9425b84077c"
        sub_key = "4932caff0ff746eab6f01bf08b70ac45"
        
        # Mock _get_wbi_keys to return test keys
        scraper._get_wbi_keys = lambda: (img_key, sub_key)
        
        params = {'mid': '486272', 'pn': '1', 'ps': '50'}
        signed_params = scraper._sign_wbi_params(params)
        
        # Check that required fields are present
        self.assertIn('w_rid', signed_params)
        self.assertIn('wts', signed_params)
        self.assertIn('mid', signed_params)
        
        # Check that w_rid is a valid 32-character hex string
        w_rid = signed_params['w_rid']
        self.assertEqual(len(w_rid), 32)
        self.assertTrue(all(c in '0123456789abcdef' for c in w_rid))
        
    def test_format_video_data(self):
        """Test video data formatting"""
        scraper = BilibiliScraper()
        
        raw_videos = [
            {
                'title': 'Test Video',
                'bvid': 'BV1test',
                'aid': 123,
                'play': 1000,
                'created': 1640995200  # 2022-01-01 00:00:00 UTC
            }
        ]
        
        user_info = {
            'name': 'Test User',
            'face': 'test_face.jpg',
            'level': 4
        }
        
        formatted = scraper.format_video_data(raw_videos, user_info)
        
        self.assertEqual(len(formatted), 1)
        self.assertEqual(formatted[0]['title'], 'Test Video')
        self.assertEqual(formatted[0]['up_name'], 'Test User')
        self.assertIn('2022-01-01', formatted[0]['created'])
        
    def test_format_timestamp(self):
        """Test timestamp formatting"""
        scraper = BilibiliScraper()
        
        # Test valid timestamp
        timestamp = 1640995200  # 2022-01-01 00:00:00 UTC
        formatted = scraper._format_timestamp(timestamp)
        self.assertIn('2022-01-01', formatted)
        
        # Test zero timestamp
        formatted = scraper._format_timestamp(0)
        self.assertEqual(formatted, '')


if __name__ == '__main__':
    unittest.main()