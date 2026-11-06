@echo off
setlocal enabledelayedexpansion
title STEPUP FOOTWEAR POS - QUAN LY BAN HANG GIAY DEP

echo ===================================================================
echo   HE THONG QUAN LY BAN HANG GIAY DEP THOI TRANG - STEPUP POS (IUH)
echo   Do an Mon hoc: Lap trinh huong su kien voi Java
echo ===================================================================

:: 1. Kiem tra Java Runtime Environment tren he thong
where javaw >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "JAVA_CMD=javaw"
) else (
    if defined JAVA_HOME (
        if exist "%JAVA_HOME%\bin\javaw.exe" (
            set "JAVA_CMD=%JAVA_HOME%\bin\javaw.exe"
        )
    )
)

if not defined JAVA_CMD (
    echo [LOI] Khong tim thay lenh 'javaw' tren PATH hoac JAVA_HOME!
    echo Vui long cai dat JDK 17 (khuyen nghi Eclipse Adoptium Temurin-17)
    echo va thiet lap bien moi truong JAVA_HOME hop le.
    echo.
    echo Nhan mot phim bat ky de thoat...
    pause >nul
    exit /b 1
)

:: 2. Kiem tra thu muc bin va file bytecode Main.class
if not exist "bin\Main.class" (
    echo [CANH BAO] Chua tim thay thu muc bin hoac Main.class.
    echo Dang tu dong bien dich ma nguon voi JDK 17 (UTF-8)...
    javac --release 17 -encoding UTF-8 -cp "lib/*;src" -d bin src\Main.java src\connectDB\*.java src\entity\*.java src\dao\*.java src\gui\*.java
    if %ERRORLEVEL% neq 0 (
        echo [LOI] Bien dich that bai! Vui long kiem tra lai ma nguon src.
        pause
        exit /b 1
    )
    echo [THANH CONG] Bien dich hoan tat.
)

:: 3. Khoi chay ung dung voi ma hoa UTF-8
echo Dang khoi chay ung dung StepUp Footwear POS...
start "" "%JAVA_CMD%" -Dfile.encoding=UTF-8 -cp "bin;lib/*" Main
exit /b 0
