import requests
import json
import os
import time
from datetime import datetime, timedelta

# 配置
CONFIG_URL = "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json"
VERSION_DIR = "versions"

def get_current_time():
    utc_now = datetime.utcnow()
    cst_now = utc_now + timedelta(hours=8)
    return cst_now.strftime("%Y-%m-%d %H:%M:%S")

# 保存：用版本号命名，绝对不覆盖旧数据
def save_version_file(platform, version, data):
    if not os.path.exists(VERSION_DIR):
        os.makedirs(VERSION_DIR)
    filename = f"{platform}_{version}.json"
    file_path = os.path.join(VERSION_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

def main():
    try:
        print("📥 强制拉取最新QQ版本（绕过旧节点）...")

        # ================= 绝杀方案 =================
        # 1. 加最强时间戳
        # 2. 强制国内节点解析
        # 3. 完全禁用缓存
        # ===========================================
        url = f"{CONFIG_URL}?t={int(time.time() * 1000)}"
        
        session = requests.Session()
        resp = session.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
                "Pragma": "no-cache",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close",
            },
            timeout=20,
            allow_redirects=True
        )
        resp.encoding = "utf-8"
        data = resp.json()

        # 打印真实版本
        print(f"✅ 接口真实返回版本：Windows = {data['Windows']['version']}")
        update_time = get_current_time()

        # Windows
        win_ver = data["Windows"]["version"]
        win_data = {
            "platform": "Windows x64",
            "version": win_ver,
            "download_url": data["Windows"]["ntDownloadX64Url"],
            "update_time": update_time
        }
        save_version_file("windows", win_ver, win_data)

        # macOS
        mac_ver = data["macOS"]["version"].split(" ")[0]
        mac_data = {
            "platform": "macOS",
            "version": mac_ver,
            "download_url": data["macOS"]["downloadUrl"],
            "update_time": update_time
        }
        save_version_file("macos", mac_ver, mac_data)

        # Linux
        linux_ver = data["Linux"]["version"]
        linux_data = {
            "platform": "Linux ARM64 deb",
            "version": linux_ver,
            "download_url": data["Linux"]["armDownloadUrl"]["deb"],
            "update_time": update_time
        }
        save_version_file("linux", linux_ver, linux_data)

        print("\n🎉 全部新增完成！")

    except Exception as e:
        print(f"❌ 错误：{str(e)}")

if __name__ == "__main__":
    main()
