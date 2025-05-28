@echo off
echo ==== EU4存档管理器打包脚本 ====
echo 正在清理旧的构建文件...

if exist "build" rd /s /q build
if exist "dist" rd /s /q dist

echo 正在通过PyInstaller打包应用...
pyinstaller eu4_save_manager.spec

echo.
if %errorlevel% neq 0 (
    echo 打包失败！
) else (
    echo 打包成功！可执行文件位于 dist\EU4存档管理器 目录中
)

echo.
pause
