@echo off
chcp 65001 > nul
title 亚马逊店铺监控数据更新与GitHub云仓自动发布流水线
echo ==============================================================
echo     亚马逊店铺竞对产品监测 · GitHub云仓与永久在线网页自动同步
echo ==============================================================
echo 正在执行自动更新并推送至 GitHub 云仓...
echo.
python update_data_pipeline.py
echo.
echo ==============================================================
echo 发布完成！任何人直接打开以下链接即可实时查看最新产品：
echo https://shenzhenyihua-stack.github.io/amz-competitor-monitor/
echo ==============================================================
pause
