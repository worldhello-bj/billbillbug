# BillBillBug 🐛

一个用于B站数据采集的爬虫工具集

## 项目简介

BillBillBug 是一个专门针对B站（bilibili）数据采集的爬虫项目，支持获取up主视频信息、用户数据等功能。项目基于B站开放API，确保数据获取的稳定性和合规性。

## 功能特性

- 🎯 **up主视频信息采集**: 获取指定up主的视频列表及详细信息
- 📊 **数据导出**: 支持CSV、JSON等多种格式的数据导出
- 🔧 **易于扩展**: 模块化设计，方便添加新的采集功能
- 📋 **详细信息**: 包含视频标题、播放量、弹幕数、发布时间等完整数据

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用示例

#### 命令行使用

```bash
# 获取指定UP主的所有视频信息
python main.py --uid 486272

# 限制获取视频数量
python main.py --uid 486272 --max-videos 50

# 指定输出格式（json/csv/both）
python main.py --uid 486272 --format json

# 指定输出目录
python main.py --uid 486272 --output ./data/

# 添加请求延迟（避免请求过快）
python main.py --uid 486272 --delay 2

# 生成总结报告
python main.py --uid 486272 --summary

# 静默模式（减少输出信息）
python main.py --uid 486272 --quiet
```

#### Python代码使用

```python
from billbillbug import BilibiliScraper, DataExporter

# 创建爬虫实例
scraper = BilibiliScraper(delay=1.0)

# 爬取UP主视频信息
data = scraper.scrape_up_master(uid="486272", max_videos=100)

# 导出数据
exporter = DataExporter()
exporter.export_to_json(data, "videos.json")
exporter.export_to_csv(data, "videos.csv")
exporter.export_summary_txt(data, "summary.txt")
```

#### 演示模式

由于网络限制，可以运行演示模式查看功能：

```bash
python demo.py
```

## API参考

本项目基于 [B站API文档](https://socialsisteryi.github.io/bilibili-API-collect/) 开发，确保使用官方支持的接口。

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目！

### 开发计划

- [x] 实现up主视频信息爬虫 ([#1](https://github.com/worldhello-bj/billbillbug/issues/1))
- [x] 添加数据存储功能
- [x] 支持多种导出格式（JSON、CSV）
- [x] 添加命令行界面
- [x] 添加错误处理和重试机制
- [ ] 支持批量采集
- [ ] 添加数据可视化功能
- [ ] 支持更多类型的数据采集

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 免责声明

本项目仅供学习和研究使用，请遵守B站的使用条款和相关法律法规。使用者应对自己的行为负责。

---

如有问题或建议，请提交 [Issue](https://github.com/worldhello-bj/billbillbug/issues)。
