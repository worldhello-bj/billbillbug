"""
Data export functionality for BillBillBug
"""

import json
import csv
import os
from typing import List, Dict, Any
from datetime import datetime


class DataExporter:
    """Export scraped data to various formats"""
    
    @staticmethod
    def export_to_json(data: Dict[str, Any], filename: str = None) -> str:
        """
        Export data to JSON format
        
        Args:
            data: Data dictionary to export
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to the created file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            uid = data.get('user_info', {}).get('mid', 'unknown')
            filename = f"bilibili_videos_{uid}_{timestamp}.json"
            
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Data exported to JSON: {filename}")
        return filename
    
    @staticmethod
    def export_to_csv(data: Dict[str, Any], filename: str = None) -> str:
        """
        Export video data to CSV format
        
        Args:
            data: Data dictionary to export
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to the created file
        """
        videos = data.get('videos', [])
        if not videos:
            print("No video data to export")
            return ""
            
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            uid = data.get('user_info', {}).get('mid', 'unknown')
            filename = f"bilibili_videos_{uid}_{timestamp}.csv"
            
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        # Get all possible field names from all videos
        fieldnames = set()
        for video in videos:
            fieldnames.update(video.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(videos)
            
        print(f"Data exported to CSV: {filename}")
        return filename
    
    @staticmethod
    def export_user_info_csv(data: Dict[str, Any], filename: str = None) -> str:
        """
        Export user information to CSV format
        
        Args:
            data: Data dictionary containing user info
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to the created file
        """
        user_info = data.get('user_info', {})
        if not user_info:
            print("No user info to export")
            return ""
            
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            uid = user_info.get('mid', 'unknown')
            filename = f"bilibili_user_{uid}_{timestamp}.csv"
            
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        # Convert user info to a list of dictionaries for CSV writing
        user_data = [{
            'uid': user_info.get('mid', ''),
            'name': user_info.get('name', ''),
            'sex': user_info.get('sex', ''),
            'face': user_info.get('face', ''),
            'sign': user_info.get('sign', ''),
            'level': user_info.get('level', 0),
            'birthday': user_info.get('birthday', ''),
            'coins': user_info.get('coins', 0),
            'fans': user_info.get('fans', 0),
            'friend': user_info.get('friend', 0),
            'attention': user_info.get('attention', 0),
            'scrape_time': data.get('scrape_time', ''),
            'total_videos': data.get('total_videos', 0)
        }]
        
        fieldnames = list(user_data[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(user_data)
            
        print(f"User info exported to CSV: {filename}")
        return filename
    
    @staticmethod
    def export_summary_txt(data: Dict[str, Any], filename: str = None) -> str:
        """
        Export a summary report in text format
        
        Args:
            data: Data dictionary to export
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to the created file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            uid = data.get('user_info', {}).get('mid', 'unknown')
            filename = f"bilibili_summary_{uid}_{timestamp}.txt"
            
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        user_info = data.get('user_info', {})
        videos = data.get('videos', [])
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== Bilibili UP Master Video Summary ===\n\n")
            f.write(f"Scrape Time: {data.get('scrape_time', 'Unknown')}\n")
            f.write(f"Total Videos: {data.get('total_videos', 0)}\n\n")
            
            # User information
            f.write("=== UP Master Information ===\n")
            f.write(f"Name: {user_info.get('name', 'Unknown')}\n")
            f.write(f"UID: {user_info.get('mid', 'Unknown')}\n")
            f.write(f"Level: {user_info.get('level', 0)}\n")
            f.write(f"Fans: {user_info.get('fans', 0)}\n")
            f.write(f"Following: {user_info.get('attention', 0)}\n")
            f.write(f"Sign: {user_info.get('sign', 'No signature')}\n\n")
            
            # Video statistics
            if videos:
                total_plays = sum(video.get('play', 0) for video in videos)
                total_comments = sum(video.get('video_review', 0) for video in videos)
                total_favorites = sum(video.get('favorites', 0) for video in videos)
                
                f.write("=== Video Statistics ===\n")
                f.write(f"Total Videos: {len(videos)}\n")
                f.write(f"Total Views: {total_plays:,}\n")
                f.write(f"Total Comments: {total_comments:,}\n")
                f.write(f"Total Favorites: {total_favorites:,}\n")
                f.write(f"Average Views per Video: {total_plays // len(videos) if videos else 0:,}\n\n")
                
                # Top 10 most popular videos
                top_videos = sorted(videos, key=lambda x: x.get('play', 0), reverse=True)[:10]
                f.write("=== Top 10 Most Popular Videos ===\n")
                for i, video in enumerate(top_videos, 1):
                    f.write(f"{i}. {video.get('title', 'Unknown Title')}\n")
                    f.write(f"   Views: {video.get('play', 0):,} | Comments: {video.get('video_review', 0):,}\n")
                    f.write(f"   Published: {video.get('created', 'Unknown')}\n\n")
            
        print(f"Summary exported to TXT: {filename}")
        return filename