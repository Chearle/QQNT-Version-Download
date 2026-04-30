import requests
import json
import os
from datetime import datetime, timedelta

# 配置
CONFIG_URL = "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json"
VERSION_DIR = "versions"

def get_current_time():
    utc_now = datetime.utcnow()
    cst_now = utc_now + timedelta(hours=8)
    return cst_now.strftime("%Y-%m-%d %H:%M:%S")

def save_to_file(filename, data):
    if not os.path.exists(VERSION_DIR):
        os.makedirs(VERSION_DIR)
    file_path = os.path.join(VERSION_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    try:
        print("📥 正在请求QQ官方接口...")

        # ==============================================
        # ✅ 终极修复：强制禁用所有缓存 + 模拟浏览器
        # ==============================================
        resp = requests.get(
            CONFIG_URL,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache"
            },
            timeout=10
        )

        resp.raise_for_status()
        data = resp.json()

        # 🧪 调试打印：看一眼脚本到底拿到了什么！
        print("【脚本真实获取到的 Windows 版本】:", data["Windows"]["version"])

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

        # macOS
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

        # Linux
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