from http.server  import HTTPServer, SimpleHTTPRequestHandler 
import ssl
import socket
import subprocess
import os
import sys
import atexit


class NoCacheHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
    # 这里使用了一个谷歌的公共DNS服务器地址和端口
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '192.168.137.1'
    finally:
        s.close()
    return IP

def set_hotspot_dns(action="add"):
    try:
        ip_addr = get_local_ip()
        # 使用PowerShell命令设置DNS
        if action == 'add':
            cmd = [
                'powershell',
                'Get-NetAdapter | '
                'Where-Object { $_.InterfaceDescription -match "Microsoft (Wi-Fi Direct|Hosted Network) Virtual Adapter" } | '
                f'Set-DnsClientServerAddress -ServerAddresses "{ip_addr}"'
            ]
        else:
            cmd = [
                'powershell',
                'Get-NetAdapter | '
                'Where-Object { $_.InterfaceDescription -match "Microsoft (Wi-Fi Direct|Hosted Network) Virtual Adapter" } | '
                f'Set-DnsClientServerAddress -ServerAddresses "114.114.114.114"'
            ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        os.system('ipconfig /flushdns')
        
        if result.returncode == 0:
            print("成功设置DNS" if action == "add" else "成功恢复DNS")
        else:
            print("设置" if action == "add" else "恢复", f"DNS失败: {result.stderr}，返回码{str(result.returncode)}")
            os.system('pause')
            cleanup()
            os._exit(-1)
            sys.exit(-1)
    except Exception as e:
        print("设置" if action == "add" else "恢复", f"DNS时发生错误: {str(e)}")
        os.system('pause')
        cleanup()
        os._exit(-1)
        sys.exit(-1)


def modify_hosts(action='add'):
        """修改hosts文件"""
        cmd = f'NSudoL.exe -UseCurrentConsole -U:T -P:E cmd /c '
        if action == 'add':
            cmd += f'echo {get_local_ip()} wapcdn.qupeiyin.cn >C:\\Windows\\System32\\drivers\\etc\\hosts'
        else:
            cmd += 'type nul > C:\\Windows\\System32\\drivers\\etc\\hosts'
        cmd += ' && ipconfig /flushdns && ipconfig /flushdns && ipconfig /flushdns  && powershell Clear-DnsClientCache'
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            print("修改hosts成功")
            if action == 'add':
                print("提示", "更改需等待几秒并让手表重新连接热点生效\n若迟迟不生效，请在电脑重启热点或/和执行ipconfig /flushdns\n有时也许要重启电脑（因为flushdns是《玄》学）")
        except subprocess.CalledProcessError as e:
            print(f"修改hosts失败: {e}")
            os.system('pause')
            cleanup()
            os._exit(-1)
            sys.exit(-1)


def cleanup():
    """清理函数，恢复hosts文件并停止服务"""
    print("\n正在清理...")
    modify_hosts(action="remove")
    print("已恢复hosts文件")
    set_hotspot_dns(action="remove")
    httpd.shutdown()
    print("服务已停止")

def print_xtc_banner():
    """打印炫酷的蓝色空心字符艺术字"""
    from colorama import init, Fore, Style
    init()  # 初始化colorama
    
    banner = r"""
 __  __  _____    ____     ____                                                
 \ \/ / |_   _|  / ___|   | __ )   _ __    ___   __      __  ___    ___   _ __ 
  \  /    | |   | |       |  _ \  | '__|  / _ \  \ \ /\ / / / __|  / _ \ | '__|
  /  \    | |   | |___    | |_) | | |    | (_) |  \ V  V /  \__ \ |  __/ | |   
 /_/\_\   |_|    \____|   |____/  |_|     \___/    \_/\_/   |___/  \___| |_|   

    Version 1.0.0, By 星旬Star, License: GPL-2.0          
    引用的外部库：
        __________________________________________
        |     库名     |    版本号   |  开源协议  |
        -------------------------------------------
        |   XTC-UI     |     1.0     |    MIT     |
        -------------------------------------------
        |   colorama   |    0.4.6    |   BSD-3    | 
        -------------------------------------------
        |     NSudo    |     8.2     |    MIT     |   
        -------------------------------------------
        |     jsQR     |    latest   |    MIT     |
        -------------------------------------------                                                  
    """
    print(Fore.BLUE + banner + Style.RESET_ALL)
    warn = Fore.YELLOW + "免责声明：这个工具内的证书为OpenSSL自签证书，仅用于模拟某QPY(化名)服务器，不具备真实法律效应，" + Style.RESET_ALL + Fore.GREEN + "另外，您也可以将证书文件替换为自己的，在证书有效的情况下，不会对程序功能造成影响" + Style.RESET_ALL
    # print(warn)

# 在try块的最开始添加打印banner
try:
    
    set_hotspot_dns()
    modify_hosts(action="add")
    server_address = ('0.0.0.0', 443)
    httpd = HTTPServer(server_address, NoCacheHTTPRequestHandler)
    
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        server_side=True,
        certfile='cert.pem',
        keyfile='key.pem',
        ssl_version=ssl.PROTOCOL_TLS
    )
    print_xtc_banner()  # 添加这行
    print("服务已成功启动！按Ctrl+C键则停止服务（千万别直接关闭窗口，否则会导致网络异常并卡入后室！！！）")
    
    # 注册清理函数
    atexit.register(cleanup)
    
    httpd.serve_forever()
except KeyboardInterrupt:
    cleanup()
except Warning as e:
    print(e)
    pass
except Exception as e:
    print(f"发生错误: {e}")
    cleanup()
