import requests

# 你的百度推送接口 (x-grok.top)
api_url = "http://data.zz.baidu.com/urls?site=https://x-grok.top&token=MkpV4it8Aq1PaVbS"

# 要推送的链接列表
urls = [
    "https://x-grok.top/",
    "https://x-grok.top/index.html",
    "https://x-grok.top/sitemap.xml"
]

headers = {
    'User-Agent': 'curl/7.12.1',
    'Content-Type': 'text/plain'
}

try:
    print("🚀 正在向百度推送 x-grok.top ...")
    response = requests.post(api_url, data="\n".join(urls), headers=headers)
    
    print("【推送结果】:", response.text)
    
    if "success" in response.text:
        print("✅ 成功！百度已接收链接。")
    else:
        print("❌ 推送失败，请检查返回信息。")
        
except Exception as e:
    print(f"脚本运行出错: {e}")
