
# XTC Browser / QuPeiyinBrowser

基于Python的本地HTTPS代理工具，用于模拟XTC电话手表的英语趣配音服务器环境，并修改数据包实现在手表上输入网址跳转功能

## 功能特性
- 🚀 本地HTTPS服务器（端口443）
- 🔒 自动SSL证书配置
- 🌐 DNS重定向功能
- 📝 自动修改系统hosts文件
- 🔄 内置清理机制确保退出时恢复系统设置

## 快速开始
0. 请打开电脑热点并让XTC手表连接
1. 安装依赖：（发行版无需操作）
```bash
pip install colorama pyopenssl
```
然后复制`NSudoL.exe`至项目的`/src/`目录下

2. 运行程序：
```bash
python main.py
```
发行版请直接运行`main.exe`

3. 手表打开英语趣配音，滑到第三页，点击“《***儿童隐私政策》”，即可打开“浏览器”

4. 按Ctrl+C停止服务

## 技术细节
- 使用Python标准库`http.server`实现Web服务
- 通过`ssl.wrap_socket`实现HTTPS加密
- 自动检测并处理443端口占用
- 支持DNS和hosts文件修改

## 注意事项
⚠️ 需要管理员权限运行  
⚠️ 会临时修改系统DNS和hosts配置  
⚠️ 使用自签名证书（可替换**发行版**中的`cert.pem`和`key.pem`）

## 文件结构
```
qupeiyin_browser/src/
├── app/
│   └── xtc/            # 前端资源
│       └── privacy/     # HTML文件存放
├── cert.pem            # SSL证书（发行版已预置）
├── key.pem             # 私钥文件（发行版已预置）
├── main.py             # 主程序入口
├── ...
└── *.min.* / *.min.*.map / *.min.*.names.json             # 压缩后的前端UI文件以及Sources Map

```

## 开源协议
GPL-2.0 License
