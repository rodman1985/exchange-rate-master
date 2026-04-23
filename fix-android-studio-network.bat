@echo off

echo 正在修复 Android Studio 网络问题...

echo 1. 检查 Android SDK 路径...
if exist "C:\Users\Microsoft\AppData\Local\Android\Sdk" (
    echo ✓ Android SDK 路径存在
) else (
    echo ✗ Android SDK 路径不存在
)

echo 2. 创建 Android Studio 网络配置...

echo 创建 studio64.exe.vmoptions.backup 备份文件...
if exist "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions" (
    copy "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions" "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions.backup" >nul
    echo ✓ 已创建备份
)

echo 3. 修改 VM 选项文件，添加网络配置...

echo 正在添加网络参数到 studio64.exe.vmoptions...

echo -Xms256m > "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Xmx2048m >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -XX:JbrShrinkingGcMaxHeapFreeRatio=40 >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -XX:ReservedCodeCacheSize=512m >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -XX:+HeapDumpOnOutOfMemoryError >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -XX:-OmitStackTraceInFastThrow >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -XX:CICompilerCount=2 >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -XX:+IgnoreUnrecognizedVMOptions >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -XX:+UnlockDiagnosticVMOptions >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -XX:TieredOldPercentage=100000 >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -ea >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Dsun.io.useCanonCaches=false >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Dsun.java2d.metal=true >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Djbr.catch.SIGABRT=true >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Djdk.http.auth.tunneling.disabledSchemes="" >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Djdk.attach.allowAttachSelf=true >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Djdk.module.illegalAccess.silent=true >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Djdk.nio.maxCachedBufferSize=2097152 >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Djava.util.zip.use.nio.for.zip.file.access=true >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Dkotlinx.coroutines.debug=off >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Djava.nio.file.spi.DefaultFileSystemProvider=com.intellij.platform.core.nio.fs.MultiRoutingFileSystemProvider >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo. >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Dflags.configuration.level=COMPLETE >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Dflags.debug.enabled=false >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo. >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo rem 网络配置 >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Djava.net.preferIPv4Stack=true >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Djava.net.preferIPv6Addresses=false >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Dhttp.proxyHost= >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Dhttp.proxyPort= >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Dhttps.proxyHost= >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"
echo -Dhttps.proxyPort= >> "D:\Program Files\Android\Android Studio\bin\studio64.exe.vmoptions"

echo ✓ 已添加网络配置

echo 4. 检查 hosts 文件...
if exist "C:\Windows\System32\drivers\etc\hosts" (
    echo ✓ hosts 文件存在
) else (
    echo ✗ hosts 文件不存在
)

echo 5. 启动 Android Studio 进行测试...
echo 请手动启动 Android Studio 并检查 SDK 管理器是否能正常访问 add-on 列表

echo 修复完成！
echo 按任意键退出...
pause >nul