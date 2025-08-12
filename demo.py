#!/usr/bin/env python3
"""
Demo script for BillBillBug using mock data
This demonstrates the functionality when API access is not available
"""

import sys
import os
from datetime import datetime

# Add the package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from billbillbug.exporter import DataExporter


def create_mock_data():
    """Create mock data that represents scraped Bilibili data"""
    
    # Mock user info
    user_info = {
        'mid': 486272,
        'name': '示例UP主',
        'sex': '男',
        'face': 'https://i2.hdslb.com/bfs/face/example.jpg',
        'sign': '这是一个示例UP主的签名，用于演示BillBillBug的功能。',
        'level': 6,
        'birthday': '2000-01-01',
        'coins': 12345,
        'fans': 123456,
        'friend': 987,
        'attention': 234
    }
    
    # Mock video data
    videos = [
        {
            'title': '【科技】人工智能的发展历程与未来展望',
            'bvid': 'BV1example001',
            'aid': 12345001,
            'pic': 'https://i2.hdslb.com/bfs/archive/example1.jpg',
            'author': '示例UP主',
            'mid': 486272,
            'play': 125000,
            'video_review': 856,
            'favorites': 3200,
            'created': '2024-01-15 14:30:00',
            'length': '12:34',
            'description': '本期视频将为大家介绍人工智能的发展历程，以及对未来的展望。',
            'up_name': '示例UP主',
            'up_face': 'https://i2.hdslb.com/bfs/face/example.jpg',
            'up_sign': '这是一个示例UP主的签名，用于演示BillBillBug的功能。',
            'up_level': 6,
            'up_fans': 123456
        },
        {
            'title': '【教程】Python爬虫入门指南',
            'bvid': 'BV1example002',
            'aid': 12345002,
            'pic': 'https://i2.hdslb.com/bfs/archive/example2.jpg',
            'author': '示例UP主',
            'mid': 486272,
            'play': 89000,
            'video_review': 623,
            'favorites': 2100,
            'created': '2024-01-10 10:15:00',
            'length': '23:45',
            'description': '从零开始学习Python爬虫，包含基本概念和实践案例。',
            'up_name': '示例UP主',
            'up_face': 'https://i2.hdslb.com/bfs/face/example.jpg',
            'up_sign': '这是一个示例UP主的签名，用于演示BillBillBug的功能。',
            'up_level': 6,
            'up_fans': 123456
        },
        {
            'title': '【生活】我的一天vlog分享',
            'bvid': 'BV1example003',
            'aid': 12345003,
            'pic': 'https://i2.hdslb.com/bfs/archive/example3.jpg',
            'author': '示例UP主',
            'mid': 486272,
            'play': 56000,
            'video_review': 312,
            'favorites': 890,
            'created': '2024-01-05 18:20:00',
            'length': '08:16',
            'description': '记录我平常的一天，希望能给大家带来一些正能量。',
            'up_name': '示例UP主',
            'up_face': 'https://i2.hdslb.com/bfs/face/example.jpg',
            'up_sign': '这是一个示例UP主的签名，用于演示BillBillBug的功能。',
            'up_level': 6,
            'up_fans': 123456
        },
        {
            'title': '【游戏】原神新版本体验分享',
            'bvid': 'BV1example004',
            'aid': 12345004,
            'pic': 'https://i2.hdslb.com/bfs/archive/example4.jpg',
            'author': '示例UP主',
            'mid': 486272,
            'play': 234000,
            'video_review': 1542,
            'favorites': 7890,
            'created': '2024-01-02 20:30:00',
            'length': '15:28',
            'description': '原神新版本的详细体验，包含新角色和新剧情介绍。',
            'up_name': '示例UP主',
            'up_face': 'https://i2.hdslb.com/bfs/face/example.jpg',
            'up_sign': '这是一个示例UP主的签名，用于演示BillBillBug的功能。',
            'up_level': 6,
            'up_fans': 123456
        },
        {
            'title': '【音乐】翻唱经典老歌《月亮代表我的心》',
            'bvid': 'BV1example005',
            'aid': 12345005,
            'pic': 'https://i2.hdslb.com/bfs/archive/example5.jpg',
            'author': '示例UP主',
            'mid': 486272,
            'play': 45000,
            'video_review': 289,
            'favorites': 1200,
            'created': '2023-12-28 16:45:00',
            'length': '04:32',
            'description': '用心演绎经典老歌，希望大家喜欢我的翻唱版本。',
            'up_name': '示例UP主',
            'up_face': 'https://i2.hdslb.com/bfs/face/example.jpg',
            'up_sign': '这是一个示例UP主的签名，用于演示BillBillBug的功能。',
            'up_level': 6,
            'up_fans': 123456
        }
    ]
    
    return {
        'user_info': user_info,
        'videos': videos,
        'total_videos': len(videos),
        'scrape_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def main():
    """Demo main function"""
    print("=== BillBillBug Demo - 使用模拟数据 ===")
    print("注意: 由于网络限制，此演示使用模拟数据展示功能")
    print("=" * 50)
    
    # Create output directory
    os.makedirs('./output/', exist_ok=True)
    
    # Generate mock data
    data = create_mock_data()
    
    print(f"模拟UP主: {data['user_info']['name']}")
    print(f"UID: {data['user_info']['mid']}")
    print(f"粉丝数: {data['user_info']['fans']:,}")
    print(f"视频数量: {data['total_videos']}")
    print()
    
    # Export data using the DataExporter
    exporter = DataExporter()
    
    print("正在导出数据...")
    
    # Export to JSON
    json_file = exporter.export_to_json(data, './output/demo_videos.json')
    
    # Export to CSV
    csv_file = exporter.export_to_csv(data, './output/demo_videos.csv')
    
    # Export user info
    user_csv_file = exporter.export_user_info_csv(data, './output/demo_user.csv')
    
    # Export summary
    summary_file = exporter.export_summary_txt(data, './output/demo_summary.txt')
    
    print("\n=== 导出完成 ===")
    print("生成的文件:")
    print(f"  - {json_file}")
    print(f"  - {csv_file}")
    print(f"  - {user_csv_file}")
    print(f"  - {summary_file}")
    
    print("\n=== 视频列表预览 ===")
    for i, video in enumerate(data['videos'], 1):
        print(f"{i}. {video['title']}")
        print(f"   播放量: {video['play']:,} | 评论数: {video['video_review']:,} | 收藏数: {video['favorites']:,}")
        print(f"   发布时间: {video['created']} | 时长: {video['length']}")
        print()


if __name__ == '__main__':
    main()