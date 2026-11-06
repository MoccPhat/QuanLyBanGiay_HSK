# Tu dong yeu cau quyen Administrator (UAC) neu chua co
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Dang yeu cau quyen Administrator de bat TCP/IP va SQL Mixed Mode..." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  DANG TU DONG SUA LOI VA CAU HINH SQL SERVER CHO DU AN   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Bat Mixed Mode Authentication (LoginMode = 2)
Write-Host "[1/4] Bat Mixed Mode (SQL Server and Windows Authentication)..." -ForegroundColor White
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQLServer" -Name "LoginMode" -Value 2

# 2. Bat giao thuc TCP/IP tren cong 1433
Write-Host "[2/4] Bat giao thuc TCP/IP va mo cong 1433..." -ForegroundColor White
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQLServer\SuperSocketNetLib\Tcp" -Name "Enabled" -Value 1
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQLServer\SuperSocketNetLib\Tcp\IPAll" -Name "TcpPort" -Value "1433"
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQLServer\SuperSocketNetLib\Tcp\IPAll" -Name "TcpDynamicPorts" -Value ""

# 3. Khoi dong lai dich vu SQL Server de ap dung
Write-Host "[3/4] Khoi dong lai dich vu MSSQL`$SQLEXPRESS..." -ForegroundColor White
Restart-Service -Name "MSSQL`$SQLEXPRESS" -Force

# 4. Kich hoat tai khoan sa va dat mat khau 'sapassword'
Write-Host "[4/4] Kich hoat tai khoan sa voi mat khau 'sapassword'..." -ForegroundColor White
Start-Sleep -Seconds 2
& sqlcmd -S ".\SQLEXPRESS" -E -Q "ALTER LOGIN sa WITH PASSWORD = 'sapassword', CHECK_POLICY = OFF; ALTER LOGIN sa ENABLE;"

Write-Host "`n>>> HOAN TAT! SQL SERVER DA SAN SANG CHO JAVA SWING KET NOI! <<<" -ForegroundColor Green
Write-Host "Nhan phim bat ky de dong cua so nay..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
