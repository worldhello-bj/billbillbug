"""
Bilibili video scraper module
Based on the Bilibili API documentation: https://socialsisteryi.github.io/bilibili-API-collect/
"""

import requests
import time
import json
import hashlib
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional


class BilibiliScraper:
    """Bilibili video information scraper"""
    
    # WBI signature encoding table
    MIXIN_KEY_ENC_TAB = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
        61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
        36, 20, 34, 44, 52
    ]
    
    def __init__(self, delay: float = 1.0):
        """
        Initialize the scraper
        
        Args:
            delay: Delay between requests in seconds (for rate limiting)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        })
        self._wbi_cache = {}  # Cache for WBI keys
        
    def _get_mixin_key(self, img_key: str, sub_key: str) -> str:
        """Get mixin key for WBI signing"""
        orig = img_key + sub_key
        temp = ''
        for i in self.MIXIN_KEY_ENC_TAB:
            temp += orig[i]
        return temp[:32]
    
    def _get_wbi_keys(self) -> tuple[str, str]:
        """Get WBI keys from bilibili nav API"""
        # Check cache first (cache for 1 hour)
        current_time = time.time()
        if self._wbi_cache and current_time - self._wbi_cache.get('timestamp', 0) < 3600:
            return self._wbi_cache['img_key'], self._wbi_cache['sub_key']
            
        try:
            response = self.session.get('https://api.bilibili.com/x/web-interface/nav', timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0 or data.get('code') == -101:  # -101 is ok (not logged in)
                wbi_img = data['data']['wbi_img']
                img_url = wbi_img['img_url']
                sub_url = wbi_img['sub_url']
                
                # Extract keys from URLs
                img_key = img_url.split('/')[-1].split('.')[0]
                sub_key = sub_url.split('/')[-1].split('.')[0]
                
                # Cache the keys
                self._wbi_cache = {
                    'img_key': img_key,
                    'sub_key': sub_key,
                    'timestamp': current_time
                }
                
                return img_key, sub_key
            else:
                print(f"Failed to get WBI keys: {data.get('message', 'Unknown error')}")
                return '', ''
        except Exception as e:
            print(f"Error getting WBI keys: {e}")
            return '', ''
    
    def _sign_wbi_params(self, params: dict) -> dict:
        """Sign parameters with WBI signature"""
        img_key, sub_key = self._get_wbi_keys()
        if not img_key or not sub_key:
            return params  # Return original params if WBI keys unavailable
            
        mixin_key = self._get_mixin_key(img_key, sub_key)
        curr_time = int(time.time())
        
        # Add timestamp
        signed_params = params.copy()
        signed_params['wts'] = curr_time
        
        # Sort parameters
        sorted_params = dict(sorted(signed_params.items()))
        
        # Filter out unwanted characters
        filtered_params = {}
        for k, v in sorted_params.items():
            value_str = str(v)
            # Remove "!'()*" characters as per API documentation
            filtered_value = ''.join(char for char in value_str if char not in "!'()*")
            filtered_params[k] = filtered_value
        
        # Create query string
        query = urllib.parse.urlencode(filtered_params)
        
        # Calculate w_rid
        wbi_sign = hashlib.md5((query + mixin_key).encode()).hexdigest()
        filtered_params['w_rid'] = wbi_sign
        
        return filtered_params
        
    def get_user_videos(self, uid: str, page: int = 1, page_size: int = 50) -> Dict:
        """
        Get video list from a specific UP master
        
        Args:
            uid: UP master's UID
            page: Page number (starts from 1)
            page_size: Number of videos per page (max 50)
            
        Returns:
            Dictionary containing video list and metadata
        """
        url = "https://api.bilibili.com/x/space/wbi/arc/search"
        params = {
            'mid': uid,
            'ps': min(page_size, 50),  # API limit is 50
            'pn': page,
            'order': 'pubdate',  # Sort by publish date
        }
        
        # Sign parameters with WBI
        signed_params = self._sign_wbi_params(params)
        
        try:
            response = self.session.get(url, params=signed_params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                return data['data']
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return {}
                
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return {}
        finally:
            time.sleep(self.delay)
    
    def get_user_info(self, uid: str) -> Dict:
        """
        Get basic information about a UP master
        
        Args:
            uid: UP master's UID
            
        Returns:
            Dictionary containing user information
        """
        url = "https://api.bilibili.com/x/space/acc/info"
        params = {'mid': uid}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                return data['data']
            elif data.get('code') == -412:
                print("Request was intercepted, trying with WBI signing...")
                # Try with WBI signing for better compatibility
                signed_params = self._sign_wbi_params(params)
                response = self.session.get(url, params=signed_params, timeout=10)
                response.raise_for_status()
                data = response.json()
                if data.get('code') == 0:
                    return data['data']
                else:
                    print(f"API Error after WBI signing: {data.get('message', 'Unknown error')}")
                    return {}
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return {}
                
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return {}
        finally:
            time.sleep(self.delay)
    
    def get_all_user_videos(self, uid: str, max_videos: Optional[int] = None) -> List[Dict]:
        """
        Get all videos from a UP master (with pagination)
        
        Args:
            uid: UP master's UID
            max_videos: Maximum number of videos to fetch (None for all)
            
        Returns:
            List of video dictionaries
        """
        all_videos = []
        page = 1
        
        print(f"Fetching videos for UID: {uid}")
        
        while True:
            print(f"Fetching page {page}...")
            data = self.get_user_videos(uid, page=page)
            
            if not data or 'list' not in data:
                print("No more videos found or API error")
                break
                
            videos = data['list']['vlist']
            if not videos:
                print("No videos in current page")
                break
                
            all_videos.extend(videos)
            print(f"Found {len(videos)} videos on page {page}")
            
            # Check if we've reached the desired limit
            if max_videos and len(all_videos) >= max_videos:
                all_videos = all_videos[:max_videos]
                break
                
            # Check if there are more pages
            if len(videos) < 50:  # If less than page size, this was the last page
                break
                
            page += 1
            
        print(f"Total videos fetched: {len(all_videos)}")
        return all_videos
    
    def format_video_data(self, videos: List[Dict], user_info: Dict = None) -> List[Dict]:
        """
        Format video data for export
        
        Args:
            videos: List of raw video data from API
            user_info: Optional user information
            
        Returns:
            List of formatted video dictionaries
        """
        formatted_videos = []
        
        for video in videos:
            formatted_video = {
                'title': video.get('title', ''),
                'bvid': video.get('bvid', ''),
                'aid': video.get('aid', ''),
                'pic': video.get('pic', ''),
                'author': video.get('author', ''),
                'mid': video.get('mid', ''),
                'play': video.get('play', 0),  # View count
                'video_review': video.get('video_review', 0),  # Comment count
                'favorites': video.get('favorites', 0),  # Favorite count
                'created': self._format_timestamp(video.get('created', 0)),
                'length': video.get('length', ''),  # Video duration
                'description': video.get('description', ''),
            }
            
            # Add user info if provided
            if user_info:
                formatted_video['up_name'] = user_info.get('name', '')
                formatted_video['up_face'] = user_info.get('face', '')
                formatted_video['up_sign'] = user_info.get('sign', '')
                formatted_video['up_level'] = user_info.get('level', 0)
                formatted_video['up_fans'] = user_info.get('fans', 0)
                
            formatted_videos.append(formatted_video)
            
        return formatted_videos
    
    def _format_timestamp(self, timestamp: int) -> str:
        """Convert timestamp to readable date format"""
        if timestamp:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return ''
    
    def scrape_up_master(self, uid: str, max_videos: Optional[int] = None) -> Dict:
        """
        Scrape complete information for a UP master
        
        Args:
            uid: UP master's UID
            max_videos: Maximum number of videos to fetch
            
        Returns:
            Dictionary containing user info and formatted video list
        """
        print(f"Starting scrape for UP master UID: {uid}")
        
        # Get user information
        user_info = self.get_user_info(uid)
        if not user_info:
            print("Failed to get user information")
            return {}
            
        print(f"UP Master: {user_info.get('name', 'Unknown')}")
        
        # Get all videos
        videos = self.get_all_user_videos(uid, max_videos)
        if not videos:
            print("No videos found")
            return {'user_info': user_info, 'videos': []}
            
        # Format video data
        formatted_videos = self.format_video_data(videos, user_info)
        
        return {
            'user_info': user_info,
            'videos': formatted_videos,
            'total_videos': len(formatted_videos),
            'scrape_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }