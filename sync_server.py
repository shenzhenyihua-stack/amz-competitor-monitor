import http.server
import socketserver
import subprocess
import os
import sys
import time
import re

PORT = 8088
WEB_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(WEB_DIR)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许跨域与无缓存
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        pass

def run():
    print(f"==================================================")
    print(f"  亚马逊店铺监控看板 · 本地与公网服务引擎")
    print(f"==================================================")
    print(f"本地目录: {WEB_DIR}")
    print(f"本地访问地址: http://127.0.0.1:{PORT}")
    
    # 尝试启动 localtunnel 生成公网访问链接
    tunnel_url = None
    try:
        print("\n正在生成公网安全访问链接（请稍候 3~5 秒）...")
        p = subprocess.Popen(
            ['npx.cmd', 'localtunnel', '--port', str(PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        
        # 读取第一行输出
        start_t = time.time()
        while time.time() - start_t < 12:
            line = p.stdout.readline()
            if 'your url is:' in line:
                tunnel_url = line.split('your url is:')[1].strip()
                break
            time.sleep(0.5)
            
    except Exception as e:
        print(f"公网隧道启动提示: {e}")

    if tunnel_url:
        print(f"\n🎉 公网分享专属链接已生成！")
        print(f"👉 复制发给他人即可直接浏览: {tunnel_url}")
        print(f"（提示：首次打开若出现安全确认页，直接点击'Click to Continue'即可进入看板）")
    else:
        print(f"\n如需局域网查看，可通过当前电脑 IP 访问: http://localhost:{PORT}")

    print("\n--------------------------------------------------")
    print("服务正在持续运行中（后续本地数据更新会自动同步显示）")
    print("如需停止服务，请按 Ctrl + C")
    print("--------------------------------------------------\n")

    with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务已平稳停止。")

if __name__ == '__main__':
    run()
