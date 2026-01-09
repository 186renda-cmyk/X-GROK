import requests
import xml.etree.ElementTree as ET
import os

# 配置信息
SITE_URL = "https://x-grok.top"
TOKEN = "MkpV4it8Aq1PaVbS"
API_URL = f"http://data.zz.baidu.com/urls?site={SITE_URL}&token={TOKEN}"
SITEMAP_FILE = "sitemap.xml"

def get_urls_from_sitemap(sitemap_path):
    """从 sitemap.xml 提取所有 URL"""
    urls = []
    if not os.path.exists(sitemap_path):
        print(f"错误: 找不到文件 {sitemap_path}")
        return urls
    
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        # Sitemap namespace
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        for url in root.findall('ns:url', namespace):
            loc = url.find('ns:loc', namespace)
            if loc is not None and loc.text:
                urls.append(loc.text.strip())
                
        print(f"成功提取 {len(urls)} 个 URL")
        return urls
    except Exception as e:
        print(f"解析 Sitemap 出错: {e}")
        return []

def push_to_baidu(urls):
    """推送 URL 到百度站长平台"""
    if not urls:
        print("没有 URL 需要推送")
        return

    headers = {
        'User-Agent': 'curl/7.12.1',
        'Host': 'data.zz.baidu.com',
        'Content-Type': 'text/plain',
        'Content-Length': str(len('\n'.join(urls)))
    }

    try:
        response = requests.post(
            API_URL, 
            data='\n'.join(urls), 
            headers=headers,
            timeout=10
        )
        
        result = response.json()
        print("-" * 30)
        print("百度推送结果:")
        print(f"状态码: {response.status_code}")
        print(f"成功推送: {result.get('success', 0)} 条")
        print(f"剩余配额: {result.get('remain', '未知')} 条")
        
        if 'not_same_site' in result:
            print(f"非本站 URL (失败): {result['not_same_site']}")
        if 'invalid' in result:
            print(f"非法 URL (失败): {result['invalid']}")
            
        print("-" * 30)
        
    except Exception as e:
        print(f"推送请求失败: {e}")

if __name__ == "__main__":
    print("开始执行百度主动推送...")
    target_urls = get_urls_from_sitemap(SITEMAP_FILE)
    
    # 也可以手动添加 URL (如果有 sitemap 没包含的)
    # target_urls.append("https://x-grok.top/new-page.html")
    
    push_to_baidu(target_urls)
