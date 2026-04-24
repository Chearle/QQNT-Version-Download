import requests
import json
import os
from datetime import datetime, timedelta

# 配置
CONFIG_URL = "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json"
# 版本文件存放文件夹
VERSION_DIR = "versions"

def get_current_time():
    utc_now = datetime.utcnow()
    cst_now = utc_now + timedelta(hours=8)
    return cst_now.strftime("%Y-%m-%d %H:%M:%S")

def save_to_file(filename, data):
    # 自动创建文件夹
    if not os.path.exists(VERSION_DIR):
        os.makedirs(VERSION_DIR)
    # 拼接完整路径
    file_path = os.path.join(VERSION_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    try:
        print("📥 正在请求QQ官方接口...")
        resp = requests.get(CONFIG_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        update_time = get_current_time()

        # Windows x64
        win = data.get("Windows", {})
        if win:
            win_data = {
                "platform": "Windows x64",
                "version": win["version"],
                "download_url": win["ntDownloadX64Url"],
                "update_time": update_time
            }
            save_to_file("windows.json", win_data)
            print("✅ versions/windows.json 写入成功")

        # macOS 通用版
        mac = data.get("macOS", {})
        if mac:
            mac_data = {
                "platform": "macOS 通用版",
                "version": mac["version"].split(" ")[0],
                "download_url": mac["downloadUrl"],
                "update_time": update_time
            }
            save_to_file("macos.json", mac_data)
            print("✅ versions/macos.json 写入成功")

        # Linux ARM64 (deb)
        linux = data.get("Linux", {})
        if linux:
            linux_data = {
                "platform": "Linux ARM64 (deb)",
                "version": linux["version"],
                "download_url": linux["armDownloadUrl"]["deb"],
                "update_time": update_time
            }
            save_to_file("linux.json", linux_data)
            print("✅ versions/linux.json 写入成功")

        print("\n🎉 全部分文件写入完成！")

    except Exception as e:
        print(f"❌ 运行错误：{str(e)}")

if __name__ == "__main__":
    main()
