import requests
import json
import os

# 配置
CONFIG_URL = "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json"
SAVE_FILE = "download_links.json"

def get_current_time():
    from datetime import datetime, timedelta
    utc_now = datetime.utcnow()
    cst_now = utc_now + timedelta(hours=8)
    return cst_now.strftime("%Y-%m-%d %H:%M:%S")

def get_latest_qq_config():
    try:
        print("📥 正在请求QQ官方接口...")
        resp = requests.get(CONFIG_URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        platforms = ["win64", "win32", "mac"]
        result = []
        for p in platforms:
            if p in data:
                result.append({
                    "platform": p,
                    "version": data[p]["version"],
                    "download_url": data[p]["url"],
                    "update_time": get_current_time()
                })
        print(f"✅ 获取到 {len(result)} 个版本")
        return result
    except Exception as e:
        print(f"❌ 请求失败：{e}")
        return []

def main():
    # 1. 获取最新版本
    latest = get_latest_qq_config()
    if not latest:
        print("❌ 无数据，退出")
        return

    # 2. 【强制写入】不管原来是什么，直接覆盖（空文件必写）
    print("💾 强制写入版本数据到文件...")
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(latest, f, ensure_ascii=False, indent=2)
        print("✅ 文件写入成功！")
        # 打印写入的内容
        print("📄 写入内容：")
        print(json.dumps(latest, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"❌ 写入文件失败：{e}")

if __name__ == "__main__":
    main()
