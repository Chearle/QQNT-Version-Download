import requests
import json
import os

# 目标配置文件URL
CONFIG_URL = "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json"
# 历史记录存储文件
SAVE_FILE = "download_links.json"

def get_latest_qq_config():
    """获取最新的QQ版本和下载地址"""
    try:
        print("🔍 正在获取QQ官方最新版本信息...")
        response = requests.get(CONFIG_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        platforms = ["win64", "win32", "mac"]
        latest_list = []
        for platform in platforms:
            if platform in data:
                info = data[platform]
                latest_list.append({
                    "platform": platform,
                    "version": info["version"],
                    "download_url": info["url"],
                    "update_time": get_current_time()
                })
        print(f"✅ 获取到 {len(latest_list)} 个平台版本")
        return latest_list
    except Exception as e:
        print(f"❌ 获取失败：{str(e)}")
        return []

def get_current_time():
    """获取北京时间"""
    from datetime import datetime, timedelta
    utc_now = datetime.utcnow()
    cst_now = utc_now + timedelta(hours=8)
    return cst_now.strftime("%Y-%m-%d %H:%M:%S")

def load_history_data():
    """加载历史数据"""
    if not os.path.exists(SAVE_FILE):
        print("ℹ️ 首次运行，创建新文件")
        return []
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print("⚠️ 历史文件损坏，重新创建")
        return []

def save_data(data):
    """保存数据（强制写入）"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("💾 文件已成功写入本地")

def main():
    # 1. 获取最新数据
    latest_data = get_latest_qq_config()
    if not latest_data:
        print("❌ 未获取到任何版本信息，退出")
        return
    
    # 2. 加载历史
    history_data = load_history_data()
    
    # 3. 合并数据（首次运行直接写入）
    new_records = []
    history_keys = {(item["platform"], item["version"]) for item in history_data}
    
    for item in latest_data:
        key = (item["platform"], item["version"])
        if key not in history_keys:
            new_records.append(item)
            history_data.append(item)
    
    # 4. 保存（有更新/首次运行 都写入）
    if new_records or len(history_data) == 0:
        save_data(history_data)
        print(f"\n🎉 成功更新 {len(new_records)} 条新版本")
        for r in new_records:
            print(f"- {r['platform']} | {r['version']}")
    else:
        print("\nℹ️ 当前已是最新版本，无更新")

if __name__ == "__main__":
    main()
