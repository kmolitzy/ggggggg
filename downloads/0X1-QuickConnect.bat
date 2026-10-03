@echo off
title 0X1 QuickConnect - Arch Linux Cloud
color 0b
echo ========================================================
echo        0X1 QUICK CONNECT - ARCH LINUX CLOUD
echo ========================================================
echo.
echo Mengambil IP aktif terbaru dari Cloud...
powershell -Command "$wc = New-Object System.Net.WebClient; try { $ip = ($wc.DownloadString('https://raw.githubusercontent.com/kmolitzy/ggggggg/main/CURRENT_IP.txt') | Select-String -Pattern '100\.\d{1,3}\.\d{1,3}\.\d{1,3}').Matches[0].Value; Set-Content -Path 'ip.tmp' -Value $ip; Write-Host '[OK] IP Ditemukan:' $ip -ForegroundColor Green } catch { Write-Host '[!] Gagal mengambil IP otomatis, memakai default 100.100.170.82' -ForegroundColor Yellow; Set-Content -Path 'ip.tmp' -Value '100.100.170.82' }"

set /p IP=<ip.tmp
del ip.tmp 2>nul

echo Menghubungkan ke %IP%:3389 (User: archuser)...
cmdkey /generic:TERMSRV/%IP% /user:archuser /pass:pochi@333 >nul 2>&1

(
echo full address:s:%IP%:3389
echo prompt for credentials:i:0
echo username:s:archuser
echo smart sizing:i:1
echo audiomode:i:0
echo redirectclipboard:i:1
echo screen mode id:i:2
echo authentication level:i:0
echo enablecredsspsupport:i:0
) > 0X1-Fast.rdp

start mstsc.exe 0X1-Fast.rdp
echo Sesi RDP telah dibuka! Selamat menikmati Arch Linux.
timeout /t 3 >nul
