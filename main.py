import requests
import json
import os
import time
from datetime import datetime, timedelta
import socket

# 强制使用国内DNS解析
def force_dns_resolve():
    import dns.resolver
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['114.114.114.114', '223.5.5.5']  # 国内公共DNS
    try:
        answers = resolver.resolve('cdn-go.cn', 'A')
        for rdata in answers:
            ip = str(rdata)
            # 强制绑定域名到国内IP
            socket.gethostbyname = lambda x: ip if x == 'cdn-go.cn' else socket.gethostbyname(x)
            break
    except:
        pass

# 安装dns模块（自动处理）
try:
    import dns.resolver
except ImportError:
    os.system("pip install dnspython")
    import dns.resolver

# 强制DNS
force_dns_resolve()

# 配置
CONFIG_URL = "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json"
VERSION_DIR = "versions"
os.makedirs(VERSION_DIR, exist_ok=True)

def get_cst_time():
    return (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

try:
    print("🚀 GitHub专用 - 强制拉取国内最新版本...")

    # 最强绕过
    url = f"{CONFIG_URL}?t={int(time.time()*1000)}"
    resp = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cache-Control": "no-cache,no-store,must-revalidate",
            "Pragma": "no-cache",
            "Host": "cdn-go.cn",
            "Accept-Encoding": "gzip"
        },
        timeout=15
    )
    data = resp.json()

    win_ver = data["Windows"]["version"]
    print(f"✅ 最终获取版本：Windows = {win_ver}")

    # 新增版本，不覆盖、不删除旧数据
    new_file = os.path.join(VERSION_DIR, f"windows_{win_ver}.json")
    with open(new_file, "w", encoding="utf-8") as f:
        json.dump({
            "platform": "Windows x64",
            "version": win_ver,
            "download_url": data["Windows"]["ntDownloadX64Url"],
            "update_time": get_cst_time()
        }, f, ensure_ascii=False, indent=2)

    print(f"✅ 已新增：{new_file}")
    print("\n🎉 GitHub 环境修复完成！")

except Exception as e:
    print(f"❌ 错误：{e}")
