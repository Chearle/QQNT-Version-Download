import requests
import json
from datetime import datetime, timedelta

# 官方配置地址
CONFIG_URL = "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json"
SAVE_FILE = "download_links.json"

def get_current_time():
    # 获取北京时间
    utc_now = datetime.utcnow()
    cst_now = utc_now + timedelta(hours=8)
    return cst_now.strftime("%Y-%m-%d %H:%M:%S")

def main():
    try:
        print("📥 正在请求QQ官方接口...")
        resp = requests.get(CONFIG_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        result = []
        
        # ==================== Windows x64（仅保留） ====================
        win = data.get("Windows", {})
        if win:
            result.append({
                "platform": "Windows x64",
                "version": win["version"],
                "download_url": win["ntDownloadX64Url"],
                "update_time": get_current_time()
            })

        # ==================== macOS 通用版（仅保留） ====================
        mac = data.get("macOS", {})
        if mac:
            result.append({
                "platform": "macOS 通用版",
                "version": mac["version"].split(" ")[0],
                "download_url": mac["downloadUrl"],
                "update_time": get_current_time()
            })

        # ==================== Linux ARM64 deb（仅保留） ====================
        linux = data.get("Linux", {})
        if linux:
            result.append({
                "platform": "Linux ARM64 (deb)",
                "version": linux["version"],
                "download_url": linux["armDownloadUrl"]["deb"],
                "update_time": get_current_time()
            })

        # 输出日志
        print(f"✅ 获取到 {len(result)} 个核心平台版本")
        print("📄 写入内容预览：")
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 写入文件
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print("✅ 核心平台下载地址写入成功！")

    except Exception as e:
        print(f"❌ 运行错误：{str(e)}")

if __name__ == "__main__":
    main()
