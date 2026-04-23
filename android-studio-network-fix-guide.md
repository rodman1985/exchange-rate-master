# Android Studio "Unable to access Android SDK add-on list" 修复指南

## 问题描述
Android Studio 启动时出现 "Unable to access Android SDK add-on list" 错误，导致无法正常访问 SDK 管理器和下载 SDK 组件。

## 可能的原因
1. 网络连接问题
2. 代理设置问题
3. Android Studio 配置问题
4. SDK 路径配置错误

## 修复步骤

### 步骤 1: 检查网络连接
- 确认您的网络连接正常
- 尝试访问 https://dl.google.com 验证是否能连接到 Google 服务器

### 步骤 2: 配置 Android Studio VM 选项
1. 关闭 Android Studio
2. 找到 Android Studio 的安装目录：
   `D:\Program Files\Android\Android Studio\bin`
3. 备份 `studio64.exe.vmoptions` 文件
4. 编辑 `studio64.exe.vmoptions` 文件，在末尾添加以下内容：
   ```
   # Network configuration
   -Djava.net.preferIPv4Stack=true
   -Djava.net.preferIPv6Addresses=false
   -Dhttp.proxyHost=
   -Dhttp.proxyPort=
   -Dhttps.proxyHost=
   -Dhttps.proxyPort=
   ```

### 步骤 3: 检查 Android SDK 路径配置
1. 打开 Android Studio
2. 进入 File > Settings > Appearance & Behavior > System Settings > Android SDK
3. 确认 SDK Location 正确设置为：
   `C:\Users\Microsoft\AppData\Local\Android\Sdk`
4. 点击 "Edit" 按钮重新选择 SDK 路径

### 步骤 4: 清除 Android Studio 缓存
1. 关闭 Android Studio
2. 删除以下目录：
   - `C:\Users\Microsoft\AppData\Local\Google\AndroidStudio2025.3.3\caches`
   - `C:\Users\Microsoft\AppData\Local\Google\AndroidStudio2025.3.3\logs`
3. 重新启动 Android Studio

### 步骤 5: 检查 hosts 文件
1. 打开 `C:\Windows\System32\drivers\etc\hosts` 文件
2. 确保没有阻止 Google 服务的条目
3. 如果有相关条目，暂时注释掉

### 步骤 6: 使用命令行启动 SDK 管理器
1. 打开命令提示符
2. 导航到 SDK tools 目录：
   `cd C:\Users\Microsoft\AppData\Local\Android\Sdk\tools\bin`
3. 运行 SDK 管理器：
   `sdkmanager --list`
4. 检查是否能正常列出可用的 SDK 包

### 步骤 7: 重置 Android Studio 配置
1. 关闭 Android Studio
2. 删除以下目录：
   `C:\Users\Microsoft\AppData\Roaming\Google\AndroidStudio2025.3.3`
3. 重新启动 Android Studio，按照向导重新配置

## 其他解决方案

### 方案 A: 使用代理服务器
如果您的网络环境需要代理，可以在 Android Studio 中配置代理：
1. File > Settings > Appearance & Behavior > System Settings > HTTP Proxy
2. 选择 "Manual proxy configuration"
3. 输入代理服务器地址和端口

### 方案 B: 使用国内镜像
1. 打开 SDK Manager
2. 点击 "SDK Update Sites"
3. 添加国内镜像地址，例如：
   - 清华大学镜像：https://mirrors.tuna.tsinghua.edu.cn/android/repository/
   - 阿里云镜像：https://maven.aliyun.com/repository/android

## 验证方法
1. 重新启动 Android Studio
2. 打开 SDK Manager
3. 检查是否能正常加载 SDK 包列表
4. 尝试下载一个 SDK 组件，验证网络连接正常

## 常见问题

**Q: 仍然无法访问 SDK add-on list**
A: 尝试暂时关闭防火墙和杀毒软件，然后重新启动 Android Studio

**Q: SDK Manager 显示空白**
A: 检查网络连接，确保能访问 Google 服务器，或使用国内镜像

**Q: 下载 SDK 组件失败**
A: 检查网络连接，或尝试使用代理服务器

如果以上方法都无法解决问题，建议重新安装 Android Studio 和 SDK。