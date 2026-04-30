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

# 保存文件：用【版本号】命名，永不覆盖！
def save_version_file(platform, version, data):
    if not os.path.exists(VERSION_DIR):
        os.makedirs(VERSION_DIR)
    
    # 文件名格式：windows_9.9.30.json
    filename = f"{platform}_{version}.json"
    file_path = os.path.join(VERSION_DIR, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

def main():
    try:
        print("📥 正在拉取最新QQ版本...")

        # 强制无缓存，一定拿到最新版
        resp = requests.get(
            CONFIG_URL,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Cache-Control": "no-cache, no-store",
                "Pragma": "no-cache"
            },
            timeout=10
        )
        data = resp.json()
        update_time = get_current_time()

        # ==============================================
        # 这里会打印真实拿到的版本！！！
        # ==============================================
        print(f"✅ 成功获取最新版本：Windows={data['Windows']['version']}")

        # Windows x64
        win = data["Windows"]
        win_ver = win["version"]
        win_data = {
            "platform": "Windows x64",
            "version": win_ver,
            "download_url": win["ntDownloadX64Url"],
            "update_time": update_time
        }
        fn = save_version_file("windows", win_ver, win_data)
        print(f"✅ 已新增版本：{fn}")

        # macOS
        mac = data["macOS"]
        mac_ver = mac["version"].split(" ")[0]
        mac_data = {
            "platform": "macOS",
            "version": mac_ver,
            "download_url": mac["downloadUrl"],
            "update_time": update_time
        }
        fn = save_version_file("macos", mac_ver, mac_data)
        print(f"✅ 已新增版本：{fn}")

        # Linux
        linux = data["Linux"]
        linux_ver = linux["version"]
        linux_data = {
            "platform": "Linux ARM64 deb",
            "version": linux_ver,
            "download_url": linux["armDownloadUrl"]["deb"],
            "update_time": update_time
        }
        fn = save_version_file("linux", linux_ver, linux_data)
        print(f"✅ 已新增版本：{fn}")

        print("\n🎉 全部完成！所有版本已归档，不覆盖、不删除！")

    except Exception as e:
        print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()
