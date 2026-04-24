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

        # ==============================================
        # 【适配真实接口结构】提取所有平台版本
        # ==============================================
        result = []
        
        # Windows NT 版本 (最新版QQ)
        win = data.get("Windows", {})
        if win:
            # Win64
            result.append({
                "platform": "Windows x64",
                "version": win["version"],
                "download_url": win["ntDownloadX64Url"],
                "update_time": get_current_time()
            })
            # Win32 (x86)
            result.append({
                "platform": "Windows x86",
                "version": win["version"],
                "download_url": win["ntDownloadUrl"],
                "update_time": get_current_time()
            })
            # Windows ARM64
            result.append({
                "platform": "Windows ARM64",
                "version": win["version"],
                "download_url": win["ntDownloadARMUrl"],
                "update_time": get_current_time()
            })

        # macOS 版本
        mac = data.get("macOS", {})
        if mac:
            result.append({
                "platform": "macOS (通用)",
                "version": mac["version"].split(" ")[0],
                "download_url": mac["downloadUrl"],
                "update_time": get_current_time()
            })

        # 打印结果
        print(f"✅ 获取到 {len(result)} 个平台版本")
        print("📄 即将写入数据：")
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 写入文件
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print("✅ 文件写入成功！")

    except Exception as e:
        print(f"❌ 运行错误：{str(e)}")

if __name__ == "__main__":
    main()
