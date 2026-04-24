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
        # 请求超时10秒，避免卡死
        response = requests.get(CONFIG_URL, timeout=10)
        response.raise_for_status()  # 抛出请求异常
        data = response.json()
        
        # 提取需要的平台信息
        platforms = ["win64", "win32", "mac"]
        latest_list = []
        for platform in platforms:
            if platform in data:
                info = data[platform]
                latest_list.append({
                    "platform": platform,
                    "version": info["version"],
                    "download_url": info["url"],
                    "update_time": get_current_time()  # 记录抓取时间
                })
        return latest_list
    except Exception as e:
        print(f"获取最新配置失败：{str(e)}")
        return []

def get_current_time():
    """获取当前时间（UTC+8，北京时间）"""
    from datetime import datetime, timedelta
    utc_now = datetime.utcnow()
    cst_now = utc_now + timedelta(hours=8)
    return cst_now.strftime("%Y-%m-%d %H:%M:%S")

def load_history_data():
    """加载历史版本记录"""
    if not os.path.exists(SAVE_FILE):
        return []
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    """保存数据到JSON文件"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # 1. 获取最新数据
    latest_data = get_latest_qq_config()
    if not latest_data:
        return
    
    # 2. 加载历史数据
    history_data = load_history_data()
    
    # 3. 去重：仅新增【平台+版本号】未存在的记录
    new_records = []
    # 生成历史唯一标识（平台+版本）
    history_keys = {(item["platform"], item["version"]) for item in history_data}
    
    for item in latest_data:
        key = (item["platform"], item["version"])
        if key not in history_keys:
            new_records.append(item)
            history_data.append(item)
    
    # 4. 有新版本则保存，无变化则退出
    if new_records:
        save_data(history_data)
        print(f"✅ 新增 {len(new_records)} 条版本记录：")
        for record in new_records:
            print(f"- {record['platform']} | {record['version']} | {record['download_url']}")
    else:
        print("ℹ️ 暂无新版本，无需更新")

if __name__ == "__main__":
    main()
