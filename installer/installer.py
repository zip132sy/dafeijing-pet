# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'installer.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""大肥鲸桌宠 · 安装程序（四步向导）\n\n  1. 许可协议：读 MIT 协议，并列出用到 / 参考的开源项目与数据服务（致谢）\n  2. 环境与位置：检测依赖，并选安装模式（仅当前用户 User / 为所有用户 System）、安装目录、快捷方式；System 模式会自动申请管理员权限\n  3. 基础配置：API、唤醒词、它该怎么称呼你（可以跳过，之后在应用里也能改）\n  4. 确认并安装：装之前先做完整性校验；本机已经装过会问你是「更新 / 修复 / 重新安装」，配置、存档、记录都保留\n\n运行库（Python、图像库、拖拽库）都已经打包进主程序，电脑上不需要额外装任何东西。\n"""
import base64
import ctypes
import hashlib
import json
import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
import winreg
from tkinter import filedialog, messagebox
APP_NAME = '大肥鲸桌宠'
APP_EXE = '大肥鲸桌宠.exe'
VERSION = '1.0'
PUBLISHER = '大肥鲸'
PAYLOAD_SHA256 = '3ebdef3efbef24f6ea0fab88515d4dfcfd2be4011bb04104b352a242024440a3'
PAYLOAD_MIN_BYTES = 1048576
REG_RUN = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
REG_UNINST = 'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\WhalePet'
RUN_VALUE = '大肥鲸桌宠'
BG, CARD = ('#eef3ff', '#ffffff')
FG, DIM = ('#2e3a5c', '#7a86a8')
OK_C, BAD_C, WARN_C = ('#1e8e4e', '#c94f4f', '#c07a12')
ACCENT = '#7ba7f0'
FONT = ('Microsoft YaHei', 10)
FONT_B = ('Microsoft YaHei', 12, 'bold')
FONT_S = ('Microsoft YaHei', 9)
MONO = ('Consolas', 9)
STEPS = ['许可协议', '环境与位置', '基础配置', '确认安装']
DEFAULT_BASE = 'https://api.deepseek.com/v1'
DEFAULT_MODEL = 'deepseek-chat'
DEFAULT_WAKE = '大肥鲸 小鲸 鲸鲸'
DEFAULT_TITLE = '主人'
PROVIDER_DEFAULTS = {'DeepSeek': ('https://api.deepseek.com/v1', 'deepseek-chat'), 'OpenAI': ('https://api.openai.com/v1', 'gpt-4o-mini'), '月之暗面 Kimi': ('https://api.moonshot.cn/v1', 'moonshot-v1-8k'), '通义千问': ('https://dashscope.aliyuncs.com/compatible-mode/v1', 'qwen-plus'), '智谱 GLM': ('https://open.bigmodel.cn/api/paas/v4', 'glm-4-flash'), '本地 Ollama': ('http://localhost:11434/v1', 'qwen2.5')}
LICENSE_TEXT = 'MIT License — 大肥鲸桌宠\n\nCopyright (c) 2026 大肥鲸\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the \"Software\"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n（简单说：随便用、随便改、随便传，但要保留上面这段版权声明；\n 出问题作者不负责。）\n\n\n═══════════ 用到的开源项目（在此致谢） ═══════════\n\n· 大肥鱼桌宠 DaFeiYu Pet\n  https://github.com/XiaoHan-612/dafeiyu-pet\n  桌宠的 16 张小表情贴图（表情/*.png）取自这个项目，表情切换、托盘图标、\n  位置记忆等做法也参考了它。感谢作者。\n  ！注意：该项目没有附带许可证、作者也没有声明授权，因此这些贴图\n    仅限个人学习自用，请勿商用或二次分发；版权归原作者（及形象权利方）所有，\n    并且不在本项目的 MIT 授权范围内。\n\n· Python                  https://www.python.org/\n· Tcl/Tk（图形界面）        https://www.tcl.tk/\n· Pillow（图像处理）        https://python-pillow.org/\n· PyInstaller（打包 exe）   https://pyinstaller.org/\n· tkinterdnd2（文件拖拽）   https://github.com/pmgagne/tkinterdnd2\n\n═══════════ 内置联网查询用到的公开服务 ═══════════\n\n这些是第三方服务，版权与条款归各自所有，本项目只是调用它们：\n· Bing 搜索            https://www.bing.com/\n· Stack Exchange       https://api.stackexchange.com/\n· Open-Meteo 天气       https://open-meteo.com/\n· wttr.in（天气备用）    https://wttr.in/\n· open.er-api.com 汇率  https://www.exchangerate-api.com/\n· timor.tech 节假日     https://timor.tech/\n· ipip.net / ipinfo.io（公网 IP）  https://ipinfo.io/\n\n在线聊天用的是你自己填的 AI 服务（例如 DeepSeek：https://platform.deepseek.com/），\n用它产生的数据与费用，以那家服务商的条款为准。\n'
CAPS = {'basic': 'Language.Basic~~~zh-CN~0.0.1.0', 'tts': 'Language.TextToSpeech~~~zh-CN~0.0.1.0', 'asr': 'Language.Speech~~~zh-CN~0.0.1.0'}
_NO_WINDOW = 134217728
_PS = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe')
_PROBE = '\n[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\nAdd-Type -AssemblyName System.Speech\n$ttsN = \'\'; $ttsErr = \'\'\ntry {\n  $sp = New-Object System.Speech.Synthesis.SpeechSynthesizer\n  $all = @($sp.GetInstalledVoices() | Where-Object { $_.Enabled })\n  $zh = @($all | Where-Object { $_.VoiceInfo.Culture.Name -like \'zh*\' })\n  $ttsN = (($zh | ForEach-Object { $_.VoiceInfo.Name }) -join \'|\')\n} catch { $ttsErr = $_.Exception.Message }\n$asrN = \'\'; $asrErr = \'\'\ntry {\n  $recs = @([System.Speech.Recognition.SpeechRecognitionEngine]::InstalledRecognizers())\n  $zh = @($recs | Where-Object { $_.Culture.Name -like \'zh*\' })\n  $asrN = (($zh | ForEach-Object { $_.Id }) -join \'|\')\n} catch { $asrErr = $_.Exception.Message }\n$mic = \'0\'\ntry {\n  $r = New-Object System.Speech.Recognition.SpeechRecognitionEngine\n  $r.SetInputToDefaultAudioDevice(); $r.Dispose(); $mic = \'1\'\n} catch { }\n[Console]::Out.WriteLine(\"TTS=$ttsN#TTSERR=$ttsErr#ASR=$asrN#ASRERR=$asrErr#MIC=$mic\")\n'
_FOLDERS = '\n[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\nforeach ($n in @(\'Desktop\', \'Programs\', \'LocalApplicationData\')) {\n  [Console]::Out.WriteLine([Environment]::GetFolderPath($n))\n}\n'
_FOLDERID = {'Desktop': '{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}', 'Programs': '{A77F5D77-2E2B-44C3-A6A2-ABA601054A51}', 'LocalApplicationData': '{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}'}
class _GUID(ctypes.Structure):
    _fields_ = [('Data1', ctypes.c_uint32), ('Data2', ctypes.c_uint16), ('Data3', ctypes.c_uint16), ('Data4', ctypes.c_byte * 8)]
def known_folder(fid):
    try:
        g = _GUID()
        if ctypes.windll.ole32.CLSIDFromString(ctypes.c_wchar_p(fid), ctypes.byref(g)):
            return ''
        buf = ctypes.c_wchar_p()
        if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(g), 0, None, ctypes.byref(buf)):
            return ''
        path = buf.value or ''
        ctypes.windll.ole32.CoTaskMemFree(buf)
        return path
    except Exception:
        return ''
def res_path(name):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)
def app_payload():
    """取要安装的主程序：打包后在解包目录里，开发时在 dist 下。"""
    p = res_path(APP_EXE)
    if os.path.isfile(p):
        return p
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        for cand in [os.path.join(base, 'dist_new', APP_EXE), os.path.join(base, 'dist', APP_EXE)]:
            if os.path.isfile(cand):
                return cand
        return ''
def file_sha256(path):
    """算文件的 SHA-256（分块读，省内存）。"""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()
def verify_payload(path):
    """完整性校验：文件在不在、像不像 exe、SHA-256 对不对。返回 (ok, 说明)。"""
    if not path or not os.path.isfile(path):
        return (False, '找不到主程序文件')
    try:
        if os.path.getsize(path) < PAYLOAD_MIN_BYTES:
            return (False, '主程序文件太小，可能不完整')
        with open(path, 'rb') as f:
            if f.read(2) != b'MZ':
                return (False, '主程序文件不是有效的 Windows 程序')
    except OSError as e:
        return (False, f'读取失败：{e}')
    if not PAYLOAD_SHA256:
        return (True, '（未配置校验值，已跳过哈希比对）')
    try:
        digest = file_sha256(path)
    except OSError as e:
        return (False, f'读取失败：{e}')
    if digest.lower() != PAYLOAD_SHA256.lower():
        return (False, f'SHA-256 不一致（实际 {digest[:16]}…，期望 {PAYLOAD_SHA256[:16]}…）')
    return (True, '')
def ps_run(script, timeout=40):
    """跑一段 PowerShell（不提权），返回标准输出。"""
    enc = base64.b64encode(script.encode('utf-16-le')).decode('ascii')
    try:
        p = subprocess.run([_PS, '-NoProfile', '-NoLogo', '-NonInteractive', '-EncodedCommand', enc], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=timeout, creationflags=_NO_WINDOW)
        return (p.stdout or '').strip()
    except Exception:
        return ''
def run_elevated(script):
    """用管理员权限跑一段 PowerShell（会弹 UAC）。返回值 >32 表示成功。"""
    enc = base64.b64encode(script.encode('utf-16-le')).decode('ascii')
    params = '-NoProfile -NoLogo -WindowStyle Hidden -EncodedCommand ' + enc
    try:
        return int(ctypes.windll.shell32.ShellExecuteW(None, 'runas', _PS, params, None, 0))
    except Exception:
        return 0
def is_admin():
    """当前进程是不是管理员。"""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False
def program_files_dir():
    return os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), APP_NAME)
def common_desktop_dir():
    return os.path.join(os.environ.get('PUBLIC', 'C:\\Users\\Public'), 'Desktop')
def common_programs_dir():
    return os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'Microsoft', 'Windows', 'Start Menu', 'Programs')
def default_dir_for(mode, folders):
    """按安装模式给出默认安装目录。mode: user=仅当前用户，system=为所有用户。"""
    if mode == 'system':
        return program_files_dir()
    else:
        return os.path.join(folders.get('LocalApplicationData') or os.path.expanduser('~'), APP_NAME)
def relaunch_self_elevated(extra_args):
    """用管理员权限重新启动本安装器（弹一次 UAC）。返回 True 表示已发起提权。"""
    try:
        frozen = bool(getattr(sys, 'frozen', False))
        exe = sys.executable
        if frozen:
            args = list(extra_args)
            workdir = os.path.dirname(os.path.abspath(exe))
        else:
            args = [os.path.abspath(__file__)] + list(extra_args)
            workdir = os.path.dirname(os.path.abspath(__file__))
        params = subprocess.list2cmdline(args)
        rc = ctypes.windll.shell32.ShellExecuteW(None, 'runas', exe, params, workdir, 1)
        return int(rc) > 32
    except Exception:
        return False
def _reg_install_dir(hive):
    try:
        with winreg.OpenKey(hive, REG_UNINST) as k:
            d = winreg.QueryValueEx(k, 'InstallLocation')[0]
        if d and os.path.isfile(os.path.join(d, APP_EXE)):
            return d
        return ''
    except OSError:
        return ''
def installed_dir():
    """本机已装过的话返回安装目录（先查当前用户，再查所有用户）。"""
    return _reg_install_dir(winreg.HKEY_CURRENT_USER) or _reg_install_dir(winreg.HKEY_LOCAL_MACHINE)
def installed_scope():
    """已装过的安装范围：'system' / 'user' / ''。"""
    if _reg_install_dir(winreg.HKEY_LOCAL_MACHINE):
        return 'system'
    if _reg_install_dir(winreg.HKEY_CURRENT_USER):
        return 'user'
    return ''
def app_running():
    """主程序是不是正在跑（更新前要先让它退出，不然覆盖不了）。"""
    try:
        out = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {APP_EXE}', '/NH'], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=15, creationflags=_NO_WINDOW)
        return APP_EXE.lower() in (out.stdout or '').lower()
    except Exception:
        return False
def wheel_scroll(box):
    """让只读的文本框也能用滚轮翻（禁用的 Text 默认不响应滚轮）。"""
    def on_wheel(event):
        box.yview_scroll((-1) if event.delta > 0 else 1, 'units')
        return 'break'
    box.bind('<MouseWheel>', on_wheel)
def kill_app():
    try:
        subprocess.run(['taskkill', '/IM', APP_EXE, '/F'], capture_output=True, timeout=20, creationflags=_NO_WINDOW)
        time.sleep(1.5)
    except Exception:
        return False
    return True
class Wizard:
    def __init__(self, job=None):
        self.job = job
        self.root = tk.Tk()
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap(res_path('app.ico'))
        except Exception:
            pass
        self.logq = queue.Queue()
        self.results = {}
        self.folders = {'Desktop': '', 'Programs': ''}
        self.busy = False
        self.checking = False
        self.alive = True
        self.step = 0
        self.accepted = False
        self.admin = is_admin()
        self.installed = installed_dir()
        self.installed_scope = installed_scope()
        self.job_deps = None
        self.root.title(f'{APP_NAME} · {('更新' if self.installed else '安装')}程序')
        self.root.protocol('WM_DELETE_WINDOW', self._close)
        self._load_folders()
        self._build()
        self.root.after(120, self._drain)
        if job:
            self._apply_job(job)
        else:
            self.root.after(300, self.check_all)
    def _apply_job(self, job):
        """被提权重启起来的那次：直接按传进来的选择装，不再让主人重走一遍向导。"""
        self.job_deps = job.get('deps') or []
        self.installed = job.get('installed')
        self.mode_var.set(job.get('mode', 'system'))
        self.path_var.set(job.get('target') or self.path_var.get())
        self.action_var.set(job.get('action', 'update'))
        self.desktop_var.set(bool(job.get('desktop')))
        self.menu_var.set(bool(job.get('menu')))
        self.start_var.set(bool(job.get('startup')))
        self.use_config_var.set(bool(job.get('use_cfg')))
        patch = job.get('patch') or {}
        if patch:
            self.v_provider.set(patch.get('provider', self.v_provider.get()))
            self.v_base.set(patch.get('api_base', self.v_base.get()))
            self.v_key.set(patch.get('api_key', self.v_key.get()))
            self.v_model.set(patch.get('model', self.v_model.get()))
            self.v_wake.set(patch.get('wake_words', self.v_wake.get()))
            self.v_title.set(patch.get('user_title', self.v_title.get()))
        self.accepted = True
        self._show(3)
        self.root.after(300, self.do_install)
    def _close(self):
        if self.busy and (not messagebox.askyesno('正在安装', '现在关掉会中断安装，确定吗？', parent=self.root)):
            return
        else:
            self.alive = False
            try:
                self.root.destroy()
            except tk.TclError:
                return None
    def _build(self):
        self.root.geometry('660x600')
        head = tk.Frame(self.root, bg=BG)
        head.pack(fill='x', padx=16, pady=(14, 4))
        tk.Label(head, text=f'{APP_NAME} · {('更新程序' if self.installed else '安装程序')}', bg=BG, fg=FG, font=FONT_B).pack(side='left')
        tk.Label(head, text=f'v{VERSION}', bg=BG, fg=DIM, font=FONT_S).pack(side='left', padx=6)
        tk.Label(head, text='· 双击桌宠聊天 · 右键有全部功能', bg=BG, fg=DIM, font=FONT_S).pack(side='left', padx=10)
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(fill='x', padx=16, pady=(0, 8))
        self.step_labels = []
        for i, name in enumerate(STEPS):
            lb = tk.Label(bar, text=f'{i + 1} {name}', bg=BG, fg=DIM, font=FONT_S, padx=9, pady=3)
            lb.pack(side='left')
            self.step_labels.append(lb)
            if i < len(STEPS) - 1:
                tk.Label(bar, text='›', bg=BG, fg='#b9c6e2', font=FONT_S).pack(side='left')
        self.holder = tk.Frame(self.root, bg=BG)
        self.holder.pack(fill='both', expand=True, padx=16)
        self.pages = [self._page_license(), self._page_env(), self._page_config(), self._page_confirm()]
        foot = tk.Frame(self.root, bg=BG)
        foot.pack(fill='x', padx=16, pady=(8, 14))
        self.hint = tk.Label(foot, text='', bg=BG, fg=DIM, font=FONT_S)
        self.hint.pack(side='left')
        self.btn_next = tk.Button(foot, text='下一步', font=FONT_B, bg=ACCENT, fg='white', activebackground='#6a97e0', relief='flat', padx=24, pady=5, command=self.next, state='disabled')
        self.btn_next.pack(side='right')
        self.btn_back = tk.Button(foot, text='上一步', font=FONT, bg='#dce7fb', fg=FG, activebackground='#cddcf7', relief='flat', padx=16, pady=5, command=self.back, state='disabled')
        self.btn_back.pack(side='right', padx=8)
        tk.Button(foot, text='退出', font=FONT, bg='#dce7fb', fg=FG, relief='flat', padx=14, pady=5, command=self._close).pack(side='right', padx=8)
        self._show(0)
    def _show(self, i):
        for k, page in enumerate(self.pages):
            if k == i:
                page.pack(fill='both', expand=True)
            else:
                page.pack_forget()
        self.step = i
        for k, lb in enumerate(self.step_labels):
            if k == i:
                lb.config(bg=ACCENT, fg='white')
            else:
                if k < i:
                    lb.config(bg=BG, fg=OK_C)
                else:
                    lb.config(bg=BG, fg=DIM)
        last = i == len(STEPS) - 1
        self.btn_back.config(state='normal' if i > 0 and (not self.busy) else 'disabled')
        self.btn_next.config(text='开始安装' if last else '下一步')
        blocked = self.busy or (i == 0 and (not self.accepted))
        self.btn_next.config(state='disabled' if blocked else 'normal')
        if i == 1:
            self._refresh_summary_env()
        if i == 3:
            self._refresh_summary()
    def step_by(self, delta):
        self._show(max(0, min(len(STEPS) - 1, self.step + delta)))
    def back(self):
        if not self.busy:
            self.step_by((-1))
    def next(self):
        if self.busy:
            return
        else:
            if self.step == 0 and (not self.accepted):
                return
            else:
                if self.step == 1 and (not self.path_var.get().strip()):
                    messagebox.showwarning('等一下', '先选一个安装位置吧。', parent=self.root)
                    return
                else:
                    if self.step == len(STEPS) - 1:
                        self.do_install()
                    else:
                        self.step_by(1)
    def _page_license(self):
        page = tk.Frame(self.root, bg=BG)
        tk.Label(page, text='请先读一下下面的许可协议和素材来源说明：', bg=BG, fg=FG, font=FONT).pack(anchor='w')
        wrap = tk.Frame(page, bg=CARD, bd=1, relief='solid')
        wrap.pack(fill='both', expand=True, pady=(6, 8))
        box = tk.Text(wrap, wrap='word', font=MONO, bg='#fbfcff', fg=FG, bd=0, relief='flat', padx=10, pady=8, height=22)
        box.pack(side='left', fill='both', expand=True)
        sb = tk.Scrollbar(wrap, command=box.yview)
        sb.pack(side='right', fill='y')
        box.config(yscrollcommand=sb.set)
        box.insert('1.0', LICENSE_TEXT)
        box.config(state='disabled')
        wheel_scroll(box)
        self.agree = tk.BooleanVar(value=False)
        tk.Checkbutton(page, text='我已阅读并同意上面的 MIT 许可协议（以及素材来源的说明）', variable=self.agree, bg=BG, fg=FG, activebackground=BG, selectcolor=CARD, font=FONT, highlightthickness=0, command=self._agree_changed).pack(anchor='w')
        tk.Label(page, text='不同意的话就没法继续安装啦（贴图素材来自没声明授权的那份项目，请别拿去做生意哦）', bg=BG, fg=DIM, font=FONT_S).pack(anchor='w')
        return page
    def _agree_changed(self):
        self.accepted = bool(self.agree.get())
        if self.step == 0:
            self.btn_next.config(state='normal' if self.accepted else 'disabled')
    CHECKS = [('os', '系统版本', True), ('ps', 'Windows PowerShell', True), ('core', '运行库（打包内置）', True), ('tts', '语音朗读（中文）', False), ('asr', '语音识别（中文）', False), ('mic', '麦克风', False)]
    def _page_env(self):
        page = tk.Frame(self.root, bg=BG)
        box = tk.LabelFrame(page, text=' 环境检测 ', bg=CARD, fg=FG, font=FONT_S, bd=1, relief='solid', labelanchor='nw')
        box.pack(fill='x')
        self.rows = {}
        for key, name, need in self.CHECKS:
            row = tk.Frame(box, bg=CARD)
            row.pack(fill='x', padx=10, pady=1)
            icon = tk.Label(row, text='…', bg=CARD, fg=DIM, font=FONT, width=3, anchor='w')
            icon.pack(side='left')
            tk.Label(row, text=name, bg=CARD, fg=FG, font=FONT, width=20, anchor='w').pack(side='left')
            detail = tk.Label(row, text='检测中…', bg=CARD, fg=DIM, font=FONT_S, anchor='w')
            detail.pack(side='left')
            self.rows[key] = (icon, detail)
        bar = tk.Frame(box, bg=CARD)
        bar.pack(fill='x', padx=10, pady=(6, 8))
        tk.Button(bar, text='重新检测', font=FONT_S, bg='#dce7fb', fg=FG, relief='flat', padx=10, command=self.check_all).pack(side='left')
        self.env_lbl = tk.Label(bar, text='检测中…', bg=CARD, fg=DIM, font=FONT_S)
        self.env_lbl.pack(side='left', padx=10)
        box1 = tk.LabelFrame(page, text=' 安装模式 ', bg=CARD, fg=FG, font=FONT_S, bd=1, relief='solid', labelanchor='nw')
        box1.pack(fill='x', pady=(0, 8))
        mrow = tk.Frame(box1, bg=CARD)
        mrow.pack(fill='x', padx=10, pady=(6, 2))
        self.mode_var = tk.StringVar(value=(self.installed_scope or 'system'))
        tk.Radiobutton(mrow, text='仅当前用户（User）', variable=self.mode_var, value='user', command=self._mode_changed, bg=CARD, fg=FG, activebackground=CARD, selectcolor=CARD, font=FONT_S, highlightthickness=0).pack(side='left', padx=(0, 18))
        tk.Radiobutton(mrow, text='为所有用户安装（System）', variable=self.mode_var, value='system', command=self._mode_changed, bg=CARD, fg=FG, activebackground=CARD, selectcolor=CARD, font=FONT_S, highlightthickness=0).pack(side='left')
        self.mode_note = tk.Label(box1, text='', bg=CARD, fg=DIM, font=FONT_S, anchor='w', justify='left', wraplength=600)
        self.mode_note.pack(fill='x', padx=10, pady=(0, 6))
        box2 = tk.LabelFrame(page, text=' 安装位置 ', bg=CARD, fg=FG, font=FONT_S, bd=1, relief='solid', labelanchor='nw')
        box2.pack(fill='x', pady=8)
        line = tk.Frame(box2, bg=CARD)
        line.pack(fill='x', padx=10, pady=(6, 2))
        default = self.installed or default_dir_for(self.mode_var.get(), self.folders)
        self.path_var = tk.StringVar(value=default)
        tk.Entry(line, textvariable=self.path_var, font=FONT, width=52).pack(side='left')
        tk.Button(line, text='浏览…', font=FONT_S, bg='#dce7fb', fg=FG, relief='flat', padx=8, command=self.pick_dir).pack(side='left', padx=6)
        self.env_note = tk.Label(box2, text='', bg=CARD, fg=OK_C, font=FONT_S, anchor='w', justify='left')
        self.env_note.pack(fill='x', padx=10, pady=(0, 4))
        opts = tk.Frame(box2, bg=CARD)
        opts.pack(fill='x', padx=10, pady=(0, 8))
        self.desktop_var = tk.BooleanVar(value=True)
        self.menu_var = tk.BooleanVar(value=True)
        self.start_var = tk.BooleanVar(value=bool(self.installed))
        for var, text in [(self.desktop_var, '创建桌面快捷方式'), (self.menu_var, '创建开始菜单快捷方式'), (self.start_var, '开机自动启动')]:
            tk.Checkbutton(opts, text=text, variable=var, bg=CARD, fg=FG, font=FONT_S, activebackground=CARD, selectcolor=CARD, highlightthickness=0).pack(side='left', padx=(0, 14))
        self.action_var = tk.StringVar(value='update')
        if self.installed:
            box3 = tk.LabelFrame(page, text=' 检测到已安装 ', bg=CARD, fg=FG, font=FONT_S, bd=1, relief='solid', labelanchor='nw')
            box3.pack(fill='x', pady=(0, 8))
            arow = tk.Frame(box3, bg=CARD)
            arow.pack(fill='x', padx=10, pady=(6, 2))
            for val, txt in [('update', '更新'), ('repair', '修复'), ('reinstall', '重新安装')]:
                tk.Radiobutton(arow, text=txt, variable=self.action_var, value=val, command=self._refresh_summary_env, bg=CARD, fg=FG, activebackground=CARD, selectcolor=CARD, font=FONT_S, highlightthickness=0).pack(side='left', padx=(0, 18))
            self.action_note = tk.Label(box3, text='', bg=CARD, fg=DIM, font=FONT_S, anchor='w', justify='left', wraplength=600)
            self.action_note.pack(fill='x', padx=10, pady=(0, 6))
        else:
            self.action_note = None
        tk.Label(page, text='缺的依赖（语音朗读 / 语音识别）会在你点「开始安装」时一起补上，需要你在弹出的窗口里允许一次管理员权限。', bg=BG, fg=DIM, font=FONT_S, wraplength=600, justify='left').pack(anchor='w')
        return page
    def _mode_changed(self):
        """切换安装模式：如果路径还是某个默认值就跟着换到新默认。"""
        m = self.mode_var.get()
        defaults = {k: default_dir_for(k, self.folders) for k in ('user', 'system')}
        cur = self.path_var.get().strip()
        if (not cur) or (cur in defaults.values()):
            self.path_var.set(defaults[m])
        self._refresh_summary_env()
    def _refresh_summary_env(self):
        if self.mode_var.get() == 'system':
            self.mode_note.config(fg=WARN_C, text='为所有用户安装：装到 Program Files、注册信息写进公共位置；点「开始安装」时会自动弹出一次管理员授权（UAC）。')
        else:
            self.mode_note.config(fg=DIM, text='仅当前用户安装：装到你自己的用户目录，不需要管理员权限，只影响你自己。')
        if self.installed:
            self.env_note.config(fg=OK_C, text=f'检测到本机已经装过：{self.installed}\n主程序换成新的，你的配置、存档、记录都留着。')
            if self.action_note is not None:
                note = {'update': '更新：只把主程序换成新的，配置 / 存档 / 记录原样保留。',
                        'repair': '修复：重装主程序，并重建快捷方式、重新登记卸载信息；缺配置时补一份。配置和数据都保留。',
                        'reinstall': '重新安装：先卸掉旧版本（主程序 / 快捷方式 / 注册表项），再全新安装；「记录 / 存档」这类数据仍会保留。'}.get(self.action_var.get(), '')
                self.action_note.config(fg=DIM, text=note)
        else:
            self.env_note.config(fg=DIM, text='本机还没装过，这次是全新安装。')
    def pick_dir(self):
        d = filedialog.askdirectory(title='选一个安装目录', initialdir=self.path_var.get() or '/')
        if d:
            self.path_var.set(d if os.path.basename(d) == APP_NAME else os.path.join(d, APP_NAME))
    def _page_config(self):
        page = tk.Frame(self.root, bg=BG)
        tk.Label(page, text='填好下面这些，桌宠一装好就能直接跟你聊天（不想填就跳过）', bg=BG, fg=FG, font=FONT).pack(anchor='w')
        box = tk.LabelFrame(page, text=' 在线 AI（可选） ', bg=CARD, fg=FG, font=FONT_S, bd=1, relief='solid', labelanchor='nw')
        box.pack(fill='x', pady=(6, 8))
        grid = tk.Frame(box, bg=CARD)
        grid.pack(fill='x', padx=10, pady=8)
        self.v_provider = tk.StringVar(value='DeepSeek')
        self.v_base = tk.StringVar(value=DEFAULT_BASE)
        self.v_key = tk.StringVar(value='')
        self.v_model = tk.StringVar(value=DEFAULT_MODEL)
        rows = [('服务商', tk.OptionMenu), ('API 地址', tk.Entry), ('API Key', tk.Entry), ('模型', tk.Entry)]
        for i, (name, _) in enumerate(rows):
            tk.Label(grid, text=name, bg=CARD, fg=FG, font=FONT_S, width=8, anchor='e').grid(row=i, column=0, padx=(0, 6), pady=2, sticky='e')
        self.pm = tk.OptionMenu(grid, self.v_provider, *PROVIDER_DEFAULTS.keys(), command=self._provider_changed)
        self.pm.config(font=FONT_S, bg='#dce7fb', fg=FG, relief='flat', highlightthickness=0, width=14)
        self.pm.grid(row=0, column=1, sticky='w', pady=2)
        for i, (var, show) in enumerate(((self.v_base, ''), (self.v_key, '*'), (self.v_model, '')), start=1):
            e = tk.Entry(grid, textvariable=var, font=FONT, width=44, show=show if not show else '•')
            e.grid(row=i, column=1, sticky='w', pady=2)
            if i == 2:
                self.key_entry = e
        tip = tk.Label(grid, text='只存在你自己电脑的 config.json 里，不会传到别的地方', bg=CARD, fg=DIM, font=FONT_S)
        tip.grid(row=4, column=1, sticky='w', pady=(2, 0))
        box2 = tk.LabelFrame(page, text=' 怎么跟它相处 ', bg=CARD, fg=FG, font=FONT_S, bd=1, relief='solid', labelanchor='nw')
        box2.pack(fill='x')
        g2 = tk.Frame(box2, bg=CARD)
        g2.pack(fill='x', padx=10, pady=8)
        self.v_wake = tk.StringVar(value=DEFAULT_WAKE)
        self.v_title = tk.StringVar(value=DEFAULT_TITLE)
        tk.Label(g2, text='唤醒词', bg=CARD, fg=FG, font=FONT_S, width=8, anchor='e').grid(row=0, column=0, padx=(0, 6), pady=2)
        tk.Entry(g2, textvariable=self.v_wake, font=FONT, width=30).grid(row=0, column=1, sticky='w')
        tk.Label(g2, text='喊它一声就能唤醒（多个词用空格隔开）', bg=CARD, fg=DIM, font=FONT_S).grid(row=0, column=2, padx=6, sticky='w')
        tk.Label(g2, text='怎么称呼你', bg=CARD, fg=FG, font=FONT_S, width=8, anchor='e').grid(row=1, column=0, padx=(0, 6), pady=2)
        tk.Entry(g2, textvariable=self.v_title, font=FONT, width=14).grid(row=1, column=1, sticky='w')
        tk.Label(g2, text='它会这么叫你（默认「主人」）', bg=CARD, fg=DIM, font=FONT_S).grid(row=1, column=2, padx=6, sticky='w')
        self.use_config_var = tk.BooleanVar(value=(not self.installed))
        if self.installed:
            tk.Label(page, text='检测到这是「更新」：默认跳过配置，保留你原来的设置（想改就勾上下面这项）。', bg=BG, fg=OK_C, font=FONT_S).pack(anchor='w', pady=(8, 0))
        tk.Checkbutton(page, text='现在就把这些配置写进去（取消勾选＝跳过，之后在桌宠右键「聊天 API 设置…」里再填）', variable=self.use_config_var, bg=BG, fg=FG, activebackground=BG, selectcolor=CARD, font=FONT_S, highlightthickness=0).pack(anchor='w', pady=(8, 0))
        tk.Button(page, text='填回默认值', font=FONT_S, bg='#dce7fb', fg=FG, relief='flat', padx=10, command=self._config_defaults).pack(anchor='w', pady=(6, 0))
        return page
    def _provider_changed(self, name):
        base, model = PROVIDER_DEFAULTS.get(name, (DEFAULT_BASE, DEFAULT_MODEL))
        self.v_base.set(base)
        self.v_model.set(model)
    def _config_defaults(self):
        self.v_provider.set('DeepSeek')
        self.v_base.set(DEFAULT_BASE)
        self.v_model.set(DEFAULT_MODEL)
        self.v_wake.set(DEFAULT_WAKE)
        self.v_title.set(DEFAULT_TITLE)
    def config_patch(self):
        """第三步填的配置（没填也会给出默认值，免得更新后一片空白）。"""
        return {'provider': self.v_provider.get().strip() or 'DeepSeek', 'api_base': self.v_base.get().strip(), 'api_key': self.v_key.get().strip(), 'model': self.v_model.get().strip(), 'wake_words': self.v_wake.get().strip() or DEFAULT_WAKE, 'user_title': self.v_title.get().strip() or DEFAULT_TITLE, 'mode': 'online' if self.v_key.get().strip() else 'local'}
    def _page_confirm(self):
        page = tk.Frame(self.root, bg=BG)
        box = tk.LabelFrame(page, text=' 确认一下 ', bg=CARD, fg=FG, font=FONT_S, bd=1, relief='solid', labelanchor='nw')
        box.pack(fill='x')
        self.summary = tk.Text(box, height=9, wrap='word', font=FONT_S, bg=CARD, fg=FG, bd=0, relief='flat', padx=10, pady=8)
        self.summary.pack(fill='x')
        self.summary.config(state='disabled')
        logbox = tk.LabelFrame(page, text=' 进度 ', bg=CARD, fg=FG, font=FONT_S, bd=1, relief='solid', labelanchor='nw')
        logbox.pack(fill='both', expand=True, pady=8)
        self.log_box = tk.Text(logbox, height=10, wrap='word', font=MONO, bg='#fbfcff', fg=FG, bd=0, relief='flat', padx=8, pady=6)
        self.log_box.pack(side='left', fill='both', expand=True, padx=(8, 0), pady=6)
        sb = tk.Scrollbar(logbox, command=self.log_box.yview)
        sb.pack(side='right', fill='y', pady=6, padx=(0, 6))
        self.log_box.config(state='disabled', yscrollcommand=sb.set)
        wheel_scroll(self.log_box)
        return page
    def _refresh_summary(self):
        deps = [n for k, n, _ in self.CHECKS if k in ['tts', 'asr'] and self.results.get(k, {}).get('ok') is False]
        target = self.path_var.get().strip()
        lines = [f'目标位置：{target}']
        if self.installed:
            act = self.action_var.get()
            lines.append('这次是：' + {'update': '更新主程序', 'repair': '修复安装', 'reinstall': '重新安装（先卸载旧的）'}.get(act, '更新主程序') + '（配置 / 存档 / 记录保留）')
        else:
            lines.append('这次是：全新安装')
        lines.append('安装模式：' + ('为所有用户（System，安装时自动申请管理员权限）' if self.mode_var.get() == 'system' else '仅当前用户（User）'))
        lines.append('要补的依赖：' + ('、'.join(deps) + '　（安装时自动补，会弹一次管理员授权）' if deps else '没有缺的'))
        lnks = []
        if self.desktop_var.get():
            lnks.append('桌面')
        if self.menu_var.get():
            lnks.append('开始菜单')
        lines.append('快捷方式：' + ('、'.join(lnks) if lnks else '不创建'))
        lines.append('开机自动启动：' + ('要' if self.start_var.get() else '不要'))
        if self.use_config_var.get():
            p = self.config_patch()
            lines.append(f'在线 AI：{p['provider']} · {p['api_base']} · 模型 {p['model']} · ' + ('已填密钥' if p['api_key'] else '没填密钥（先用本地模式）'))
            lines.append(f'唤醒词：{p['wake_words']}　称呼你：{p['user_title']}')
        else:
            lines.append('基础配置：跳过（装完在右键「聊天 API 设置…」里填）')
        self.summary.config(state='normal')
        self.summary.delete('1.0', 'end')
        self.summary.insert('1.0', '\n'.join(lines))
        self.summary.config(state='disabled')
    def do_install(self):
        target = self.path_var.get().strip()
        mode = self.mode_var.get()
        src = app_payload()
        if not src:
            messagebox.showerror('安装包不完整', '没找到主程序文件，请重新下载安装包。', parent=self.root)
            return
        if not target:
            messagebox.showwarning('等一下', '先选一个安装位置吧。', parent=self.root)
            return
        ok, why = verify_payload(src)
        if not ok:
            if not messagebox.askyesno('完整性校验没通过', f'{why}\n\n安装包可能损坏或被改动过。仍要继续安装吗？', parent=self.root):
                self.log('已取消：完整性校验没通过。')
                return
            self.log(f'注意：完整性校验没通过（{why}），按主人要求继续安装。')
        else:
            self.log('完整性校验通过：' + (why or 'SHA-256 一致'))
        if mode == 'system' and (not self.admin):
            self._elevate_and_install(target)
            return
        if app_running() and (not messagebox.askyesno('要先关掉旧版本', f'{APP_NAME} 正在运行，更新要先让它退出（不然文件换不了）。\n\n现在替你关掉并继续吗？', parent=self.root)):
            self.log('已取消：请先退出大肥鲸桌宠（托盘图标右键 → 退出应用）再安装。')
            return
        self._refresh_summary()
        self.busy = True
        self.btn_next.config(state='disabled')
        self.btn_back.config(state='disabled')
        self.hint.config(text='安装中，请别关窗口…')
        deps = self.job_deps if self.job_deps is not None else [k for k, _n, _f in self.CHECKS if k in ['tts', 'asr'] and self.results.get(k, {}).get('ok') is False]
        action = self.action_var.get()
        threading.Thread(target=self._install_worker, args=(src, target, deps, self.desktop_var.get(), self.menu_var.get(), self.start_var.get(), self.use_config_var.get(), mode, action), daemon=True).start()
    def _elevate_and_install(self, target):
        """System 模式但当前不是管理员：把这次的选择写进临时文件，自动用管理员权限重启自己来装。"""
        deps = [k for k, _n, _f in self.CHECKS if k in ['tts', 'asr'] and self.results.get(k, {}).get('ok') is False]
        job = {'target': target, 'mode': 'system', 'desktop': bool(self.desktop_var.get()), 'menu': bool(self.menu_var.get()), 'startup': bool(self.start_var.get()), 'use_cfg': bool(self.use_config_var.get()), 'patch': self.config_patch() if self.use_config_var.get() else None, 'installed': bool(self.installed), 'deps': deps, 'action': self.action_var.get()}
        path = os.path.join(tempfile.gettempdir(), 'whale_pet_install_job.json')
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(job, f, ensure_ascii=False)
        except OSError as e:
            messagebox.showerror('出错了', f'写临时文件失败：{e}', parent=self.root)
            return False
        if relaunch_self_elevated(['--job', path]):
            self.alive = False
            try:
                self.root.destroy()
            except Exception:
                pass
            return True
        messagebox.showwarning('需要管理员权限', '为所有用户安装需要管理员权限，但授权被取消了。\n\n可以改用「仅当前用户（User）」，那种不需要管理员。', parent=self.root)
        return False
    def _uninstall_old(self):
        """重新安装前，把旧版本的主程序 / 快捷方式 / 注册表项清掉（「记录 / 存档」等数据保留）。"""
        for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
            try:
                with winreg.OpenKey(hive, REG_UNINST) as k:
                    try:
                        shortcuts = winreg.QueryValueEx(k, 'Shortcuts')[0] or ''
                    except OSError:
                        shortcuts = ''
                    try:
                        loc = winreg.QueryValueEx(k, 'InstallLocation')[0] or ''
                    except OSError:
                        loc = ''
                for p in [x for x in shortcuts.split('|') if x]:
                    try:
                        if os.path.isfile(p):
                            os.remove(p)
                    except OSError:
                        pass
                if loc:
                    exe = os.path.join(loc, APP_EXE)
                    try:
                        if os.path.isfile(exe):
                            os.remove(exe)
                    except OSError:
                        pass
                try:
                    winreg.DeleteKey(hive, REG_UNINST)
                except OSError:
                    pass
                try:
                    with winreg.OpenKey(hive, REG_RUN, 0, winreg.KEY_ALL_ACCESS) as k:
                        winreg.DeleteValue(k, RUN_VALUE)
                except OSError:
                    pass
            except OSError:
                pass
    def _install_worker(self, src, target, deps, desktop, menu, startup, use_cfg, mode, action):
        hive = winreg.HKEY_LOCAL_MACHINE if mode == 'system' else winreg.HKEY_CURRENT_USER
        if mode == 'system':
            desk_dir = common_desktop_dir()
            menu_dir = common_programs_dir()
        else:
            desk_dir = self.folders.get('Desktop') or ''
            menu_dir = self.folders.get('Programs') or ''
        self.log('安装模式：' + ('为所有用户（System）' if mode == 'system' else '仅当前用户（User）'))
        self.log('这次的动作：' + {'update': '更新', 'repair': '修复', 'reinstall': '重新安装'}.get(action, '安装'))
        if deps:
            self._install_deps(deps)
        else:
            self.log('依赖齐全，跳过补依赖。')
        if app_running():
            self.log('先让旧版本退出…')
            kill_app()
        if action == 'reinstall':
            self.log('重新安装：先卸载旧版本（保留记录 / 存档）…')
            self._uninstall_old()
        try:
            os.makedirs(target, exist_ok=True)
        except OSError as e:
            self.log(f'！创建目录失败：{e}')
            self._finish(False)
            return
        dst = os.path.join(target, APP_EXE)
        try:
            shutil.copy2(src, dst)
            self.log(f'主程序已{('更新' if self.installed else '安装')}到：{dst}')
        except OSError as e:
            self.log(f'！复制失败：{e}（如果桌宠还开着，退出后再点一次安装）')
            self._finish(False)
            return
        lnks = []
        if desktop and desk_dir:
            lnks.append((os.path.join(desk_dir, APP_NAME + '.lnk'), dst))
        if menu and menu_dir:
            lnks.append((os.path.join(menu_dir, APP_NAME + '.lnk'), dst))
        if lnks:
            self._make_shortcuts(lnks, target)
            self.log('已建快捷方式：' + '、'.join((os.path.basename(p) for p, _ in lnks)))
        else:
            self.log('没有勾选快捷方式。')
        try:
            if startup:
                with winreg.CreateKey(hive, REG_RUN) as k:
                    winreg.SetValueEx(k, RUN_VALUE, 0, winreg.REG_SZ, f'"{dst}"')
                self.log('已设置开机自动启动')
            else:
                try:
                    with winreg.OpenKey(hive, REG_RUN, 0, winreg.KEY_ALL_ACCESS) as k:
                        winreg.DeleteValue(k, RUN_VALUE)
                except OSError:
                    pass
                self.log('没有设置开机自启。')
        except OSError as e:
            self.log(f'！设置开机自启失败：{e}')
        try:
            with winreg.CreateKey(hive, REG_UNINST) as k:
                winreg.SetValueEx(k, 'DisplayName', 0, winreg.REG_SZ, APP_NAME)
                winreg.SetValueEx(k, 'DisplayVersion', 0, winreg.REG_SZ, VERSION)
                winreg.SetValueEx(k, 'Publisher', 0, winreg.REG_SZ, PUBLISHER)
                winreg.SetValueEx(k, 'InstallLocation', 0, winreg.REG_SZ, target)
                winreg.SetValueEx(k, 'DisplayIcon', 0, winreg.REG_SZ, dst)
                winreg.SetValueEx(k, 'Shortcuts', 0, winreg.REG_SZ, '|'.join((p for p, _ in lnks)))
                winreg.SetValueEx(k, 'UninstallString', 0, winreg.REG_SZ, f'"{dst}" --uninstall')
                winreg.SetValueEx(k, 'NoModify', 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(k, 'NoRepair', 0, winreg.REG_DWORD, 1)
            self.log('已登记卸载信息（设置 → 应用 → 已安装的应用）')
        except OSError as e:
            self.log(f'！写卸载信息失败：{e}')
        cfgp = os.path.join(target, 'config.json')
        if use_cfg:
            self._write_config(cfgp, self.config_patch())
            self.log('配置已写入 config.json（存档、记录、米饭都没动）')
        else:
            if not os.path.isfile(cfgp):
                self._write_config(cfgp, {'mode': 'local'})
                self.log('跳过了配置，先用本地模式（不联网也能玩）')
            else:
                self.log('跳过了配置，保留你原来的设置')
        self._finish(True, dst)
    def _install_deps(self, need):
        names = {'tts': '语音朗读', 'asr': '语音识别'}
        caps = [CAPS['basic']] + [CAPS[k] for k in need if k in CAPS]
        logfile = os.path.join(tempfile.gettempdir(), 'whale_pet_dep.log')
        try:
            os.remove(logfile)
        except OSError:
            pass
        lit = ', '.join(('\'' + c + '\'' for c in caps))
        script = f'\n$ErrorActionPreference = \'Continue\'\n$log = \'{logfile}\'\n"=== 开始装依赖 ===" | Out-File -FilePath $log -Encoding utf8\nforeach ($c in @({lit})) {{\n  "正在安装 $c ……" | Out-File -Append -FilePath $log -Encoding utf8\n  try {{\n    $r = Add-WindowsCapability -Online -Name $c -ErrorAction Stop\n    "  完成：状态=$($r.State)  需要重启=$($r.RestartNeeded)" | Out-File -Append -FilePath $log -Encoding utf8\n  }} catch {{\n    "  失败：$($_.Exception.Message)" | Out-File -Append -FilePath $log -Encoding utf8\n  }}\n}}\n"=== 结束 ===" | Out-File -Append -FilePath $log -Encoding utf8\n'
        self.log('要补：' + '、'.join((names[k] for k in need)) + '（正在申请管理员权限）')
        rc = run_elevated(script)
        if rc == 5:
            self.log('你取消了管理员授权，依赖没装上（不影响安装，语音之后能用设置里的「Windows 功能」再补）。')
            return False
        else:
            if rc <= 32:
                self.log(f'提权失败（{rc}），依赖没装上，继续装桌宠。')
                return False
            else:
                self.log('依赖正在后台安装，请稍候…')
                seen, waited = (0, 0.0)
        while waited < 1500:
            time.sleep(1.0)
            waited += 1.0
            try:
                with open(logfile, 'r', encoding='utf-8', errors='ignore') as f:
                    data = f.read()
            except OSError:
                continue
            if len(data) > seen:
                for line in data[seen:].splitlines():
                    if line.strip():
                        self.log(line.replace('\ufeff', ''))
                seen = len(data)
            if '=== 结束 ===' in data:
                self.log('依赖安装结束。')
                return True
        self.log('等超时了（可能还在装），继续装桌宠。')
        return False
    def _write_config(self, path, patch):
        cfg = {}
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    old = json.load(f)
                if isinstance(old, dict):
                    cfg = old
            except (OSError, ValueError):
                cfg = {}
        cfg.update(patch)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
        except OSError as e:
            self.log(f'！写配置失败：{e}')
    def _make_shortcuts(self, lnks, workdir):
        lines = ['$w = New-Object -ComObject WScript.Shell']
        for lnk, tgt in lnks:
            q = lambda s: str(s).replace('\'', '\'\'')
            lines += [f'$s = $w.CreateShortcut(\'{q(lnk)}\')', f'$s.TargetPath = \'{q(tgt)}\'', f'$s.WorkingDirectory = \'{q(workdir)}\'', f'$s.IconLocation = \'{q(tgt)},0\'', f'$s.Description = \'{APP_NAME}\'', '$s.Save()']
        ps_run('\n'.join(lines), timeout=40)
    def _finish(self, ok, dst=''):
        self.busy = False
        self.logq.put(('done' if ok else 'failed', dst))
    def _load_folders(self):
        for key, fid in _FOLDERID.items():
            self.folders[key] = known_folder(fid)
        if not all(self.folders.values()):
            out = ps_run(_FOLDERS, timeout=25).splitlines()
            for i, key in enumerate(('Desktop', 'Programs', 'LocalApplicationData')):
                if not self.folders.get(key) and i < len(out) and out[i].strip():
                            self.folders[key] = out[i].strip()
        if not self.folders.get('Desktop'):
            self.folders['Desktop'] = os.path.join(os.path.expanduser('~'), 'Desktop')
        if not self.folders.get('LocalApplicationData'):
            self.folders['LocalApplicationData'] = os.path.expanduser('~')
    def check_all(self):
        if self.busy or self.checking:
            return None
        else:
            self.checking = True
            for key, _, _ in self.CHECKS:
                icon, detail = self.rows[key]
                icon.config(text='…', fg=DIM)
                detail.config(text='检测中…', fg=DIM)
            self.env_lbl.config(text='检测中…')
            self.btn_next.config(state='disabled')
            threading.Thread(target=self._check_worker, daemon=True).start()
    def _check_worker(self):
        res = {}
        try:
            v = sys.getwindowsversion()
            name = 'Windows 11' if v.build >= 22000 else f'Windows {v.major}.{v.minor}'
            res['os'] = (v.major >= 10, f'{name}（{v.major}.{v.minor}.{v.build}）', True)
        except Exception as e:
            res['os'] = (False, f'识别不了：{e}', True)
        ok = os.path.isfile(_PS)
        res['ps'] = (ok, '已就绪' if ok else '找不到 Windows PowerShell 5.1', True)
        res['core'] = (True, 'Python / 图像库 / 拖拽库已内置，无需安装', True)
        out = ps_run(_PROBE, timeout=60)
        if 'TTS=' not in out:
            out = ps_run(_PROBE, timeout=60)
        info = {}
        for part in out.split('#'):
            k, _, v = part.partition('=')
            info[k.strip()] = v.strip()
        if 'TTS=' not in out:
            why = '检测失败（不影响安装），可以点「重新检测」再试'
            res['tts'] = (None, why, False)
            res['asr'] = (None, why, False)
            res['mic'] = (None, '未能检测', False)
        else:
            tts = [x for x in info.get('TTS', '').split('|') if x]
            asr = [x for x in info.get('ASR', '').split('|') if x]
            res['tts'] = (bool(tts), '音色：' + '、'.join(tts) if tts else '没找到中文音色' + (f'（{info['TTSERR']}）' if info.get('TTSERR') else ''), True)
            res['asr'] = (bool(asr), '引擎：' + '、'.join(asr) if asr else '没找到中文识别引擎' + (f'（{info['ASRERR']}）' if info.get('ASRERR') else ''), True)
            mic = info.get('MIC') == '1'
            res['mic'] = (mic, '已检测到录音设备' if mic else '没检测到麦克风（只影响语音对话）', False)
        self.logq.put(('checks', res))
    def apply_results(self, res):
        miss = []
        for key, name, need in self.CHECKS:
            ok, detail, fixable = res.get(key, (None, '未检测', False))
            icon, dlab = self.rows[key]
            if ok is True:
                icon.config(text='✓', fg=OK_C)
                dlab.config(text=detail, fg=DIM)
            else:
                if ok is None:
                    icon.config(text='?', fg=WARN_C)
                    dlab.config(text=detail, fg=WARN_C)
                else:
                    if fixable:
                        icon.config(text='✗', fg=BAD_C)
                        dlab.config(text=detail + ' ← 点「开始安装」时会自动补上', fg=BAD_C)
                        miss.append(key)
                    else:
                        icon.config(text='!', fg=WARN_C)
                        dlab.config(text=detail, fg=WARN_C)
        self.checking = False
        names = dict(((k, n) for k, n, _ in self.CHECKS))
        self.env_lbl.config(text='缺：' + '、'.join((names[k] for k in miss)) + '（安装时自动补）' if miss else '依赖齐全，可以直接安装')
        if not miss:
            self.env_lbl.config(fg=OK_C)
        else:
            self.env_lbl.config(fg=WARN_C)
        self.log('环境检测完成：' + ('缺 ' + '、'.join((names[k] for k in miss)) if miss else '没有缺东西'))
        if not self.busy and self.step != 0:
                self.btn_next.config(state='normal')
        if self.step == 1 or self.step == 3:
            self._refresh_summary_env()
            self._refresh_summary()
    def log(self, text):
        self.logq.put(('line', text))
    def _drain(self):
        if not self.alive:
            return
        try:
            while True:
                item = self.logq.get_nowait()
                kind = item[0]
                if kind == 'line':
                    self.log_box.config(state='normal')
                    self.log_box.insert('end', f'[{time.strftime("%H:%M:%S")}] {item[1]}\n')
                    self.log_box.see('end')
                    self.log_box.config(state='disabled')
                elif kind == 'checks':
                    self.results = {k: {'ok': v[0], 'detail': v[1], 'fix': v[2]} for k, v in item[1].items()}
                    self.apply_results(item[1])
                elif kind == 'done':
                    dst = item[1]
                    self.hint.config(text='装好啦～')
                    self.btn_next.config(state='normal', text='完成')
                    self.btn_back.config(state='disabled')
                    self.btn_next.config(command=self._close)
                    if messagebox.askyesno('更新完成' if self.installed else '安装完成', f'{APP_NAME} 已经{("更新" if self.installed else "装")}好啦～\n\n现在启动吗？', parent=self.root):
                        try:
                            subprocess.Popen([dst], cwd=os.path.dirname(dst))
                        except Exception as e:
                            self.log(f'启动失败：{e}')
                    self._close()
                elif kind == 'failed':
                    self.hint.config(text='出了点问题，看上面的进度')
                    self.btn_next.config(state='normal')
                    self.btn_back.config(state='normal')
                    self.busy = False
        except queue.Empty:
            pass
        except tk.TclError:
            return None
        if self.alive:
            self.root.after(120, self._drain)
    def run(self):
        self.root.mainloop()
if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--hash' in argv:
        p = app_payload()
        if not p:
            print('找不到主程序文件。')
        else:
            print(os.path.basename(p))
            print(f'size   {os.path.getsize(p)}')
            print(f'sha256 {file_sha256(p)}')
        sys.exit(0)
    if not os.path.isfile(_PS):
        print('找不到 Windows PowerShell，无法继续。')
        sys.exit(1)
    job = None
    if '--job' in argv:
        try:
            with open(argv[argv.index('--job') + 1], 'r', encoding='utf-8') as f:
                job = json.load(f)
        except Exception:
            job = None
    Wizard(job).run()
