@echo off

echo 正在反编译 crashDigger1.1.apk...

rem 设置变量
set APK_FILE="D:\文档\04_总结分享\crashDigger1.1.apk"
set OUTPUT_DIR="D:\trae_project\crashDigger1.1"
set APKTOOL_JAR="%~dp0apktool.jar"

echo APK文件: %APK_FILE%
echo 输出目录: %OUTPUT_DIR%
echo Apktool路径: %APKTOOL_JAR%

rem 检查Java是否安装
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Java环境，请先安装Java
    pause
    exit /b 1
)

rem 检查APK文件是否存在
if not exist %APK_FILE% (
    echo 错误: APK文件不存在
    pause
    exit /b 1
)

rem 创建输出目录
if exist %OUTPUT_DIR% (
    echo 警告: 输出目录已存在，将被覆盖
    rd /s /q %OUTPUT_DIR%
)
mkdir %OUTPUT_DIR%

rem 运行apktool反编译
echo 开始反编译...
java -jar %APKTOOL_JAR% d -f %APK_FILE% -o %OUTPUT_DIR%

if %errorlevel% equ 0 (
    echo 成功: 反编译完成
    echo 反编译结果保存在: %OUTPUT_DIR%
) else (
    echo 错误: 反编译失败
)

echo 按任意键退出...
pause >nul