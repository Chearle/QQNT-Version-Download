import requests
import json
import os

# 官方接口
CONFIG_URL = "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json"
SAVE_FILE = "download_links.json"

def get_current_time():
    from datetime import datetime, timedelta
    utc_now = datetime.utcnow()
    cst_now = utc_now + timedelta(hours=8)
    return cst_now.strftime("%Y-%m-%d %H:%M:%S")

def main():
    try:
        print("📥 正在请求QQ官方接口...")
        resp = requests.get(CONFIG_URL, timeout=10)
        data = resp.json()
        
        # ✅ 修复核心：版本在 pc 字段下！！！
        pc_data = data.get("pc", {})
        
        # 读取三个平台
        platforms = ["win64", "win32", "mac"]
        result = []
        for p in platforms:
            if p in pc_data:
                result.append({
                    "platform": p,
                    "version": pc_data[p]["version"],
                    "download_url": pc_data[p]["url"],
                    "update_time": get_current_time()
                })

        print(f"✅ 获取到 {len(result)} 个平台版本")
        
        # 强制写入文件
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print("✅ 文件写入成功！")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()
