#!/usr/bin/env python3
"""
0X1 Desktop Client v1.0.4
Cross-Platform Remote Desktop Manager (Windows, Linux, macOS)
"""
import sys
import os
import platform
import subprocess
import urllib.request
import configparser
import tkinter as tk
from tkinter import ttk, messagebox

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "0X1-Settings.ini")
GITHUB_IP_URL = "https://raw.githubusercontent.com/kmolitzy/ggggggg/main/CURRENT_IP.txt"

class App0X1(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("0X1 Desktop Client v1.0.4 - Remote Arch Linux")
        self.geometry("640x580")
        self.resizable(False, False)

        # Theme Colors (Tokyo Night)
        self.c_bg = "#1a1b26"
        self.c_card = "#24283b"
        self.c_fg = "#c0caf5"
        self.c_accent = "#7aa2f7"
        self.c_green = "#9ece6a"
        self.c_btn = "#3b4261"
        self.c_btn_fg = "#ffffff"

        self.configure(bg=self.c_bg)

        # Style configuration
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=self.c_bg, foreground=self.c_fg, font=("Segoe UI", 10))
        style.configure("TLabel", background=self.c_bg, foreground=self.c_fg)
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=self.c_accent)
        style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#7982a9")
        style.configure("Card.TLabelframe", background=self.c_card, foreground=self.c_accent, relief="flat", borderwidth=1)
        style.configure("Card.TLabelframe.Label", background=self.c_card, foreground=self.c_accent, font=("Segoe UI", 10, "bold"))
        style.configure("TCheckbutton", background=self.c_card, foreground=self.c_fg)

        self.build_ui()
        self.load_settings()

    def build_ui(self):
        # Header
        f_top = tk.Frame(self, bg=self.c_bg, padx=20, pady=12)
        f_top.pack(fill=tk.X)

        tk.Label(f_top, text="⚡ 0X1 DESKTOP CLIENT v1.0.4", font=("Segoe UI", 15, "bold"), bg=self.c_bg, fg=self.c_accent).pack(anchor="w")
        tk.Label(f_top, text="Koneksi Remote Desktop Cepat & Optimal ke Arch Linux Cloud", font=("Segoe UI", 9), bg=self.c_bg, fg="#7982a9").pack(anchor="w")

        # Container
        f_body = tk.Frame(self, bg=self.c_bg, padx=20)
        f_body.pack(fill=tk.BOTH, expand=True)

        # Card 1: Server Config
        lf_server = tk.LabelFrame(f_body, text=" [1] Konfigurasi Server & Akun Cloud ", bg=self.c_card, fg=self.c_accent, font=("Segoe UI", 10, "bold"), padx=12, pady=10)
        lf_server.pack(fill=tk.X, pady=(0, 10))

        # IP Row
        r1 = tk.Frame(lf_server, bg=self.c_card)
        r1.pack(fill=tk.X, pady=4)
        tk.Label(r1, text="IP Tailscale:", width=14, anchor="w", bg=self.c_card, fg=self.c_fg).pack(side=tk.LEFT)
        self.ent_ip = tk.Entry(r1, bg="#16161e", fg="#ffffff", insertbackground="#ffffff", font=("Consolas", 11, "bold"), relief="flat", highlightbackground="#414868", highlightthickness=1)
        self.ent_ip.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=3)
        btn_fetch = tk.Button(r1, text="🌐 Ambil IP Aktif", bg="#3d59a1", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", activebackground="#7aa2f7", command=self.fetch_ip)
        btn_fetch.pack(side=tk.RIGHT, ipadx=10, ipady=2)

        # Port & Username Row
        r2 = tk.Frame(lf_server, bg=self.c_card)
        r2.pack(fill=tk.X, pady=4)
        tk.Label(r2, text="Port RDP:", width=14, anchor="w", bg=self.c_card, fg=self.c_fg).pack(side=tk.LEFT)
        self.ent_port = tk.Entry(r2, bg="#16161e", fg="#ffffff", insertbackground="#ffffff", font=("Consolas", 10), relief="flat", highlightbackground="#414868", highlightthickness=1, width=10)
        self.ent_port.pack(side=tk.LEFT, ipady=3)

        tk.Label(r2, text="Username:", width=10, anchor="e", bg=self.c_card, fg=self.c_fg).pack(side=tk.LEFT, padx=(10, 4))
        self.ent_user = tk.Entry(r2, bg="#16161e", fg="#ffffff", insertbackground="#ffffff", font=("Consolas", 10), relief="flat", highlightbackground="#414868", highlightthickness=1)
        self.ent_user.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)

        # Password Row
        r3 = tk.Frame(lf_server, bg=self.c_card)
        r3.pack(fill=tk.X, pady=4)
        tk.Label(r3, text="Password Cloud:", width=14, anchor="w", bg=self.c_card, fg=self.c_fg).pack(side=tk.LEFT)
        self.ent_pass = tk.Entry(r3, bg="#16161e", fg="#ffffff", insertbackground="#ffffff", font=("Consolas", 10), relief="flat", highlightbackground="#414868", highlightthickness=1, show="*")
        self.ent_pass.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=3)
        self.show_pass_var = tk.BooleanVar(value=False)
        chk_show = tk.Checkbutton(r3, text="Lihat", variable=self.show_pass_var, bg=self.c_card, fg=self.c_fg, selectcolor="#16161e", activebackground=self.c_card, command=self.toggle_pass)
        chk_show.pack(side=tk.RIGHT)

        # Card 2: Display & Options
        lf_disp = tk.LabelFrame(f_body, text=" [2] Pengaturan Tampilan & Performa ", bg=self.c_card, fg=self.c_accent, font=("Segoe UI", 10, "bold"), padx=12, pady=10)
        lf_disp.pack(fill=tk.X, pady=(0, 10))

        # Resolution Row
        r4 = tk.Frame(lf_disp, bg=self.c_card)
        r4.pack(fill=tk.X, pady=4)
        tk.Label(r4, text="Resolusi Layar:", width=14, anchor="w", bg=self.c_card, fg=self.c_fg).pack(side=tk.LEFT)
        self.res_options = [
            "Fullscreen (Layar Penuh Otomatis Sesuai Layar Laptop)",
            "1920 x 1080 (Full HD)",
            "1600 x 900 (HD+)",
            "1366 x 768 (Standar Laptop 14 Inci)",
            "1280 x 720 (HD 720p - Paling Ringan)"
        ]
        self.res_var = tk.StringVar(value=self.res_options[0])
        self.cmb_res = ttk.Combobox(r4, textvariable=self.res_var, values=self.res_options, state="readonly")
        self.cmb_res.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Checkboxes
        self.chk_clip_var = tk.BooleanVar(value=True)
        self.chk_audio_var = tk.BooleanVar(value=True)
        self.chk_smart_var = tk.BooleanVar(value=True)
        self.chk_cred_var = tk.BooleanVar(value=True)

        c1 = tk.Checkbutton(lf_disp, text="Sinkronisasi Clipboard (Copy-Paste Laptop <-> Cloud)", variable=self.chk_clip_var, bg=self.c_card, fg=self.c_fg, selectcolor="#16161e", activebackground=self.c_card)
        c1.pack(anchor="w", pady=2)
        c2 = tk.Checkbutton(lf_disp, text="Streaming Suara / Audio Cloud ke Speaker Laptop", variable=self.chk_audio_var, bg=self.c_card, fg=self.c_fg, selectcolor="#16161e", activebackground=self.c_card)
        c2.pack(anchor="w", pady=2)
        c3 = tk.Checkbutton(lf_disp, text="Smart Sizing (Auto-Scale jika jendela RDP di-resize)", variable=self.chk_smart_var, bg=self.c_card, fg=self.c_fg, selectcolor="#16161e", activebackground=self.c_card)
        c3.pack(anchor="w", pady=2)
        c4 = tk.Checkbutton(lf_disp, text="Auto-Login Kredensial Windows (Simpan ke cmdkey tanpa tanya password)", variable=self.chk_cred_var, bg=self.c_card, fg=self.c_fg, selectcolor="#16161e", activebackground=self.c_card)
        c4.pack(anchor="w", pady=2)

        # Action Buttons
        f_actions = tk.Frame(f_body, bg=self.c_bg)
        f_actions.pack(fill=tk.X, pady=8)

        btn_conn = tk.Button(f_actions, text="🚀 SAMBUNGKAN KE RDP SEKARANG", font=("Segoe UI", 11, "bold"), bg="#9ece6a", fg="#1a1b26", relief="flat", activebackground="#73daca", command=self.launch_rdp)
        btn_conn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=8)

        btn_save = tk.Button(f_actions, text="💾 Simpan Profil", font=("Segoe UI", 10), bg="#3b4261", fg="#ffffff", relief="flat", command=self.save_settings)
        btn_save.pack(side=tk.LEFT, padx=(0, 8), ipadx=8, ipady=8)

        btn_help = tk.Button(f_actions, text="📖 Panduan", font=("Segoe UI", 10), bg="#3b4261", fg="#ffffff", relief="flat", command=self.open_guide)
        btn_help.pack(side=tk.LEFT, ipadx=8, ipady=8)

        # Status Bar
        self.lbl_status = tk.Label(self, text="Status: Siap terhubung ke Arch Linux Cloud.", font=("Segoe UI", 9), bg="#16161e", fg="#a9b1d6", anchor="w", padx=15, pady=6)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def toggle_pass(self):
        if self.show_pass_var.get():
            self.ent_pass.config(show="")
        else:
            self.ent_pass.config(show="*")

    def load_settings(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE)
            ip = config.get("Connection", "IP", fallback="100.100.170.82")
            port = config.get("Connection", "Port", fallback="3389")
            user = config.get("Connection", "Username", fallback="archuser")
            pwd = config.get("Connection", "Password", fallback="pochi@333")
            res_idx = config.getint("Display", "Resolution", fallback=0)
            clip = config.getboolean("Features", "Clipboard", fallback=True)
            audio = config.getboolean("Features", "Audio", fallback=True)
            smart = config.getboolean("Features", "SmartSizing", fallback=True)
            creds = config.getboolean("Features", "SaveCreds", fallback=True)
        else:
            ip, port, user, pwd = "100.100.170.82", "3389", "archuser", "pochi@333"
            res_idx = 0
            clip, audio, smart, creds = True, True, True, True

        self.ent_ip.delete(0, tk.END)
        self.ent_ip.insert(0, ip)
        self.ent_port.delete(0, tk.END)
        self.ent_port.insert(0, port)
        self.ent_user.delete(0, tk.END)
        self.ent_user.insert(0, user)
        self.ent_pass.delete(0, tk.END)
        self.ent_pass.insert(0, pwd)

        if 0 <= res_idx < len(self.res_options):
            self.res_var.set(self.res_options[res_idx])
        self.chk_clip_var.set(clip)
        self.chk_audio_var.set(audio)
        self.chk_smart_var.set(smart)
        self.chk_cred_var.set(creds)

    def save_settings(self):
        config = configparser.ConfigParser()
        config["Connection"] = {
            "IP": self.ent_ip.get().strip(),
            "Port": self.ent_port.get().strip(),
            "Username": self.ent_user.get().strip(),
            "Password": self.ent_pass.get().strip()
        }
        idx = self.res_options.index(self.res_var.get()) if self.res_var.get() in self.res_options else 0
        config["Display"] = {
            "Resolution": str(idx)
        }
        config["Features"] = {
            "Clipboard": str(self.chk_clip_var.get()),
            "Audio": str(self.chk_audio_var.get()),
            "SmartSizing": str(self.chk_smart_var.get()),
            "SaveCreds": str(self.chk_cred_var.get())
        }
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
        self.lbl_status.config(text="[OK] Profil pengaturan berhasil disimpan ke 0X1-Settings.ini!", fg=self.c_green)

    def fetch_ip(self):
        self.lbl_status.config(text="[INFO] Menghubungi GitHub untuk mengambil IP aktif...", fg=self.c_accent)
        self.update()
        try:
            req = urllib.request.Request(GITHUB_IP_URL, headers={"User-Agent": "0X1-Desktop/1.0.4"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = resp.read().decode("utf-8", errors="ignore")
            # Parse IP
            import re
            m = re.search(r"100\.\d{1,3}\.\d{1,3}\.\d{1,3}", data)
            if m:
                new_ip = m.group(0)
                self.ent_ip.delete(0, tk.END)
                self.ent_ip.insert(0, new_ip)
                self.lbl_status.config(text=f"[SUKSES] IP berhasil diperbarui: {new_ip}", fg=self.c_green)
            else:
                self.lbl_status.config(text="[PERINGATAN] IP format Tailscale tidak ditemukan di CURRENT_IP.txt.", fg="#e0af68")
        except Exception as e:
            self.lbl_status.config(text=f"[ERROR] Gagal mengambil IP: {str(e)}", fg="#f7768e")

    def open_guide(self):
        guide_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Panduan-0X1.html")
        if os.path.exists(guide_path):
            if platform.system() == "Windows":
                os.startfile(guide_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", guide_path])
            else:
                subprocess.Popen(["xdg-open", guide_path])
        else:
            messagebox.showinfo("Panduan", "Panduan dapat diakses via repo: https://github.com/kmolitzy/ggggggg")

    def launch_rdp(self):
        ip = self.ent_ip.get().strip()
        port = self.ent_port.get().strip() or "3389"
        user = self.ent_user.get().strip() or "archuser"
        pwd = self.ent_pass.get().strip()

        if not ip:
            messagebox.showwarning("Peringatan", "Harap masukkan IP Tailscale Cloud!")
            return

        self.save_settings()

        cur_os = platform.system()
        if cur_os == "Windows":
            # Windows Credential Manager
            if self.chk_cred_var.get() and pwd:
                try:
                    subprocess.run(
                        f"cmdkey /generic:TERMSRV/{ip} /user:{user} /pass:{pwd}",
                        shell=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                except Exception:
                    pass

            # RDP File generation
            idx = self.res_options.index(self.res_var.get()) if self.res_var.get() in self.res_options else 0
            screen_mode = 2 if idx == 0 else 1
            dims = [(1920, 1080), (1920, 1080), (1600, 900), (1366, 768), (1280, 720)]
            w, h = dims[idx]

            rdp_content = f"""screen mode id:i:{screen_mode}
use multimon:i:0
desktopwidth:i:{w}
desktopheight:i:{h}
session bpp:i:32
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:6
networkautodetect:i:1
bandwidthautodetect:i:1
displayconnectionbar:i:1
enableworkspacereconnect:i:0
disable wallpaper:i:0
allow font smoothing:i:1
allow desktop composition:i:1
disable full window drag:i:0
disable menu anims:i:0
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
full address:s:{ip}:{port}
audiomode:i:{0 if self.chk_audio_var.get() else 2}
redirectprinters:i:0
redirectcomports:i:0
redirectsmartcards:i:0
redirectclipboard:i:{1 if self.chk_clip_var.get() else 0}
redirectposdevices:i:0
autoreconnection enabled:i:1
authentication level:i:0
prompt for credentials:i:0
negotiate security layer:i:1
remoteapplicationmode:i:0
username:s:{user}
smart sizing:i:{1 if self.chk_smart_var.get() else 0}
enablecredsspsupport:i:0
"""
            rdp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "0X1-Session.rdp")
            with open(rdp_file, "w") as f:
                f.write(rdp_content)

            self.lbl_status.config(text="[CONNECTING] Membuka sesi mstsc.exe...", fg=self.c_accent)
            subprocess.Popen(["mstsc.exe", rdp_file])
            self.lbl_status.config(text="[TERHUBUNG] Sesi RDP telah dibuka di laptop Anda!", fg=self.c_green)

        elif cur_os == "Linux":
            self.lbl_status.config(text="[LINUX] Membuka koneksi RDP (xfreerdp)...", fg=self.c_accent)
            cmd = [
                "xfreerdp",
                f"/v:{ip}:{port}",
                f"/u:{user}",
                f"/p:{pwd}",
                "/dynamic-resolution",
                "/clipboard",
                "/sound:sys:alsa",
                "/cert:ignore"
            ]
            try:
                subprocess.Popen(cmd)
                self.lbl_status.config(text="[TERHUBUNG] xfreerdp berhasil dijalankan!", fg=self.c_green)
            except FileNotFoundError:
                messagebox.showerror("Error", "xfreerdp tidak ditemukan di sistem Linux Anda. Install via: sudo apt install freerdp2-x11 atau pacman -S freerdp")
        elif cur_os == "Darwin":
            self.lbl_status.config(text="[macOS] Membuka URL RDP...", fg=self.c_accent)
            subprocess.Popen(["open", f"rdp://{user}@{ip}:{port}"])
            self.lbl_status.config(text="[TERHUBUNG] Microsoft Remote Desktop dibuka!", fg=self.c_green)

if __name__ == "__main__":
    app = App0X1()
    app.mainloop()
