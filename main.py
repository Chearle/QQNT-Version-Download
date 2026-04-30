import json
import os
from datetime import datetime, timedelta

VERSION_DIR = "versions"
os.makedirs(VERSION_DIR, exist_ok=True)

def get_cst_time():
    return (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

# 直接新增最新版，不覆盖、不删除旧数据
new_data = {
    "platform": "Windows x64",
    "version": "9.9.30",
    "download_url": "https://dldir1v6.qq.com/qqfile/qq/QQNT/Windows/QQ_9.9.30_260429_x64_01.exe",
    "update_time": get_cst_time()
}

new_file = os.path.join(VERSION_DIR, "windows_9.9.30.json")
with open(new_file, "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print("✅ 已直接新增最新版本：windows_9.9.30.json")
print("🎉 旧数据完全不动，只新增！")
