# WBI Authentication Fix

## 问题描述 (Problem Description)

之前的版本在未登录状态下访问B站API时会返回"非法访问"错误。这是因为B站从2023年3月开始对部分Web端接口采用WBI签名鉴权，未正确签名的请求会被拒绝。

The previous version would return "illegal access" errors when accessing Bilibili APIs without login. This is because Bilibili started using WBI signature authentication for some web APIs since March 2023, and unsigned requests are rejected.

## 解决方案 (Solution)

根据 [@SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 文档，实现了完整的WBI签名机制：

Based on the [@SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) documentation, implemented complete WBI signing mechanism:

### 主要变更 (Key Changes)

1. **WBI密钥获取**: 从nav接口获取img_key和sub_key
   - **WBI Key Retrieval**: Get img_key and sub_key from nav API

2. **密钥混合**: 按照特定映射表对密钥进行重排生成mixin_key  
   - **Key Mixing**: Rearrange keys according to specific mapping table to generate mixin_key

3. **参数签名**: 对请求参数进行排序、编码并计算MD5签名
   - **Parameter Signing**: Sort, encode parameters and calculate MD5 signature

4. **缓存优化**: 缓存WBI密钥1小时避免频繁请求
   - **Caching**: Cache WBI keys for 1 hour to avoid frequent requests

### 技术细节 (Technical Details)

#### WBI签名算法步骤 (WBI Signing Algorithm Steps)

1. 获取实时密钥 `img_key`, `sub_key`
2. 使用映射表重排生成32位 `mixin_key`  
3. 添加时间戳 `wts` 到参数
4. 参数按key排序并URL编码
5. 拼接查询字符串和mixin_key计算MD5得到 `w_rid`
6. 将 `w_rid` 和 `wts` 加入最终请求参数

#### 映射表 (Mapping Table)

```python
MIXIN_KEY_ENC_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]
```

### 受影响的API (Affected APIs)

- `https://api.bilibili.com/x/space/wbi/arc/search` - 用户视频搜索 (User video search)
- `https://api.bilibili.com/x/space/acc/info` - 用户信息 (User info, fallback support)

### 向后兼容性 (Backward Compatibility)

- 现有功能保持不变
- 自动降级处理：如果WBI签名失败，会尝试原始请求方式
- 对于不需要WBI签名的接口，保持原有逻辑

- Existing functionality remains unchanged
- Automatic fallback: If WBI signing fails, tries original request method  
- For APIs that don't require WBI signing, keeps original logic

## 测试验证 (Testing & Verification)

### 单元测试 (Unit Tests)

新增了以下测试用例：

- `test_wbi_mixin_key_generation`: 验证mixin_key生成正确性
- `test_wbi_params_signing`: 验证参数签名功能

### 功能测试 (Functional Tests)

使用官方文档提供的测试数据验证：

```python
# 测试数据 (Test Data)
img_key = "7cd084941338484aae1ad9425b84077c"
sub_key = "4932caff0ff746eab6f01bf08b70ac45" 
expected_mixin = "ea1db124af3c7062474693fa704f4ff8"

# 验证结果 (Verification Result)  
✅ Mixin key generation: PASS
✅ Parameter signing: PASS
✅ Complete workflow: PASS
```

## 使用方法 (Usage)

使用方法保持不变，WBI签名是透明的：

Usage remains the same, WBI signing is transparent:

```python
from billbillbug import BilibiliScraper

scraper = BilibiliScraper()
data = scraper.scrape_up_master(uid="486272", max_videos=50)
```

现在可以在未登录状态下正常工作！

Now works without login!

## 参考资料 (References)

- [SocialSisterYi/bilibili-API-collect - WBI签名](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md)
- [B站API文档 - 用户空间相关](https://socialsisteryi.github.io/bilibili-API-collect/docs/user/space.html)