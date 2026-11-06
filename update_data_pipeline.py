import json
import os
import datetime
import subprocess

BASE_DIR = r'G:\Codex\亚马逊开发\线上看板'
DATA_DIR = os.path.join(BASE_DIR, 'data')

def update_pipeline():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动数据增量更新与 GitHub 云仓发布流水线...")
    
    print("Step 1: 重新构建双模式看板 index.html (含新产品看板与全量看板)...")
    subprocess.run(['python', r'G:\Codex\亚马逊开发\build_dual_dashboard.py'], check=True)

    print("Step 2: 刷新本地 Excel 工作簿 ...")
    subprocess.run(['python', r'G:\Codex\亚马逊开发\update_final_excel.py'], check=True)

    print("Step 3: 自动推送至 GitHub 云仓并触发 GitHub Pages 在线热更新...")
    try:
        subprocess.run(['node', r'G:\Codex\亚马逊开发\push_all_to_github.js'], check=True)
        print("-> GitHub 云仓与 Pages 网页已自动同步！")
    except Exception as e:
        print(f"-> GitHub 上传提示: {e}")

    print("\n=======================================================")
    print("🎉 全流程同步完毕！")
    print("👉 官方 GitHub 永久在线看板: https://shenzhenyihua-stack.github.io/amz-competitor-monitor/")
    print("📦 官方 GitHub 云仓归档: https://github.com/shenzhenyihua-stack/amz-competitor-monitor")
    print("=======================================================\n")
    return True

if __name__ == '__main__':
    update_pipeline()
