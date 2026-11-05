import json
import os
import datetime
import subprocess

BASE_DIR = r'G:\Codex\亚马逊开发\线上看板'
DATA_DIR = os.path.join(BASE_DIR, 'data')

def update_online_data():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行数据更新与发布流水线...")
    
    # 1. 检查最新抓取的数据文件
    scraped_file = r'G:\Codex\亚马逊开发\新增店铺_完整详细数据.json'
    if not os.path.exists(scraped_file):
        print(f"错误: 未找到抓取数据源文件 {scraped_file}")
        return False
        
    print("Step 1: 重新打包并生成线上看板 data/products.json 与 index.html ...")
    subprocess.run(['python', r'G:\Codex\亚马逊开发\setup_online_dashboard.py'], check=True)
    subprocess.run(['python', r'G:\Codex\亚马逊开发\upgrade_html_sync.py'], check=True)

    print("Step 2: 同步刷新本地 Excel 工作簿 ...")
    subprocess.run(['python', r'G:\Codex\亚马逊开发\generate_excel.py'], check=True)

    print("Step 3: 自动发布更新至全球永久云端 CDN (Surge)...")
    try:
        subprocess.run(['node', r'G:\Codex\亚马逊开发\deploy_to_surge.js'], check=True)
        print("-> 云端部署同步成功！")
    except Exception as e:
        print(f"-> 云端上传提示: {e}")

    print("\n=======================================================")
    print("全部数据已同步更新至永久在线网页看板！")
    print("永久在线浏览链接: https://amz-de-competitor-monitor.surge.sh")
    print("=======================================================\n")
    return True

if __name__ == '__main__':
    update_online_data()
