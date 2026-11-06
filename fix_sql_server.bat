@echo off
title SUA LOI KET NOI SQL SERVER - STEPUP POS (IUH)
echo ===================================================================
echo   DANG KHOI CHAY TRINH SUA LOI KET NOI SQL SERVER TU DONG...
echo   (Vui long nhan "Yes" tren bang hop thoai Administrator neu co)
echo ===================================================================
powershell -Command "Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"\"%~dp0fix_sql_server.ps1\"\"' -Verb RunAs"
exit
