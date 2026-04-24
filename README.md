# 🚀 NTQQ 自动版本监控
> 7×24 小时全自动监控 | 官方最新下载地址实时同步 | 历史版本永久留存
> 依托 GitHub Actions 免费运行，无需服务器、无需维护

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-运行中-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![支持平台](https://img.shields.io/badge/支持-Win64%2FWin32%2FMac-orange)
![许可证](https://img.shields.io/github/license/your-username/qq-pc-monitor)

---

## 📌 项目介绍
本项目通过定时请求 QQ 官方公开配置接口，**自动获取最新版本下载地址**，检测到版本更新时自动追加记录，永久保存所有历史版本数据，全程无人值守自动运行。

## ✨ 核心特性
- ✅ **全自动运行**：GitHub Actions 7×24 小时定时监控
- ✅ **多平台适配**：同步 Windows/Mac/Linux 官方下载地址
- ✅ **增量更新**：仅新增新版本，不覆盖、不删除历史数据
- ✅ **自动记录**：每条数据附带北京时间、版本号、下载链接
- ✅ **零成本部署**：完全免费，无需服务器，开箱即用

## 📂 文件结构
├── main.py # 核心监控脚本
├── .github/workflows/sync.yml # 定时任务配置
├── .versions/linux.json #Linux 历史版本
├── .versions/macos.json #mac 历史版本
├── .versions/windows.json #win 历史版本
└── README.md # 项目说明文档

## 🚀 部署教程
1. **新建 GitHub 仓库**
2. 上传本项目所有文件
3. 进入仓库 `Actions` 页面，启用工作流
4. 手动触发一次运行，测试是否正常
5. 部署完成！自动开始监控

## 📊 数据查看
所有版本下载地址统一存储在：
👉 [versions](versions)

## 🔧 自定义配置
### 修改监控频率
编辑 `.github/workflows/sync.yml` 中的 `cron` 表达式：
- 每 30 分钟：`*/30 * * * *`
- 每 1 小时（默认）：`0 */1 * * *`
- 每 6 小时：`0 */6 * * *`

## ⚠️ 免责声明
1. 本项目仅用于**学习和技术研究**，所有数据均来源于 QQ 官方公开接口
2. 请勿用于商业用途或非法用途
3. 如有侵权，请联系删除

---
