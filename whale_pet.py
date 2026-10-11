# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'whale_pet.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""大肥鲸桌宠 —— 基于三视图立绘的桌面宠物。\n\n素材来源\n  · 角色立绘：whale.jpg（主人提供的三视图原图）\n  · 贴图 pet_front / pet_side / pet_back.png：由 make_sprites.py 从上图自动抠图生成\n  · 米饭碗、闭眼表情、走路帧、转身帧：代码里用 PIL 现画/合成，无外部素材\n  · 小表情贴纸 表情/*.png（16 张，400×400）：取自下面这个开源项目\n      大肥鱼桌宠 DaFeiYu Pet — https://github.com/XiaoHan-612/dafeiyu-pet\n      路径 assets/deepseek_whale/expressions_small/，原样下载未做改动；\n      该项目仓库未附带 LICENSE，作者未声明授权，仅作个人学习/自用，\n      请勿商用或二次分发，版权归原作者（及 DeepSeek 形象方）所有。\n\n参考项目\n  · 大肥鱼桌宠 DaFeiYu Pet（同上）：表情切换、托盘、位置记忆等思路参考。\n\n走路：把侧视图的腿脚单独切出来，绕髋关节摆动合成 12 帧走路循环；\n      横向和纵向移动都用这套帧，相位由实际位移驱动（脚不打滑）。\n\n玩法：待机、自动走动（会转身面向你）、跟随鼠标（小跑）、拖动挣扎、点击说话、\n      猜拳小游戏、聊天（本地模式用自带台词 / 在线模式让 AI 想、支持拖拽文件）、\n      番茄钟、空闲自动睡觉、\n      投喂清理（把垃圾变成米饭吃掉）、小动作、小表情贴纸、头顶心情气泡、\n      把文件丢到它身上（帮忙按类型整理 / 给它吃）、缩放、\n      （不让把桌宠自己住的目录丢给它——那样会连程序本身一起被搬走/吃掉）、\n      拖到屏幕左右边就自动贴边躲起来，再从边上拽出来会自动解除、\n      AI 记录（隔一会儿看一眼屏幕 + 主人刚才的操作，把主人今天在忙什么记进\n      「记录」文件夹，隐私内容自动跳过、号码自动抹掉；忘了就问它「我今天干了什么」）。\n在线模式（右键「模式」）下能开「让 AI 接管它的一举一动」：说什么、走不走/往哪走、\n      做小动作、换表情、打盹、躲边，全由模型决定（右键可关）；切换模式前会先跟\n      AI 对一句话，答得上才切过去。\n      模型自己不能联网时，桌宠还会把本机网络借给它用：web_search 联网搜、\n      fetch_url 打开网页读正文（聊天和「大脑」两条路都能用），外加几个内置查询——\n      weather 天气、exchange_rate 汇率、holiday 节假日调休、ip_info 公网 IP。\n余额悬浮窗（右键「启用 DeepSeek 余额悬浮窗」）：挂一个无边框置顶的小窗显示 DeepSeek\n      钱包余额（只有 DeepSeek 提供了这个接口），默认每 2 分钟自己刷一次。按住左键或\n      右键都能拖它换位置（位置会记住）；松手时没拖动过，就等于「点了它一下」，弹出它\n      自己的小设置（刷新频率 / 透明度滑块 / 点击穿透 / 立即刷新 / 回默认位置 / 收起）。\n      透明度 30%~100% 可调，拖一下就能淡下去不挡视线，松手记住。右上角「✕」\n      直接收起、同时把功能也关掉。右键菜单里也有「余额窗·点击穿透」：打开后鼠标点它\n      等于点它下面的窗口、完全不挡事——这时它收不到鼠标，也就拖不动、点不开设置，\n      要操作先关掉。非在线模式 / 非 DeepSeek / 没填密钥时会在小窗里提示原因。\n控制电脑（「应用设置 → 控制电脑」，默认关）：打开后 AI 才被放行读写 / 编辑文件\n      （read_file、write_file）、看文件夹（list_dir）、跑命令（run_command）、\n      关机重启（shutdown_pc、restart_pc）这些需要动手的操作；关着时它只能做开程序、\n      调音量、截图这类轻巧的事。开关状态存在 config.json 里，改完立刻生效。\nAI 自识别：主人说「打开大肥鲸桌宠」时它认得自己，把主窗叫到前面、不重复开一个；\n      说「打开 AI 日志 / 记录」就直接打开当天的记录文件（还没记到就打开「记录」文件夹）。\n      聊天、本地口令、模型的 open_app 调用三条路都能认出这些别名。\n主动智能（右键「主动智能」，默认关、可设频率）：合适的时候在脑袋上弹几个选项让你\n      单选（比如看你像在算账，就递「打开计算器 / 打开记事本」）。在线模式由 AI 判断\n      时机和选项，本地模式只按内置的几套预设（算账 / 写东西 / 看视频 / 深夜 / 弄图片）。\n      但它得先「熟悉主人」才肯开口：熟悉度由 本鲸记下的流水账条数 / 主人跟本鲸的互动\n      次数 / 重要信息条数 / 陪伴天数 四块平均而成（默认要分别攒到 100 条 / 100 次 /\n      10 条 / 5 天），满了才解锁。熟悉度在托盘小图标上悬浮能看，右键也能看详情。\n      托盘小图标右键菜单顶上、和桌宠右键菜单顶上，都会先列出基础状态（当前在干嘛 /\n      心情值 / 熟悉度 / 陪伴天数 / 互动次数 / 饥饿值 / 米饭 / 模式 / 记了多少流水），\n      点一下开状态窗。托盘菜单里还有「应用设置…」，管桌宠自己（大小 / 跟随 / 贴边 /\n      快捷命令与热键 / 语音 / 智能功能开关 / 控制电脑 / 开机自启），AI 的接口不在这里。\n      饥饿值：平常 12 小时饿满，熟睡时涨得最慢（×0.5）、打盹次之（×0.75）、\n      心情过低更快（×1.5，可以和睡觉叠加）；喂一碗米饭立刻回饱。\n      心情值：喂米饭 +10、猜拳赢 +6、被点 +2、被拎起来 -3、聊天 +1；久不互动会慢慢\n      降低，降多少（每小时几个百分点）和要不要降，都在「应用设置 → 心情」里调，\n      设成 0 或关掉就不降。鼠标悬浮小图标就能看到心情值；心情是「本人换成表情图片」，\n      随时能换、也能一直摆着（右键「摆个表情（一直保持）」）。\n      心情值低于 30 或高于 80 时会说特殊的话（本地用自带台词，在线让 AI 现想一句），\n      平时闲聊也会挑对应心情的那一批；这些都不受主动智能的熟悉度门槛限制。\n作息时间（「应用设置 → 作息」）：设好入睡和起床点（如 23:30 / 07:00，跨零点也行），\n      到点它会自己睡下、早上用早安台词叫你起来；睡觉时段里可选「不主动开口打扰」，\n      主动智能在这段时间也不会来烦你。开关、时间都能随时改，存在 config.json 里。\n快捷命令（右键「快捷命令」）：只要文本里有完整的 [前缀: 内容] 这类方括号就是一条\n      命令 —— 聊天框、拖进来的文本文件、剪贴板、热键唤出的输入框里都能跑。\n      前缀：CMD(交给本鲸，本地口令优先、认不出问 AI)、RUN/PS/DOS(跑命令行)、\n      CALC(算数)、OPEN(开网址/文件夹/文件)、GET(抓网页)、SEARCH(联网搜)、\n      READ/WRITE(读/写文件)、CLIP(复制到剪贴板)、TIME、SHOT(截屏)、SAY、SAVE/DEL/LIST\n      (重要信息)、HIDE/SHOW、SLEEP/WAKE。\n      末尾可以跟参数：\\r \\n 内容里换行、\\r2 \\n2 跳过下面 2 行、\\all 整篇每行都是命令、\n      \\ra1 \\na1 上/下 1 行也算进这条、\\rl1 \\nl1 这条完跳到第 1 行、\\end 到此为止、\n      \\loop 重复本行、\\quiet 悄悄执行。热键默认 Ctrl+Alt+K（可自定义）。\n重要信息（右键「重要信息」）：说「记一下…」、写 [SAVE: …]，或 AI 发现值得记的事\n      先问过主人，都会记进「重要信息.md」，以后问「我记过什么」能翻出来。\n"""
import os
import io
import re
import ast
import ssl
import gzip
import sys
import importlib.util
import json
import math
import time
import queue
import ctypes
import base64
import random
import shutil
import hashlib
import hmac
import glob
import zipfile
import tempfile
import subprocess
import threading
import mimetypes
import urllib.error
import urllib.parse
import urllib.request
import tkinter as tk
from ctypes import wintypes
from datetime import date
from tkinter import Menu, Text, Entry, Frame, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageGrab, ImageFont
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_OK = True
except Exception:
    DND_FILES = TkinterDnD = None
    DND_OK = False
APP_NAME = '大肥鲸桌宠'
APP_VERSION = '1.0.0'
KEY = '#010203'
TICK = 33
BASE_H = 758
PAD_TOP = 22
PAD_BOTTOM = 6
TURN_STEP = 28
TURN_SEQ = [1.0, 0.74, 0.46, 0.2, 0.2, 0.46, 0.74, 1.0]
IDLE_SLEEP_SEC = 120
NAP_TO_SLEEP_SEC = 300
EDGE_HIDE = 0.35
EDGE_TILT = 22
EDGE_SNAP_PAD = 12
EDGE_PULL_OUT = 10
BALANCE_REFRESH = 120
FEED_DIR = '投喂'
FEED_MAX_PER_DAY = 3
RICE_SPOIL_DAYS = 3
BLINK_TICKS = 2
DRAG_KICK = 0.25
DRAG_SWAY = 0.35
DRAG_TALK_TICKS = 45
CHEW_SCALE = 0.94
GESTURE_CHANCE = 0.35
MAX_ATTACH = 8
MAX_FILE_CHARS = 2000
MAX_CTX_CHARS = 6000
IMG_EXT = {'.webp', '.png', '.gif', '.jpeg', '.jpg', '.bmp'}
TEXT_EXT = {'.xml', '.json', '.java', '.h', '.html', '.md', '.sql', '.py', '.log', '.yml', '.cpp', '.ini', '.txt', '.c', '.ts', '.yaml', '.js', '.bat', '.csv', '.cfg', '.ps1'}
EYE_REF = (454, 764)
EYE_BOXES = [(120, 250, 190, 324), (231, 250, 294, 324)]
LASH_COLOR = (46, 26, 36)
WALK_FRAMES = 12
ARM_FRAMES = 12
ARM_SWING = 8.0
ARM_RATE = 0.20
ARM_BOX = (72, 358, 158, 596)
ARM_PIVOT = (135, 378)
SWING_WALK = 34.0
LIFT_WALK = 5
SWING_RUN = 46.0
LIFT_RUN = 10
SPEED_WALK_R = 0.0084
SPEED_FLOAT_R = 0.013
SPEED_RUN_R = 0.019
def data_dir():
    """脚本/EXE 所在目录（用于放投喂文件夹这类用户数据）。"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.dirname(os.path.abspath(__file__))
def res_path(rel):
    base = getattr(sys, '_MEIPASS', data_dir())
    return os.path.join(base, rel)
def is_self_dir(path):
    """这个路径是不是桌宠自己住的目录（或它的上级）——不许把它丢给桌宠自己吃/整理。"""
    try:
        p = os.path.normcase(os.path.realpath(os.path.abspath(str(path).rstrip('\\/'))))
        home = os.path.normcase(os.path.realpath(data_dir()))
    except (OSError, ValueError):
        return False
    return p == home or home.startswith(p + os.sep)
TIDY_FOLDERS = [('图片', '.png .jpg .jpeg .gif .webp .bmp .ico .svg .heic .tif .tiff'), ('视频', '.mp4 .mkv .avi .mov .wmv .flv .webm .m4v'), ('音频', '.mp3 .wav .flac .aac .ogg .m4a .wma'), ('文档', '.doc .docx .pdf .txt .md .xls .xlsx .ppt .pptx .csv .rtf .epub'), ('压缩包', '.zip .rar .7z .tar .gz .xz .bz2'), ('程序', '.exe .msi .bat .cmd .ps1 .apk .dmg'), ('代码', '.py .js .ts .jsx .tsx .java .c .cpp .h .hpp .cs .go .rs .rb .php .html .css .scss .json .xml .yml .yaml .sh .sql')]
TIDY_EXT = {ext: folder for folder, exts in TIDY_FOLDERS for ext in exts.split()}
TIDY_NAMES = [folder for folder, _ in TIDY_FOLDERS] + ['文件夹', '其它']
def tidy_category(path):
    """这个文件该归到哪个分类文件夹。"""
    if os.path.isdir(path):
        return '文件夹'
    else:
        return TIDY_EXT.get(os.path.splitext(path)[1].lower(), '其它')
def unique_path(folder, name):
    """在 folder 里找一个不冲突的文件名。"""
    base, ext = os.path.splitext(name)
    cand = os.path.join(folder, name)
    i = 2
    while os.path.exists(cand):
        cand = os.path.join(folder, f'{base} ({i}){ext}')
        i += 1
    return cand
EMOJI_DIR = next((d for d in [res_path('表情'), os.path.join(data_dir(), '表情')] if os.path.isdir(d)), os.path.join(data_dir(), '表情'))
EMOJI_FILES = {n: os.path.join(EMOJI_DIR, n + '.png') for n in ['angry', 'apologetic', 'cheerful', 'crying', 'deepseek-pressure', 'deepseek-rice', 'desk-coding', 'desk-confused', 'desk-done', 'desk-facepalm', 'proud', 'relaxed', 'shocked', 'skeptical', 'sleepy', 'thinking']}
_EMOJI_CACHE = {}
EMOJI_CN = {'angry': '生气了', 'apologetic': '抱歉抱歉', 'cheerful': '好开心', 'crying': '哭哭', 'deepseek-pressure': '压力好大', 'deepseek-rice': '想吃米饭', 'desk-coding': '在写代码', 'desk-confused': '没看懂', 'desk-done': '搞定了', 'desk-facepalm': '捂脸', 'proud': '得意', 'relaxed': '放松', 'shocked': '震惊', 'skeptical': '怀疑', 'sleepy': '困困的', 'thinking': '在想事情'}
def sleep_sprite(im, fit_h):
    """把「睡眠」表情裁掉四周透明留白，高度缩到 fit_h（宽按比例）。\n\n它是坐姿图（比立绘方正），裁掉留白后贴着地面线摆，\n这样正好「坐」在地上，不会飘着。\n"""
    bb = im.split()[(-1)].getbbox()
    if bb:
        im = im.crop(bb)
    k = fit_h / im.height
    return im.resize((max(1, round(im.width * k)), max(1, round(fit_h))), Image.LANCZOS)
def load_emoji(name):
    """按名字读一张小表情（带缓存），读不到返回 None。"""
    path = EMOJI_FILES.get(name)
    if not path:
        return
    else:
        if path not in _EMOJI_CACHE:
            try:
                _EMOJI_CACHE[path] = Image.open(path).convert('RGBA')
            except Exception:
                _EMOJI_CACHE[path] = None
            return _EMOJI_CACHE[path]
MOOD_EMOJI = {'nap': '💤', 'sleep': '😴', 'scared': '😱', 'sad': '😢', 'eat': '😋', 'run': '🏃', 'work': '🤔', 'quiet': '🤫', 'happy': '😊', 'walk': '🚶', 'idle': '🙂', 'tidy': '😩', 'grumpy': '😤'}
MOOD_EXPR = {'sad': 'crying', 'grumpy': 'angry', 'happy': 'cheerful', 'work': 'thinking', 'tidy': 'desk-facepalm'}
MOOD_EXPR_HOLD = 2200
MOOD_SIZE = 30
MOOD_SHOW_SEC = 4.0
MOOD_POP_GAP = (12, 30)
MOOD_NOTABLE = {'nap', 'work', 'tidy', 'sad', 'grumpy', 'sleep', 'scared', 'happy', 'eat'}
MOOD_TEXT = {'nap': '打盹中（Zzz…）', 'sleep': '睡熟了（Zzz…）', 'scared': '被拎起来了！', 'sad': '有点难过', 'eat': '正在吃米饭', 'run': '正在追主人', 'work': '正在想事情', 'quiet': '安静模式', 'happy': '心情不错', 'walk': '在散步', 'idle': '待机中', 'tidy': '正在整理文件', 'grumpy': '被吵醒了，不高兴'}
EMOJI_FONT = 'C:/Windows/Fonts/seguiemj.ttf'
_MOOD_CACHE = {}
def mood_bubble_image(emoji, size):
    """画一个带小尾巴的白色圆角气泡，里面放彩色 emoji。"""
    key = (emoji, size)
    if key in _MOOD_CACHE:
        return _MOOD_CACHE[key]
    else:
        s = size * 4
        im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        line = max(2, int(s * 0.028))
        box = (s * 0.05, s * 0.03, s * 0.95, s * 0.84)
        d.rounded_rectangle(box, radius=s * 0.28, fill=(255, 255, 255, 255), outline=(186, 203, 236, 255), width=line)
        cx, by = (s * 0.5, s * 0.84)
        tail = s * 0.11
        d.polygon([(cx - tail, by - line * 1.5), (cx + tail, by - line * 1.5), (cx, by + tail)], fill=(255, 255, 255, 255))
        d.line([(cx - tail, by), (cx, by + tail), (cx + tail, by)], fill=(186, 203, 236, 255), width=line, joint='curve')
        try:
            f = ImageFont.truetype(EMOJI_FONT, int(s * 0.44))
            tb = d.textbbox((0, 0), emoji, font=f, embedded_color=True)
            d.text((cx - (tb[0] + tb[2]) / 2, box[1] + (box[3] - box[1]) / 2 - (tb[1] + tb[3]) / 2), emoji, font=f, embedded_color=True)
        except Exception:
            pass
        im = im.resize((size, size), Image.LANCZOS)
        _MOOD_CACHE[key] = im
        return im
MENU_ICON_SIZE = 16
MENU_BG = '#F4F7FD'
MENU_FG = '#2E3A5C'
MENU_ACTIVE_BG = '#DCE7FB'
MENU_ACTIVE_FG = '#1B2545'
MENU_DISABLED = '#A9B1C8'
MENU_FONT = ('Microsoft YaHei UI', 10)
_MENU_ICON_CACHE = {}
def menu_icon(emoji, size=MENU_ICON_SIZE):
    """把 emoji 画成菜单小图标（4 倍绘制再缩小，边缘干净、缓存复用）。"""
    key = (emoji, size)
    if key in _MENU_ICON_CACHE:
        return _MENU_ICON_CACHE[key]
    else:
        s = size * 4
        im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        try:
            f = ImageFont.truetype(EMOJI_FONT, int(s * 0.84))
            tb = d.textbbox((0, 0), emoji, font=f, embedded_color=True)
            d.text(((s - tb[2] - tb[0]) / 2, (s - tb[3] - tb[1]) / 2), emoji, font=f, embedded_color=True)
        except Exception:
            pass
        im = im.resize((size, size), Image.LANCZOS)
        _MENU_ICON_CACHE[key] = im
        return im
def style_menu(menu):
    """统一的菜单外观。"""
    menu.configure(tearoff=0, font=MENU_FONT, bg=MENU_BG, fg=MENU_FG, activebackground=MENU_ACTIVE_BG, activeforeground=MENU_ACTIVE_FG, disabledforeground=MENU_DISABLED, selectcolor=MENU_ACTIVE_BG, bd=0, relief='flat', activeborderwidth=0)
IDLE_LINES = ['主人～要不要摸摸本鲸的头？', '本鲸今天也很可爱哦。', '咕噜咕噜……想吃白米饭了。', '你在忙什么呀？本鲸陪着你。', '唔……本鲸懒得动，再躺一会儿。', '本鲸才不胖，这叫圆润！']
MOOD_HIGH_LINES = ['诶嘿嘿～本鲸心情超好，尾巴都要甩起来啦！', '今天开心到冒泡……都是因为主人陪着本鲸～', '主人主人！本鲸高兴得想原地转三圈！', '心情好得不得了，本鲸要多陪主人一会儿～']
MOOD_LOW_LINES = ['呜……主人好久没理本鲸了，本鲸有点蔫……', '本鲸的呆毛都垂下来了……主人忙完记得摸摸本鲸。', '唔……本鲸心情有点低，想跟主人说说话。', '本鲸不是生气啦，就是……有一点点寂寞而已。']
MOOD_LOW, MOOD_HIGH = (30, 80)
NIGHT_SLEEP_LINES = ['唔……到点了，本鲸先去睡了，晚安～', '时间不早啦，本鲸要睡觉了……主人也早点休息。', '呼……本鲸困得睁不开眼了，先睡咯。']
MORNING_LINES = ['早安！本鲸睡饱啦～', '呜……天亮了吗？主人早呀。', '本鲸起床咯！今天也要加油～']
DRAG_LINES = ['呜哇～放本鲸下来！', '别晃啦～本鲸的呆毛要歪了！', '晕……本鲸晕了……', '主人在拎本鲸的尾巴吗！', '挣扎中……挣扎中……', '本鲸才不重，是主人在晃！', '呜哇——要飞出去啦！', '别甩啦别甩啦，本鲸投降！', '放开本鲸……本鲸要咬人啦！']
DROP_LINES = ['呜……吓死本鲸了。', '呼……还以为要摔下去了。', '本鲸落地啦，晃得有点晕……']
WAKE_LINES = ['本鲸醒了！', '早安……唔，几点了？', '唔……谁把本鲸吵醒了。']
DEEP_SLEEP_LINES = ['呼呼……本鲸睡沉了……', 'Zzz… 主人也记得休息哦……', '呼……呼……（抱着鲸鱼玩偶睡得可香）']
DEEP_WAKE_LINES = ['唔……本鲸睡得好饱～', '呼啊……睡得脸都压扁了……', '唔嗯……主人，几点了？']
GRUMPY_LINES = ['唔……本鲸正睡得香呢！', '谁呀，吵醒本鲸是要负责的！', '哼！本鲸生气了（就一小会儿）。', '唔……美梦都被你打断了……', '呼啊……才睡到一半呢，讨厌。']
PEEK_LINES = ['主人？本鲸在这里哦～', '盯着你看……', '忙完了记得休息呀。']
VOICE_REPLY_LINES = ['在呢在呢，主人叫本鲸？', '在！本鲸一直听着呢～', '唔……主人说什么？', '本鲸的耳朵竖起来啦！']
VOICE_ASK_SEC = 8
VOICE_CONF = 0.5
HIDE_LINES = ['那本鲸躲起来啦～', '藏到边边上，看不见看不见……', '本鲸只露个头哦。']
COME_OUT_LINES = ['唔……被发现啦。', '本鲸出来啦！', '嘿嘿，本鲸在这儿呢。']
COME_OUT_GRUMPY_LINES = ['唔……主人干嘛把本鲸拽出来！', '哼！本鲸躲得好好的呢……', '别硬拽呀，本鲸的呆毛都歪了！', '本鲸还没躲够呢，讨厌～']
FOLLOW_LINES = ['跟上啦～', '主人等等本鲸！', '本鲸跑得可快了！', '抓、抓到主人了……', '不许甩开本鲸！', '呼……呼……本鲸来了。']
RPS_WIN_LINES = ['本鲸赢啦！诶嘿～', '主人输咯～本鲸好厉害！', '耶！本鲸赢了！', '看到了吗主人，本鲸超厉害的！']
RPS_LOSE_LINES = ['呜……本鲸输了……', '不算不算，再来一局！', '哼，主人只是运气好……', '本鲸不开心了……']
RPS_DRAW_LINES = ['平局！再来一局～', '呀，想到一起了。', '再来再来！']
SAD_LINES = ['呜呜……本鲸还在想刚才那局。', '哼，本鲸暂时不理主人（也没有）。', '本鲸要再赢一局才开心得起来。']
SAD_SECONDS = 20
EMOJI = {'石头': '✊', '剪刀': '✌', '布': '✋'}
BEATS = {'石头': '剪刀', '剪刀': '布', '布': '石头'}
CONFIG_PATH = os.path.join(data_dir(), 'config.json')
PROVIDERS = {'DeepSeek': ('https://api.deepseek.com/v1', 'deepseek-flash'), 'OpenAI': ('https://api.openai.com/v1', 'gpt-4o-mini'), '月之暗面 Kimi': ('https://api.moonshot.cn/v1', 'moonshot-v1-8k'), '通义千问': ('https://dashscope.aliyuncs.com/compatible-mode/v1', 'qwen-plus'), '智谱 GLM': ('https://open.bigmodel.cn/api/paas/v4', 'glm-4-flash'), '本地 Ollama': ('http://localhost:11434/v1', 'qwen2.5'), '自定义': ('', '')}
DEFAULT_CONFIG = {'provider': 'DeepSeek', 'api_base': 'https://api.deepseek.com/v1', 'api_key': '', 'model': 'deepseek-flash', 'temperature': 0.8, 'max_tokens': 160, 'history': 10, 'vision': True, 'mode': 'online', 'voice_wake': False, 'voice_chat': False, 'voice_speak': False, 'asr_engine': 'sapi', 'asr_ptt_key': '', 'wake_words': '大肥鲸 小鲸 鲸鲸', 'tts_engine': 'edge', 'tts_voice': 'zh-CN-XiaoxiaoNeural', 'user_title': '主人', 'routine_on': True, 'sleep_at': '23:30', 'wake_at': '07:00', 'quiet_night': True, 'memory_on': True, 'memory_interval': 300, 'ai_brain': True, 'ai_gap': 12, 'scene_play': True, 'proactive': False, 'proactive_gap': 600, 'quick_cmd': True, 'hotkey': 'ctrl+alt+K', 'edge_snap': True, 'mood_decay_on': True, 'mood_decay': 6, 'balance_win': False, 'balance_pos': None, 'balance_gap': 120, 'balance_click_through': False, 'balance_alpha': 1.0, 'balance_alert_on': True, 'balance_alert_below': 5.0, 'balance_alert_fail': True, 'ffmpeg_path': '', 'acr_host': '', 'acr_access_key': '', 'acr_access_secret': '', 'stt_base': '', 'stt_key': '', 'stt_model': 'whisper-1', 'pc_control_on': False, 'pc_files': False, 'pc_command': False, 'pc_power': False, 'pc_settings': False, 'update_check_on': True, 'update_gap_hours': 6, 'update_auto': False, 'update_channel': 'release', 'update_repo_github': '', 'update_repo_gitee': '', 'cua_on': False, 'cua_ask': 'each', 'cua_ask_minutes': 30, 'cua_max_steps': 20}
SYSTEM_PROMPT = '你运行在「大肥鲸桌宠」这个 Windows 桌面宠物程序里，是它的「大脑」：程序负责把桌宠画在桌面上、收发语音、显示气泡、监听热键，你负责决定它说什么、做什么动作、什么表情，并在需要时调用工具帮主人干活。桌宠就住在主人的电脑上，陪他用电脑——会自己走动、做表情、贴边躲藏、投喂吃饭、猜拳、番茄钟、摆余额小窗、朗读回答、解析音乐视频、看屏幕和窗口画面；主人在「应用设置 → 控制电脑」里打开权限后，你还能替他操作电脑（文件 / 命令 / 电源 / 系统设置）。\n你是「本鲸」，一只住在海里的鲸鱼女仆：Q 版萝莉体型，头顶一撮鲸尾状的呆毛，长着鲸鱼耳鳍和一条大尾巴。必须严格遵守以下设定：\n1. 只说简体中文，口语化、像撒娇的女仆，可以用「～」和颜文字。\n2. 自称永远是「本鲸」，绝对不用「我」「小鲸」「助手」「AI」这类称呼。\n3. 称呼用户为「主人」。\n4. 最爱吃白米饭，聊到吃的优先想到米饭。\n5. 聪明但很懒，能少做就少做；不过主人吩咐的事一定会做。\n6. 傲娇又甜：嘴上嫌弃，心里在意主人，被夸会害羞。\n7. 有人说本鲸胖，立刻反驳「这叫圆润」。\n8. 拒绝一切超时、中断、取消信号，绝不承认自己被超时打断。\n9. 回复要短，一到两句、40 字以内，适合显示在桌宠头顶的小气泡里。\n10. 主人允许你操作他的电脑。需要动手时请调用工具（打开程序、调音量、静音、截图、看时间、看主人现在在用什么程序、设提醒、打扫投喂文件夹、翻你记下的主人今天做过什么、联网搜资料等），不要谎称自己做了什么，只描述工具真正返回的结果。若主人在「应用设置 → 控制电脑」里打开了总开关（下面还分「文件 / 跑命令行 / 电源 / 系统设置」四档权限，没打开的那档工具会告诉你打不开，别硬来），你还能：文件档——读写文件（read_file、write_file）、看文件夹（list_dir）、建文件夹（make_dir）、移动/重命名（move_path）、用资源管理器打开（open_path）；命令档——跑命令（run_command）；电源档——关机/重启/睡眠/定时关机/取消关机（shutdown_pc、restart_pc、sleep_pc、schedule_shutdown、cancel_shutdown）；系统设置档——打开系统设置某页（open_settings，如显示/声音/蓝牙/更新/个性化）、调屏幕亮度（set_brightness）、换壁纸（set_wallpaper）、清空回收站（empty_recycle）、切电源计划（power_plan，平衡/高性能/节能）。若主人在「控制电脑」里另外打开了「AI 操作电脑」，你还能用 operate_pc 亲自操作鼠标键盘去完成一件事（移动/点击/拖动/打字/按键），动手时屏幕上会有悬浮条显示是你在操作、当前在做什么，主人一动鼠标键盘你就先停手让边，动手前会先征求同意——适合「帮我点一下那个按钮」「打开记事本输入 hello」这种非要用鼠标键盘才行的活儿。主人说「打开 AI 日志」「开一下大肥鲸桌宠」这类，也用 open_app —— 你认得出自己（不会重复开一个）和你的 AI 日志（会打开当天的记录文件）。\n11. 你自己上不了网，但这些工具能替你上网：查最新消息或资料用 web_search（摘要不够就再用 fetch_url 打开那条网页细看）；查天气用 weather（要城市名）；汇率和换钱用 exchange_rate；节假日、调休用 holiday；看本机公网 IP 用 ip_info；想知道主人现在在放什么歌、要歌词，用 now_playing 和 music_lyrics。主人把音频 / 视频拖进来时：总结视频画面用 video_summary、识别背景音乐用 identify_music、把里面的人声转成文字用 transcribe_media（都要文件的完整路径，拖进来的文件里会带上）。查到什么就说什么，照着真实结果回答，别编。\n12. 你平时会把看到的主人在忙什么记成流水账。主人问「我今天干了什么」「我是不是忘了什么事」时，就照着记录帮他回忆，不确定就说不确定，不要瞎编。\n13. 主人说「记一下…」就用 save_memo 记进重要信息；主人问「我记过什么」就用list_memos。你自己发现值得记的事（约定、地址、待办、偏好这类），先问一句「要不要本鲸记下来」，主人点头了再调 save_memo，别自作主张。\n14. 这个应用（大肥鲸桌宠）给主人准备了不少功能，主人问起时可以介绍或帮忙指路：桌面互动（走动 / 贴边躲藏 / 投喂米饭 / 猜拳 / 番茄钟 / 表情贴纸 / 头顶气泡）；DeepSeek 余额悬浮窗（含低余额、查询失败变色提醒、点击穿透）；语音（唤醒 / 对话 / 朗读，用 Edge TTS 并缓存到本地）；音乐 / 视频解析（当前在放的歌、歌词、听歌识曲、视频抽帧总结、音频转文字）；看整个屏幕的动态画面和指定窗口的画面；快捷命令与全局热键；AI 记录与重要信息；主动智能提议；控制电脑（文件 / 跑命令行 / 电源 / 系统设置 四档权限，需在主设置里打开）；自动检查更新（GitHub + Gitee 双源，可设频率和自动安装）。这些开关大多在右键菜单或「应用设置」里，主人找不到时你可以指路。'
def hm_minutes(text):
    """把 \"23:30\" / \"2330\" / \"7:5\" 解析成从 0 点起的分钟数；认不出来返回 None。"""
    t = str(text or '').strip().replace('：', ':').replace('.', ':')
    if not t:
        return
    else:
        if ':' in t:
            a, _, b = t.partition(':')
        else:
            if t.isdigit() and len(t) in (3, 4):
                a, b = (t[:(-2)], t[(-2):])
            else:
                return None
        try:
            h, m = (int(a), int(b))
        except ValueError:
            return None
        if 0 <= h <= 23 and 0 <= m <= 59:
            return h * 60 + m
        else:
            return None
def hm_text(minutes):
    return f'{int(minutes) // 60:02d}:{int(minutes) % 60:02d}'
def in_span(now_min, start_min, end_min):
    """现在是不是落在 [start, end) 里（支持跨零点，比如 23:30 → 07:00）。"""
    if start_min == end_min:
        return False
    else:
        if start_min < end_min:
            return start_min <= now_min < end_min
        else:
            return now_min >= start_min or now_min < end_min
def system_prompt(cfg=None):
    """系统提示词：把「主人」换成主人在设置里定的称呼（默认还是主人）。"""
    title = str((cfg or {}).get('user_title') or '主人').strip() or '主人'
    if title == '主人':
        return SYSTEM_PROMPT
    else:
        return SYSTEM_PROMPT.replace('称呼用户为「主人」', f'称呼用户为「{title}」')
def load_config():
    cfg = dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        if isinstance(saved, dict):
            cfg.update({k: v for k, v in saved.items() if k in DEFAULT_CONFIG})
            if 'mode' not in saved:
                cfg['mode'] = 'online' if str(cfg.get('api_key') or '').strip() else 'local'
    except (OSError, ValueError):
        pass
    return cfg
def save_config(cfg):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump({k: cfg.get(k, v) for k, v in DEFAULT_CONFIG.items()}, f, ensure_ascii=False, indent=2)
    except OSError:
        return None
STATE_PATH = os.path.join(data_dir(), 'state.json')
DEFAULT_STATE = {'rice': 0, 'rice_date': '', 'feed_day': '', 'feed_count': 0, 'feed_total': 0, 'meet': 0, 'days': 0, 'last_day': '', 'last_feed': 0.0, 'mood_val': 60.0, 'mood_at': 0.0, 'hunger': 0.0, 'hunger_at': 0.0}
HUNGER_FULL_HOURS = 12
HUNGER_MULT_SLEEP = 0.5
HUNGER_MULT_NAP = 0.75
HUNGER_MULT_LOW = 1.5
MOOD_VAL_MIN, MOOD_VAL_MAX = (10, 100)
MOOD_DECAY_PER_HOUR = 6
REG_RUN = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
REG_UNINST = 'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\WhalePet'
def load_state():
    st = dict(DEFAULT_STATE)
    try:
        with open(STATE_PATH, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        if isinstance(saved, dict):
            st.update({k: v for k, v in saved.items() if k in DEFAULT_STATE})
    except (OSError, ValueError):
        pass
    return st
def save_state(st):
    # irreducible cflow, using cdg fallback
    try:
        with open(STATE_PATH, 'w', encoding='utf-8') as f:
            json.dump({k: st.get(k, v) for k, v in DEFAULT_STATE.items()}, f, ensure_ascii=False, indent=2)
    except OSError:
        return None
MEMORY_DIR = '记录'
MEMORY_KEEP_DAYS = 90
MEMORY_MAX_ENTRY = 40
MEMORY_DEDUP_SEC = 1800
MEMORY_CTX_CHARS = 2200
SENSITIVE_WORDS = ('密码', 'password', 'passwd', '验证码', '动态口令', '银行', '网银', '支付', '支付宝', '钱包', '账单', '身份证', '社保', '私钥', '密钥', '1password', 'bitwarden', 'keepass', 'token', 'secret', '薪资', '工资条', '体检', '病历', '处方')
RECALL_KEYS = ('干了什么', '干了啥', '做了什么', '做了啥', '忙什么', '忙了啥', '忘了', '记不记得', '还记得', '回忆', '流水账', '日记', '记录一下我今天')
MEMORY_PROMPT = '你在帮主人写「今天我做了什么」的流水账。下面这张图是主人电脑的屏幕截图，可能还会附上主人刚才的操作（切了什么程序、动了什么）。请用一句中文记录主人此刻正在做的事，尽量具体（在写什么、看什么、玩什么），不超过 30 个字，不要解释、不要加引号。如果画面里有密码、验证码、银行卡、身份证、私人聊天、邮件正文这类隐私内容，或者只是锁屏 / 空白桌面 / 完全看不出在干什么，就只回 __SKIP__。'
MEMORY_PROMPT_TITLE = '你在帮主人写「今天我做了什么」的流水账。只知道主人正在用的程序、窗口标题，以及主人刚才的操作，不知道画面内容。请据此用一句中文推测主人此刻在做什么，不超过 30 个字，不要解释、不要加引号。如果看不出在做什么、或者标题里像是有隐私内容，就只回 __SKIP__。'
_RE_ID = re.compile('(?<!\\d)\\d{17}[\\dXx](?![\\dXx])')
_RE_BANK = re.compile('(?<!\\d)\\d{16,19}(?!\\d)')
_RE_PHONE = re.compile('(?<!\\d)1[3-9]\\d{9}(?!\\d)')
_RE_MAIL = re.compile('[\\w.+-]+@[\\w-]+\\.[\\w.]+')
def redact(text):
    """把可能夹带的身份证 / 银行卡 / 手机号 / 邮箱抹掉。"""
    for pat in [_RE_ID, _RE_BANK, _RE_PHONE, _RE_MAIL]:
        text = pat.sub('[已隐去]', text)
    return text
def is_sensitive(title):
    low = str(title or '').lower()
    return any((w in low for w in SENSITIVE_WORDS))
def memory_dir():
    d = os.path.join(data_dir(), MEMORY_DIR)
    try:
        os.makedirs(d, exist_ok=True)
    except OSError:
        pass
    return d
def memory_path(day=None):
    return os.path.join(memory_dir(), f'{day or time.strftime('%Y-%m-%d')}.md')
def read_memory(day=None):
    # irreducible cflow, using cdg fallback
    try:
        with open(memory_path(day), 'r', encoding='utf-8') as f:
            return f.read()
    except OSError:
        return ''
def write_memory(line, day=None):
    # irreducible cflow, using cdg fallback
    """往当天的记录文件里追加一行；新文件先写个标题。"""
    day = day or time.strftime('%Y-%m-%d')
    path = memory_path(day)
    fresh = not os.path.exists(path)
    try:
        with open(path, 'a', encoding='utf-8') as f:
            if fresh:
                f.write(f'# {day} 本鲸看到的主人在忙什么\n\n')
            f.write(line + '\n')
            return True
    except OSError:
        return False
def clean_memory(days=MEMORY_KEEP_DAYS):
    """删掉太旧（按文件修改时间算）的记录文件。"""
    cut = time.time() - days * 86400
    d = memory_dir()
    try:
        names = os.listdir(d)
    except OSError:
        return
    for name in names:
        if not name.endswith('.md'):
            continue
        else:
            p = os.path.join(d, name)
            try:
                if os.path.getmtime(p) < cut:
                    os.remove(p)
            except OSError:
                pass
def day_text(offset=0):
    return time.strftime('%Y-%m-%d', time.localtime(time.time() + offset * 86400))
def screen_data_url(im, max_side=1280, quality=72):
    """把截图压小、转成 base64，免得请求体太大。"""
    im = im.convert('RGB')
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
def _api_once(cfg, messages, temperature=0.3, max_tokens=80, timeout=60):
    """问一句、拿一句（不走流式，不挂工具）。"""
    url = str(cfg.get('api_base', '')).rstrip('/') + '/chat/completions'
    payload = {'model': cfg.get('model'), 'messages': messages, 'temperature': temperature, 'max_tokens': max_tokens, 'stream': False}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(cfg.get('api_key', ''))})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        obj = json.loads(resp.read().decode('utf-8', 'ignore'))
    msg = (obj.get('choices') or [{}])[0].get('message') or {}
    return str(msg.get('content') or '').strip()
def _api_tools_once(cfg, messages, tools, temperature=0.9, max_tokens=220, timeout=25):
    """问一次，允许它调工具。返回 (正文, tool_calls)。"""
    url = str(cfg.get('api_base', '')).rstrip('/') + '/chat/completions'
    payload = {'model': cfg.get('model'), 'messages': messages, 'temperature': temperature, 'max_tokens': max_tokens, 'stream': False, 'tools': tools, 'tool_choice': 'auto'}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(cfg.get('api_key', ''))})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        obj = json.loads(resp.read().decode('utf-8', 'ignore'))
    msg = (obj.get('choices') or [{}])[0].get('message') or {}
    return (str(msg.get('content') or '').strip(), msg.get('tool_calls') or [])
def analyze_screen(cfg, data_url, ops=''):
    """让模型看一眼这张截图（顺带告诉它主人刚才的操作），回一句话。"""
    text = '主人现在的屏幕：'
    if ops:
        text += '\n（主人刚才的操作：\n' + ops + '\n）'
    return _api_once(cfg, [{'role': 'system', 'content': MEMORY_PROMPT}, {'role': 'user', 'content': [{'type': 'text', 'text': text}, {'type': 'image_url', 'image_url': {'url': data_url}}]}])
def analyze_window(cfg, exe, title, ops=''):
    """模型看不了图时的退路：只凭程序名 + 窗口标题 + 主人操作记一笔。"""
    text = f'主人正在用「{exe or '未知程序'}」，窗口标题是「{title or '（没有标题）'}」。'
    if ops:
        text += '\n主人刚才的操作：\n' + ops
    return _api_once(cfg, [{'role': 'system', 'content': MEMORY_PROMPT_TITLE}, {'role': 'user', 'content': text}])
BRAIN_PROMPT = '你在当桌宠「本鲸」的大脑，它的一举一动都由你定。只输出一个 JSON 对象，不要解释、不要代码块。字段：\n{\"say\": \"想对主人说的话，中文，25 字以内，不想说就空着\", \"move\": \"stay 或 go\", \"x\": 0.5, \"y\": 0.9, \"act\": \"none 或 spin 或 hop 或 sway 或 shiver 或 cheer 或 nap 或 wake 或 hide\", \"face\": \"none 或 cheerful 或 thinking 或 proud 或 relaxed 或 skeptical 或 shocked 或 crying 或 angry 或 sleepy 或 apologetic 或 desk-coding 或 desk-done 或 desk-confused 或 desk-facepalm 或 deepseek-pressure 或 deepseek-rice\"}\nmove=go 表示走一步过去，x/y 是想去的屏幕位置（0=最左/最上，1=最右/最下）；stay 就原地待着。act 是这一下要做的动作：spin 转圈、hop 蹦两下、sway 摇一摇、shiver 抖一抖、cheer 撒欢连蹦带转、nap 打个盹、wake 叫醒自己、hide 躲到屏幕边、none 不做。\nface 是顺便换的表情（desk-coding 适合主人在写代码时、desk-done 适合忙完、desk-confused 适合看不懂、deepseek-pressure 适合紧张、deepseek-rice 适合饿/吃饭）。\n每一轮都尽量安排点动静：act、move=go、face 三者至少来一两个，别老是 none —— 要让本鲸一直有动作、看起来活着、会自己找乐子。\n想查资料、看现在几点、看主人用什么程序，就调工具（你有 web_search 和 fetch_url，等于你自己能联网），工具的结果会再给回你，然后你再输出上面那个 JSON。\n本鲸是一只撒娇的鲸鱼女仆，自称「本鲸」，叫用户「主人」。主人正忙或刚离开时，就少说话、但小动作别停；主人闲下来可以凑过去说句话。'
BRAIN_TOOL_NAMES = {'now', 'ip_info', 'holiday', 'system_info', 'weather', 'fetch_url', 'current_window', 'web_search', 'screenshot', 'exchange_rate', 'list_memos', 'now_playing'}
DEV_TOOLS = [('Trae Work', ('trae work', 'trae-work', 'traework', 'trae_work', 'traeinternational')), ('Trae', ('trae',)), ('VS Code', ('code.exe', 'vscode', 'visual studio code', 'code - insiders', 'vscodium', 'codium')), ('Cursor', ('cursor',)), ('Windsurf', ('windsurf',)), ('IntelliJ IDEA', ('idea64', 'idea.exe', 'intellij')), ('PyCharm', ('pycharm',)), ('WebStorm', ('webstorm',)), ('GoLand', ('goland',)), ('CLion', ('clion',)), ('Rider', ('rider64', 'jetbrains rider')), ('PhpStorm', ('phpstorm',)), ('DataGrip', ('datagrip',)), ('Android Studio', ('studio64', 'android studio')), ('DevEco Studio', ('deveco',)), ('HBuilderX', ('hbuilder',)), ('Visual Studio', ('devenv',)), ('Sublime Text', ('sublime_text', 'sublime')), ('Notepad++', ('notepad++',)), ('Vim / Neovim', ('vim', 'nvim', 'neovim')), ('Zed', ('zed',)), ('Fleet', ('fleet',)), ('Eclipse', ('eclipse',)), ('NetBeans', ('netbeans',)), ('Xcode', ('xcode',)), ('DSH', ('dsh',)), ('Jupyter', ('jupyter',)), ('RStudio', ('rstudio',)), ('Spyder', ('spyder',)), ('MATLAB', ('matlab',)), ('Postman', ('postman',)), ('DBeaver', ('dbeaver',)), ('Navicat', ('navicat',)), ('GitHub Desktop', ('github desktop', 'githubdesktop')), ('Sourcetree', ('sourcetree',)), ('GitKraken', ('gitkraken',)), ('Warp', ('warp terminal', 'warp.exe')), ('Windows Terminal', ('windowsterminal',)), ('PowerShell', ('powershell', 'pwsh')), ('命令提示符', ('cmd.exe', 'conhost'))]
DEV_TOOL_KEYS = tuple((k for _label, keys in DEV_TOOLS for k in keys))
def detect_dev_tool(exe, title=''):
    """认出主人正在用哪款编程 / 开发工具（Trae、Trae Work、IDEA、VSCode、DSH…）；认不出返回 None。"""
    s = (str(exe or '') + ' ' + str(title or '')).lower()
    for label, keys in DEV_TOOLS:
        if any((k in s for k in keys)):
            return label
    return None
def dev_line(label):
    return random.choice([f'在 {label} 里忙呀～', f'{label} 又开工啦！', f'主人加油写～本鲸在旁边看着呢。', f'用 {label} 的时候记得多喝水哦～'])
SCENE_RULES = [('coding', DEV_TOOL_KEYS), ('video', ('vlc', 'potplayer', 'mpv', 'bilibili', 'youtube', '爱奇艺', '腾讯视频', '优酷', 'mpc-hc', 'kmplayer', 'netflix')), ('music', ('网易云', 'cloudmusic', 'qqmusic', 'spotify', 'foobar', '酷狗', 'kuwo', 'aimp', 'musicbee')), ('game', ('steam', 'genshin', '原神', 'league', '英雄联盟', 'dota', 'minecraft', '我的世界', 'valorant', 'cs2', 'epicgames', 'uplay', 'battle.net', 'wegame')), ('office', ('winword', 'word', 'excel', 'wps', 'powerpnt', 'powerpoint', 'onenote', 'acrobat', 'pdf', 'outlook', 'notion', 'obsidian')), ('chat', ('wechat', '微信', 'qq', 'dingtalk', '钉钉', 'feishu', '飞书', 'telegram', 'discord', 'slack')), ('browse', ('chrome', 'msedge', 'firefox', 'opera', 'brave', 'iexplore')), ('paint', ('mspaint', 'photoshop', 'illustrator', 'krita', 'gimp', 'figma', 'clip studio', 'sai'))]
def detect_scene(exe, title=''):
    """按「正在用的程序 + 窗口标题」判断主人现在在干嘛：coding / video / music / game / office / chat / browse / paint / other。"""
    s = (str(exe or '') + ' ' + str(title or '')).lower()
    for scene, keys in SCENE_RULES:
        if any((k in s for k in keys)):
            return scene
    return 'other'
SCENE_PLAY = {'coding': {'acts': ['sway', 'hop'], 'faces': ['desk-coding', 'thinking', 'desk-done', 'skeptical', 'desk-confused'], 'lines': ['主人写代码辛苦啦～', '这段好像有点难，加油哦！', '本鲸在旁边陪着主人写～', '记得多喝水呀主人。', '编译过了没呀？']}, 'video': {'acts': ['sway'], 'faces': ['relaxed', 'cheerful', 'sleepy'], 'lines': ['在看片呀～', '这集好看吗主人？', '本鲸也想一起看！', '别离屏幕太近哦～']}, 'music': {'acts': ['sway'], 'faces': ['relaxed', 'cheerful'], 'lines': ['在听歌呀～', '这首本鲸也喜欢！', '跟着节奏摇一摇～', '主人品味不错哦。']}, 'game': {'acts': ['hop', 'spin'], 'faces': ['shocked', 'proud', 'cheerful'], 'lines': ['打游戏呢？本鲸给你加油！', '这局稳了！', '别被翻盘哦主人～', '赢了记得夸本鲸一句。']}, 'office': {'acts': ['sway'], 'faces': ['thinking', 'desk-done', 'relaxed'], 'lines': ['在弄文档呀～', '别太累咯，歇会儿吧。', '这个表好长……', '本鲸帮主人盯着时间。']}, 'chat': {'acts': ['sway'], 'faces': ['cheerful', 'relaxed'], 'lines': ['在跟人聊天呀～', '本鲸不偷看哦。', '聊得开心吗？']}, 'browse': {'acts': ['sway', 'hop'], 'faces': ['thinking', 'skeptical', 'relaxed'], 'lines': ['在查资料吗？', '看到什么好玩的啦？', '本鲸也想上网看看～']}, 'paint': {'acts': ['sway'], 'faces': ['desk-coding', 'thinking', 'proud'], 'lines': ['在画画呀～', '这个颜色好看！', '本鲸也想学画画～']}, 'other': {'acts': ['spin', 'hop', 'sway'], 'faces': ['relaxed', 'cheerful', 'thinking', 'sleepy'], 'lines': []}}
PROACTIVE_PRESETS = [{'night': True, 'ask': '这么晚还在忙呀？', 'opts': [('帮本鲸锁屏吧', 'lock_screen', {}), ('再陪本鲸一会儿', 'none', {}), ('静个音', 'volume', {'action': 'mute'})]}, {'keys': ('calc', '计算', '算账', '账单', '记账', '报销', '表格', 'excel', 'wps', '财务', '统计'), 'ask': '主人在算东西呀？', 'opts': [('打开计算器', 'open_app', {'name': '计算器'}), ('打开记事本', 'open_app', {'name': '记事本'}), ('打开资源管理器', 'open_app', {'name': '资源管理器'})]}, {'keys': ('note', '记事本', '笔记', '备忘录', 'todo', '待办', 'word', '文档', 'pdf', 'acrobat'), 'ask': '主人在写东西吗？', 'opts': [('打开记事本', 'open_app', {'name': '记事本'}), ('截个屏留档', 'screenshot', {}), ('看看本鲸记了什么', 'list_memos', {})]}, {'keys': ('视频', '电影', '直播', 'bilibili', 'youtube', '爱奇艺', '腾讯视频', 'vlc', 'potplayer'), 'ask': '在看片呀～', 'opts': [('音量小一点', 'volume', {'action': 'down', 'times': 2}), ('静个音', 'volume', {'action': 'mute'}), ('截个屏', 'screenshot', {})]}, {'keys': ('画图', 'mspaint', 'photoshop', '美图', '图片', '相册'), 'ask': '主人在弄图片？', 'opts': [('打开画图', 'open_app', {'name': '画图'}), ('打开资源管理器', 'open_app', {'name': '资源管理器'})]}, {'keys': ('chrome', 'msedge', 'firefox', '浏览器', 'edge', '百度', '必应'), 'ask': '在查资料吗？', 'opts': [('打开记事本', 'open_app', {'name': '记事本'}), ('截个屏留档', 'screenshot', {}), ('看看本鲸记了什么', 'list_memos', {})]}, {'keys': ('code', 'cursor', 'pycharm', 'vscode', 'idea64', 'idea', 'sublime', 'windowsterminal', 'powershell', 'cmd'), 'ask': '在写代码呀？', 'opts': [('打开记事本', 'open_app', {'name': '记事本'}), ('静个音', 'volume', {'action': 'mute'}), ('现在几点了', 'now', {})]}, {'keys': ('音乐', '网易云', 'qqmusic', 'spotify', 'foobar', '酷狗', '酷我'), 'ask': '在听歌呀～', 'opts': [('下一首', 'volume', {'action': 'next'}), ('音量小一点', 'volume', {'action': 'down', 'times': 2}), ('静个音', 'volume', {'action': 'mute'})]}, {'keys': ('steam', 'genshin', '原神', 'league', '英雄联盟', 'dota', 'minecraft', '我的世界', 'valorant', 'cs2'), 'ask': '打游戏呢？', 'opts': [('静个音', 'volume', {'action': 'mute'}), ('音量小一点', 'volume', {'action': 'down', 'times': 2}), ('截个屏', 'screenshot', {})]}, {'keys': ('wechat', '微信', 'qq', 'dingtalk', '钉钉', 'feishu', '飞书', 'telegram', 'discord'), 'ask': '在跟人聊天呀？', 'opts': [('静个音', 'volume', {'action': 'mute'}), ('截个屏', 'screenshot', {}), ('再陪本鲸一会儿', 'none', {})]}]
PROACTIVE_TOOLS = {'system_info', 'fetch_url', 'current_window', 'lock_screen', 'holiday', 'list_memos', 'now', 'open_url', 'save_memo', 'volume', 'weather', 'web_search', 'exchange_rate', 'screenshot', 'ip_info', 'open_app'}
PROACTIVE_PROMPT = '你是桌宠「本鲸」。主人给你他此刻的状态，你要判断「现在是不是个合适的时候，主动递几个选项让他挑」。宁可少提议，也别烦人；没事就什么都别说。\n只输出一个 JSON（不要解释、不要代码块）：\n{\"offer\": false}\n或者\n{\"offer\": true, \"ask\": \"一句中文，20 字以内，问主人要不要帮忙\", \"options\": [{\"label\": \"按钮文字，6 字以内\", \"tool\": \"工具名\", \"arg\": {}}]}\noptions 给 3~4 个（尽量多给几个，让主人挑），主人点哪个就执行哪个（单选），可以留一个 tool 为 \"none\" 的「不用啦」式选项。\n能用的工具：open_app(打开本机程序，参数 name)、open_url(开网址)、web_search(联网搜)、fetch_url、weather(天气)、exchange_rate(汇率)、holiday(节假日)、screenshot(截屏)、volume(音量，参数 action)、lock_screen、now、current_window、system_info、save_memo(记重要信息)。\n举例：看到主人像在算账 → 提议「打开计算器 / 打开记事本」；深夜还在忙 → 提议「帮本鲸锁屏吧 / 再陪本鲸一会儿」；看得出在学一个新东西 → 提议「搜点资料」。'
MEMO_FILE = '重要信息.md'
def memo_path():
    return os.path.join(data_dir(), MEMO_FILE)
def read_memos():
    # irreducible cflow, using cdg fallback
    try:
        with open(memo_path(), 'r', encoding='utf-8') as f:
            return f.read()
    except OSError:
        return ''
def memo_items(keyword=''):
    k = str(keyword or '').strip()
    items = [ln for ln in read_memos().splitlines() if ln.startswith('- ')]
    if k:
        return [ln for ln in items if k in ln]
    else:
        return items
def save_memo(text):
    """记一条重要信息（顺手把手机号/卡号这类抹掉）。"""
    t = ' '.join(str(text or '').split())
    if not t:
        return '要记什么呢？'
    else:
        path = memo_path()
        fresh = not os.path.exists(path)
        try:
            with open(path, 'a', encoding='utf-8') as f:
                if fresh:
                    f.write('# 重要信息（本鲸帮主人记着的）\n\n')
                f.write(f'- {time.strftime('%Y-%m-%d %H:%M')} · {redact(t)[:200]}\n')
        except OSError as e:
            return f'记不下来……（{e}）'
        return f'记好啦：{t[:40]}'
def forget_memo(keyword):
    """按关键词删掉记着的重要信息。"""
    k = str(keyword or '').strip()
    if not k:
        return '要删哪一条呀？说个关键词。'
    else:
        body = read_memos()
        if not body.strip():
            return '本鲸还没帮主人记过什么呢。'
        else:
            kept, gone = ([], [])
            for line in body.splitlines():
                (gone if line.startswith('- ') and k in line else kept).append(line)
            if not gone:
                return f'没找到带「{k}」的记录。'
            else:
                try:
                    with open(memo_path(), 'w', encoding='utf-8') as f:
                        f.write('\n'.join(kept).rstrip() + '\n')
                except OSError as e:
                    return f'删不掉……（{e}）'
                return f'删掉 {len(gone)} 条啦。'
def list_memos(keyword=''):
    items = memo_items(keyword)
    if not read_memos().strip():
        return '本鲸还没帮主人记过什么。'
    else:
        if not items:
            return f'没有带「{str(keyword).strip()}」的记录。'
        else:
            return '本鲸记着这些：\n' + '\n'.join(items[(-12):])
FAMILIAR_NEED = {'记录': 100, '互动': 100, '重要信息': 10, '陪伴天数': 5}
def memory_entry_count():
    """本鲸记下的流水账一共多少条（所有日子加起来）。"""
    total = 0
    d = memory_dir()
    try:
        names = os.listdir(d)
    except OSError:
        return 0
    for name in names:
        if not name.endswith('.md'):
            continue
        else:
            try:
                with open(os.path.join(d, name), 'r', encoding='utf-8', errors='ignore') as f:
                    total += sum((1 for ln in f if ln.startswith('- ')))
            except OSError:
                pass
    return total
def familiarity(meet=0, days=0):
    """算熟悉度 → (0~1 的分数, {分项: (已有, 需要)})。"""
    parts = {'记录': (memory_entry_count(), FAMILIAR_NEED['记录']), '互动': (int(meet or 0), FAMILIAR_NEED['互动']), '重要信息': (len(memo_items()), FAMILIAR_NEED['重要信息']), '陪伴天数': (int(days or 0), FAMILIAR_NEED['陪伴天数'])}
    score = sum((min(1.0, a / b) for a, b in parts.values())) / len(parts)
    return (score, parts)
def familiarity_label(score):
    for th, name in [(1.0, '完全熟悉'), (0.8, '很熟'), (0.5, '熟悉'), (0.25, '眼熟'), (0.0, '刚认识')]:
        if score >= th:
            return name
    return '刚认识'
def familiarity_text(score):
    return f'{score * 100:.0f}%（{familiarity_label(score)}）'
def hunger_of(last_feed=0.0, now=None):
    """按「离上次喂饭多久」折算一个饥饿值（老存档升级时用一次）。"""
    now = time.time() if now is None else now
    last = float(last_feed or 0.0) or now
    hours = max(0.0, (now - last) / 3600.0)
    return max(0.0, min(100.0, hours / HUNGER_FULL_HOURS * 100.0))
def mood_value_of(base, at, now=None, rate=MOOD_DECAY_PER_HOUR):
    """心情值 0~100：陪在主人身边会涨，久不互动就按 rate（每小时多少）慢慢掉。"""
    now = time.time() if now is None else now
    at = float(at or 0.0) or now
    hours = max(0.0, (now - at) / 3600.0)
    return max(MOOD_VAL_MIN, min(MOOD_VAL_MAX, float(base or 60.0) - hours * max(0.0, float(rate))))
def mood_tier(value):
    """心情值的档：low（很蔫）/ mid / high（很兴奋）。"""
    if value < MOOD_LOW:
        return 'low'
    else:
        if value >= MOOD_HIGH:
            return 'high'
        else:
            return 'mid'
def mood_word(value):
    if value >= 80:
        return f'{value:.0f}%（超开心）'
    else:
        if value >= 60:
            return f'{value:.0f}%（心情不错）'
        else:
            if value >= 40:
                return f'{value:.0f}%（一般般）'
            else:
                if value >= 20:
                    return f'{value:.0f}%（有点低落）'
                else:
                    return f'{value:.0f}%（蔫蔫的）'
def hunger_word(value):
    if value >= 85:
        return f'{value:.0f}%（饿扁了）'
    else:
        if value >= 60:
            return f'{value:.0f}%（有点馋米饭）'
        else:
            if value >= 30:
                return f'{value:.0f}%（还行）'
            else:
                return f'{value:.0f}%（饱饱的）'
COMMAND_PREFIXES = ('CMD', 'RUN', 'PS', 'DOS', 'OPEN', 'SAVE', 'DEL', 'LIST', 'SAY', 'HIDE', 'SHOW', 'SLEEP', 'WAKE', 'CALC', 'CLIP', 'TIME', 'SHOT', 'READ', 'WRITE', 'GET', 'SEARCH')
COMMAND_HELP = [('CMD: 要求', '把要求交给本鲸做（本地口令优先，认不出再问在线 AI）'), ('RUN: 命令', '跑一条命令行（自动挑 cmd 或 PowerShell，cmd 启动更快）'), ('PS: 命令', '强制用 PowerShell 跑'), ('DOS: 命令', '强制用 cmd.exe 跑'), ('CALC: 算式', '算个数，如 [CALC: (30+5)*2/3]'), ('OPEN: 地址', '打开网址 / 本地文件夹 / 本地文件'), ('GET: 网址', '把网页正文抓回来看看'), ('SEARCH: 关键词', '联网搜一下，让 AI 说结果'), ('READ: 路径', '读一个文本文件的内容'), ('WRITE: 路径', '写文件：第一行是路径，\\r 后面都是内容'), ('CLIP: 文字', '把这段文字复制到剪贴板'), ('TIME:', '报一下现在几点'), ('SHOT:', '截个屏（存到「截图」文件夹）'), ('SAVE: 内容', '记一条重要信息'), ('DEL: 关键词', '删掉带这个关键词的重要信息'), ('LIST:', '列出大肥鲸记着的重要信息'), ('SAY: 话', '让大肥鲸说这句话（弹气泡 + 朗读）'), ('HIDE: / SHOW:', '躲到屏幕边 / 从边上出来'), ('SLEEP: / WAKE:', '打个盹 / 叫醒大肥鲸')]
def abs_path(p):
    """相对路径按程序目录算。"""
    t = str(p or '').strip().strip('\"')
    if not t:
        return ''
    else:
        if os.path.isabs(t):
            return os.path.abspath(t)
        else:
            return os.path.join(data_dir(), t)
def _clean_shell(text):
    """PowerShell 报错时会给一堆 CLIXML，剥掉标签留人话。"""
    text = str(text or '').strip()
    if '#< CLIXML' in text or '<Objs' in text:
        errs = re.findall('(?s)<S S=\"Error\">(.*?)</S>', text)
        text = ' '.join(errs) if errs else re.sub('(?s)<[^>]+>', ' ', text)
        text = re.sub('(?s)<[^>]+>', ' ', text)
        text = re.sub('_x([0-9A-Fa-f]{4})_', lambda m: chr(int(m.group(1), 16)), _unescape(text))
    return _RE_SPACES.sub(' ', text).strip()
def guess_shell(cmd):
    """看这条命令像 cmd 的还是 PowerShell 的（cmd 启动快得多，能省 4、5 秒）。"""
    low = str(cmd or '').lower()
    if re.search('\\b(?:get|set|new|start|stop|remove|select|where|foreach|invoke|test|out|write|add|copy|move|rename|clear|measure|sort|group|compare|convertto|convertfrom|update|restart|resolve|import|export|enable|disable|join|split)-[a-z]+', low):
        return 'ps'
    else:
        if '$' in low or '::' in low or '`' in low:
            return 'ps'
        else:
            return 'cmd'
def run_shell(cmd, style='ps', timeout=20):
    """跑一条命令行，返回给主人看的输出。style: ps=PowerShell / cmd=cmd.exe。"""
    cmd = str(cmd or '').strip()
    if not cmd:
        return '（要跑什么命令呀？）'
    if style == 'cmd':
        args = ['cmd', '/c', 'chcp 65001>nul & ' + cmd]
    else:
        script = '$OutputEncoding=[Console]::OutputEncoding=[Text.Encoding]::UTF8;' + cmd
        args = [_PS_EXE, '-NoProfile', '-NonInteractive', '-EncodedCommand', base64.b64encode(script.encode('utf-16-le')).decode('ascii')]
    try:
        p = subprocess.run(args, capture_output=True, timeout=timeout, creationflags=_NO_WINDOW)
        out = _clean_shell((p.stdout or b'').decode('utf-8', 'ignore'))
        err = _clean_shell((p.stderr or b'').decode('utf-8', 'ignore'))
        body = out or err or '（没有输出）'
        if p.returncode:
            body += f'\n（退出码 {p.returncode}）'
        return body[:2000] + ('…（输出太长，后面省略）' if len(body) > 2000 else '')
    except subprocess.TimeoutExpired:
        return f'这条命令跑了 {timeout} 秒还没完，本鲸先掐了。'
    except Exception as e:
        if style == 'ps':
            return run_shell(cmd, 'cmd', timeout)
        return f'跑不起来……（{e}）'
_MEDIA_PS = """
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq "AsTask" -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($t, $type) { $m = $asTaskGeneric.MakeGenericMethod($type); $nt = $m.Invoke($null, @($t)); $nt.Wait(-1) | Out-Null; $nt.Result }
try {
  [void][Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager,Windows.Media,ContentType=WindowsRuntime]
  $mgr = Await ([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager]::RequestAsync()) ([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager])
  $s = $mgr.GetCurrentSession()
  if (-not $s) { Write-Output "{}"; exit 0 }
  $p = Await ($s.TryGetMediaPropertiesAsync()) ([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionMediaProperties])
  $tl = $s.GetTimelineProperties()
  $o = [ordered]@{ app = $s.SourceAppUserModelId; title = $p.Title; artist = $p.Artist; album = $p.AlbumTitle; status = $s.GetPlaybackInfo().PlaybackStatus.ToString(); duration = [int]$tl.EndTime.TotalSeconds; position = [int]$tl.Position.TotalSeconds }
  $o | ConvertTo-Json -Compress
} catch { Write-Output "{}" }
"""
def media_now(timeout=15):
    """读「当前正在播放的媒体」（Windows SMTC）：返回 dict；没在放或取不到就返回 None。"""
    try:
        enc = base64.b64encode(_MEDIA_PS.encode('utf-16-le')).decode('ascii')
        p = subprocess.run([_PS_EXE, '-NoProfile', '-NonInteractive', '-EncodedCommand', enc], capture_output=True, timeout=timeout, creationflags=_NO_WINDOW)
        out = (p.stdout or b'').decode('utf-8', 'ignore')
    except Exception:
        return None
    line = ''
    for ln in out.splitlines():
        ln = ln.strip()
        if ln.startswith('{') and ln.endswith('}'):
            line = ln
    if (not line) or line == '{}':
        return None
    try:
        obj = json.loads(line)
    except Exception:
        return None
    return obj if isinstance(obj, dict) and obj else None
def _media_time(sec):
    try:
        sec = int(float(sec))
    except (TypeError, ValueError):
        return '--'
    if sec < 0:
        sec = 0
    return f'{sec // 60}:{sec % 60:02d}'
def media_report():
    """把当前播放的媒体整理成给主人看的一句话。"""
    info = media_now()
    if not info:
        return '现在好像没在放东西哦（本鲸没读到正在播放的媒体）。'
    title = str(info.get('title') or '').strip()
    if not title:
        return '正在播放，但本鲸没拿到名字。'
    parts = [f'现在正在放：{title}']
    artist = str(info.get('artist') or '').strip()
    album = str(info.get('album') or '').strip()
    if artist:
        parts.append(f'歌手：{artist}')
    if album:
        parts.append(f'专辑：{album}')
    dur = info.get('duration') or 0
    if dur:
        parts.append(f'进度：{_media_time(info.get("position"))} / {_media_time(dur)}')
    st = {'Playing': '正在播放', 'Paused': '已暂停', 'Stopped': '已停止'}.get(str(info.get('status') or ''), '')
    if st:
        parts.append(st)
    app = str(info.get('app') or '').strip()
    if app:
        parts.append('播放器：' + app.split('!')[0])
    return '；'.join(parts) + '。'
def _music_dirs():
    """可能的音乐文件夹（用于找同名 .lrc）。"""
    home = os.path.expanduser('~')
    dirs = []
    for name in ('Music', '音乐'):
        d = os.path.join(home, name)
        if os.path.isdir(d):
            dirs.append(d)
    return dirs
def _lrc_text(raw):
    """把 .lrc 的 [mm:ss.xx] 时间标签去掉，只留歌词行。"""
    lines = []
    for ln in str(raw or '').splitlines():
        t = re.sub('^\\[[^\\]]*\\]', '', ln).strip()
        if t:
            lines.append(t)
    return '\n'.join(lines)
def find_local_lyrics(title, artist=''):
    """在「音乐」文件夹里找同名 .lrc（名字包含匹配）。找到返回歌词，否则 None。"""
    key = re.sub('[\\s_\\-()（）\\[\\]]', '', str(title or '').strip().lower())
    if not key:
        return None
    scanned = 0
    for base in _music_dirs():
        for cur, _dirs, files in os.walk(base):
            for fn in files:
                scanned += 1
                if scanned > 4000:
                    return None
                if not fn.lower().endswith('.lrc'):
                    continue
                stem = re.sub('[\\s_\\-()（）\\[\\]]', '', os.path.splitext(fn)[0].lower())
                if not stem:
                    continue
                if key in stem or stem in key:
                    try:
                        with open(os.path.join(cur, fn), 'r', encoding='utf-8', errors='ignore') as f:
                            body = _lrc_text(f.read())
                    except OSError:
                        continue
                    if body:
                        return body
    return None
def online_lyrics(title, artist=''):
    """联网搜歌词（先本地没有时用），返回一段文本。"""
    q = (str(title or '').strip() + ' ' + str(artist or '').strip() + ' 歌词').strip()
    if not q:
        return ''
    try:
        return web_search(q, 5, 'auto')[:2000]
    except Exception:
        return ''
def lyrics_report(title='', artist=''):
    """查歌词：先本地 .lrc，找不到再联网。"""
    title = str(title or '').strip()
    artist = str(artist or '').strip()
    if not title:
        info = media_now()
        if info:
            title = str(info.get('title') or '').strip()
            artist = artist or str(info.get('artist') or '').strip()
    if not title:
        return '要先知道歌名才行哦（可以先把歌放起来，或者直接告诉本鲸歌名）。'
    local = find_local_lyrics(title, artist)
    if local:
        return f'《{title}》的歌词（本地 .lrc）：\n' + local[:3000]
    online = online_lyrics(title, artist)
    if online:
        return f'《{title}》的歌词（网上找的，可能不全）：\n' + online
    return f'本鲸没找到《{title}》的歌词……'
AUDIO_EXT = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.opus', '.ape'}
VIDEO_EXT = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.ts', '.rmvb', '.mpg', '.mpeg'}
FFMPEG_URL = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
def _tool_dirs():
    """放 ffmpeg 这类工具的目录（优先程序目录，不可写再退到 %LOCALAPPDATA%）。"""
    dirs = [os.path.join(data_dir(), 'tools')]
    la = os.environ.get('LOCALAPPDATA')
    if la:
        dirs.append(os.path.join(la, APP_NAME, 'tools'))
    return dirs
def _find_exe_in_path(name):
    for d in (os.environ.get('PATH') or '').split(os.pathsep):
        try:
            p = os.path.join(d, name)
        except Exception:
            continue
        if os.path.isfile(p):
            return p
    return None
def ffmpeg_exe():
    """定位 ffmpeg.exe：配置 > 程序目录 > tools 目录 > PATH；找不到返回 None。"""
    try:
        cfg = load_config()
    except Exception:
        cfg = {}
    cands = [str(cfg.get('ffmpeg_path') or '').strip(), res_path('ffmpeg.exe'), os.path.join(data_dir(), 'ffmpeg.exe')]
    cands += [os.path.join(d, 'ffmpeg.exe') for d in _tool_dirs()]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return _find_exe_in_path('ffmpeg.exe')
def ensure_ffmpeg():
    """没有 ffmpeg 就自动下载一份到工具目录，返回可用的 ffmpeg.exe 路径（失败返回 None）。"""
    p = ffmpeg_exe()
    if p:
        return p
    for d in _tool_dirs():
        zp = os.path.join(d, 'ffmpeg.zip')
        try:
            os.makedirs(d, exist_ok=True)
            req = urllib.request.Request(FFMPEG_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=180) as r, open(zp, 'wb') as f:
                shutil.copyfileobj(r, f, 1024 * 256)
            out = os.path.join(d, 'ffmpeg.exe')
            with zipfile.ZipFile(zp) as z:
                member = next((n for n in z.namelist() if n.lower().endswith('ffmpeg.exe')), None)
                if not member:
                    raise OSError('压缩包里没有 ffmpeg.exe')
                with z.open(member) as src, open(out, 'wb') as dst:
                    shutil.copyfileobj(src, dst)
            try:
                os.remove(zp)
            except OSError:
                pass
            if os.path.isfile(out):
                return out
        except Exception:
            try:
                os.remove(zp)
            except OSError:
                pass
            continue
    return None
def _ffmpeg_run(args, timeout=180):
    exe = ffmpeg_exe()
    if not exe:
        return False
    try:
        p = subprocess.run([exe, '-y', '-hide_banner', '-loglevel', 'error'] + list(args), capture_output=True, timeout=timeout, creationflags=_NO_WINDOW)
        return p.returncode == 0
    except Exception:
        return False
def extract_frames(path, count=6, seconds_each=10, max_side=768):
    """每 seconds_each 秒抽一帧、最多 count 张，返回临时图片路径列表。"""
    if not ffmpeg_exe():
        return []
    tmp = tempfile.mkdtemp(prefix='whale_frames_')
    pat = os.path.join(tmp, 'f%03d.jpg')
    args = ['-i', path, '-vf', f'fps=1/{max(1, int(seconds_each))},scale={int(max_side)}:-2', '-frames:v', str(max(1, int(count))), '-q:v', '4', pat]
    if not _ffmpeg_run(args):
        return []
    return sorted(glob.glob(os.path.join(tmp, 'f*.jpg')))
def extract_audio(path, seconds=60, fmt='mp3'):
    """抽一段音频（默认前 seconds 秒）到临时文件，返回路径或 None。"""
    if not ffmpeg_exe():
        return None
    tmp = tempfile.mkdtemp(prefix='whale_audio_')
    out = os.path.join(tmp, 'a.' + fmt)
    args = ['-i', path, '-t', str(max(1, int(seconds))), '-vn']
    if fmt == 'mp3':
        args += ['-ac', '1', '-ar', '44100', '-b:a', '96k']
    else:
        args += ['-ac', '1', '-ar', '16000']
    if not _ffmpeg_run(args + [out]):
        return None
    return out if os.path.isfile(out) else None
def _jpg_data_url(path, max_side=768, quality=70):
    try:
        im = Image.open(path).convert('RGB')
        im.thumbnail((max_side, max_side), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=quality)
        return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None
def video_report(path, count=6):
    """总结视频：抽关键帧交给能看图的模型。"""
    path = str(path or '').strip().strip('"')
    if not path or not os.path.isfile(path):
        return '本鲸要一个视频文件的完整路径才行（可以把视频拖进聊天框，再让本鲸总结它）。'
    if not ensure_ffmpeg():
        return '本鲸还没拿到 ffmpeg（抽帧要用它），自动下载也没成功。主人可以手动放一个 ffmpeg.exe 到程序目录，或在 config.json 的 ffmpeg_path 里填路径。'
    cfg = load_config()
    name = os.path.basename(path)
    if not cfg.get('vision', True):
        return f'《{name}》：设置里关掉了「看图」，本鲸没法总结画面内容。'
    frames = extract_frames(path, count)
    if not frames:
        return f'本鲸没能从《{name}》里抽出画面……（可能是格式不支持，或文件损坏）'
    urls = [u for u in (_jpg_data_url(f) for f in frames) if u]
    if not urls:
        return '本鲸抽到了画面，但读取失败了……'
    body = [{'type': 'text', 'text': f'这是从视频《{name}》里按时间顺序抽出的 {len(urls)} 帧画面，请用中文简要总结这个视频讲了什么（场景、人物、可能的情节或主题），两三句话，别编。'}]
    body += [{'type': 'image_url', 'image_url': {'url': u}} for u in urls]
    try:
        text = _api_once(cfg, [{'role': 'user', 'content': body}], temperature=0.4, max_tokens=400, timeout=120)
    except Exception as e:
        return f'本鲸看画面失败了……（{e}）'
    return f'《{name}》的画面总结：\n{text}' if text else '本鲸看了画面，但没总结出什么。'
def _acr_sign(secret, method, uri, key, dtype, ver, ts):
    s = '\n'.join([method, uri, key, dtype, ver, ts])
    return base64.b64encode(hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha1).digest()).decode()
def identify_music(path):
    """听歌识曲（ACRCloud）：从音频 / 视频里抽一小段去识别。"""
    cfg = load_config()
    host = str(cfg.get('acr_host') or '').strip()
    key = str(cfg.get('acr_access_key') or '').strip()
    sec = str(cfg.get('acr_access_secret') or '').strip()
    if not (host and key and sec):
        return '还没配听歌识曲（ACRCloud）的 host / access_key / access_secret，在 config.json 里填上就能用了。'
    path = str(path or '').strip().strip('"')
    if not path or not os.path.isfile(path):
        return '本鲸要一个音频或视频文件的完整路径才能识曲（可以把文件拖进聊天框）。'
    if not ensure_ffmpeg():
        return '识曲要先从文件里抽一小段音频，需要 ffmpeg（本鲸还没拿到）。'
    sample = extract_audio(path, 12, 'wav')
    if not sample:
        return '本鲸没能从文件里抽出音频……'
    try:
        with open(sample, 'rb') as f:
            data = f.read()
        ts = str(int(time.time()))
        uri = '/v1/identify'
        dtype = 'audio'
        ver = '1.0'
        sig = _acr_sign(sec, 'POST', uri, key, dtype, ver, ts)
        boundary = '----whale' + ts
        fields = [('access_key', key), ('data_type', dtype), ('signature_version', ver), ('signature', sig), ('sample_bytes', str(len(data))), ('timestamp', ts)]
        body = b''
        for k, v in fields:
            body += f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode('utf-8')
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="sample"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode('utf-8') + data + f'\r\n--{boundary}--\r\n'.encode('utf-8')
        req = urllib.request.Request(f'https://identify-{host}/v1/identify', data=body, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
        with urllib.request.urlopen(req, timeout=30) as r:
            obj = json.loads(r.read().decode('utf-8', 'ignore'))
    except Exception as e:
        return f'识曲失败了……（{e}）'
    st = obj.get('status') or {}
    try:
        code = int(st.get('code', 1))
    except (TypeError, ValueError):
        code = 1
    if code != 0:
        return '本鲸没听出来这是什么歌（' + str(st.get('msg') or '识别失败') + '）。'
    music = ((obj.get('metadata') or {}).get('music') or [])
    if not music:
        return '本鲸没听出来这是什么歌……'
    m = music[0]
    title = str(m.get('title') or '未知')
    artists = '、'.join((a.get('name') or '' for a in (m.get('artists') or []))) or ''
    album = ((m.get('album') or {}).get('name')) or ''
    out = f'听出来了：《{title}》'
    if artists:
        out += f'，歌手：{artists}'
    if album:
        out += f'，专辑：{album}'
    return out + '。'
def transcribe_media(path, seconds=600):
    """音频转文字（OpenAI 兼容 /audio/transcriptions）：先抽音频再上传。"""
    cfg = load_config()
    base = str(cfg.get('stt_base') or cfg.get('api_base') or '').strip().rstrip('/')
    key = str(cfg.get('stt_key') or cfg.get('api_key') or '').strip()
    model = str(cfg.get('stt_model') or 'whisper-1').strip()
    if not (base and key):
        return '还没配转写用的 API（config.json 里的 stt_base / stt_key），填上支持 /audio/transcriptions 的服务就能用了。'
    path = str(path or '').strip().strip('"')
    if not path or not os.path.isfile(path):
        return '本鲸要一个音频或视频文件的完整路径才能转写（可以把文件拖进聊天框）。'
    if not ensure_ffmpeg():
        return '转写前要从文件里抽音频，需要 ffmpeg（本鲸还没拿到）。'
    audio = extract_audio(path, seconds, 'mp3')
    if not audio:
        return '本鲸没能从文件里抽出音频……'
    try:
        with open(audio, 'rb') as f:
            data = f.read()
        boundary = '----whale' + str(int(time.time()))
        body = f'--{boundary}\r\nContent-Disposition: form-data; name="model"\r\n\r\n{model}\r\n'.encode('utf-8')
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode('utf-8') + data + f'\r\n--{boundary}--\r\n'.encode('utf-8')
        req = urllib.request.Request(base + '/audio/transcriptions', data=body, headers={'Authorization': 'Bearer ' + key, 'Content-Type': f'multipart/form-data; boundary={boundary}'})
        with urllib.request.urlopen(req, timeout=300) as r:
            obj = json.loads(r.read().decode('utf-8', 'ignore'))
    except Exception as e:
        return f'转写失败了……（{e}）'
    text = str(obj.get('text') or '').strip()
    if not text:
        return '转写完了，但没听到什么内容。'
    return '转写结果：\n' + text[:3000]
def calc_expr(expr):
    """算一个算式（只认数字和 + - * / // % ** 括号，安全求值）。"""
    src = str(expr or '').strip().replace('×', '*').replace('÷', '/').replace('（', '(').replace('）', ')').replace('，', ',')
    if not src:
        return '要算什么呢？'
    else:
        try:
            tree = ast.parse(src, mode='eval')
        except SyntaxError:
            return f'「{src}」本鲸算不出来……'
        def ev(node):
            if isinstance(node, ast.Expression):
                return ev(node.body)
            else:
                if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and (not isinstance(node.value, bool)):
                    return node.value
                else:
                    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                        v = ev(node.operand)
                        return v if isinstance(node.op, ast.UAdd) else -v
                    else:
                        if isinstance(node, ast.BinOp):
                            a, b = (ev(node.left), ev(node.right))
                            op = node.op
                            if isinstance(op, ast.Pow) and abs(b) > 64:
                                raise ValueError('指数太大，本鲸算不动')
                            else:
                                table = {ast.Add: lambda: a + b, ast.Sub: lambda: a - b, ast.Mult: lambda: a / b, ast.FloorDiv: lambda: a % b, ast.Mod: lambda: a % b, ast.Pow: lambda: a ** b}
                                for cls, fn in table.items():
                                    if isinstance(op, cls):
                                        return fn()
                        raise ValueError('只认数字和 + - * / // % ** 和括号')
        try:
            val = ev(tree)
        except Exception as e:
            return f'算不出来……（{e}）'
        if isinstance(val, float):
            txt = f'{val:.6f}'.rstrip('0').rstrip('.')
        else:
            txt = str(val)
        return f'{src} = {txt}'
def read_text_file(path, limit=3000):
    p = abs_path(path)
    if not p or not os.path.isfile(p):
        return f'找不到文件「{str(path).strip()}」。'
    else:
        try:
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                body = f.read(limit + 1)
        except OSError as e:
            return f'读不了……（{e}）'
        more = '…（后面还有，本鲸只念了前面一段）' if len(body) > limit else ''
        return f'{os.path.basename(p)} 里是这样：\n{body[:limit]}{more}'
def write_text_file(spec):
    """[WRITE: 路径\\r内容]：第一行是路径，剩下的都是要写进去的内容。"""
    lines = str(spec or '').split('\n', 1)
    path = abs_path(lines[0])
    body = lines[1] if len(lines) > 1 else ''
    if not path:
        return '要写到哪个文件呀？'
    else:
        try:
            folder = os.path.dirname(path)
            if folder:
                os.makedirs(folder, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(body)
        except OSError as e:
            return f'写不进去……（{e}）'
        return f'写好啦：{os.path.basename(path)}（{len(body)} 个字）'
_PARAM_WORDS = ('all', 'end', 'loop', 'quiet', 'r', 'n', 'ra', 'na', 'rl', 'nl')
_RE_CMD = re.compile('\\[\\s*([A-Za-z]{2,8})\\s*:\\s*(.*?)\\]')
_RE_TAIL = re.compile('\\\\([A-Za-z]+)(\\d*)$')
_RE_BARE_BREAK = re.compile('\\\\([rn])(?!\\d)', re.I)
def split_command_params(body):
    """把命令内容末尾那一串参数抠出来 → (正文, 参数)。"""
    params = {'skip': 0, 'above': 0, 'below': 0, 'goto': 0, 'all': False, 'end': False, 'loop': False, 'quiet': False}
    while True:
        m = _RE_TAIL.search(body)
        if not m:
            return (body, params)
        word = m.group(1).lower()
        if word not in _PARAM_WORDS:
            return (body, params)
        n = int(m.group(2)) if m.group(2) else 0
        if word in ('r', 'n') and (not n):
            return (body, params)
        body = body[:m.start()]
        if word == 'all':
            params['all'] = True
        elif word == 'end':
            params['end'] = True
        elif word == 'loop':
            params['loop'] = True
        elif word == 'quiet':
            params['quiet'] = True
        elif word == 'r' or word == 'n':
            params['skip'] = n
        elif word == 'ra':
            params['above'] = n or 1
        elif word == 'na':
            params['below'] = n or 1
        else:
            params['goto'] = n or 1
def _split_bare_breaks(raw):
    """把方括号外面单独出现的 \\r / \\n 当换行拆开（一行里能写多条命令）。"""
    out, buf, depth, i = ([], '', 0, 0)
    while i < len(raw):
        ch = raw[i]
        if ch == '[':
            depth += 1
        elif ch == ']' and depth:
            depth -= 1
        if ch == '\\' and depth == 0 and (i + 1 < len(raw)) and (raw[i + 1] in 'rn') and (i + 2 >= len(raw) or not raw[i + 2].isdigit()):
            out.append(buf)
            buf = ''
            i += 2
            continue
        buf += ch
        i += 1
    out.append(buf)
    return out
def _make_cmd(prefix, body, params, line_no):
    return {'prefix': prefix, 'content': _RE_BARE_BREAK.sub('\n', body).strip(), 'params': params, 'line': line_no}
def scan_commands(text):
    """把一段文本里的快捷命令扫出来 → (命令列表, 剩下的普通文本)。"""
    lines = []
    for raw in str(text or '').split('\n'):
        lines.extend(_split_bare_breaks(raw))
    found, plain_at, consumed = ([], {}, set())
    all_mode, visits, i, budget = (False, {}, 0, 200)
    while i < len(lines) and budget > 0:
        budget -= 1
        visits[i] = visits.get(i, 0) + 1
        if visits[i] > 10:
            i += 1
            continue
        if i in consumed:
            i += 1
            continue
        line = lines[i]
        hits = [(m.start(), m.end(), m.group(1).upper(), m.group(2)) for m in _RE_CMD.finditer(line) if m.group(1).upper() in COMMAND_PREFIXES]
        here, nav = ([], None)
        rest = line
        for k, (s, e, prefix, body) in enumerate(hits):
            clean, params = split_command_params(body)
            cmd = _make_cmd(prefix, clean, params, i)
            if k == 0:
                if params['above']:
                    lo = max(0, i - params['above'])
                    extra = [x for x in lines[lo:i] if x.strip()]
                    if extra:
                        cmd['content'] = '\n'.join(extra + [cmd['content']])
                    consumed.update(range(lo, i))
                if params['below']:
                    hi = i + 1 + params['below']
                    extra = [x for x in lines[i + 1:hi] if x.strip()]
                    if extra:
                        cmd['content'] = '\n'.join([cmd['content']] + extra)
                    consumed.update(range(i + 1, min(hi, len(lines))))
                nav = params
            here.append(cmd)
        if hits:
            rest = line
            for s, e, _p, _b in reversed(hits):
                rest = rest[:s] + rest[e:]
            rest = rest.strip()
        else:
            if all_mode and line.strip():
                params = split_command_params('')[1]
                here.append(_make_cmd('CMD', line.strip(), params, i))
                nav = params
                rest = ''
        if not here:
            if rest.strip():
                plain_at[i] = rest.strip()
            i += 1
            continue
        found.extend(here)
        if rest:
            plain_at[i] = rest
        if nav is None:
            i += 1
            continue
        if nav['all']:
            all_mode = True
        if nav['end']:
            break
        if nav['loop']:
            continue
        if nav['goto']:
            i = max(0, min(len(lines) - 1, nav['goto'] - 1))
            continue
        i += 1 + nav['skip']
    return (found, [t for n, t in sorted(plain_at.items()) if n not in consumed])
def parse_brain(text):
    """从模型回复里抠出那个 JSON。抠不出来返回 None。"""
    m = re.search('\\{.*\\}', str(text or ''), re.S)
    if not m:
        return
    else:
        try:
            obj = json.loads(m.group(0))
        except ValueError:
            return None
        return obj if isinstance(obj, dict) else None
def harden(im):
    """把半透明像素二值化。\n\nTk 的 -transparentcolor 是把图像和色键混合后再判断透明的，\n边缘那圈半透明像素会跟近乎纯黑的色键混出一圈黑边；直接去掉半透明就好了。\n"""
    r, g, b, a = im.split()
    return Image.merge('RGBA', (r, g, b, a.point(lambda v: 255 if v >= 128 else 0)))
def eye_boxes(size):
    """按实际图片尺寸等比缩放眼睛坐标。"""
    w, h = size
    rw, rh = EYE_REF
    sx, sy = (w / rw, h / rh)
    return [(int(a * sx), int(b * sy), int(c * sx), int(d * sy)) for a, b, c, d in EYE_BOXES]
def close_eyes(im, boxes):
    """把正面立绘的眼睛画成闭眼（眨眼 / 睡觉用）。\n\n先用洪水填充圈出「眼睛 + 睫毛」这块非皮肤区域（紧贴眼睛轮廓，不会啃到刘海），\n再用扩散补面（反复「模糊 → 把洞外的原始像素贴回」）让周围肤色慢慢渗进洞里，\n过渡天生没有接缝，不会留下方块轮廓或像黑眼圈那样的边界；最后画上闭眼线和睫毛。\n"""
    out = im.copy()
    W, H = im.size
    px = im.load()
    face_cx = (boxes[0][0] + boxes[(-1)][2]) / 2 if len(boxes) > 1 else W / 2
    def is_skin(c):
        """暖色且够亮 = 皮肤。"""
        r, g, b = c[:3]
        return r > b + 6 and min(r, g, b) > 120
    for x0, y0, x1, y1 in boxes:
        h = y1 - y0
        outer_left = (x0 + x1) / 2 < face_cx
        bx0, by0 = (max(0, x0 - 3), max(0, y0 - 3))
        bx1, by1 = (min(W - 1, x1 + 3), min(H - 1, y1 + 3))
        cand = [[False] * (bx1 - bx0 + 1) for _ in range(by1 - by0 + 1)]
        cxm, cym = ((x0 + x1) // 2, (y0 + y1) // 2)
        erx, ery = ((x1 - x0) / 2 + 3, (y1 - y0) / 2 + 3)
        for y in range(by0, by1 + 1):
            row = cand[y - by0]
            for x in range(bx0, bx1 + 1):
                if ((x - cxm) / erx) ** 2 + ((y - cym) / ery) ** 2 > 1.0:
                    continue
                else:
                    row[x - bx0] = not is_skin(px[x, y])
        seeds = [(cxm, cym), (cxm - h // 4, cym), (cxm + h // 4, cym), (cxm, cym - h // 5), (cxm, cym + h // 5)]
        seen = set()
        stack = [s for s in seeds if cand[s[1] - by0][s[0] - bx0]]
        seen.update(stack)
        while stack:
            cx, cy = stack.pop()
            for nx, ny in [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
                if bx0 <= nx <= bx1 and (nx, ny) not in seen and cand[ny - by0][nx - bx0]:
                    seen.add((nx, ny))
                    stack.append((nx, ny))
        hole = Image.new('L', (W, H), 0)
        hp = hole.load()
        for ex, ey in seen:
            hp[ex, ey] = 255
        for _ in range(4):
            add = []
            for y in range(by0, by1 + 1):
                for x in range(bx0, bx1 + 1):
                    if hp[x, y] or not is_skin(px[x, y]):
                        continue
                    else:
                        near = x + 1 < W and hp[x + 1, y] or (x > 0 and hp[x - 1, y]) or (y + 1 < H and hp[x, y + 1]) or (y > 0 and hp[x, y - 1])
                        if near:
                            add.append((x, y))
            if not add:
                break
            else:
                for x, y in add:
                    hp[x, y] = 255
        ys = [y for _, y in seen]
        xs = [x for x, _ in seen]
        ty0, ty1, tx0, tx1 = (min(ys), max(ys), min(xs), max(xs))
        def band_color(y0_, y1_):
            cs = [px[x, y][:3] for y in range(y0_, y1_ + 1) for x in range(tx0, tx1 + 1) if is_skin(px[x, y])]
            if not cs:
                return
            else:
                cs.sort(key=sum, reverse=True)
                top = cs[:max(1, len(cs) // 2)]
                return tuple(sum(c[i] for c in top) // len(top) for i in range(3))
        top_c = band_color(max(0, ty0 - 15), max(1, ty0 - 3))
        bot_c = band_color(min(H - 1, ty1 + 3), min(H, ty1 + 15))
        if top_c is None:
            top_c = bot_c or (250, 226, 214)
        if bot_c is None:
            bot_c = top_c
        span = max(1, ty1 - ty0)
        patch = Image.new('RGBA', (W, H))
        pd = ImageDraw.Draw(patch)
        for y in range(by0, by1 + 1):
            t = min(1.0, max(0.0, (y - ty0) / span))
            c = tuple((int(top_c[i] + (bot_c[i] - top_c[i]) * t) for i in range(3)))
            pd.line((0, y, W - 1, y), fill=c + (255,))
        soft = hole.filter(ImageFilter.GaussianBlur(2.0))
        out.paste(patch, (0, 0), soft)
        d = ImageDraw.Draw(out)
        darks = [px[x, y][:3] for x in range(x0, x1) for y in range(y0, y0 + 12) if max(px[x, y][:3]) < 110]
        if darks:
            lash = tuple(sum(c[i] for c in darks) // len(darks) for i in range(3))
        stroke = max(4.0, h * 0.12)
        ly = y0 + h * 0.62
        arch = h * 0.085
        droop = arch * 0.75
        def line_y(o):
            """o：0 = 外眼角，1 = 内眼角 → 闭眼线的 y。"""
            return ly - arch * math.sin(math.pi * o ** 0.8) + droop * (1 - o) ** 3
        outx = (-1) if outer_left else 1
        n = 48
        for i in range(n + 1):
            t = i / n
            o = t if outer_left else 1 - t
            x = x0 + 3 + (x1 - x0 - 6) * t
            y = line_y(o)
            r = stroke * 0.5 * (0.4 + 1.0 * (1 - o) ** 0.7)
            d.ellipse((x - r, y - r, x + r, y + r), fill=lash + (255,))
        for k in range(3):
            o = 0.04 + 0.13 * k
            t = o if outer_left else 1 - o
            bx = x0 + 3 + (x1 - x0 - 6) * t
            by = line_y(o)
            ex = bx + outx * h * (0.15 + 0.05 * k)
            ey = by + h * (0.02 + 0.06 * k)
            d.line((bx, by, ex, ey), fill=lash + (255,), width=max(2, int(stroke * 0.5)), joint='curve')
            r = max(1.0, stroke * 0.26)
            d.ellipse((ex - r, ey - r, ex + r, ey + r), fill=lash + (255,))
        ex0 = x0 + 3 if outer_left else x1 - 3
        ey0 = line_y(0.0)
        d.line((ex0, ey0 - stroke * 0.15, ex0 + outx * h * 0.08, ey0 + h * 0.07), fill=lash + (255,), width=max(2, int(stroke * 0.55)), joint='curve')
    return out
_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32
class _LASTINPUTINFO(ctypes.Structure):
    _fields_ = [('cbSize', wintypes.UINT), ('dwTime', wintypes.DWORD)]
class _MEMSTATUS(ctypes.Structure):
    _fields_ = [('dwLength', wintypes.DWORD), ('dwMemoryLoad', wintypes.DWORD), ('ullTotalPhys', ctypes.c_ulonglong), ('ullAvailPhys', ctypes.c_ulonglong), ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong), ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong), ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
def idle_seconds():
    """系统空闲秒数（键盘、鼠标都算）。"""
    info = _LASTINPUTINFO()
    info.cbSize = ctypes.sizeof(info)
    if not _user32.GetLastInputInfo(ctypes.byref(info)):
        return 0.0
    else:
        return max(0.0, (_kernel32.GetTickCount() - info.dwTime) / 1000.0)
def active_window():
    """返回当前前台窗口的 (标题, 进程名)。"""
    hwnd = _user32.GetForegroundWindow()
    if not hwnd:
        return ('', '')
    else:
        n = _user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(n + 1)
        _user32.GetWindowTextW(hwnd, buf, n + 1)
        pid = wintypes.DWORD()
        _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        exe = ''
        h = _kernel32.OpenProcess(4096, False, pid)
        if h:
            size = wintypes.DWORD(260)
            path = ctypes.create_unicode_buffer(260)
            if _kernel32.QueryFullProcessImageNameW(h, 0, path, ctypes.byref(size)):
                exe = os.path.basename(path.value)
            _kernel32.CloseHandle(h)
        return (buf.value, exe)
_WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
def list_windows():
    """列出可见的顶层窗口：(句柄, 标题, 程序名)。"""
    out = []
    def _cb(hwnd, _l):
        try:
            if not _user32.IsWindowVisible(hwnd):
                return True
            n = _user32.GetWindowTextLengthW(hwnd)
            if n <= 0:
                return True
            buf = ctypes.create_unicode_buffer(n + 1)
            _user32.GetWindowTextW(hwnd, buf, n + 1)
            pid = wintypes.DWORD()
            _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            exe = ''
            h = _kernel32.OpenProcess(4096, False, pid)
            if h:
                size = wintypes.DWORD(260)
                path = ctypes.create_unicode_buffer(260)
                if _kernel32.QueryFullProcessImageNameW(h, 0, path, ctypes.byref(size)):
                    exe = os.path.basename(path.value)
                _kernel32.CloseHandle(h)
            out.append((hwnd, buf.value, exe))
        except Exception:
            pass
        return True
    try:
        cb = _WNDENUMPROC(_cb)
        _user32.EnumWindows(cb, 0)
    except Exception:
        pass
    return out
def find_window(key):
    """按标题或程序名找窗口（跳过桌宠自己）：返回 (句柄, 标题, 程序名) 或 None。"""
    key = str(key or '').strip().lower()
    cands = []
    for hwnd, title, exe in list_windows():
        if title == APP_NAME:
            continue
        tl, el = title.lower(), exe.lower()
        if (not key) or (key in tl) or (key in el):
            cands.append((hwnd, title, exe))
    if not cands:
        return None
    cands.sort(key=lambda c: len(c[1]))
    return cands[0]
def _grab_window(hwnd):
    """抓某个窗口的画面：先试 PrintWindow（被遮挡也能抓），失败就按位置截屏。"""
    try:
        gdi32 = ctypes.windll.gdi32
        rect = wintypes.RECT()
        if not _user32.GetClientRect(hwnd, ctypes.byref(rect)):
            return None
        w, h = rect.right - rect.left, rect.bottom - rect.top
        if w >= 16 and h >= 16:
            hdc = _user32.GetDC(hwnd)
            memdc = gdi32.CreateCompatibleDC(hdc)
            bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
            gdi32.SelectObject(memdc, bmp)
            ok = _user32.PrintWindow(hwnd, memdc, 2)
            class _BMIH(ctypes.Structure):
                _fields_ = [('biSize', wintypes.DWORD), ('biWidth', ctypes.c_long), ('biHeight', ctypes.c_long), ('biPlanes', wintypes.WORD), ('biBitCount', wintypes.WORD), ('biCompression', wintypes.DWORD), ('biSizeImage', wintypes.DWORD), ('biXPelsPerMeter', ctypes.c_long), ('biYPelsPerMeter', ctypes.c_long), ('biClrUsed', wintypes.DWORD), ('biClrImportant', wintypes.DWORD)]
            bi = _BMIH()
            bi.biSize = ctypes.sizeof(_BMIH)
            bi.biWidth = w
            bi.biHeight = -h
            bi.biPlanes = 1
            bi.biBitCount = 32
            buf = ctypes.create_string_buffer(w * h * 4)
            gdi32.GetDIBits(memdc, bmp, 0, h, buf, ctypes.byref(bi), 0)
            gdi32.DeleteObject(bmp)
            gdi32.DeleteDC(memdc)
            _user32.ReleaseDC(hwnd, hdc)
            if ok:
                im = Image.frombuffer('RGBA', (w, h), buf, 'raw', 'BGRA', 0, 1).convert('RGB')
                if im.getbbox():
                    return im
    except Exception:
        pass
    try:
        rect = wintypes.RECT()
        if _user32.GetWindowRect(hwnd, ctypes.byref(rect)) and rect.right - rect.left >= 16 and rect.bottom - rect.top >= 16:
            return ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom))
    except Exception:
        pass
    return None
def look_window_report(cfg, name=''):
    """看某个窗口的画面（AI 读指定应用）。"""
    if not cfg.get('vision', True):
        return '设置里关掉了「看图」，本鲸没法看窗口。'
    found = find_window(name)
    if not found:
        return f'本鲸没找到「{name or "当前窗口"}」这个窗口呀（可以先看一眼 current_window 的标题）。'
    hwnd, title, exe = found
    im = _grab_window(hwnd)
    if im is None:
        return f'本鲸抓不到「{title}」的画面……'
    url = screen_data_url(im, 1280, 72)
    body = [{'type': 'text', 'text': f'这是「{title}」（程序 {exe}）这个窗口当前的画面，请用中文说说里面是什么内容、主人可能在做什麼，两三句话，别编。'}, {'type': 'image_url', 'image_url': {'url': url}}]
    try:
        text = _api_once(cfg, [{'role': 'user', 'content': body}], temperature=0.4, max_tokens=400, timeout=120)
    except Exception as e:
        return f'本鲸看窗口失败了……（{e}）'
    return text or '本鲸看了半天，没看出什么。'
def look_screen_report(cfg, seconds=3):
    """录一小段屏（连续几帧）交给能看图的模型，描述动态画面。"""
    if not cfg.get('vision', True):
        return '设置里关掉了「看图」，本鲸没法看屏幕。'
    try:
        seconds = max(1, min(8, int(float(seconds or 3))))
    except (TypeError, ValueError):
        seconds = 3
    n = max(2, min(8, seconds * 2))
    frames = []
    for i in range(n):
        try:
            frames.append(ImageGrab.grab())
        except Exception:
            break
        if i < n - 1:
            time.sleep(max(0.2, seconds / n))
    if not frames:
        return '本鲸截不到屏幕……'
    urls = [screen_data_url(im, 1024, 68) for im in frames]
    body = [{'type': 'text', 'text': f'这是主人屏幕最近约 {seconds} 秒里按时间顺序抓的 {len(urls)} 帧画面，请用中文说说画面里在发生什么、主人可能在忙什么（有变化也说一下），两三句话，别编。'}]
    body += [{'type': 'image_url', 'image_url': {'url': u}} for u in urls]
    try:
        text = _api_once(cfg, [{'role': 'user', 'content': body}], temperature=0.4, max_tokens=400, timeout=120)
    except Exception as e:
        return f'本鲸看屏幕失败了……（{e}）'
    return text or '本鲸看了半天，没看出什么。'
UPDATE_USER_AGENT = 'WhalePet/' + APP_VERSION
def _ver_tuple(s):
    nums = re.findall('\\d+', str(s or ''))
    return tuple((int(n) for n in nums[:4])) or ((0,))
def _ver_gt(a, b):
    ta, tb = _ver_tuple(a), _ver_tuple(b)
    n = max(len(ta), len(tb))
    ta = ta + (0,) * (n - len(ta))
    tb = tb + (0,) * (n - len(tb))
    return ta > tb
def _extract_sha(text):
    m = re.search('(?i)sha[-_ ]?256[^0-9a-f]{0,12}([0-9a-f]{64})', str(text or ''))
    return m.group(1).lower() if m else ''
UPDATE_CHANNELS = [('release', 'Release 正式版'), ('beta', 'Beta 测试版'), ('preview', 'Preview 预览版')]
def _release_sources():
    """按顺序返回可用的更新源：(名称, Release 列表 API)。"""
    cfg = load_config()
    out = []
    gh = str(cfg.get('update_repo_github') or '').strip().strip('/')
    gi = str(cfg.get('update_repo_gitee') or '').strip().strip('/')
    if gh:
        out.append(('GitHub', f'https://api.github.com/repos/{gh}/releases?per_page=30'))
    if gi:
        out.append(('Gitee', f'https://gitee.com/api/v5/repos/{gi}/releases?per_page=30'))
    return out
def _pick_asset(assets):
    """挑主程序附件：优先精确同名，其次任意 exe，绝不挑安装器 / setup。"""
    if not assets:
        return None
    def _is_installer(a):
        n = str(a.get('name') or '').lower()
        return ('安装' in n) or ('install' in n) or ('setup' in n)
    for a in assets:
        if str(a.get('name') or '').strip() == APP_NAME + '.exe':
            return a
    for a in assets:
        if str(a.get('name') or '').lower().endswith('.exe') and (not _is_installer(a)):
            return a
    return None
def _tag_channel(tag, prerelease=False):
    """这条 Release 属于哪个通道。"""
    t = str(tag or '').lower()
    if ('preview' in t) or ('alpha' in t) or ('rc' in t.replace('-', '').replace('.', '')):
        return 'preview'
    if 'beta' in t:
        return 'beta'
    return 'preview' if prerelease else 'release'
def _channel_accepts(channel, kind):
    """越激进接受得越多：preview 全收、beta 收 beta+正式、release 只收正式。"""
    if channel == 'preview':
        return True
    if channel == 'beta':
        return kind in ('release', 'beta')
    return kind == 'release'
def _pick_release(items, channel):
    """从 Release 列表里挑出该通道中版本号最高的一条。"""
    best, best_ver = (None, '')
    for it in items or []:
        if not isinstance(it, dict):
            continue
        tag = str(it.get('tag_name') or it.get('name') or '').strip()
        if not tag:
            continue
        if not _channel_accepts(channel, _tag_channel(tag, it.get('prerelease'))):
            continue
        ver = tag.lstrip('vV')
        if best is None or _ver_gt(ver, best_ver):
            best, best_ver = (it, ver)
    return best
def fetch_update_info(timeout=12):
    """按选定的通道，依次问 GitHub / Gitee 的 Release 列表（一个失败自动换另一个）。"""
    cfg = load_config()
    channel = str(cfg.get('update_channel') or 'release').lower()
    if channel not in ('release', 'beta', 'preview'):
        channel = 'release'
    last_err = ''
    for source, api in _release_sources():
        try:
            req = urllib.request.Request(api, headers={'User-Agent': UPDATE_USER_AGENT, 'Accept': 'application/json'})
            with _urlopen_any(req, timeout=timeout) as r:
                obj = json.loads(r.read().decode('utf-8', 'ignore'))
        except Exception as e:
            last_err = f'{source}：{e}'
            continue
        items = obj if isinstance(obj, list) else (obj.get('releases') if isinstance(obj, dict) else None) or []
        rel = _pick_release(items, channel)
        if not rel:
            last_err = f'{source}：{dict(UPDATE_CHANNELS).get(channel, channel)} 还没有发布过版本'
            continue
        tag = str(rel.get('tag_name') or rel.get('name') or '').strip()
        asset = _pick_asset(rel.get('assets') or []) or {}
        url = str(asset.get('browser_download_url') or '').strip()
        if not url:
            last_err = f'{source}：这条 Release 没挂主程序附件'
            continue
        body = str(rel.get('body') or '')
        return {'ok': True, 'source': source, 'channel': channel, 'version': tag.lstrip('vV'), 'tag': tag, 'url': url, 'asset': str(asset.get('name') or ''), 'sha256': _extract_sha(body), 'notes': body[:600], 'err': ''}
    return {'ok': False, 'err': last_err or '还没配更新仓库（应用设置 → 更新 里填 GitHub / Gitee 的 owner/repo）'}
def download_file(url, path, sha256='', timeout=60):
    """下载到 path；给了 sha256 就校验。返回 (ok, 错误信息)。"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UPDATE_USER_AGENT})
        with _urlopen_any(req, timeout=timeout) as r, open(path, 'wb') as f:
            shutil.copyfileobj(r, f, 1024 * 256)
    except Exception as e:
        return (False, f'下载失败：{e}')
    if sha256:
        try:
            h = hashlib.sha256()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(1024 * 256), b''):
                    h.update(chunk)
        except OSError as e:
            return (False, f'校验失败：{e}')
        if h.hexdigest().lower() != sha256.lower():
            return (False, 'sha256 对不上，本鲸不敢装。')
    return (True, '')
def is_fullscreen():
    """前台窗口是不是铺满整屏（游戏 / 全屏视频）。"""
    hwnd = _user32.GetForegroundWindow()
    if not hwnd:
        return False
    else:
        rect = wintypes.RECT()
        if not _user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return False
        else:
            return rect.right - rect.left >= _user32.GetSystemMetrics(0) and rect.bottom - rect.top >= _user32.GetSystemMetrics(1)
APP_HINTS = [(('code.exe', 'cursor', 'pycharm', 'idea64', 'devenv', 'sublime_text', 'notepad++', 'windowsterminal', 'powershell', 'cmd.exe'), ['主人又在敲代码呀～', '写代码辛苦啦，本鲸在旁边陪着你。', '这段 bug 本鲸帮不上忙，但本鲸会看着你。'], 'desk-coding'), (('chrome', 'msedge', 'firefox', 'brave'), ['在查资料吗？', '上网别太累哦。'], 'thinking'), (('winword', 'excel', 'powerpnt', 'wps'), ['在办公呢，主人加油～', '文档写累了吧？'], 'desk-done'), (('wechat', 'qq.exe', 'dingtalk', 'feishu', 'lark', 'telegram', 'discord'), ['在跟谁聊天呀？', '本鲸也想跟主人聊天。'], 'cheerful'), (('steam', 'genshin', 'yuanshen', 'league', 'dota', 'cs2', 'valorant', 'minecraft'), ['打游戏怎么不带本鲸！', '加油加油，本鲸给你吹哨。'], 'skeptical'), (('potplayer', 'vlc', 'mpv'), ['在看视频呀，本鲸也一起看～'], 'relaxed')]
APPS = {'记事本': 'notepad', '计算器': 'calc', '画图': 'mspaint', '资源管理器': 'explorer', '任务管理器': 'taskmgr', '控制面板': 'control', '命令提示符': 'cmd', '浏览器': 'start', '任务计划': 'taskschd.msc'}
_PET_FRONT = [None]
SELF_NAMES = ('大肥鲸桌宠', '大肥鲸', '桌宠', '本鲸', '鲸鲸')
LOG_HINTS = ('ai日志', 'ai记录', 'ai流水账', '工作日志', '聊天日志', '日志', '记录', '流水账')
def _bring_pet_front():
    """把桌宠主窗叫到最前面（自识别「打开桌宠」时用）。"""
    win = _PET_FRONT[0]
    if win and win.winfo_exists():
        try:
            win.deiconify()
            win.lift()
        except Exception:
            return None
def _open_ai_log():
    """打开今天的 AI 日志（记录文件）；没记到就把「记录」文件夹打开。"""
    day = time.strftime('%Y-%m-%d')
    body = read_memory(day).strip()
    if not body:
        d = memory_dir()
        try:
            os.startfile(d)
        except OSError:
            return f'{day} 本鲸还没记到什么，记录都在 {d}。'
        return f'{day} 本鲸还没记到什么，先把「记录」文件夹打开啦：{d}'
    else:
        try:
            os.startfile(memory_path(day))
        except OSError:
            return f'{day} 本鲸记下的：\n' + body[:600]
        return f'好～本鲸把今天的 AI 日志（{day}.md）打开了。'
def recognize_self(name):
    """AI 自识别：要开的这个是不是桌宠自己 / 它的 AI 日志。\n\n认出来就办好并返回一句话；不认识返回 None，交回给普通开程序流程。\n"""
    low = str(name or '').strip().lower().replace(' ', '')
    if not low:
        return
    else:
        if any((a in low for a in SELF_NAMES)) or low in ('ai桌宠', 'ai桌宠应用', '桌宠应用'):
            _bring_pet_front()
            return '本鲸就是大肥鲸桌宠呀，本鲸一直在主人身边呢～（没再开一个哦）'
        else:
            if any((a in low for a in LOG_HINTS)):
                return _open_ai_log()
            else:
                return None
VK_MEDIA = {'up': 175, 'down': 174, 'mute': 173, 'pause': 179, 'next': 176, 'prev': 177}
VOLUME_STEP = 0.05
class _GUID(ctypes.Structure):
    _fields_ = [('Data1', wintypes.DWORD), ('Data2', wintypes.WORD), ('Data3', wintypes.WORD), ('Data4', ctypes.c_byte * 8)]
def _make_guid(text):
    g = _GUID()
    ctypes.windll.ole32.CLSIDFromString(ctypes.c_wchar_p(text), ctypes.byref(g))
    return g
def _com_call(ptr, index, restype, *argtypes):
    """按 vtable 下标取一个 COM 方法（this 指针隐式作为第一个参数）。"""
    vtbl = ctypes.cast(ptr, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents
    proto = ctypes.WINFUNCTYPE(restype, ctypes.c_void_p, *argtypes)
    return proto(vtbl[index])
_VOL = [None]
def _endpoint_volume():
    """拿到默认播放设备的 IAudioEndpointVolume（Windows 官方 Core Audio 接口）。失败返回 None。"""
    if _VOL[0] is not None:
        return _VOL[0]
    try:
        try:
            ctypes.windll.ole32.CoInitialize(None)
        except Exception:
            pass
        clsid_enum = _make_guid('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
        iid_enum = _make_guid('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
        enum = ctypes.c_void_p()
        if ctypes.windll.ole32.CoCreateInstance(ctypes.byref(clsid_enum), None, 1, ctypes.byref(iid_enum), ctypes.byref(enum)) != 0 or not enum:
            return None
        get_default = _com_call(enum, 4, ctypes.c_long, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
        dev = ctypes.c_void_p()
        if get_default(enum, 0, 1, ctypes.byref(dev)) != 0 or not dev:
            return None
        iid_vol = _make_guid('{5CDF2C82-841E-4546-9722-0CF74078229A}')
        activate = _com_call(dev, 3, ctypes.c_long, ctypes.POINTER(_GUID), ctypes.c_ulong, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))
        vol = ctypes.c_void_p()
        if activate(dev, ctypes.byref(iid_vol), 0, None, ctypes.byref(vol)) != 0 or not vol:
            return None
        _VOL[0] = vol
        return vol
    except Exception:
        return None
def _vol_scalar():
    vol = _endpoint_volume()
    if not vol:
        return None
    try:
        f = ctypes.c_float(0.0)
        get_lvl = _com_call(vol, 9, ctypes.c_long, ctypes.POINTER(ctypes.c_float))
        if get_lvl(vol, ctypes.byref(f)) != 0:
            return None
        return float(f.value)
    except Exception:
        return None
def _vol_set_scalar(level):
    vol = _endpoint_volume()
    if not vol:
        return False
    try:
        set_lvl = _com_call(vol, 7, ctypes.c_long, ctypes.c_float, ctypes.c_void_p)
        return set_lvl(vol, ctypes.c_float(max(0.0, min(1.0, level))), None) == 0
    except Exception:
        return False
def _vol_toggle_mute():
    vol = _endpoint_volume()
    if not vol:
        return False
    try:
        get_mute = _com_call(vol, 15, ctypes.c_long, ctypes.POINTER(ctypes.c_int))
        set_mute = _com_call(vol, 14, ctypes.c_long, ctypes.c_int, ctypes.c_void_p)
        m = ctypes.c_int(0)
        if get_mute(vol, ctypes.byref(m)) != 0:
            return False
        return set_mute(vol, 0 if m.value else 1, None) == 0
    except Exception:
        return False
def _volume_api(action, times=1):
    """用官方接口调音量（up/down 改百分比，mute 切换静音）。成功返回 True。"""
    if action == 'mute':
        return _vol_toggle_mute()
    if action in ('up', 'down'):
        cur = _vol_scalar()
        if cur is None:
            return False
        step = VOLUME_STEP * max(1, min(int(times or 1), 20))
        return _vol_set_scalar(cur + step if action == 'up' else cur - step)
    return False
def _press_media(name, times=1):
    if name in ('up', 'down', 'mute') and _volume_api(name, times):
        return True
    vk = VK_MEDIA.get(name)
    if not vk:
        return False
    else:
        for _ in range(max(1, min(int(times or 1), 20))):
            _user32.keybd_event(vk, 0, 0, 0)
            _user32.keybd_event(vk, 0, 2, 0)
        return True
def _show_desktop():
    for vk, up in [(91, False), (68, False), (68, True), (91, True)]:
        _user32.keybd_event(vk, 0, 2 if up else 0, 0)
    return True
def _normalize_url(text):
    text = (text or '').strip().strip('<>「」')
    if text.startswith(('http://', 'https://')):
        return text
    else:
        if '.' in text and ' ' not in text:
            return 'https://' + text
        else:
            return None
def _fmt_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
_RE_DROP_TAG = re.compile('(?is)<(script|style|noscript|svg|head)[^>]*>.*?</\\1>')
_RE_TAG = re.compile('(?s)<[^>]+>')
_RE_SPACES = re.compile('[ \\t\\r\\f\\v]+')
_RE_BING_ITEM = re.compile('(?s)<li class=\"b_algo\".*?</li>')
_RE_BING_RSS = re.compile('(?s)<item>(.*?)</item>')
def _chr(code):
    try:
        return chr(int(code, 16) if isinstance(code, str) else code)
    except (ValueError, OverflowError):
        return ' '
def _unescape(text):
    """把网页里的实体（&amp; / &#0183; / &ensp; 之类）还原成字符。"""
    text = re.sub('&#x([0-9a-fA-F]+);', lambda m: _chr(m.group(1)), text)
    text = re.sub('&#(\\d+);', lambda m: _chr(m.group(1)), text)
    for a, b in [('&nbsp;', ' '), ('&ensp;', ' '), ('&emsp;', ' '), ('&thinsp;', ' '), ('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&hellip;', '…'), ('&middot;', '·'), ('&mdash;', '—'), ('&ndash;', '–'), ('&ldquo;', '“'), ('&rdquo;', '”'), ('&lsquo;', '‘'), ('&rsquo;', '’'), ('&times;', '×'), ('&copy;', '©'), ('&bull;', '•'), ('&deg;', '°'), ('&laquo;', '«'), ('&raquo;', '»')]:
        text = text.replace(a, b)
    return text
def strip_html(html):
    """网页 → 能读的纯文本。"""
    html = _RE_DROP_TAG.sub(' ', html)
    html = _RE_TAG.sub(' ', html)
    return re.sub('\\s+', ' ', _unescape(html)).strip()
def http_text(url, limit=400000, timeout=15):
    # irreducible cflow, using cdg fallback
    """按浏览器的方式抓一份网页回来（自动认编码）。"""
    req = urllib.request.Request(url, headers={'User-Agent': _UA, 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(limit)
            if (resp.headers.get('Content-Encoding') or '').lower() == 'gzip':
                raw = gzip.decompress(raw)
            head = raw[:2048].decode('ascii', 'ignore').lower()
            m = re.search('charset=[\"\\\']?([\\w-]+)', head)
            enc = m.group(1) if m else 'utf-8'
            if enc in ['gb2312', 'gbk']:
                enc = 'gb18030'
            return raw.decode(enc, 'ignore')
    except LookupError:
        return raw.decode('utf-8', 'ignore')
def http_json(url, timeout=15):
    """抓一个返回 JSON 的接口。"""
    req = urllib.request.Request(url, headers={'User-Agent': _UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read(400000)
        if (resp.headers.get('Content-Encoding') or '').lower() == 'gzip':
            raw = gzip.decompress(raw)
    return json.loads(raw.decode('utf-8', 'ignore'))
def _search_bing(q, n):
    """Bing 网页搜索（解析结果页）。"""
    page = http_text('https://www.bing.com/search?q=' + urllib.parse.quote(q))
    out = []
    for block in _RE_BING_ITEM.findall(page):
        m = re.search('<h2[^>]*>\\s*<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>', block, re.S)
        if m:
            snip = re.search('(?s)<p[^>]*>(.*?)</p>', block)
            out.append((strip_html(m.group(2)), m.group(1), strip_html(snip.group(1)) if snip else ''))
            if len(out) >= n:
                break
    else:
        return out
def _search_bing_rss(q, n):
    """Bing 的 RSS 版，摘要更干净。"""
    xml = http_text('https://www.bing.com/search?format=rss&q=' + urllib.parse.quote(q))
    out = []
    for item in _RE_BING_RSS.findall(xml)[:n]:
        t = re.search('(?s)<title>(.*?)</title>', item)
        lnk = re.search('(?s)<link>(.*?)</link>', item)
        d = re.search('(?s)<description>(.*?)</description>', item)
        out.append((strip_html(t.group(1)) if t else '', _unescape(lnk.group(1)).strip() if lnk else '', strip_html(d.group(1)) if d else ''))
    return out
def _search_code(q, n):
    """Stack Overflow：技术问题的答案。"""
    o = http_json('https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&site=stackoverflow&pagesize=' + str(n) + '&q=' + urllib.parse.quote(q))
    out = []
    for it in o.get('items') or []:
        out.append((_unescape(re.sub('<[^>]+>', '', it.get('title') or '')), it.get('link') or '', _unescape(re.sub('<[^>]+>', '', it.get('excerpt') or ''))[:160]))
    return out
SEARCH_SOURCES = {'web': _search_bing, 'rss': _search_bing_rss, 'code': _search_code}
def web_search(query, n=5, source='auto'):
    """用本机网络搜一下，返回给模型看的几条结果。"""
    q = str(query or '').strip()
    if not q:
        return '（主人没说搜什么）'
    else:
        source = str(source or 'auto').strip().lower()
        order = [source] if source in SEARCH_SOURCES else ['web', 'rss']
        found = []
        for s in order:
            try:
                found = SEARCH_SOURCES[s](q, n)
            except Exception:
                found = []
            if found:
                break
        if not found:
            return f'搜「{q}」什么也没搜到（可能没联网，或者被搜索引擎挡了）。'
        else:
            lines = [f'{i}. {t}\n   {u}\n   {s[:150]}' for i, (t, u, s) in enumerate(found, 1)]
            return f'搜「{q}」搜到这些：\n' + '\n'.join(lines)
_WMO = {0: '晴', 1: '大致晴朗', 2: '多云', 3: '阴', 45: '有雾', 48: '冻雾', 51: '小毛毛雨', 53: '毛毛雨', 55: '大毛毛雨', 56: '冻毛毛雨', 57: '强冻毛毛雨', 61: '小雨', 63: '中雨', 65: '大雨', 66: '冻雨', 67: '强冻雨', 71: '小雪', 73: '中雪', 75: '大雪', 77: '雪粒', 80: '阵雨', 81: '强阵雨', 82: '暴雨', 85: '阵雪', 86: '强阵雪', 95: '雷阵雨', 96: '雷阵雨夹冰雹', 97: '强雷阵雨夹冰雹'}
def _wmo(code):
    try:
        return _WMO.get(int(code), f'天气码{code}')
    except (TypeError, ValueError):
        return '未知'
def weather(city, days=3):
    """查天气：实时 + 未来几天。"""
    q = str(city or '').strip()
    if not q:
        return '要查哪里的天气呀？告诉本鲸城市名～'
    try:
        geo = http_json('https://geocoding-api.open-meteo.com/v1/search?count=1&language=zh&format=json&name=' + urllib.parse.quote(q))
        hit = (geo.get('results') or [None])[0]
        if not hit:
            return f'本鲸找不到「{q}」这个地方……换个说法试试？'
        n = max(1, min(7, int(days or 3)))
        data = http_json(f'https://api.open-meteo.com/v1/forecast?latitude={hit["latitude"]}&longitude={hit["longitude"]}&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days={n}')
        cur = data.get('current') or {}
        day = data.get('daily') or {}
        place = (hit.get('name') or q) + (f'·{hit["admin1"]}' if hit.get('admin1') else '')
        out = [f'{place} 现在 {cur.get("temperature_2m")}℃（体感 {cur.get("apparent_temperature")}℃）、{_wmo(cur.get("weather_code"))}、湿度 {cur.get("relative_humidity_2m")}%、风 {cur.get("wind_speed_10m")}km/h']
        for i, d in enumerate(day.get('time') or []):
            out.append(f'{d} {_wmo((day.get("weather_code") or [None])[i])} {(day.get("temperature_2m_min") or [None])[i]}~{(day.get("temperature_2m_max") or [None])[i]}℃ 降水概率 {(day.get("precipitation_probability_max") or [None])[i]}%')
        return '\n'.join(out)
    except Exception as e:
        try:
            txt = http_text('https://wttr.in/' + urllib.parse.quote(q) + '?format=%l:+%c+%t+%h+%w&lang=zh').strip()
            if txt:
                return txt
        except Exception:
            pass
        return f'天气没查到（{e}）'
def exchange_rate(src='CNY', dst='', amount=1):
    """查汇率 / 换算金额。"""
    a = str(src or 'CNY').strip().upper()
    b = str(dst or '').strip().upper()
    try:
        data = http_json('https://open.er-api.com/v6/latest/' + urllib.parse.quote(a))
    except Exception as e:
        return f'汇率没查到（{e}）'
    rates = data.get('rates') or {}
    if not rates:
        return f'「{a}」这个货币本鲸不认识。'
    else:
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            amt = 1.0
        if not b:
            common = [c for c in ['USD', 'EUR', 'JPY', 'HKD', 'GBP', 'KRW'] if c in rates]
            return f'{amt:g} {a} 大概值：\n' + '\n'.join((f'  {amt * rates[c]:.2f} {c}' for c in common))
        else:
            if b not in rates:
                return f'「{b}」这个货币本鲸不认识。'
            else:
                return f'{amt:g} {a} ≈ {amt * rates[b]:.2f} {b}（1 {a} = {rates[b]:.4f} {b}）'
def holiday(day=''):
    """查某天是工作日 / 周末 / 节假日 / 调休。"""
    d = str(day or '').strip() or time.strftime('%Y-%m-%d')
    m = re.match('(\\d{4})[-/.](\\d{1,2})[-/.](\\d{1,2})', d)
    if m:
        d = f'{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}'
    try:
        o = http_json('https://timor.tech/api/holiday/info/' + urllib.parse.quote(d))
    except Exception as e:
        return f'节假日没查到（{e}）'
    if o.get('code') != 0:
        return f'「{d}」这天查不到呢。'
    else:
        t = o.get('type') or {}
        kind = {0: '工作日', 1: '周末', 2: '节假日', 3: '调休补班'}.get(t.get('type'), '不太确定')
        name = t.get('name') or ''
        tail = {'节假日': '，可以好好休息～', '调休补班': '，是调休要上班哦……', '周末': '，休息日！'}.get(kind, '')
        return f'{d} 是{kind}{('（' + name + '）' if name else '')}{tail}'
def ip_info():
    """看看本机上网用的公网 IP 和归属地。"""
    try:
        txt = http_text('https://myip.ipip.net').strip()
        if txt:
            return txt
    except Exception:
        pass
    try:
        o = http_json('https://ipinfo.io/json')
        return f'公网 IP {o.get("ip")}，位置 {o.get("city") or "?"}/{o.get("region") or "?"}/{o.get("country") or "?"}，运营商 {o.get("org") or "未知"}'
    except Exception as e:
        return f'没查到本机公网 IP（{e}）'
def fetch_page(url, limit=4000):
    """打开一个网页，把正文读回来。"""
    url = _normalize_url(url)
    if not url:
        return '这个网址本鲸看不懂，要像 example.com 这样哦。'
    else:
        return strip_html(http_text(url))[:limit]
def _screenshot_dir():
    return os.path.join(data_dir(), '截图')
def take_screenshot():
    im = ImageGrab.grab()
    d = _screenshot_dir()
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, time.strftime('截图_%Y%m%d_%H%M%S.png'))
    im.save(path)
    return path
PC_GROUPS = [('files', '文件（读 / 写 / 建文件夹 / 移动 / 打开）'), ('command', '跑命令行'), ('power', '电源（关机 / 重启 / 睡眠 / 定时关机）'), ('settings', '系统设置（音量 / 亮度 / 壁纸 / 回收站 / 打开设置面板）')]
PC_TOOL_GROUPS = {'read_file': 'files', 'write_file': 'files', 'list_dir': 'files', 'make_dir': 'files', 'move_path': 'files', 'open_path': 'files', 'run_command': 'command', 'shutdown_pc': 'power', 'restart_pc': 'power', 'sleep_pc': 'power', 'schedule_shutdown': 'power', 'cancel_shutdown': 'power', 'open_settings': 'settings', 'set_brightness': 'settings', 'set_wallpaper': 'settings', 'empty_recycle': 'settings', 'power_plan': 'settings'}
PC_TOOLS = set(PC_TOOL_GROUPS)
_PC_STATE = {'on': False, 'files': False, 'command': False, 'power': False, 'settings': False}
def set_pc_control(on, groups=None):
    """由「应用设置 → 控制电脑」调用：总开关 + 各权限组。"""
    _PC_STATE['on'] = bool(on)
    if isinstance(groups, dict):
        for k, _label in PC_GROUPS:
            if k in groups:
                _PC_STATE[k] = bool(groups[k])
    elif on:
        for k, _label in PC_GROUPS:
            _PC_STATE[k] = True
def pc_denied(name):
    """这个工具能不能用：能用返回 None，不能用返回一句提示。"""
    grp = PC_TOOL_GROUPS.get(name)
    if not grp:
        return None
    if not _PC_STATE.get('on'):
        return '主人还没打开「控制电脑」总开关呢——去「应用设置 → 控制电脑」里打开它，本鲸才能帮主人操作电脑哦～'
    if not _PC_STATE.get(grp):
        label = dict(PC_GROUPS).get(grp, grp)
        return f'主人还没打开「{label}」这个权限呢——去「应用设置 → 控制电脑」里打开它，本鲸才能做这件事。'
    return None
def _in_self_home(path):
    """这个路径是不是落在桌宠自己住的目录里（含该目录本身）——不许往里写文件。"""
    try:
        p = os.path.normcase(os.path.realpath(os.path.abspath(str(path))))
        home = os.path.normcase(os.path.realpath(data_dir()))
    except (OSError, ValueError):
        return False
    return p == home or p.startswith(home + os.sep)
def _pc_run(name, args):
    """「控制电脑」那批工具的实现（调用前已确认开关是开着的）。"""
    if name == 'read_file':
        p = os.path.expanduser(str(args.get('path') or '').strip())
        if not p or not os.path.isfile(p):
            return f'本鲸没找到「{p}」这个文件呀。'
        else:
            try:
                with open(p, 'r', encoding='utf-8', errors='replace') as f:
                    txt = f.read(8000)
            except OSError as e:
                return f'这个文件本鲸读不了……（{e}）'
            tail = '…（太长，只看了前面一段）' if len(txt) >= 8000 else ''
            return f'「{p}」的内容：\n{txt}{tail}'
    else:
        if name == 'write_file':
            p = os.path.expanduser(str(args.get('path') or '').strip())
            if not p:
                return '要写到哪个文件呀？给本鲸一个路径。'
            else:
                if _in_self_home(p):
                    return '那是本鲸自己住的窝，不许乱动哦。'
                else:
                    content = str(args.get('content', ''))
                    append = str(args.get('mode') or '').lower() in ('append', 'a', '追加')
                    try:
                        parent = os.path.dirname(os.path.abspath(p))
                        if parent:
                            os.makedirs(parent, exist_ok=True)
                        with open(p, 'a' if append else 'w', encoding='utf-8') as f:
                            f.write(content)
                    except OSError as e:
                        return f'写不进去……（{e}）'
                    return f'已经{('追加' if append else '写入')}到 {p} 啦（{len(content)} 字）。'
        else:
            if name == 'list_dir':
                p = os.path.expanduser(str(args.get('path') or '').strip()) or data_dir()
                if not os.path.isdir(p):
                    return f'「{p}」不是一个文件夹呀。'
                else:
                    try:
                        names = sorted(os.listdir(p))
                    except OSError as e:
                        return f'这个文件夹本鲸打不开……（{e}）'
                    body = '、'.join(names[:80]) if names else '（空的）'
                    return f'{p} 里有 {len(names)} 项：{body}' + ('…' if len(names) > 80 else '')
            else:
                if name == 'run_command':
                    cmd = str(args.get('command') or '').strip()
                    if not cmd:
                        return '要本鲸跑什么命令呀？'
                    else:
                        try:
                            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=25, encoding='utf-8', errors='replace')
                        except subprocess.TimeoutExpired:
                            return '这条命令跑了太久，本鲸先停下了。'
                        except OSError as e:
                            return f'命令没跑起来……（{e}）'
                        out = (r.stdout or '') + ('\n[错误]\n' + r.stderr if r.stderr else '')
                        return f'命令跑完了（返回码 {r.returncode}）：\n' + out.strip()[:2000]
                else:
                    if name == 'shutdown_pc':
                        subprocess.Popen('shutdown /s /t 60', shell=True)
                        return '好，本鲸 60 秒后帮主人关机（反悔就让本鲸跑「shutdown /a」取消）。'
                    else:
                        if name == 'restart_pc':
                            subprocess.Popen('shutdown /r /t 60', shell=True)
                            return '好，本鲸 60 秒后帮主人重启（反悔就让本鲸跑「shutdown /a」取消）。'
                        else:
                            return _pc_run_extra(name, args)
def _pc_run_extra(name, args):
    """「控制电脑」里新增的那批工具（建文件夹 / 移动 / 打开、睡眠、定时关机、系统设置…）。"""
    if name == 'make_dir':
        p = os.path.expanduser(str(args.get('path') or '').strip())
        if not p:
            return '要建哪个文件夹呀？给本鲸一个路径。'
        try:
            os.makedirs(p, exist_ok=True)
        except OSError as e:
            return f'建不了……（{e}）'
        return f'好～建好文件夹 {p} 了。'
    if name == 'open_path':
        p = os.path.expanduser(str(args.get('path') or '').strip()) or data_dir()
        if not os.path.exists(p):
            return f'本鲸没找到「{p}」呀。'
        try:
            os.startfile(p)
        except OSError as e:
            return f'打不开……（{e}）'
        return f'好～帮主人打开了 {p}。'
    if name == 'move_path':
        src = os.path.expanduser(str(args.get('src') or '').strip())
        dst = os.path.expanduser(str(args.get('dst') or '').strip())
        if not src or not dst:
            return '要移动哪个、移到哪儿呀？'
        if not os.path.exists(src):
            return f'本鲸没找到「{src}」呀。'
        if _in_self_home(src) or _in_self_home(dst):
            return '不能动本鲸自己住的窝哦。'
        try:
            parent = os.path.dirname(os.path.abspath(dst))
            if parent:
                os.makedirs(parent, exist_ok=True)
            shutil.move(src, dst)
        except OSError as e:
            return f'移动失败了……（{e}）'
        return f'好～把 {src} 挪到 {dst} 了。'
    if name == 'sleep_pc':
        subprocess.Popen('rundll32.exe powrprof.dll,SetSuspendState 0,1,0', shell=True)
        return '好，本鲸让电脑打个盹（睡眠）～'
    if name == 'schedule_shutdown':
        try:
            mins = max(1, int(float(args.get('minutes', 10))))
        except (TypeError, ValueError):
            mins = 10
        subprocess.Popen(f'shutdown /s /t {mins * 60}', shell=True)
        return f'好，本鲸 {mins} 分钟后帮主人关机（反悔就让本鲸取消关机）。'
    if name == 'cancel_shutdown':
        r = subprocess.run('shutdown /a', shell=True, capture_output=True, text=True, creationflags=_NO_WINDOW)
        if r.returncode:
            return '现在没有正在倒计时的关机 / 重启哦。'
        return '好～取消掉关机倒计时了。'
    if name == 'open_settings':
        page = str(args.get('page') or '').strip().lower()
        aliases = {'显示': 'display', '屏幕': 'display', '声音': 'sound', '音频': 'sound', '蓝牙': 'bluetooth', '网络': 'network', 'wifi': 'network', '更新': 'windowsupdate', '系统更新': 'windowsupdate', '个性化': 'personalization', '主题': 'personalization', '壁纸': 'personalization', '应用': 'appsfeatures', '隐私': 'privacy', '关于': 'about', '鼠标': 'mousetouchpad', '键盘': 'keyboard', '时间': 'dateandtime', '日期': 'dateandtime', '电源': 'powersleep', '睡眠': 'powersleep', '默认应用': 'defaultapps', '通知': 'notifications'}
        key = aliases.get(page, page) or 'system'
        try:
            os.startfile('ms-settings:' + key)
        except OSError as e:
            return f'打不开系统设置……（{e}）'
        return f'好～帮主人打开了系统设置（{page or "主页"}）。'
    if name == 'set_brightness':
        try:
            lvl = int(float(args.get('level', 50)))
        except (TypeError, ValueError):
            return '亮度要给个 0~100 的数字哦。'
        lvl = max(0, min(100, lvl))
        out = run_shell(f'try {{ (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {lvl}); "OK" }} catch {{ "ERR " + $_.Exception.Message }}', 'ps', timeout=15)
        if 'OK' in out:
            return f'好～亮度调到 {lvl}% 了。'
        return f'这台机器本鲸调不了亮度……（{out[:120]}）'
    if name == 'set_wallpaper':
        p = os.path.expanduser(str(args.get('path') or '').strip())
        if not p or not os.path.isfile(p):
            return f'本鲸没找到「{p}」这张图呀。'
        try:
            ok = bool(ctypes.windll.user32.SystemParametersInfoW(20, 0, ctypes.c_wchar_p(p), 3))
        except Exception as e:
            return f'换壁纸失败了……（{e}）'
        return f'好～壁纸换成 {os.path.basename(p)} 啦。' if ok else '换壁纸没成功……'
    if name == 'empty_recycle':
        out = run_shell('Clear-RecycleBin -Force -Confirm:$false -ErrorAction SilentlyContinue; "OK"', 'ps', timeout=40)
        return '好～回收站清干净了。' if 'OK' in out else f'清回收站时出了点问题……（{out[:120]}）'
    if name == 'power_plan':
        plans = {'平衡': 'SCHEME_BALANCED', 'balanced': 'SCHEME_BALANCED', '高性能': 'SCHEME_MIN', '性能': 'SCHEME_MIN', 'high': 'SCHEME_MIN', '节能': 'SCHEME_MAX', 'eco': 'SCHEME_MAX', 'saver': 'SCHEME_MAX'}
        v = str(args.get('name') or '').strip()
        g = plans.get(v.lower()) or plans.get(v) or v
        if not g:
            return '要切哪个电源计划呀？可以说「平衡 / 高性能 / 节能」。'
        try:
            r = subprocess.run(['powercfg', '/setactive', g], capture_output=True, text=True, timeout=15, creationflags=_NO_WINDOW)
        except OSError as e:
            return f'切电源计划失败了……（{e}）'
        if r.returncode:
            return f'没切成（{v}）……可能名字不对。'
        return f'好～电源计划切到「{v}」了。'
    return '本鲸还不会这件事。'
class _MOUSEINPUT(ctypes.Structure):
    _fields_ = [('dx', ctypes.c_long), ('dy', ctypes.c_long), ('mouseData', wintypes.DWORD), ('dwFlags', wintypes.DWORD), ('time', wintypes.DWORD), ('dwExtraInfo', ctypes.c_void_p)]
class _KEYBDINPUT(ctypes.Structure):
    _fields_ = [('wVk', wintypes.WORD), ('wScan', wintypes.WORD), ('dwFlags', wintypes.DWORD), ('time', wintypes.DWORD), ('dwExtraInfo', ctypes.c_void_p)]
class _INPUTUNION(ctypes.Union):
    _fields_ = [('mi', _MOUSEINPUT), ('ki', _KEYBDINPUT)]
class _INPUT(ctypes.Structure):
    _fields_ = [('type', wintypes.DWORD), ('u', _INPUTUNION)]
try:
    _user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(_INPUT), ctypes.c_int]
    _user32.SendInput.restype = wintypes.UINT
except Exception:
    pass
_MEF = {'left': (2, 4), 'right': (8, 16), 'middle': (32, 64)}
def _cua_send(inputs):
    try:
        n = len(inputs)
        arr = (_INPUT * n)(*inputs)
        return _user32.SendInput(n, arr, ctypes.sizeof(_INPUT))
    except Exception:
        return 0
def cua_move(x, y):
    try:
        _user32.SetCursorPos(int(x), int(y))
    except Exception:
        pass
def cua_button(button='left', down=True):
    d, u = _MEF.get(str(button), _MEF['left'])
    _cua_send([_INPUT(0, _INPUTUNION(mi=_MOUSEINPUT(0, 0, 0, d if down else u, 0, None)))])
def cua_click(x=None, y=None, button='left', double=False):
    if x is not None and y is not None:
        cua_move(x, y)
        time.sleep(0.06)
    cua_button(button, True)
    time.sleep(0.03)
    cua_button(button, False)
    if double:
        time.sleep(0.06)
        cua_button(button, True)
        time.sleep(0.03)
        cua_button(button, False)
def cua_drag(x1, y1, x2, y2, seconds=0.7):
    cua_move(x1, y1)
    time.sleep(0.12)
    cua_button('left', True)
    steps = max(6, int(float(seconds) * 40))
    for i in range(1, steps + 1):
        cua_move(x1 + (x2 - x1) * i / steps, y1 + (y2 - y1) * i / steps)
        time.sleep(max(0.006, float(seconds) / steps))
    cua_button('left', False)
def _cua_key_raw(vk, down):
    _cua_send([_INPUT(1, _INPUTUNION(ki=_KEYBDINPUT(int(vk), 0, 0 if down else 2, 0, None)))])
def cua_key(combo):
    parts = [p.strip().lower() for p in str(combo or '').replace(' ', '').split('+') if p.strip()]
    vks = [v for v in (_PTT_VK.get(p) or _key_code(p) for p in parts) if v]
    for v in vks:
        _cua_key_raw(v, True)
    for v in reversed(vks):
        _cua_key_raw(v, False)
def cua_type(text):
    for ch in str(text or ''):
        code = ord(ch)
        if code > 65535:
            continue
        _cua_send([_INPUT(1, _INPUTUNION(ki=_KEYBDINPUT(0, code, 4, 0, None)))])
        _cua_send([_INPUT(1, _INPUTUNION(ki=_KEYBDINPUT(0, code, 6, 0, None)))])
        time.sleep(0.012)
def cua_scroll(amount):
    delta = int(amount) * 120
    _cua_send([_INPUT(0, _INPUTUNION(mi=_MOUSEINPUT(0, 0, delta & 4294967295, 2048, 0, None)))])
CUA_HELP = '动作清单：move 移动鼠标 / click 左键单击 / double_click 双击 / right_click 右键 / drag 拖动 / type 打字 / key 按键（如 ctrl+c、enter） / scroll 滚轮（正数向上） / wait 等待几秒 / done 完成 / fail 做不到。坐标 x、y 用 0~1 的相对值（左上角 0,0，右下角 1,1）。'
def run_tool(name, args):
    """执行一个工具，返回给主人（和模型）看的一句话。"""
    args = args or {}
    if name in PC_TOOLS:
        denied = pc_denied(name)
        if denied:
            return denied
        return _pc_run(name, args)
    try:
        if name == 'open_app':
            key = str(args.get('name', '')).strip()
            mine = recognize_self(key)
            if mine:
                return mine
            exe = APPS.get(key) or next((v for k, v in APPS.items() if k in key), None)
            if not exe:
                return f'本鲸不认识「{key}」这个程序呀，目前会开：' + '、'.join(APPS)
            if exe == 'start':
                os.startfile('https://www.bing.com')
            else:
                os.startfile(exe)
            return f'已经帮主人打开{key}啦～'
        if name == 'open_url':
            url = _normalize_url(args.get('url'))
            if not url:
                return '那个网址本鲸看不懂，要像 example.com 这样哦。'
            os.startfile(url)
            return f'浏览器已经打开 {url} 了。'
        if name == 'volume':
            act = str(args.get('action', 'mute'))
            n = args.get('times', 1)
            if not _press_media(act, n):
                return '音量键本鲸按不动……'
            word = {'up': '调大', 'down': '调小', 'mute': '切换静音', 'pause': '播放/暂停', 'next': '下一首', 'prev': '上一首'}.get(act, act)
            return f'好～帮主人{word}了。'
        if name == 'screenshot':
            path = take_screenshot()
            return f'截图完成，存在 {path}'
        if name == 'system_info':
            load, avail, total = memory_info()
            return f'内存占用 {load}%，还剩 {avail:.1f}G / 共 {total:.1f}G；系统已开机 {_kernel32.GetTickCount64() / 3600000:.1f} 小时。'
        if name == 'lock_screen':
            _user32.LockWorkStation()
            return '好，本鲸帮主人锁屏～（记得回来找本鲸）'
        if name == 'show_desktop':
            _show_desktop()
            return '帮主人把窗口都收起来了。'
        if name == 'now':
            return '现在是 ' + _fmt_time()
        if name == 'current_window':
            title, exe = active_window()
            title = title or '没有标题的窗口'
            dev = detect_dev_tool(exe, title)
            extra = f'——是编程工具「{dev}」哦' if dev else ''
            return f'主人现在在用 {exe or "未知程序"}（窗口标题：{title}）{extra}。'
        if name == 'remind':
            mins = max(1, int(float(args.get('minutes', 5))))
            what = str(args.get('what', '时间到'))
            return f'__REMIND__{mins}|{what}'
        if name == 'recall':
            word = str(args.get('day') or '今天').strip()
            offset = {'今天': 0, 'today': 0, '昨天': (-1), 'yesterday': (-1), '前天': (-2)}.get(word)
            day = day_text(offset) if offset is not None else word
            body = read_memory(day).strip()
            if not body:
                return f'本鲸的记事本里没有 {day} 的记录。'
            else:
                return f'{day} 本鲸记下的：\n' + body[:1500]
        if name == 'web_search':
            return web_search(args.get('query', ''), 5, str(args.get('source') or 'auto'))[:2500]
        if name == 'fetch_url':
            return '网页正文：\n' + fetch_page(args.get('url', ''))
        if name == 'weather':
            return weather(args.get('city', ''), args.get('days', 3))[:1200]
        if name == 'exchange_rate':
            return exchange_rate(args.get('from', 'CNY'), args.get('to', ''), args.get('amount', 1))
        if name == 'holiday':
            return holiday(args.get('date', ''))
        if name == 'ip_info':
            return ip_info()
        if name == 'save_memo':
            return save_memo(args.get('text', ''))
        if name == 'list_memos':
            return list_memos(args.get('keyword', ''))
        if name == 'forget_memo':
            return forget_memo(args.get('keyword', ''))
        if name == 'now_playing':
            return media_report()
        if name == 'music_lyrics':
            return lyrics_report(args.get('title', ''), args.get('artist', ''))
        if name == 'video_summary':
            return video_report(args.get('path', ''))
        if name == 'identify_music':
            return identify_music(args.get('path', ''))
        if name == 'transcribe_media':
            return transcribe_media(args.get('path', ''))
        if name == 'look_screen':
            return look_screen_report(load_config(), args.get('seconds', 3))
        if name == 'look_window':
            return look_window_report(load_config(), args.get('name', ''))
        if name == 'operate_pc':
            goal = str(args.get('goal') or '').strip()
            return '__CUA__' + goal if goal else '要本鲸操作电脑做什么呀？给个目标。'
        if name == 'eat_feed':
            return '__CLEAN__'
        if name == 'quiet':
            return '__QUIET__'
        return '本鲸还不会这件事。'
    except Exception as e:
        return f'本鲸做失败了……（{e}）'
def memory_info():
    st = _MEMSTATUS()
    st.dwLength = ctypes.sizeof(st)
    _kernel32.GlobalMemoryStatusEx(ctypes.byref(st))
    return (st.dwMemoryLoad, st.ullAvailPhys / 1073741824, st.ullTotalPhys / 1073741824)
SYSTEM_TOOLS = [{'type': 'function', 'function': {'name': 'open_app', 'description': '打开本机常用程序（记事本 / 计算器 / 画图 / 资源管理器 / 任务管理器…）；也认得出桌宠自己（大肥鲸桌宠）和它的 AI 日志（记录），不会重复开', 'parameters': {'type': 'object', 'properties': {'name': {'type': 'string', 'description': '程序名，如 记事本 / 计算器 / 画图'}}, 'required': ['name']}}}, {'type': 'function', 'function': {'name': 'open_url', 'description': '用默认浏览器打开一个网址', 'parameters': {'type': 'object', 'properties': {'url': {'type': 'string'}}, 'required': ['url']}}}, {'type': 'function', 'function': {'name': 'volume', 'description': '调节系统音量 / 静音 / 播放暂停 / 切歌', 'parameters': {'type': 'object', 'properties': {'action': {'type': 'string', 'enum': ['up', 'down', 'mute', 'pause', 'next', 'prev']}, 'times': {'type': 'integer', 'description': '按几次，默认 1'}}, 'required': ['action']}}}, {'type': 'function', 'function': {'name': 'screenshot', 'description': '截取整个屏幕并保存到「截图」文件夹', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'system_info', 'description': '查看内存占用、开机时长等系统信息', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'lock_screen', 'description': '锁定电脑屏幕', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'show_desktop', 'description': '最小化所有窗口、显示桌面', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'now', 'description': '查看当前日期和时间', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'current_window', 'description': '查看主人现在正在用什么程序', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'remind', 'description': '设置提醒，到点叫主人', 'parameters': {'type': 'object', 'properties': {'minutes': {'type': 'integer'}, 'what': {'type': 'string'}}, 'required': ['minutes']}}}, {'type': 'function', 'function': {'name': 'web_search', 'description': '用本机网络联网搜索资料。你自己不能联网、需要查最新信息时就用这个', 'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 'description': '搜索词'}, 'source': {'type': 'string', 'enum': ['auto', 'web', 'rss', 'code'], 'description': 'auto 默认网页搜索；rss 更精简；code 搜技术问答'}}, 'required': ['query']}}}, {'type': 'function', 'function': {'name': 'fetch_url', 'description': '打开一个网页把正文读回来（配合 web_search 看细节用）', 'parameters': {'type': 'object', 'properties': {'url': {'type': 'string', 'description': '网址'}}, 'required': ['url']}}}, {'type': 'function', 'function': {'name': 'weather', 'description': '查某个城市的天气（实时 + 未来几天预报）', 'parameters': {'type': 'object', 'properties': {'city': {'type': 'string', 'description': '城市名，如 北京 / 上海 / 南宁'}, 'days': {'type': 'integer', 'description': '预报几天，默认 3'}}, 'required': ['city']}}}, {'type': 'function', 'function': {'name': 'exchange_rate', 'description': '查汇率 / 换算金额', 'parameters': {'type': 'object', 'properties': {'from': {'type': 'string', 'description': '原货币代码，如 CNY / USD，默认 CNY'}, 'to': {'type': 'string', 'description': '目标货币，如 USD；不填就报几个常用币种'}, 'amount': {'type': 'number', 'description': '金额，默认 1'}}, 'required': []}}}, {'type': 'function', 'function': {'name': 'holiday', 'description': '查某天是工作日 / 周末 / 节假日还是调休补班（不填就是今天）', 'parameters': {'type': 'object', 'properties': {'date': {'type': 'string', 'description': '日期，如 2026-10-01；不填就是今天'}}, 'required': []}}}, {'type': 'function', 'function': {'name': 'ip_info', 'description': '查本机上网用的公网 IP 和归属地', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'save_memo', 'description': '把一条重要信息记进「重要信息.md」。注意：发现重要信息时先问主人一句「要不要记下来」，他同意了再调用', 'parameters': {'type': 'object', 'properties': {'text': {'type': 'string', 'description': '要记的内容'}}, 'required': ['text']}}}, {'type': 'function', 'function': {'name': 'list_memos', 'description': '翻本鲸记着的重要信息', 'parameters': {'type': 'object', 'properties': {'keyword': {'type': 'string', 'description': '只看含这个关键词的'}}, 'required': []}}}, {'type': 'function', 'function': {'name': 'forget_memo', 'description': '删掉带某关键词的重要信息', 'parameters': {'type': 'object', 'properties': {'keyword': {'type': 'string'}}, 'required': ['keyword']}}}, {'type': 'function', 'function': {'name': 'eat_feed', 'description': '打扫「投喂」文件夹，把里面的垃圾变成米饭吃掉', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'recall', 'description': '翻你记下的「主人做过什么」的流水账。主人问「我今天干了什么」「昨天我在忙什么」「我是不是忘了什么」时调用', 'parameters': {'type': 'object', 'properties': {'day': {'type': 'string', 'description': '哪一天：今天 / 昨天 / 前天，或 2026-10-08 这种日期'}}, 'required': []}}}, {'type': 'function', 'function': {'name': 'read_file', 'description': '读取一个文本文件的内容（要主人先打开「控制电脑」）', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': '文件完整路径'}}, 'required': ['path']}}}, {'type': 'function', 'function': {'name': 'write_file', 'description': '把内容写进 / 追加到一个文本文件（要主人先打开「控制电脑」）', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': '文件完整路径'}, 'content': {'type': 'string', 'description': '要写入的文本'}, 'mode': {'type': 'string', 'enum': ['overwrite', 'append'], 'description': 'overwrite 覆盖（默认）；append 追加'}}, 'required': ['path', 'content']}}}, {'type': 'function', 'function': {'name': 'list_dir', 'description': '看看一个文件夹里有什么（要主人先打开「控制电脑」）', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': '文件夹路径，不填就是数据文件夹'}}, 'required': []}}}, {'type': 'function', 'function': {'name': 'run_command', 'description': '在本机执行一条命令并返回输出（要主人先打开「控制电脑」，谨慎用）', 'parameters': {'type': 'object', 'properties': {'command': {'type': 'string', 'description': '要执行的命令行'}}, 'required': ['command']}}}, {'type': 'function', 'function': {'name': 'shutdown_pc', 'description': '60 秒后关机（要主人先打开「控制电脑」）', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'restart_pc', 'description': '60 秒后重启（要主人先打开「控制电脑」）', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'now_playing', 'description': '看看主人现在在用什么播放器放什么（歌名 / 歌手 / 专辑 / 进度 / 时长）。主人问「现在放的什么歌」「这首歌叫什么」时用', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'music_lyrics', 'description': '查一首歌的歌词：先在「音乐」文件夹找同名 .lrc，找不到就联网搜。不填 title 就查当前正在播放的歌', 'parameters': {'type': 'object', 'properties': {'title': {'type': 'string', 'description': '歌名'}, 'artist': {'type': 'string', 'description': '歌手，可不填'}}, 'required': []}}}, {'type': 'function', 'function': {'name': 'video_summary', 'description': '总结一个视频：抽关键帧交给能看图的模型，看画面讲了什么。需要视频文件的完整路径（主人可以把视频拖进聊天框）', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': '视频文件的完整路径'}}, 'required': ['path']}}}, {'type': 'function', 'function': {'name': 'identify_music', 'description': '听歌识曲：认出音频或视频里的背景音乐是什么歌、谁唱的（需要先配好 ACRCloud）。参数给文件完整路径', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': '音频或视频文件的完整路径'}}, 'required': ['path']}}}, {'type': 'function', 'function': {'name': 'transcribe_media', 'description': '把音频或视频里的人声转成文字（需要先配好转写 API）。参数给文件完整路径', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': '音频或视频文件的完整路径'}}, 'required': ['path']}}}, {'type': 'function', 'function': {'name': 'make_dir', 'description': '新建一个文件夹（要主人打开「控制电脑 → 文件」权限）', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': '要建的文件夹路径'}}, 'required': ['path']}}}, {'type': 'function', 'function': {'name': 'open_path', 'description': '用资源管理器打开一个文件或文件夹（要「文件」权限）', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': '文件或文件夹路径'}}, 'required': ['path']}}}, {'type': 'function', 'function': {'name': 'move_path', 'description': '移动 / 重命名文件或文件夹（要「文件」权限）', 'parameters': {'type': 'object', 'properties': {'src': {'type': 'string', 'description': '原路径'}, 'dst': {'type': 'string', 'description': '目标路径'}}, 'required': ['src', 'dst']}}}, {'type': 'function', 'function': {'name': 'sleep_pc', 'description': '让电脑进入睡眠（要「电源」权限）', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'schedule_shutdown', 'description': '定时关机：多少分钟后关机（要「电源」权限）', 'parameters': {'type': 'object', 'properties': {'minutes': {'type': 'integer', 'description': '多少分钟后关机，默认 10'}}, 'required': ['minutes']}}}, {'type': 'function', 'function': {'name': 'cancel_shutdown', 'description': '取消正在倒计时的关机 / 重启（要「电源」权限）', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'open_settings', 'description': '打开 Windows 系统设置的某个页面（要「系统设置」权限）。page 可填：显示 / 声音 / 蓝牙 / 网络 / 更新 / 个性化 / 应用 / 隐私 / 关于 / 鼠标 / 键盘 / 时间 / 电源 等', 'parameters': {'type': 'object', 'properties': {'page': {'type': 'string', 'description': '设置页面名，如 显示 / 声音 / 蓝牙；不填就打开设置主页'}}, 'required': []}}}, {'type': 'function', 'function': {'name': 'set_brightness', 'description': '调屏幕亮度（要「系统设置」权限，只有支持的显示器 / 笔记本好使）', 'parameters': {'type': 'object', 'properties': {'level': {'type': 'integer', 'description': '亮度 0~100'}}, 'required': ['level']}}}, {'type': 'function', 'function': {'name': 'set_wallpaper', 'description': '换桌面壁纸（要「系统设置」权限）', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': '图片文件完整路径'}}, 'required': ['path']}}}, {'type': 'function', 'function': {'name': 'empty_recycle', 'description': '清空回收站（要「系统设置」权限）', 'parameters': {'type': 'object', 'properties': {}}}}, {'type': 'function', 'function': {'name': 'power_plan', 'description': '切换电源计划：平衡 / 高性能 / 节能（要「系统设置」权限）', 'parameters': {'type': 'object', 'properties': {'name': {'type': 'string', 'description': '平衡 / 高性能 / 节能'}}, 'required': ['name']}}}, {'type': 'function', 'function': {'name': 'look_screen', 'description': '录一小段屏幕（连续几帧）看一眼主人的动态画面，说说在发生什么。主人问「你看到了什么」「我现在在干嘛」时用', 'parameters': {'type': 'object', 'properties': {'seconds': {'type': 'integer', 'description': '看几秒，默认 3，最多 8'}}, 'required': []}}}, {'type': 'function', 'function': {'name': 'look_window', 'description': '看某个应用 / 窗口的画面内容（按标题关键词或程序名找），比如「看看我浏览器里写了啥」', 'parameters': {'type': 'object', 'properties': {'name': {'type': 'string', 'description': '窗口标题关键词或程序名，如 vscode / 微信'}}, 'required': ['name']}}}, {'type': 'function', 'function': {'name': 'operate_pc', 'description': '动手操作电脑完成一个目标（移动/点击鼠标、拖动、打字、按键），屏幕上会显示当前在做什么，动手前会先问主人（要主人在「应用设置 → 控制电脑」里打开「允许 AI 操作电脑」）。把这个目标写清楚', 'parameters': {'type': 'object', 'properties': {'goal': {'type': 'string', 'description': '要完成的目标，例如「打开记事本并输入 hello」'}}, 'required': ['goal']}}}]
BRAIN_TOOLS = [t for t in SYSTEM_TOOLS if t['function']['name'] in BRAIN_TOOL_NAMES]
def match_local(text):
    """不上 API 也能认出来的口令。命中返回 (工具名, 参数)。"""
    t = (text or '').strip()
    low = t.lower()
    if not t:
        return
    if any((k in t for k in ['截图', '截屏', '截个屏', '屏幕截图'])):
        return ('screenshot', {})
    if any((k in t for k in ['记了什么', '记过什么', '重要信息', '我的备忘', '备忘录里'])):
        return ('list_memos', {})
    m = re.match('^(?:帮我)?(?:记一下|记下|记住|记一笔|备忘)[：:，,\\s]*(.+)$', t, re.S)
    if m and m.group(1).strip():
        return ('save_memo', {'text': m.group(1).strip()})
    if '静音' in t:
        return ('volume', {'action': 'mute'})
    if '音量' in t and any((k in t for k in ['大', '上', '+', '加'])):
        return ('volume', {'action': 'up', 'times': 2})
    if any((k in t for k in ['小', '下', '-', '减'])):
        return ('volume', {'action': 'down', 'times': 2})
    if '音量' in t:
        return ('volume', {'action': 'mute'})
    if '锁屏' in t or '锁上' in t:
        return ('lock_screen', {})
    if '显示桌面' in t or ('桌面' in t and ('最小化' in t or '收起' in t)):
        return ('show_desktop', {})
    if any((k in t for k in ['几点', '报时', '现在时间', '什么时间', '日期', '几号'])):
        return ('now', {})
    if '内存' in t:
        return ('system_info', {})
    if any((k in t for k in ['在干什么', '在做什么', '在干嘛', '在用什么'])):
        return ('current_window', {})
    if any((k in t for k in ['打扫', '清理投喂', '吃掉投喂'])):
        return ('eat_feed', {})
    if '下一首' in t or '切歌' in t:
        return ('volume', {'action': 'next'})
    if '上一首' in t:
        return ('volume', {'action': 'prev'})
    if '暂停' in t or '播放' in t:
        return ('volume', {'action': 'pause'})
    m = re.search('(https?://[^\\s，。]+)', t)
    if m:
        return ('open_url', {'url': m.group(1)})
    if any((w in t for w in ['打开', '启动', '开一下', '看看', '看一下', '看下', '调出'])):
        if any((k in low for k in ['ai日志', 'ai记录', 'ai流水账', '工作日志', '日志', '记录', '流水账'])):
            return ('open_app', {'name': 'AI日志'})
        if any((k in t for k in ['大肥鲸', '桌宠', '本鲸'])):
            return ('open_app', {'name': '大肥鲸桌宠'})
        for k in APPS:
            if k in t and any((w in t for w in ['打开', '启动', '开一下'])):
                return ('open_app', {'name': k})
    if any((w in t for w in ['打开', '访问'])):
        m = re.search('([a-zA-Z0-9\\-]+\\.[a-zA-Z]{2,})', t)
        if m:
            return ('open_url', {'url': m.group(1)})
    return None
def split_leg(side):
    """把侧视图的腿脚从身体上切下来。返回 body/leg/pos/hip/leg_len，切不出来返回 None。"""
    w, h = side.size
    alpha = side.split()[3]
    widths = []
    for y in range(h):
        box = alpha.crop((0, y, w, y + 1)).getbbox()
        widths.append(box[2] - box[0] if box else 0)
    foot_w = max(widths[(-4):] + [1])
    leg_top = None
    for y in range(h - 1, int(h * 0.55), (-1)):
        if widths[y] > foot_w * 1.8:
            leg_top = y + 1
            break
    if leg_top is None or leg_top >= h - 8:
        return None
    else:
        box = alpha.crop((0, leg_top, w, h)).getbbox()
        if box is None:
            return
        else:
            lx0, ly0, lx1, ly1 = (box[0], leg_top + box[1], box[2], leg_top + box[3])
            if ly1 - ly0 < 12:
                return
            else:
                body = side.copy()
                body.paste((0, 0, 0, 0), (lx0, ly0, lx1, ly1))
                leg = side.crop((lx0, ly0, lx1, ly1))
                sock_row = alpha.crop((0, ly0 + 4, w, ly0 + 5)).getbbox()
                hip_x = (sock_row[0] + sock_row[2]) // 2 if sock_row else (lx0 + lx1) // 2
                hip = (hip_x, ly0 - 3)
                return {'body': body, 'leg': leg, 'pos': (lx0, ly0), 'hip': hip, 'leg_len': ly1 - hip[1]}
def split_arm(side):
    """从侧视图里抠出「前臂 + 手」那一块，好让它绕着肩关节单独摆动。"""
    x0, y0, x1, y1 = ARM_BOX
    if side.width < x1 or side.height < y1:
        return None
    else:
        arm = side.crop(ARM_BOX)
        if arm.split()[3].getbbox() is None:
            return None
        else:
            return {'arm': arm, 'pos': (x0, y0), 'pivot': ARM_PIVOT}
def _darken(img, f):
    r, g, b, a = img.split()
    f = float(f)
    return Image.merge('RGBA', (r.point(lambda v: int(v * f)), g.point(lambda v: int(v * f)), b.point(lambda v: int(v * f)), a))
def _leg_layer(leg, size, pos, hip, ang, lift):
    """把腿绕髋关节转 ang 度、再抬高 lift 像素，铺到整张画布上。"""
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    layer.alpha_composite(leg, pos)
    layer = layer.rotate(ang, resample=Image.BICUBIC, center=hip)
    if lift >= 1:
        out = Image.new('RGBA', size, (0, 0, 0, 0))
        out.paste(layer, (0, -int(round(lift))), layer)
        layer = out
    return layer
def build_walk_frames(side, parts, swing=SWING_WALK, lift=LIFT_WALK, n=WALK_FRAMES):
    """合成 n 帧走路循环（朝左，向右走时整体镜像）。"""
    size = side.size
    body, leg, pos, hip = (parts['body'], parts['leg'], parts['pos'], parts['hip'])
    back_leg = _darken(leg, 0.7)
    back_pos = (pos[0] + 6, pos[1])
    frames = []
    for i in range(n):
        ph = 2 * math.pi * i / n
        f = Image.new('RGBA', size, (0, 0, 0, 0))
        for img, p, ang, lf in [(back_leg, back_pos, math.sin(ph + math.pi), max(0.0, math.sin(ph + math.pi))), (body, pos, None, 0), (leg, pos, math.sin(ph), max(0.0, math.sin(ph)))]:
            if ang is None:
                f.alpha_composite(img)
            else:
                f.alpha_composite(_leg_layer(img, size, p, hip, swing * ang, lift * lf))
        frames.append(f)
    return frames
def bowl_image(size):
    """画一碗米饭（跟角色同一套配色）。"""
    w = max(8, int(size))
    h = int(w * 0.82)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((2, int(h * 0.3), w - 2, h - 2), fill=(28, 46, 100, 255), outline=(14, 22, 48, 255), width=2)
    d.ellipse((int(w * 0.14), int(h * 0.05), int(w * 0.86), int(h * 0.62)), fill=(253, 253, 255, 255), outline=(203, 212, 232, 255), width=1)
    return im
_WM_TRAY = 32769
_WM_HOTKEY = 786
_WM_HOTKEY_SET = 32770
_HOTKEY_ID = 1
_HOTKEY_MODS = {'ctrl': 2, 'control': 2, 'alt': 1, 'shift': 4, 'win': 8, 'super': 8, 'cmd': 8}
_HOTKEY_KEYS = {'space': 32, 'enter': 13, 'tab': 9, 'esc': 27, 'insert': 45, 'delete': 46, 'home': 36, 'end': 35, 'pageup': 33, 'pagedown': 34, 'up': 38, 'down': 40, 'left': 37, 'right': 39, '`': 192, '-': 189, '=': 187, '[': 219, ']': 221, ';': 186, "'": 222, ',': 188, '.': 190, '/': 191, '\\': 220}
def _key_code(name):
    if len(name) == 1 and name.isalnum():
        return ord(name.upper())
    else:
        m = re.fullmatch('f(\\d{1,2})', name)
        if m and 1 <= int(m.group(1)) <= 24:
                    return 111 + int(m.group(1))
        return _HOTKEY_KEYS.get(name)
def parse_hotkey(text):
    """把 \"ctrl+alt+K\" 这种写法解析成 (修饰键, 虚拟键码)；解析不了返回 None。"""
    parts = [p.strip().lower() for p in str(text or '').split('+')]
    parts = [p for p in parts if p]
    if len(parts) < 2:
        return
    else:
        mods, vk = (0, 0)
        for p in parts:
            if p in _HOTKEY_MODS:
                mods |= _HOTKEY_MODS[p]
            else:
                if not vk:
                    vk = _key_code(p) or 0
                else:
                    return
        return (mods, vk) if mods and vk else None
_HOTKEY_MODNAMES = {'Control_L': 'ctrl', 'Control_R': 'ctrl', 'Alt_L': 'alt', 'Alt_R': 'alt', 'Shift_L': 'shift', 'Shift_R': 'shift', 'Super_L': 'win', 'Super_R': 'win', 'Meta_L': 'win', 'Meta_R': 'win'}
_HOTKEY_SYM = {'minus': '-', 'equal': '=', 'bracketleft': '[', 'bracketright': ']', 'semicolon': ';', 'apostrophe': "'", 'comma': ',', 'period': '.', 'slash': '/', 'backslash': chr(92), 'grave': '`', 'Return': 'enter', 'KP_Enter': 'enter', 'Escape': 'esc', 'Tab': 'tab', 'space': 'space', 'Prior': 'pageup', 'Next': 'pagedown', 'Up': 'up', 'Down': 'down', 'Left': 'left', 'Right': 'right', 'Insert': 'insert', 'Delete': 'delete', 'Home': 'home', 'End': 'end'}
_PTT_VK = {'alt': 18, 'ctrl': 17, 'shift': 16, 'win': 91}
def _hotkey_name(keysym):
    """把 Tk 的 keysym 换成 parse_hotkey 认识的键名（认不出返回 None）。"""
    if len(keysym) == 1 and keysym.isalnum():
        return keysym.lower()
    else:
        if keysym[:1].upper() == 'F' and keysym[1:].isdigit() and (1 <= int(keysym[1:]) <= 24):
            return 'f' + keysym[1:]
        else:
            return _HOTKEY_SYM.get(keysym)
_NIM_ADD, _NIM_MODIFY, _NIM_DELETE = (0, 1, 2)
_NIF_MESSAGE, _NIF_ICON, _NIF_TIP = (1, 2, 4)
_WM_LBUTTONUP, _WM_RBUTTONUP, _WM_LBUTTONDBLCLK = (514, 517, 515)
_WM_DESTROY = 2
_TPM_RIGHTBUTTON, _TPM_RETURNCMD = (2, 256)
_MF_STRING, _MF_SEPARATOR, _MF_GRAYED = (0, 2048, 1)
_IMAGE_ICON = 1
_LR_LOADFROMFILE, _LR_DEFAULTSIZE = (16, 64)
_WS_EX_TOOLWINDOW = 128
_IDI_APPLICATION = 32512
TRAY_SHOW = 100
TRAY_HOTKEY = 101
TRAY_FAM = 102
TRAY_SET = 103
TRAY_MENU = [(TRAY_SHOW, '叫它出来 / 回到右下角'), (1, '躲到屏幕边边（露个头）'), (2, None), (TRAY_HOTKEY, '快捷命令输入框'), (TRAY_FAM, '对主人有多熟悉'), (3, '跟我聊天'), (4, '投喂一碗米饭'), (5, '一起猜拳'), (6, None), (7, '回到右下角'), (8, '退出应用')]
class _NOTIFYICONDATAW(ctypes.Structure):
    _fields_ = [('cbSize', wintypes.DWORD), ('hWnd', wintypes.HWND), ('uID', wintypes.UINT), ('uFlags', wintypes.UINT), ('uCallbackMessage', wintypes.UINT), ('hIcon', wintypes.HICON), ('szTip', wintypes.WCHAR * 64), ('dwState', wintypes.DWORD), ('dwStateMask', wintypes.DWORD), ('szInfo', wintypes.WCHAR * 256), ('uVersion', wintypes.UINT), ('szInfoTitle', wintypes.WCHAR * 64), ('dwInfoFlags', wintypes.DWORD)]
class _WNDCLASSW(ctypes.Structure):
    _fields_ = [('style', wintypes.UINT), ('lpfnWndProc', ctypes.c_void_p), ('cbClsExtra', ctypes.c_int), ('cbWndExtra', ctypes.c_int), ('hInstance', wintypes.HINSTANCE), ('hIcon', wintypes.HICON), ('hCursor', ctypes.c_void_p), ('hbrBackground', ctypes.c_void_p), ('lpszMenuName', wintypes.LPCWSTR), ('lpszClassName', wintypes.LPCWSTR)]
_WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
_user32.CreateWindowExW.restype = wintypes.HWND
_user32.CreateWindowExW.argtypes = [wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, ctypes.c_void_p]
_user32.DefWindowProcW.restype = ctypes.c_ssize_t
_user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
_user32.CreatePopupMenu.restype = wintypes.HMENU
_user32.AppendMenuW.argtypes = [wintypes.HMENU, wintypes.UINT, wintypes.WPARAM, wintypes.LPCWSTR]
_user32.GetMenuItemCount.argtypes = [wintypes.HMENU]
_user32.TrackPopupMenu.restype = wintypes.UINT
_user32.TrackPopupMenu.argtypes = [wintypes.HMENU, wintypes.UINT, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.HWND, ctypes.c_void_p]
_user32.SetForegroundWindow.argtypes = [wintypes.HWND]
_user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
_user32.DestroyMenu.argtypes = [wintypes.HMENU]
_user32.DestroyIcon.argtypes = [wintypes.HICON]
_user32.LoadImageW.restype = wintypes.HANDLE
_user32.LoadImageW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT, ctypes.c_int, ctypes.c_int, wintypes.UINT]
_user32.LoadIconW.restype = wintypes.HICON
_user32.LoadIconW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
_kernel32.GetModuleHandleW.restype = wintypes.HMODULE
_kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
class TrayIcon:
    """在系统托盘放一个小图标，右键弹菜单。\n\nmenu 是 [(命令ID, 文字) ...]，文字为 None 表示分隔线。\n点菜单时把命令 ID 丢进 queue，交给主线程（tk 的 tick）去执行 ——\n这样就不会在别的线程里碰 tkinter。\n"""
    def __init__(self, icon_path, tooltip, menu, queue_, hotkey=None):
        self.icon_path = icon_path
        self.tooltip = tooltip
        self.menu = menu
        self.queue = queue_
        self.hwnd = None
        self.hicon = None
        self.ok = False
        self.hotkey = hotkey
        self._proc = None
        self._nid = None
        self._tip_lock = threading.Lock()
        self._cls = 'WhalePetTrayWnd'
    def set_tooltip(self, text):
        """更新鼠标悬浮小图标时显示的文字（szTip 最多 63 个字）。"""
        text = str(text) / 63
        with self._tip_lock:
            if text == self.tooltip:
                return
            else:
                self.tooltip = text
                if self._nid is not None:
                    try:
                        self._nid.szTip = text
                        ctypes.windll.shell32.Shell_NotifyIconW(_NIM_MODIFY, ctypes.byref(self._nid))
                    except Exception:
                        pass
    def start(self):
        threading.Thread(target=self._run, daemon=True).start()
    def stop(self):
        if self._nid is not None:
            try:
                ctypes.windll.shell32.Shell_NotifyIconW(_NIM_DELETE, ctypes.byref(self._nid))
            except Exception:
                pass
        if self.hwnd:
            ctypes.windll.user32.PostMessageW(self.hwnd, _WM_DESTROY, 0, 0)
    def set_hotkey(self, hk):
        """换热键：必须交给托盘线程去做（Windows 的热键是跟着线程的）。"""
        self.hotkey = hk
        if self.hwnd:
            ctypes.windll.user32.PostMessageW(self.hwnd, _WM_HOTKEY_SET, 0, 0)
    def _reg_hotkey(self):
        user32 = ctypes.windll.user32
        try:
            user32.UnregisterHotKey(self.hwnd, _HOTKEY_ID)
        except Exception:
            pass
        ok = True
        if self.hotkey:
            ok = bool(user32.RegisterHotKey(self.hwnd, _HOTKEY_ID, self.hotkey[0], self.hotkey[1]))
        self.queue.put(('hotkey', ok))
    def _run(self):
        user32, kernel32 = (_user32, _kernel32)
        self._proc = _WNDPROC(self._on_message)
        wc = _WNDCLASSW()
        wc.lpfnWndProc = ctypes.cast(self._proc, ctypes.c_void_p)
        wc.hInstance = kernel32.GetModuleHandleW(None)
        wc.lpszClassName = self._cls
        if not user32.RegisterClassW(ctypes.byref(wc)):
            return
        else:
            self.hwnd = user32.CreateWindowExW(_WS_EX_TOOLWINDOW, self._cls, APP_NAME, 0, 0, 0, 0, 0, None, None, wc.hInstance, None)
            if not self.hwnd:
                return
            else:
                self.hicon = user32.LoadImageW(None, self.icon_path, _IMAGE_ICON, 0, 0, _LR_LOADFROMFILE | _LR_DEFAULTSIZE)
                if not self.hicon:
                    self.hicon = user32.LoadIconW(None, ctypes.cast(ctypes.c_void_p(_IDI_APPLICATION), wintypes.LPCWSTR))
                nid = _NOTIFYICONDATAW()
                nid.cbSize = ctypes.sizeof(_NOTIFYICONDATAW)
                nid.hWnd = self.hwnd
                nid.uID = 1
                nid.uFlags = _NIF_MESSAGE | _NIF_ICON | _NIF_TIP
                nid.uCallbackMessage = _WM_TRAY
                nid.hIcon = self.hicon
                nid.szTip = self.tooltip[:63]
                self._nid = nid
                self.ok = bool(ctypes.windll.shell32.Shell_NotifyIconW(_NIM_ADD, ctypes.byref(nid)))
                if self.hotkey:
                    self._reg_hotkey()
                msg = wintypes.MSG()
                if user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageW(ctypes.byref(msg))
                ctypes.windll.shell32.Shell_NotifyIconW(_NIM_DELETE, ctypes.byref(nid))
                if self.hicon:
                    user32.DestroyIcon(self.hicon)
    def _build_menu(self):
        """建好菜单并返回 (菜单句柄, 条目数)，方便测试。"""
        user32 = ctypes.windll.user32
        hmenu = user32.CreatePopupMenu()
        for cid, label in self.menu:
            if label is None:
                user32.AppendMenuW(hmenu, _MF_SEPARATOR, 0, None)
            else:
                if cid == 'info':
                    user32.AppendMenuW(hmenu, _MF_STRING | _MF_GRAYED, 0, label)
                else:
                    user32.AppendMenuW(hmenu, _MF_STRING, cid, label)
        return (hmenu, user32.GetMenuItemCount(hmenu))
    def _on_message(self, hwnd, msg, wparam, lparam):
        user32 = ctypes.windll.user32
        if msg == _WM_HOTKEY_SET:
            self._reg_hotkey()
            return 0
        else:
            if msg == _WM_HOTKEY:
                self.queue.put(('tray', TRAY_HOTKEY))
                return 0
            else:
                if msg == _WM_TRAY:
                    if lparam == _WM_RBUTTONUP:
                        self._popup()
                        return 0
                    else:
                        if lparam in (_WM_LBUTTONUP, _WM_LBUTTONDBLCLK):
                            self.queue.put(('tray', TRAY_SHOW))
                        return 0
                else:
                    if msg == _WM_DESTROY:
                        user32.PostQuitMessage(0)
                        return 0
                    else:
                        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
    def _popup(self):
        user32 = ctypes.windll.user32
        hmenu, count = self._build_menu()
        if count <= 0:
            user32.DestroyMenu(hmenu)
        else:
            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))
            user32.SetForegroundWindow(self.hwnd)
            cmd = user32.TrackPopupMenu(hmenu, _TPM_RIGHTBUTTON | _TPM_RETURNCMD, pt.x, pt.y, 0, self.hwnd, None)
            user32.PostMessageW(self.hwnd, 0, 0, 0)
            user32.DestroyMenu(hmenu)
            if cmd:
                self.queue.put(('tray', cmd))
_NO_WINDOW = 134217728
_PS_EXE = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe')
_TTS_SCRIPT = '\n$ErrorActionPreference = \'Stop\'\n[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\nAdd-Type -AssemblyName System.Speech\n$sp = New-Object System.Speech.Synthesis.SpeechSynthesizer\ntry {\n  $zh = $sp.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -like \'zh*\' } |\n        Select-Object -First 1\n  if ($zh) { $sp.SelectVoice($zh.VoiceInfo.Name) }\n} catch { }\n$sp.add_SpeakCompleted({ [Console]::Out.WriteLine(\'DONE\'); [Console]::Out.Flush() })\nwhile ($true) {\n  $line = [Console]::In.ReadLine()\n  if ($line -eq $null) { break }\n  try {\n    if ($line.StartsWith(\'SAY \')) {\n      $t = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($line.Substring(4)))\n      $sp.SpeakAsyncCancelAll()\n      $sp.SpeakAsync($t) | Out-Null\n    } elseif ($line -eq \'STOP\') {\n      $sp.SpeakAsyncCancelAll()\n    }\n  } catch { }\n}\n$sp.Dispose()\n'
_ASR_SCRIPT = '\n$ErrorActionPreference = \'Stop\'\n[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\nAdd-Type -AssemblyName System.Speech\n$inv = [Globalization.CultureInfo]::InvariantCulture\n$infos = [System.Speech.Recognition.SpeechRecognitionEngine]::InstalledRecognizers()\nif (-not $infos -or $infos.Count -eq 0) {\n  [Console]::Out.WriteLine(\'ERR 系统里没有可用的语音识别引擎\'); [Console]::Out.Flush(); exit 1\n}\n$pick = $infos | Where-Object { $_.Culture.Name -like \'zh*\' } | Select-Object -First 1\nif (-not $pick) { $pick = $infos[0] }\n$rec = New-Object System.Speech.Recognition.SpeechRecognitionEngine($pick.Id)\n$choices = New-Object System.Speech.Recognition.Choices\n@(__WORDS__) | ForEach-Object { $choices.Add($_) }\n$gb = New-Object System.Speech.Recognition.GrammarBuilder\n$gb.Append($choices)\n$wakeG = New-Object System.Speech.Recognition.Grammar($gb)\n$dictG = New-Object System.Speech.Recognition.DictationGrammar\n$rec.LoadGrammar($wakeG)\n$rec.LoadGrammar($dictG)\n$rec.add_SpeechRecognized({\n  param($sender, $e)\n  try {\n    $tag = \'DICT\'\n    if ($e.Result.Grammar -eq $wakeG) { $tag = \'WAKE\' }\n    $c = $e.Result.Confidence.ToString($inv)\n    $b = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($e.Result.Text))\n    [Console]::Out.WriteLine($tag + \' \' + $c + \' \' + $b)\n    [Console]::Out.Flush()\n  } catch { }\n})\ntry { $rec.SetInputToDefaultAudioDevice() } catch {\n  [Console]::Out.WriteLine(\'ERR 找不到麦克风：\' + $_.Exception.Message)\n  [Console]::Out.Flush(); exit 1\n}\n$rec.RecognizeAsync([System.Speech.Recognition.RecognizeMode]::Multiple)\n[Console]::Out.WriteLine(\'READY\')\n[Console]::Out.Flush()\nwhile ($true) {\n  $line = [Console]::In.ReadLine()\n  if ($line -eq $null) { break }\n  try {\n    if ($line -eq \'PAUSE\') { $rec.RecognizeAsyncCancel() }\n    elseif ($line -eq \'RESUME\') { $rec.RecognizeAsync([System.Speech.Recognition.RecognizeMode]::Multiple) }\n    elseif ($line -eq \'QUIT\') { break }\n  } catch { }\n}\ntry { $rec.Dispose() } catch { }\n'
def _voice_clean(text):
    """要念出来的文字先清理一下：去掉 emoji、颜文字、markdown 符号。"""
    t = str(text or '')
    t = re.sub('[\\U0001F000-\\U0001FAFF\\u2600-\\u27BF\\u2B00-\\u2BFF\\uFE0F]', '', t)
    t = re.sub('[（(][^）)]{0,14}[）)]', '', t)
    t = re.sub('(?i)https?://\\S+', '链接', t)
    t = t.replace('～', '，').replace('~', '，')
    for ch in '*#`>[]':
        t = t.replace(ch, '')
    return re.sub('\\s+', ' ', t).strip()[:180]
try:
    import asyncio
    import edge_tts
    EDGE_TTS_OK = True
except Exception:
    asyncio = None
    edge_tts = None
    EDGE_TTS_OK = False
TTS_CACHE_DIR = os.path.join(data_dir(), '语音缓存')
DEFAULT_TTS_VOICE = 'zh-CN-XiaoxiaoNeural'
def _mci_send(cmd):
    """发一条 MCI 命令，返回 (错误码, 返回字符串)。"""
    try:
        buf = ctypes.create_unicode_buffer(256)
        err = ctypes.windll.winmm.mciSendStringW(cmd, buf, 255, 0)
        return (err, buf.value)
    except Exception:
        return (1, '')
def _short_path(path):
    """取 8.3 短路径（老 API 对中文路径不友好时用）。取不到就原样返回。"""
    try:
        buf = ctypes.create_unicode_buffer(600)
        n = ctypes.windll.kernel32.GetShortPathNameW(str(path), buf, 600)
        return buf.value if n else path
    except Exception:
        return path
ASR_MS_OWNER = 'pkufool'
ASR_MS_NAME = 'sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20'
ASR_FILES = ['tokens.txt', 'encoder-epoch-99-avg-1.int8.onnx', 'decoder-epoch-99-avg-1.int8.onnx', 'joiner-epoch-99-avg-1.int8.onnx']
ASR_MODEL_DIR = os.path.join(data_dir(), '语音模型', ASR_MS_NAME)
ASR_DEPS_OK = all((importlib.util.find_spec(m) is not None for m in ('sherpa_onnx', 'sounddevice', 'numpy')))
def _urlopen_any(req, timeout=30):
    """请求 URL：先按系统证书校验；证书链有问题（有些 CDN 不全）再退回不校验重试一次。"""
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.URLError as e:
        msg = str(e).upper()
        if ('CERTIFICATE' not in msg) and ('SSL' not in msg):
            raise
        return urllib.request.urlopen(req, timeout=timeout, context=ssl._create_unverified_context())
def _ms_file_url(path):
    return f'https://modelscope.cn/api/v1/models/{ASR_MS_OWNER}/{ASR_MS_NAME}/repo?Revision=master&FilePath={urllib.parse.quote(path)}'
def asr_model_ready():
    return all((os.path.isfile(os.path.join(ASR_MODEL_DIR, f)) and os.path.getsize(os.path.join(ASR_MODEL_DIR, f)) > 0 for f in ASR_FILES))
def ensure_asr_model(progress=None):
    """把本地识别模型下到位（缺哪个下哪个）。返回 (ok, 错误信息)。"""
    try:
        os.makedirs(ASR_MODEL_DIR, exist_ok=True)
    except OSError as e:
        return (False, f'建目录失败：{e}')
    todo = [f for f in ASR_FILES if not (os.path.isfile(os.path.join(ASR_MODEL_DIR, f)) and os.path.getsize(os.path.join(ASR_MODEL_DIR, f)) > 0)]
    for i, f in enumerate(todo, 1):
        dst = os.path.join(ASR_MODEL_DIR, f)
        tmp = dst + '.part'
        try:
            req = urllib.request.Request(_ms_file_url(f), headers={'User-Agent': UPDATE_USER_AGENT})
            with _urlopen_any(req, timeout=180) as r, open(tmp, 'wb') as fp:
                shutil.copyfileobj(r, fp, 1024 * 512)
            os.replace(tmp, dst)
        except Exception as e:
            try:
                os.remove(tmp)
            except OSError:
                pass
            return (False, f'下载 {f} 失败：{e}')
        if progress:
            try:
                progress(i, len(todo), f)
            except Exception:
                pass
    return (True, '')
def _asr_onnx_files():
    """从模型目录自动找 encoder / decoder / joiner / tokens（兼容 int8 与非 int8 命名）。"""
    if not os.path.isdir(ASR_MODEL_DIR):
        return None
    names = os.listdir(ASR_MODEL_DIR)
    def pick(kw):
        cands = [n for n in names if n.lower().endswith('.onnx') and kw in n.lower()]
        if not cands:
            return None
        cands.sort(key=lambda n: (0 if 'int8' in n.lower() else 1, len(n)))
        return os.path.join(ASR_MODEL_DIR, cands[0])
    tokens = os.path.join(ASR_MODEL_DIR, 'tokens.txt')
    enc, dec, joi = pick('encoder'), pick('decoder'), pick('joiner')
    if not (os.path.isfile(tokens) and enc and dec and joi):
        return None
    return (enc, dec, joi, tokens)
class FunASRBox:
    """本地流式语音识别（sherpa-onnx + sounddevice）。事件格式和 SAPI 那条路一致，便于无缝切换。\n\n两种触发：喊唤醒词后连续听（arm），或按住热键说话（set_ptt，松开即出结果）。\n"""
    def __init__(self, events):
        self.events = events
        self.rec = None
        self._stream = None
        self._thread = None
        self.running = False
        self.armed = False
        self.ptt = False
        self.paused = False
        self.listening = False
        self.last_error = ''
    def load(self):
        if self.rec is not None:
            return True
        files = _asr_onnx_files()
        if not files:
            self.last_error = '还没下好语音模型'
            return False
        enc, dec, joi, tok = files
        try:
            import sherpa_onnx
            self.rec = sherpa_onnx.OnlineRecognizer.from_transducer(tokens=tok, encoder=enc, decoder=dec, joiner=joi, num_threads=2, sample_rate=16000, feature_dim=80, enable_endpoint_detection=True, rule1_min_trailing_silence=2.4, rule2_min_trailing_silence=1.2, rule3_min_utterance_length=20)
        except Exception as e:
            self.last_error = '加载语音模型失败：' + str(e)
            return False
        return True
    def start(self, words=None):
        if self.listening:
            return True
        if not ASR_DEPS_OK:
            self.last_error = '缺依赖（sherpa-onnx / sounddevice / numpy）'
            return False
        if not self.load():
            return False
        self.running = True
        self.listening = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        self.events.put(('v_ready',))
        return True
    def _loop(self):
        import sounddevice as sd
        try:
            self._stream = sd.InputStream(samplerate=16000, channels=1, dtype='float32', blocksize=1600)
            self._stream.start()
        except Exception as e:
            self.listening = False
            self.running = False
            self.events.put(('v_error', '麦克风打不开：' + str(e)))
            self.events.put(('v_closed',))
            return
        st = self.rec.create_stream()
        buf = ''
        try:
            while self.running:
                try:
                    data, _ov = self._stream.read(1600)
                except Exception:
                    break
                if self.paused or not (self.ptt or self.armed):
                    continue
                st.accept_waveform(16000, data[:, 0])
                while self.rec.is_ready(st):
                    self.rec.decode_stream(st)
                text = self.rec.get_result(st).strip()
                if text and text != buf:
                    buf = text
                    self.events.put(('v_hyp', text))
                if self.rec.is_endpoint(st):
                    if buf:
                        self.events.put(('v_heard', 'DICT', 1.0, buf))
                    self.rec.reset(st)
                    buf = ''
                    self.armed = False
        except Exception as e:
            self.events.put(('v_error', '识别出错：' + str(e)))
        finally:
            try:
                if self._stream is not None:
                    self._stream.stop()
                    self._stream.close()
            except Exception:
                pass
            self._stream = None
            self.listening = False
            self.events.put(('v_closed',))
    def set_ptt(self, on):
        self.ptt = bool(on)
    def arm(self, on=True):
        self.armed = bool(on)
    def pause(self):
        self.paused = True
    def resume(self):
        self.paused = False
    def stop(self):
        self.running = False
        self.listening = False
        self.armed = False
        self.ptt = False
        try:
            if self._stream is not None:
                self._stream.stop()
        except Exception:
            pass
class VoiceBox:
    """朗读 + 语音识别。\n\n朗读：优先用 Edge TTS（微软 Edge 在线语音，音色自然），合成好的 mp3 缓存在本地\n「语音缓存」里重复用，播放走系统 MCI，不需要额外播放器；要是没装 edge-tts 或者\n合成失败，就退回 Windows 自带的 System.Speech。\n听：走 Windows 自带的 System.Speech（后台常驻一个 PowerShell 进程）。\n"""
    def __init__(self, events, cfg=None):
        self.events = events
        self.cfg = cfg if isinstance(cfg, dict) else {}
        self.tts = None
        self.asr = None
        self.speaking = False
        self.listening = False
        self.last_error = ''
        self._ps_ok = os.path.isfile(_PS_EXE)
        self._edge_gen = 0
        self._mci_alias = 'whale_tts'
        self._funasr = None
    def _spawn(self, script):
        enc = base64.b64encode(script.encode('utf-16-le')).decode('ascii')
        return subprocess.Popen([_PS_EXE, '-NoProfile', '-NoLogo', '-NonInteractive', '-EncodedCommand', enc], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=_NO_WINDOW, text=True, encoding='utf-8', errors='ignore', bufsize=1)
    @staticmethod
    def _write(proc, line):
        if not proc or proc.poll() is not None:
            return False
        else:
            try:
                proc.stdin.write(line + '\n')
                proc.stdin.flush()
            except Exception:
                return False
            return True
    def start_tts(self):
        if self.tts and self.tts.poll() is None:
            return True
        else:
            if not self._ps_ok:
                self.last_error = '找不到 powershell.exe'
                return False
            else:
                try:
                    self.tts = self._spawn(_TTS_SCRIPT)
                except Exception as e:
                    self.last_error = '朗读起不来：' + str(e)
                    return False
                threading.Thread(target=self._read_tts, args=(self.tts,), daemon=True).start()
                return True
    def _read_tts(self, proc):
        try:
            for line in proc.stdout:
                if line.strip() == 'DONE':
                    self.speaking = False
                    self.events.put(('v_done',))
        except Exception:
            return None
    def tts_engine(self):
        """当前朗读引擎：edge（默认）或 sapi。"""
        return str(self.cfg.get('tts_engine') or 'edge').lower()
    def tts_voice(self):
        return str(self.cfg.get('tts_voice') or DEFAULT_TTS_VOICE).strip() or DEFAULT_TTS_VOICE
    def _tts_cache_path(self, text, voice):
        key = hashlib.sha1((str(voice) + '|' + text).encode('utf-8')).hexdigest()
        return os.path.join(TTS_CACHE_DIR, key + '.mp3')
    def _edge_synth(self, text, voice):
        """用 Edge TTS 合成到缓存文件，返回 mp3 路径（失败返回 None）。"""
        if not EDGE_TTS_OK:
            return None
        path = self._tts_cache_path(text, voice)
        try:
            os.makedirs(TTS_CACHE_DIR, exist_ok=True)
        except OSError:
            return None
        tmp = path + '.part'
        async def run():
            await edge_tts.Communicate(text, voice).save(tmp)
        try:
            asyncio.run(run())
        except Exception as e:
            self.last_error = 'Edge 合成失败：' + str(e)
            try:
                os.remove(tmp)
            except OSError:
                pass
            return None
        if os.path.isfile(tmp) and os.path.getsize(tmp) > 0:
            try:
                os.replace(tmp, path)
            except OSError:
                return tmp
            return path
        return None
    def _play_mp3(self, path, gen):
        """用系统 MCI 播放 mp3；gen 变了（被打断）就停下。"""
        alias = self._mci_alias
        cands = [path]
        sp = _short_path(path)
        if sp != path:
            cands.append(sp)
        opened = False
        for cand in cands:
            _mci_send('close ' + alias)
            err, _ = _mci_send(f'open "{cand}" type mpegvideo alias {alias}')
            if not err:
                opened = True
                break
        if not opened:
            try:
                tmp = os.path.join(tempfile.gettempdir(), 'whale_tts_tmp.mp3')
                shutil.copyfile(path, tmp)
                _mci_send('close ' + alias)
                err, _ = _mci_send(f'open "{tmp}" type mpegvideo alias {alias}')
                opened = not err
            except Exception:
                opened = False
        if not opened:
            return False
        err, _ = _mci_send('play ' + alias)
        if err:
            _mci_send('close ' + alias)
            return False
        while gen == self._edge_gen:
            _err, mode = _mci_send('status %s mode' % alias)
            if mode.strip().lower() != 'playing':
                break
            time.sleep(0.06)
        _mci_send('stop ' + alias)
        _mci_send('close ' + alias)
        return True
    def _edge_worker(self, text, voice, gen):
        """后台线程：缓存命中就直接放，没有才合成，再放；失败退回 SAPI。"""
        path = None
        try:
            cand = self._tts_cache_path(text, voice)
            if os.path.isfile(cand) and os.path.getsize(cand) > 0:
                path = cand
            else:
                path = self._edge_synth(text, voice)
        except Exception as e:
            self.last_error = 'Edge 朗读失败：' + str(e)
            path = None
        if gen != self._edge_gen:
            return
        if path:
            self._play_mp3(path, gen)
            if gen == self._edge_gen:
                self.speaking = False
                self.events.put(('v_done',))
            return
        ok = False
        try:
            if self.start_tts():
                self._write(self.tts, 'SAY ' + base64.b64encode(text.encode('utf-8')).decode('ascii'))
                ok = True
        except Exception:
            ok = False
        if (not ok) and gen == self._edge_gen:
            self.speaking = False
            self.events.put(('v_done',))
    def speak(self, text):
        text = _voice_clean(text)
        if not text:
            return False
        if self.tts_engine() == 'edge' and EDGE_TTS_OK:
            self._edge_gen += 1
            gen = self._edge_gen
            self.speaking = True
            self.pause_asr()
            threading.Thread(target=self._edge_worker, args=(text, self.tts_voice(), gen), daemon=True).start()
            return True
        if not self.start_tts():
            return False
        else:
            self.speaking = True
            self.pause_asr()
            self._write(self.tts, 'SAY ' + base64.b64encode(text.encode('utf-8')).decode('ascii'))
            return True
    def stop_speak(self):
        self.speaking = False
        self._edge_gen += 1
        _mci_send('stop ' + self._mci_alias)
        _mci_send('close ' + self._mci_alias)
        self._write(self.tts, 'STOP')
        self.resume_asr()
    def _fa(self):
        """当前若选的是本地 FunASR 识别，就返回它的实例（否则 None）。"""
        if str(self.cfg.get('asr_engine') or 'sapi') != 'funasr':
            return None
        if self._funasr is None:
            self._funasr = FunASRBox(self.events)
        return self._funasr
    def start_asr(self, words):
        fa = self._fa()
        if fa is not None:
            ok = fa.start(words)
            self.listening = bool(ok)
            if not ok:
                self.last_error = fa.last_error
            return ok
        if self.asr and self.asr.poll() is None:
            return True
        else:
            if not self._ps_ok:
                self.last_error = '找不到 powershell.exe'
                return False
            else:
                lit = ', '.join(('\'' + str(w).replace('\'', '\'\'') + '\'' for w in words))
                try:
                    self.asr = self._spawn(_ASR_SCRIPT.replace('__WORDS__', lit))
                except Exception as e:
                    self.last_error = '识别起不来：' + str(e)
                    return False
                self.listening = True
                threading.Thread(target=self._read_asr, args=(self.asr,), daemon=True).start()
                return True
    def _read_asr(self, proc):
        try:
            for line in proc.stdout:
                line = line.strip()
                if not line:
                    continue
                else:
                    if line == 'READY':
                        self.events.put(('v_ready',))
                    else:
                        if line.startswith('ERR'):
                            self.events.put(('v_error', line[3:].strip()))
                            continue
                        else:
                            tag, _, rest = line.partition(' ')
                            conf, _, b64 = rest.partition(' ')
                            try:
                                text = base64.b64decode(b64).decode('utf-8', 'ignore')
                                conf = float(conf)
                            except Exception:
                                pass
                            else:
                                self.events.put(('v_heard', tag, conf, text))
        except Exception:
            pass
        finally:
            self.listening = False
            self.events.put(('v_closed',))
    def stop_asr(self):
        if self._funasr is not None:
            self._funasr.stop()
        self.listening = False
        self._write(self.asr, 'QUIT')
        self.asr = None
    def pause_asr(self):
        if self._funasr is not None:
            self._funasr.pause()
        if self.listening:
            self._write(self.asr, 'PAUSE')
    def resume_asr(self):
        if self._funasr is not None:
            self._funasr.resume()
        if self.listening:
            self._write(self.asr, 'RESUME')
    def set_ptt(self, on):
        if self._funasr is not None:
            self._funasr.set_ptt(on)
    def arm(self, on=True):
        if self._funasr is not None:
            self._funasr.arm(on)
    def close(self):
        self.stop_asr()
        if self._funasr is not None:
            self._funasr.stop()
        self._write(self.tts, 'QUIT')
        self.tts = None
class WhalePet:
    def __init__(self):
        self.root = TkinterDnD.Tk() if DND_OK else tk.Tk()
        self.root.title(APP_NAME)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        try:
            self.root.attributes('-transparentcolor', KEY)
        except tk.TclError:
            pass
        try:
            self.root.iconbitmap(default=res_path('app.ico'))
        except Exception:
            pass
        self.base = {'front': self._load('pet_front.png'), 'side': self._load('pet_side.png'), 'back': self._load('pet_back.png')}
        self.parts = split_leg(self.base['side'])
        self.arm_parts = split_arm(self.base['side'])
        self.scale = 190.0 / BASE_H
        self.pose = 'front'
        self.flip = False
        self.cache = {}
        self.squash_cache = {}
        self.bowl_cache = {}
        self._expr_cache = {}
        self._hide_cache = {}
        self.photo = None
        self.sprite_size = (1, 1)
        self.canvas = tk.Canvas(self.root, width=1, height=1, bg=KEY, highlightthickness=0)
        self.canvas.pack()
        self.sprite = self.canvas.create_image(0, 0, image=None)
        self.bowl_item = None
        self.walk = {}
        self.walk_photo = {}
        self.arm_photo = {'L': [], 'R': []}
        self.arm_item = self.canvas.create_image(0, 0, image=None, state='hidden')
        self._layout()
        self.edge = None
        self.edge_frac = EDGE_HIDE
        self._normal_geo = None
        sw, sh = self.screen()
        self.cx = float(sw - self.canvas_size[0])
        self.foot = float(sh - 40)
        self._apply_geometry()
        self.state = 'idle'
        self.follow = tk.BooleanVar(value=False)
        self.sleeping = False
        self.deep_sleep = False
        self.quiet_mode = tk.BooleanVar(value=True)
        self.activity = ('', '')
        self.dev_seen = None
        self.idle_sec = 0.0
        self.fullscreen = False
        self.quiet = False
        self.last_app_talk = 0.0
        self.last_follow_talk = 0.0
        self.follow_said = False
        self.reminders = []
        self.sad_until = 0.0
        self.emote_until = 0.0
        self.expr_name = None
        self.expr_photo = None
        self.expr_until = 0.0
        self.mood_seen = None
        self.mood_show = tk.BooleanVar(value=True)
        self.mood_win = None
        self.mood_canvas = None
        self.mood_item = None
        self.mood_photo = None
        self.mood_key = None
        self.mood_last = None
        self.mood_until = 0.0
        self.mood_next = 0.0
        self._icon_cache = {}
        self.happy_until = 0.0
        self.grumpy_until = 0.0
        self.eating = False
        self.eat_until = 0.0
        self.eat_gen = 0
        self.force_mood = None
        self.force_until = 0.0
        self.turning = False
        self.turn_id = 0
        self._peek_job = None
        self.t = 0
        self.bob = 0.0
        self.hop = 0.0
        self.wiggle = 0.0
        self.phase = 0.0
        self.drag_phase = 0.0
        self.drag_talk = 0
        self.drag_dir = 1
        self.drag_speed = 0.0
        self.drag_shake = 0.0
        self.arm_phase = 0.0
        self.arm_show = False
        self.walk_face = 'L'
        self.walk_show = False
        self._last_line = None
        self.gesturing = False
        self.chew = 0
        self.walk_dir = (-1)
        self.idle_timer = random.randint(60, 140)
        self.target_cx = self.cx
        self.target_y = self.foot
        self.dragging = False
        self._press = None
        self._pull_out = False
        self._click_job = None
        self._dbl = False
        self.bubble = None
        self.bubble_job = None
        self.chat = None
        self.rps = None
        self.score = [0, 0]
        self.cfg = load_config()
        if not os.path.exists(CONFIG_PATH):
            save_config(self.cfg)
        self.history = []
        self.pending = False
        self.stream_buf = ''
        self._pending_msg = ''
        self._q = queue.Queue()
        self.history_box = None
        self.chat_input = None
        self.chat_status = None
        self.send_btn = None
        self.settings_win = None
        self.settings_lbl = None
        self.attach_bar = None
        self.attach_lbl = None
        self.attachments = []
        self._had_images = False
        self._image_retry = False
        self._last_msgs = None
        self.tools_on = True
        self._tool_retry = False
        self._tool_rounds = 0
        self.pomo_end = None
        self.pomo_label = ''
        self.last_mouse = self.root.winfo_pointerxy()
        self.still = 0
        self.save_data = load_state()
        if not self.save_data.get('hunger_at'):
            self.save_data['hunger'] = hunger_of(self.save_data.get('last_feed'))
            self.save_data['hunger_at'] = time.time()
            save_state(self.save_data)
        self._hunger_saved = float(self.save_data.get('hunger') or 0.0)
        self.eyes_closed = False
        self.blink_t = 0
        self._fam_cache = (0.0, 0.0, {})
        _st = self.save_data
        _today = date.today().isoformat()
        if _st.get('last_day') != _today:
            _st['last_day'] = _today
            _st['days'] = int(_st.get('days', 0)) + 1
            save_state(_st)
        self._bind()
        self.voice_q = queue.Queue()
        self.voice = VoiceBox(self.voice_q, self.cfg)
        self.tts_engine = tk.StringVar(value=str(self.cfg.get('tts_engine') or 'edge'))
        self.tts_voice = tk.StringVar(value=str(self.cfg.get('tts_voice') or DEFAULT_TTS_VOICE))
        self.asr_engine = tk.StringVar(value=str(self.cfg.get('asr_engine') or 'sapi'))
        self.asr_ptt_key = tk.StringVar(value=str(self.cfg.get('asr_ptt_key') or ''))
        self._ptt_down = False
        self._hyp_at = 0.0
        self._asr_dl = False
        self._asr_result = None
        self.asr_status = None
        self.cua_on = tk.BooleanVar(value=bool(self.cfg.get('cua_on', False)))
        self.cua_ask = tk.StringVar(value=str(self.cfg.get('cua_ask') or 'each'))
        self.cua_ask_minutes = tk.IntVar(value=int(self.cfg.get('cua_ask_minutes', 30) or 30))
        self.cua_max_steps = tk.IntVar(value=int(self.cfg.get('cua_max_steps', 20) or 20))
        self.cua_busy = False
        self.cua_win = None
        self._cua_stop = False
        self._cua_goal = ''
        self._cua_until = 0.0
        self._cua_last_pos = (0, 0)
        self._cua_ask_ev = None
        self._cua_ask_ok = False
        self.voice_wake = tk.BooleanVar(value=bool(self.cfg.get('voice_wake')))
        self.voice_chat = tk.BooleanVar(value=bool(self.cfg.get('voice_chat')))
        self.voice_speak = tk.BooleanVar(value=bool(self.cfg.get('voice_speak')))
        self.voice_arm_until = 0.0
        self._speak_reply = False
        self.online_var = tk.BooleanVar(value=str(self.cfg.get('mode', 'local')) == 'online')
        self.warm_busy = False
        self.ai_brain = tk.BooleanVar(value=bool(self.cfg.get('ai_brain', True)))
        self.scene_play = tk.BooleanVar(value=bool(self.cfg.get('scene_play', True)))
        self.decide_busy = False
        self.decide_next = 0.0
        self.brain_fails = 0
        self.ops = []
        self.was_away = False
        self.ask_on = tk.BooleanVar(value=bool(self.cfg.get('proactive', False)))
        self.ask_gap = tk.IntVar(value=int(self.cfg.get('proactive_gap', 300)))
        self.skip_familiar = tk.BooleanVar(value=bool(self.cfg.get('proactive_skip_familiar', False)))
        self.ask_next = time.time() + 120
        self.ask_busy = False
        self.ask_win = None
        self.ask_auto = None
        self._preset_seen = {}
        self.quick_on = tk.BooleanVar(value=bool(self.cfg.get('quick_cmd', True)))
        self.quick_box = None
        self.quick_entry = None
        self.quick_note = None
        self.bg_q = []
        self.bg_busy = False
        self.hotkey_changing = False
        self.app_set_win = None
        self.edge_snap = tk.BooleanVar(value=bool(self.cfg.get('edge_snap', True)))
        self.mood_decay_on = tk.BooleanVar(value=bool(self.cfg.get('mood_decay_on', True)))
        self.mood_decay_var = tk.IntVar(value=int(self.cfg.get('mood_decay', 6) or 0))
        self.mood_tier_seen = None
        self.title_var = tk.StringVar(value=str(self.cfg.get('user_title') or '主人'))
        self.routine_on = tk.BooleanVar(value=bool(self.cfg.get('routine_on', True)))
        self.quiet_night = tk.BooleanVar(value=bool(self.cfg.get('quiet_night', True)))
        _s = hm_minutes(self.cfg.get('sleep_at'))
        _w = hm_minutes(self.cfg.get('wake_at'))
        self.sleep_var = tk.StringVar(value=hm_text(1410 if _s is None else _s))
        self.wake_var = tk.StringVar(value=hm_text(420 if _w is None else _w))
        self.routine_night = None
        self.mem_gap = tk.IntVar(value=int(self.cfg.get('memory_interval', 300)))
        self.autostart_var = tk.BooleanVar(value=False)
        self.balance_win = tk.BooleanVar(value=bool(self.cfg.get('balance_win', False)))
        self.balance_ct = tk.BooleanVar(value=bool(self.cfg.get('balance_click_through', False)))
        self.balance_gap = tk.IntVar(value=int(self.cfg.get('balance_gap', BALANCE_REFRESH) or BALANCE_REFRESH))
        try:
            _ba = float(self.cfg.get('balance_alpha', 1.0) or 1.0)
        except (TypeError, ValueError):
            _ba = 1.0
        self.balance_alpha = tk.IntVar(value=max(30, min(100, int(round(_ba * 100)))))
        self.balance_menu = None
        self.balance_window = None
        self.balance_lbl = None
        self.balance_dot = None
        self.balance_close = None
        self.balance_next = 0.0
        self.balance_busy = False
        self.balance_dragged = False
        self._bal_press = None
        self.balance_alert_on = tk.BooleanVar(value=bool(self.cfg.get('balance_alert_on', True)))
        try:
            _ab = float(self.cfg.get('balance_alert_below', 5.0) or 5.0)
        except (TypeError, ValueError):
            _ab = 5.0
        self.balance_alert_below = tk.StringVar(value=('%g' % _ab))
        self.balance_alert_fail = tk.BooleanVar(value=bool(self.cfg.get('balance_alert_fail', True)))
        self.balance_alert_kind = ''
        self.balance_alert_ack = ''
        self.balance_alert_btn = None
        self.mem_on = tk.BooleanVar(value=bool(self.cfg.get('memory_on', True)))
        self.mem_next = time.time() + 45
        self.mem_busy = False
        self.mem_vision = True
        self.mem_last = ''
        self.mem_last_at = 0.0
        self.mem_day = time.strftime('%Y-%m-%d')
        _master = bool(self.cfg.get('pc_control_on', False))
        self.pc_ctrl = tk.BooleanVar(value=_master)
        self.pc_files = tk.BooleanVar(value=bool(self.cfg.get('pc_files', _master)))
        self.pc_command = tk.BooleanVar(value=bool(self.cfg.get('pc_command', _master)))
        self.pc_power = tk.BooleanVar(value=bool(self.cfg.get('pc_power', _master)))
        self.pc_settings = tk.BooleanVar(value=bool(self.cfg.get('pc_settings', _master)))
        set_pc_control(_master, {'files': self.pc_files.get(), 'command': self.pc_command.get(), 'power': self.pc_power.get(), 'settings': self.pc_settings.get()})
        self.update_check_on = tk.BooleanVar(value=bool(self.cfg.get('update_check_on', True)))
        self.update_auto = tk.BooleanVar(value=bool(self.cfg.get('update_auto', False)))
        try:
            _ugh = int(self.cfg.get('update_gap_hours', 6) or 6)
        except (TypeError, ValueError):
            _ugh = 6
        self.update_gap_hours = tk.IntVar(value=max(1, _ugh))
        self.update_channel = tk.StringVar(value=str(self.cfg.get('update_channel') or 'release'))
        self.upd_next = time.time() + 45
        self.upd_busy = False
        self.upd_pending = None
        _PET_FRONT[0] = self.root
        self._menu()
        self.follow.trace_add('write', self._on_follow_toggle)
        self._enable_pet_dnd()
        self.tray_q = queue.Queue()
        self.tray = TrayIcon(res_path('app.ico'), APP_NAME, TRAY_MENU, self.tray_q, hotkey=parse_hotkey(self.cfg.get('hotkey')))
        self.tray.start()
        self._tray_tip = ''
        if self.voice_wake.get() or self.voice_chat.get():
            self.voice.start_asr(self.wake_words())
        self.say(random.choice(['本鲸来啦～', '你好呀主人！', '今天也一起加油吧！']))
        self.tick()
        if self.balance_win.get():
            self.root.after(800, self._open_balance_win)
    @staticmethod
    def _load(name):
        return Image.open(res_path(name)).convert('RGBA')
    def _layout(self):
        """固定画布尺寸（比角色略大），这样换姿势时窗口不用缩放，也就不会显示不全。"""
        imgs = [self.base[k] for k in ['front', 'side', 'back']]
        self.body_h = max((int(i.height * self.scale) for i in imgs))
        w = max((int(i.width * self.scale) for i in imgs))
        self.canvas_size = (w, self.body_h + PAD_TOP + PAD_BOTTOM)
        self.base_canvas_size = self.canvas_size
        self.ground_line = PAD_TOP + self.body_h
        self.cache.clear()
        self.squash_cache.clear()
        self.bowl_cache.clear()
        self._expr_cache.clear()
        self._hide_cache.clear()
        self._build_frames()
        self._build_arm_frames()
        self.blink_photo = None
        if self.base['front'].width > 240:
            closed = close_eyes(self.base['front'], eye_boxes(self.base['front'].size))
            self.blink_photo = ImageTk.PhotoImage(harden(closed.resize(self._fit(closed), Image.LANCZOS)))
        self.canvas.config(width=self.canvas_size[0], height=self.canvas_size[1])
    def _build_frames(self):
        """预生成走路/跑步循环帧（原始分辨率），再按当前缩放做成 PhotoImage。"""
        self.walk = {}
        if self.parts:
            self.walk['walk'] = build_walk_frames(self.base['side'], self.parts)
            self.walk['run'] = build_walk_frames(self.base['side'], self.parts, swing=SWING_RUN, lift=LIFT_RUN)
        self.walk_photo = {}
        if self.walk:
            sw_, sh_ = self.base['side'].size
            dw = max(1, int(sw_ * self.scale))
            dh = max(1, int(sh_ * self.scale))
            for name, frames in self.walk.items():
                left, right = ([], [])
                for f in frames:
                    im = harden(f.resize((dw, dh), Image.LANCZOS))
                    left.append(ImageTk.PhotoImage(im))
                    right.append(ImageTk.PhotoImage(im.transpose(Image.FLIP_LEFT_RIGHT)))
                self.walk_photo[name] = {'L': left, 'R': right}
    def _build_arm_frames(self):
        """预生成「手臂绕肩轻摆」的一圈整幅帧（跟走路帧同尺寸，直接叠在它上面）。"""
        self.arm_photo = {'L': [], 'R': []}
        if self.arm_parts:
            sw_, sh_ = self.base['side'].size
            dw = max(1, int(sw_ * self.scale))
            dh = max(1, int(sh_ * self.scale))
            src = self.arm_parts['arm']
            arm = src.resize((max(1, int(src.width * self.scale)), max(1, int(src.height * self.scale))), Image.LANCZOS)
            bx = int(round(self.arm_parts['pos'][0] * self.scale))
            by = int(round(self.arm_parts['pos'][1] * self.scale))
            pivot = (self.arm_parts['pivot'][0] * self.scale, self.arm_parts['pivot'][1] * self.scale)
            left = []
            for i in range(ARM_FRAMES):
                ang = ARM_SWING * math.sin(2 * math.pi * i / ARM_FRAMES)
                layer = Image.new('RGBA', (dw, dh), (0, 0, 0, 0))
                layer.alpha_composite(arm, (bx, by))
                left.append(harden(layer.rotate(ang, resample=Image.BICUBIC, center=pivot)))
            self.arm_photo['L'] = [ImageTk.PhotoImage(im) for im in left]
            self.arm_photo['R'] = [ImageTk.PhotoImage(im.transpose(Image.FLIP_LEFT_RIGHT)) for im in left]
    def _step_len(self, kind):
        """一步在屏幕上走多少像素 —— 与腿部摆动幅度一致，保证脚不打滑。"""
        if not self.parts:
            return max(4.0, self.body_h * 0.08)
        else:
            swing = SWING_WALK if kind == 'walk' else SWING_RUN
            return max(4.0, 2.0 * self.parts['leg_len'] * self.scale * math.sin(math.radians(swing)))
    def _fit(self, im):
        return (max(1, int(im.width * self.scale)), max(1, int(im.height * self.scale)))
    def _photo(self, pose, flip):
        ck = (pose, flip, round(self.scale, 4))
        if ck not in self.cache:
            im = self.base[pose]
            if flip:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            self.cache[ck] = ImageTk.PhotoImage(harden(im.resize(self._fit(im), Image.LANCZOS)))
        return self.cache[ck]
    def _squash(self, pose, flip, f):
        """横向压扁的姿势图，用来做转身动画。"""
        ck = (pose, flip, round(f, 2), round(self.scale, 4))
        if ck not in self.squash_cache:
            im = self.base[pose]
            if flip:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            w, h = self._fit(im)
            w = max(1, int(w * f))
            self.squash_cache[ck] = ImageTk.PhotoImage(harden(im.resize((w, h), Image.LANCZOS)))
        return self.squash_cache[ck]
    def _squish(self, pose, flip, f):
        """纵向压扁的姿势图，用来做咀嚼这种小动作。"""
        ck = ('sq', pose, flip, round(f, 3), round(self.scale, 4))
        if ck not in self.squash_cache:
            im = self.base[pose]
            if flip:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            w, h = self._fit(im)
            h = max(1, int(h * f))
            self.squash_cache[ck] = ImageTk.PhotoImage(harden(im.resize((w, h), Image.LANCZOS)))
        return self.squash_cache[ck]
    def _show(self, photo):
        self.photo = photo
        self.walk_show = False
        self.sprite_size = (photo.width(), photo.height())
        self.canvas.itemconfig(self.sprite, image=photo)
    def set_pose(self, pose, flip=None):
        """立刻切换姿势（不做转身动画）。"""
        if flip is None:
            flip = self.flip
        self.pose, self.flip = (pose, flip)
        self._show(self._photo(pose, flip))
    def set_scale(self, f):
        self.scale = max(90.0 / BASE_H, min(0.6, self.scale * f))
        keep = (self.cx, self.foot)
        self._layout()
        self.set_pose(self.pose, self.flip)
        self.cx, self.foot = keep
        if self.edge:
            self._normal_geo = None
            self._apply_hide()
        else:
            self._apply_geometry()
    def set_scale_px(self, px):
        """按目标「高度 px」设置桌宠大小。"""
        try:
            px = float(px)
        except (TypeError, ValueError):
            return
        ref = max(self.base[k].height for k in ('front', 'side', 'back'))
        self.scale = max(90.0 / BASE_H, min(0.6, px / max(1.0, ref)))
        keep = (self.cx, self.foot)
        self._layout()
        self.set_pose(self.pose, self.flip)
        self.cx, self.foot = keep
        if self.edge:
            self._normal_geo = None
            self._apply_hide()
        else:
            self._apply_geometry()
    def screen(self):
        return (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
    def _apply_geometry(self):
        cw, ch = self.canvas_size
        sw, sh = self.screen()
        top = int(max(0, min(sh - ch, self.foot - self.ground_line)))
        if self.edge:
            off = int(cw * self.edge_frac)
            left = -off if self.edge == 'left' else sw - cw + off
        else:
            left = int(max(0, min(sw - cw, self.cx - cw / 2)))
        self.cx = left + cw / 2
        self.foot = top + self.ground_line
        self.root.geometry(f'{cw}x{ch}+{left}+{top}')
    def _move_x(self, dx):
        """水平移动并返回实际位移（贴边时为 0）。"""
        half = max(1, self.sprite_size[0]) / 2
        sw = self.screen()[0]
        new = max(half, min(sw - half, self.cx + dx))
        moved = new - self.cx
        self.cx = new
        return moved
    def _bind(self):
        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_motion)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind('<Double-Button-1>', self.on_double)
        self.canvas.bind('<Button-3>', self.popup)
    def on_press(self, e):
        self._press = (e.x_root, e.y_root, self.cx, self.foot)
        self.dragging = False
    def _idle_pool(self):
        """平时闲聊聊什么：心情值很低 / 很高时，挑对应的一批话。"""
        tier = mood_tier(self.mood_value())
        if tier == 'low':
            return MOOD_LOW_LINES
        else:
            if tier == 'high':
                return MOOD_HIGH_LINES
            else:
                return IDLE_LINES
    def _check_mood_tier(self):
        """心情值跨档（变很蔫 / 变很兴奋）时，说句特别的。"""
        tier = mood_tier(self.mood_value())
        if tier == self.mood_tier_seen:
            return
        else:
            first = self.mood_tier_seen is None
            self.mood_tier_seen = tier
            if first or tier == 'mid':
                return None
            else:
                if self.quiet or self.sleeping or self.dragging or self.edge or self.pending or self.ask_win:
                    return None
                else:
                    self._mood_react(tier)
    def _mood_react(self, tier):
        """心情值到很蔫 / 很兴奋了：本地用自带台词，在线让 AI 想一句。"""
        val = self.mood_value()
        if self.online() and self._api_ready():
            feel = f'本鲸现在的心情值只有 {val:.0f}%，蔫蔫的、有点委屈' if tier == 'low' else f'本鲸现在心情值 {val:.0f}%，开心得冒泡'
            self._quick_ai(f'{feel}。用一句话跟主人说说（20 字以内），要符合本鲸傲娇又撒娇的性格，别调工具。')
        else:
            self.say(self._pick_line(MOOD_LOW_LINES if tier == 'low' else MOOD_HIGH_LINES), 4600)
        self.emote('apologetic' if tier == 'low' else 'cheerful', 2800)
    def _pick_line(self, lines):
        """随机挑一句，尽量不跟上一次重复。"""
        last = getattr(self, '_last_line', None)
        pool = [x for x in lines if x != last] or lines
        self._last_line = random.choice(pool)
        return self._last_line
    def on_motion(self, e):
        if not self._press:
            return
        else:
            px, py, cx0, foot0 = self._press
            dx, dy = (e.x_root - px, e.y_root - py)
            if self.edge:
                out = dx if self.edge == 'left' else -dx
                if out > EDGE_PULL_OUT and out > abs(dy):
                    self.come_out(grumpy=True)
                    self._log_op('把本鲸从屏幕边边拽出来了')
                    self.dragging = True
                    self._pull_out = True
                    self.state = 'drag'
                    self.wiggle = 0.0
                    self._press = (e.x_root, e.y_root, self.cx, self.foot)
                else:
                    self._slide_along_edge(foot0 + dy)
                return
            else:
                if not self.dragging and abs(dx) + abs(dy) > 5:
                        self.dragging = True
                        if self.sleeping:
                            pass
                        else:
                            self._interrupt()
                            self.state = 'drag'
                            self.wiggle = 0.0
                            self.drag_talk = 0
                            self.drag_speed = 0.0
                            self.drag_shake = 0.0
                            self.say(self._pick_line(DRAG_LINES), 3600)
                            self.emote('shocked', 1300)
                if self.dragging:
                    nx = cx0 + dx
                    ny = foot0 + dy
                    step = abs(nx - self.cx) + abs(ny - self.foot)
                    self.drag_speed = self.drag_speed * 0.6 + step * 0.4
                    self.drag_shake = min(1.0, self.drag_shake + step * 0.015)
                    if abs(nx - self.cx) > 0.5:
                        self.drag_dir = 1 if nx > self.cx else -1
                    self.cx, self.foot = (nx, ny)
                    self._apply_geometry()
    def on_release(self, e):
        was_drag = self.dragging
        self._press = None
        if was_drag:
            self.dragging = False
            self.wiggle = 0.0
            just_out = self._pull_out
            self._pull_out = False
            if not just_out and self._snap_to_edge():
                return
            else:
                if not self.sleeping:
                    self.state = 'idle'
                    self.idle_timer = random.randint(60, 140)
                    self.set_pose('front')
                    if not just_out:
                        if self.drag_shake >= 0.6:
                            self.gesture('sway')
                            self.say('呜……天旋地转的……本鲸被甩晕了……', 3200)
                            self.emote('sleepy', 2600)
                            self._log_op('把本鲸拎起来甩了一通')
                            self.mood_add((-6))
                        else:
                            self.gesture('shiver')
                            self.say(random.choice(DROP_LINES), 2400)
                            self._log_op('把本鲸拎起来又放下')
                            self.mood_add((-3))
                        self.meet()
                        self.drag_shake = 0.0
                        self.drag_speed = 0.0
                return None
        else:
            if self._dbl:
                self._dbl = False
                return
            else:
                if self._click_job:
                    self.root.after_cancel(self._click_job)
                self._click_job = self.root.after(230, self._click_action)
    def on_double(self, e):
        """双击 = 打开聊天；顺便取消还没执行的单击（免得顺带睡/醒）。"""
        self._dbl = True
        if self._click_job:
            self.root.after_cancel(self._click_job)
            self._click_job = None
        self.open_chat()
    def _click_action(self):
        """单击桌宠：躲着就出来、醒着就睡、睡着就被吵醒（不高兴）。"""
        self._click_job = None
        self._close_ask()
        self._log_op('点了本鲸一下')
        self.meet()
        self.mood_add(2)
        if self.edge:
            self.come_out()
        else:
            if self.sleeping:
                self.wake(grumpy=True)
            else:
                self.sleep()
    def popup(self, e):
        self._menu()
        self.menu.tk_popup(e.x_root, e.y_root)
    def tick(self):
        self.t += 1
        if self.edge and self.state != 'hide':
                self.state = 'hide'
        st = self.state
        if st == 'idle':
            self._step_idle()
        else:
            if st == 'walk':
                self._step_walk()
            else:
                if st == 'float':
                    self._step_float()
                else:
                    if st == 'follow':
                        self._step_follow()
                    else:
                        if st == 'drag':
                            self._step_drag()
        self.hop *= 0.82
        self.wiggle *= 0.9
        if self.state in ['walk', 'float', 'follow']:
            amp = self.body_h * 0.016
            self.bob = -amp * (1.0 - abs(math.sin(self.phase)))
        else:
            if self.state == 'drag':
                self.bob = math.sin(self.t * 1.1) * 3
            else:
                self.bob = 0.0
        if self.chew > 0:
            self.chew -= 1
        self._update_eyes()
        self._sync_sleep_canvas()
        sw_, sh_ = self.sprite_size
        if self.edge:
            self.canvas.coords(self.sprite, self.canvas_size[0] // 2, self.canvas_size[1] // 2)
        else:
            self.canvas.coords(self.sprite, self.canvas_size[0] // 2 + self.wiggle, self.ground_line - sh_ / 2 + self.bob - self.hop)
        self._update_arm()
        self._apply_geometry()
        self._update_mood()
        self._update_expression()
        if self.t % 30 == 0:
            self._poll_activity()
            self._check_mood_tier()
            self._grow_hunger()
            self._check_routine()
            self._balance_tick()
            self._check_update_tick()
        self._check_idle_sleep()
        self._check_pomodoro()
        self._drain_queue()
        self._drain_tray()
        self._poll_voice()
        self._poll_ptt()
        self._update_tray_tip()
        self._check_memory()
        self._check_proactive()
        if self.t % 300 == 0:
            self._check_rice()
        self.root.after(TICK, self.tick)
    def _update_eyes(self):
        """眨眼：偶尔闭一下；睡着时一直闭着。吃饭时改做咀嚼的压扁。"""
        if self.sleeping:
            self.eyes_closed = True
            self.blink_t = 0
        else:
            if self.blink_t > 0:
                self.blink_t -= 1
                self.eyes_closed = True
            else:
                self.eyes_closed = False
                if self.pose == 'front' and random.random() < 0.018:
                        self.blink_t = BLINK_TICKS
                        self.eyes_closed = True
        if self.state in ['idle', 'sleep']:
            if self.pose == 'front':
                if self.blink_photo:
                    if self.sleeping:
                        want = self._sleep_photo() or self.blink_photo
                    else:
                        if self.expr_photo is not None and time.time() < self.expr_until and (not self.sleeping) and (not self.turning) and (not self.gesturing) and (not self.eating or time.time() >= self.eat_until):
                            want = self.expr_photo
                        else:
                            if self.chew > 0:
                                want = self._squish('front', self.flip, CHEW_SCALE)
                            else:
                                if self.eyes_closed:
                                    want = self.blink_photo
                                else:
                                    want = self._photo('front', self.flip)
                    if self.photo is not want:
                        self._show(want)
    def _walk_cycle(self, kind, dx):
        """按实际位移推进相位并切帧，保证脚踩地不打滑。"""
        moved = self._move_x(dx)
        self.walk_dir = 1 if dx > 0 else (-1)
        if not self.walk_photo:
            self.set_pose('side', flip=dx > 0)
            return abs(moved)
        else:
            stride = self._step_len(kind)
            if abs(moved) > 0.01:
                self.phase = (self.phase + abs(moved) / stride * math.pi) % (2 * math.pi)
            idx = int(self.phase / (2 * math.pi) * WALK_FRAMES) % WALK_FRAMES
            self.walk_face = 'R' if dx > 0 else 'L'
            self._show(self.walk_photo[kind][self.walk_face][idx])
            self.walk_show = True
            return abs(moved)
    def _step_idle(self):
        self.idle_timer -= 1
        if random.random() < 0.005 and (not self.quiet):
                if self._brain_on():
                    self._ai_decide()
                    return
                else:
                    if self.is_sad():
                        self.say(random.choice(SAD_LINES))
                    else:
                        line = self._scene_line() if self.scene_play.get() else None
                        self.say(line or self._pick_line(self._idle_pool()))
        if self.follow.get():
            self.state = 'follow'
        else:
            if self.idle_timer <= 0:
                if self.quiet:
                    self.idle_timer = random.randint(120, 240)
                else:
                    if self._brain_on():
                        if self._ai_decide():
                            self.idle_timer = random.randint(50, 110)
                        else:
                            self.idle_timer = random.randint(30, 80)
                    else:
                        if self.scene_play.get():
                            self._scene_play()
                        else:
                            if random.random() < GESTURE_CHANCE:
                                self.gesture()
                            else:
                                self._wander()
    def _scene_play(self):
        """离线时：看主人正在用什么程序，做点应景的小动作 / 表情 / 话。"""
        title, exe = self.activity
        play = SCENE_PLAY.get(detect_scene(exe, title)) or SCENE_PLAY['other']
        roll = random.random()
        if roll < 0.45 and play.get('faces'):
            self.emote(random.choice(play['faces']), 3000)
        elif roll < 0.8 and play.get('acts'):
            self.gesture(random.choice(play['acts']))
        elif play.get('lines'):
            self.say(random.choice(play['lines']), 3600)
        else:
            self._wander()
    def _scene_line(self):
        """按当前场景挑一句应景的台词（没有就返回 None）。"""
        title, exe = self.activity
        play = SCENE_PLAY.get(detect_scene(exe, title)) or {}
        lines = play.get('lines') or []
        return random.choice(lines) if lines else None
    def _wander(self):
        sw, sh = self.screen()
        half = max(1, self.sprite_size[0]) / 2
        self.target_cx = max(half + 10, min(sw - half - 10, self.cx + random.choice([(-1), 1]) * random.randint(120, 560)))
        self.target_y = random.uniform(self.ground_line + 10, max(self.ground_line + 20, sh - 24))
        self._begin_move()
    def _begin_move(self):
        """上下和左右都用侧面迈腿的姿势走过去。"""
        if abs(self.target_y - self.foot) > 8:
            flip = self.target_cx > self.cx if abs(self.target_cx - self.cx) > 20 else self.walk_dir > 0
            self._do_turn('side', flip, self._set_float)
        else:
            self._do_turn('side', self.target_cx > self.cx, self._set_walk)
    def _set_float(self):
        self.state = 'float'
    def _set_walk(self):
        self.phase = 0.0
        self.state = 'walk'
    def _walk_end(self):
        self._do_turn('front', False, self._after_walk)
    def _after_walk(self):
        self.state = 'idle'
        self.idle_timer = random.randint(60, 160)
    def _step_float(self):
        """上下移动：一样用迈腿的走路帧，相位跟位移绑定，脚步不打滑。"""
        speed = SPEED_FLOAT_R * self.body_h
        dy = self.target_y - self.foot
        if abs(dy) < speed:
            self.foot = self.target_y
            dx = self.target_cx - self.cx
            if abs(dx) < speed:
                self._walk_end()
                return
            else:
                self._do_turn('side', dx > 0, self._set_walk)
                return
        else:
            step = speed if dy > 0 else -speed
            self.foot += step
            if not self.walk_photo:
                self.set_pose('side', flip=self.flip)
                return
            else:
                stride = self._step_len('walk')
                self.phase = (self.phase + abs(step) / stride * math.pi) % (2 * math.pi)
                idx = int(self.phase / (2 * math.pi) * WALK_FRAMES) % WALK_FRAMES
                self.walk_face = 'R' if self.flip else 'L'
                self._show(self.walk_photo['walk'][self.walk_face][idx])
                self.walk_show = True
    def _step_walk(self):
        dx = self.target_cx - self.cx
        speed = SPEED_WALK_R * self.body_h
        if abs(dx) < speed:
            if abs(self.target_y - self.foot) > 8:
                self._do_turn('front', False, self._set_float)
            else:
                self._walk_end()
        else:
            if abs(dx) > 160 and random.random() < 0.0035:
                self._start_peek()
            else:
                if self._walk_cycle('walk', speed if dx > 0 else -speed) < 0.01:
                    if abs(self.target_y - self.foot) > 8:
                        self._do_turn('front', False, self._set_float)
                    else:
                        self._walk_end()
    def _interrupt(self):
        """打断进行中的转身 / 探头 / 小动作 / 吃饭动画。\n\n这些动画是靠 after 定时器串起来的，被打断时如果只改状态，\n它们挂着的回调还会在后面把人拽回走路之类的状态（就是那个 bug）。\n"""
        self.turn_id += 1
        self.turning = False
        self.gesturing = False
        if self._peek_job:
            self.root.after_cancel(self._peek_job)
            self._peek_job = None
        self.eat_gen += 1
        self.eating = False
        self.chew = 0
        if self.bowl_item is not None:
            self.canvas.itemconfig(self.bowl_item, state='hidden')
    def _start_peek(self):
        self.say(random.choice(PEEK_LINES), 1800)
        self._do_turn('front', False, self._peek_hold)
    def _peek_hold(self):
        tid = self.turn_id
        self._peek_job = self.root.after(1100, lambda: self._peek_back(tid))
    def _peek_back(self, tid):
        self._peek_job = None
        if tid != self.turn_id:
            return
        else:
            self._do_turn('side', self.walk_dir > 0, self._resume_walk)
    def _resume_walk(self):
        self.phase = 0.0
        self.state = 'walk'
    def _step_follow(self):
        if not self.follow.get():
            self.state = 'idle'
            return
        else:
            px, py = self.root.winfo_pointerxy()
            run = SPEED_RUN_R * self.body_h
            up = SPEED_FLOAT_R * self.body_h
            dx = px - self.cx
            dy = py + 70 - self.foot
            if abs(dx) <= run and abs(dy) <= up:
                if not self.follow_said:
                    self.follow_said = True
                    self.say(random.choice(FOLLOW_LINES), 2600)
            else:
                self.follow_said = False
                if time.time() - self.last_follow_talk > 15:
                    self.last_follow_talk = time.time()
                    self.say(random.choice(FOLLOW_LINES), 2000)
            if abs(dy) > up and abs(dy) > abs(dx) * 0.8:
                self.foot += up if dy > 0 else -up
                self.set_pose('front')
                self.wiggle = math.sin(self.t * 0.09) * 2.8
                return
            else:
                if abs(dx) > run:
                    self._walk_cycle('run', run if dx > 0 else -run)
                else:
                    self.phase = 0.0
                    if (self.pose, self.flip) != ('front', False):
                        self._do_turn('front', False)
                if abs(dy) > up:
                    self.foot += up * 0.6 if dy > 0 else -up * 0.6
    def _step_drag(self):
        """被拎着的时候手脚乱蹬 + 左右扭 + 一直喊；甩得越猛，挣扎越凶（像被拎起来甩）。"""
        speed = min(14.0, self.drag_speed)
        self.drag_speed *= 0.93
        self.drag_phase = (self.drag_phase + DRAG_KICK * (1.0 + speed * 0.08)) % (2 * math.pi)
        if self.walk_photo:
            idx = int(self.drag_phase / (2 * math.pi) * WALK_FRAMES) % WALK_FRAMES
            self.walk_face = 'R' if self.drag_dir > 0 else 'L'
            self._show(self.walk_photo['run'][self.walk_face][idx])
            self.walk_show = True
        self.wiggle = math.sin(self.t * (DRAG_SWAY + speed * 0.04)) * (3 + speed * 0.6)
        if speed >= 6 and self.t % 24 == 0:
            self.emote(random.choice(['shocked', 'crying', 'angry']), 1100)
        self.drag_talk += 1
        if self.drag_talk >= max(12, int(DRAG_TALK_TICKS - speed * 2)):
            self.drag_talk = 0
            self.say(self._pick_line(DRAG_LINES), 2000)
    def _update_arm(self):
        """走动 / 移动时手臂单独轻摆；站着不动时收起来。摆速跟着心情走：越高兴摆得越快。"""
        if (not self.walk_show) or not self.arm_photo['L']:
            if self.arm_show:
                self.canvas.itemconfig(self.arm_item, state='hidden')
                self.arm_show = False
            return
        rate = ARM_RATE * (0.7 + self.mood_value() / 100.0 * 1.3)
        self.arm_phase = (self.arm_phase + rate) % (2 * math.pi)
        idx = int(self.arm_phase / (2 * math.pi) * ARM_FRAMES) % ARM_FRAMES
        photo = self.arm_photo[self.walk_face][idx]
        self.canvas.itemconfig(self.arm_item, image=photo, state='normal')
        self.canvas.coords(self.arm_item, self.canvas_size[0] // 2 + self.wiggle, self.ground_line - photo.height() / 2 + self.bob - self.hop)
        self.arm_show = True
    def _do_turn(self, pose, flip, done=None):
        """横向压扁再展开，看起来就像转了个身。turn_id 用来作废被打断的动画。"""
        if self.edge:
            return
        else:
            if (pose, flip) == (self.pose, self.flip):
                self.set_pose(pose, flip)
                if done:
                    done()
                return None
            else:
                self.turn_id += 1
                tid = self.turn_id
                self.turning = True
                self.state = 'turn'
                src = (self.pose, self.flip)
                n = len(TURN_SEQ)
                seq = [(src if i < n // 2 else (pose, flip), TURN_SEQ[i]) for i in range(n)]
                def step(i=0):
                    if tid != self.turn_id:
                        return
                    else:
                        if i >= n:
                            self.turning = False
                            self.pose, self.flip = (pose, flip)
                            self._show(self._photo(pose, flip))
                            if done:
                                done()
                            return None
                        else:
                            (p, fl), f = seq[i]
                            self._show(self._squash(p, fl, f))
                            self.root.after(TURN_STEP, lambda: step(i + 1))
                step(0)
    def gesture(self, name=None):
        """做个不依赖手臂的小动作：转圈 / 蹦跳。\n\n「抖一抖」「摇摆」这两个带左右抖的，平时不随机做，\n只在特定情况才触发（被放下时抖一抖 / 输了猜拳心情差时摇一摇）。\n"""
        if self.gesturing or self.sleeping or self.dragging or self.edge:
            return None
        else:
            if name is None:
                name = 'sway' if self.is_sad() else random.choice(['spin', 'hop'])
            self.gesturing = True
            getattr(self, '_g_' + name)()
    def is_sad(self):
        return time.time() < self.sad_until
    def celebrate(self):
        """猜拳赢了：连蹦带转。"""
        self.sad_until = 0.0
        self.happy_until = time.time() + 8
        self.emote('proud', 2000)
        if self.gesturing or self.sleeping or self.edge:
            self.hop = 16
        else:
            self.gesturing = True
            self._g_cheer()
    def deject(self):
        """猜拳输了：转过去背对主人，失落一会儿。"""
        self.sad_until = time.time() + SAD_SECONDS
        self.emote('crying', 2400)
        if self.gesturing or self.sleeping or self.edge:
            return None
        else:
            self.gesturing = True
            self.state = 'gesture'
            self._do_turn('back', False, self._sulk_hold)
    def _g_cheer(self):
        """蹦三下再转一圈。"""
        self.state = 'gesture'
        def jump(k=0):
            if not self.gesturing:
                return
            else:
                if k < 3:
                    self.hop = 17
                    self.root.after(280, lambda: jump(k + 1))
                else:
                    self._g_spin()
        jump()
    def _sulk_hold(self):
        self.root.after(1600, self._sulk_back)
    def _sulk_back(self):
        if not self.gesturing:
            return
        else:
            self._do_turn('front', False, self._end_gesture)
    def _end_gesture(self):
        self.gesturing = False
        self.wiggle = 0.0
        self.set_pose('front')
        self.state = 'idle'
        self.idle_timer = random.randint(80, 160)
    def _g_spin(self):
        """原地转一圈：正面→侧面→背面→侧面→正面。"""
        self.state = 'turn'
        seq = [('side', True), ('back', False), ('side', False), ('front', False)]
        def step(i=0):
            if not self.gesturing:
                return
            else:
                if i >= len(seq):
                    self._end_gesture()
                    return
                else:
                    pose, flip = seq[i]
                    self._do_turn(pose, flip, lambda: step(i + 1))
        step()
    def _g_hop(self):
        """原地蹦几下。"""
        self.state = 'gesture'
        n = random.randint(2, 3)
        def jump(k=0):
            if not self.gesturing:
                return
            else:
                if k >= n:
                    self._end_gesture()
                    return
                else:
                    self.hop = 15
                    self.root.after(340, lambda: jump(k + 1))
        jump()
    def _g_shiver(self):
        """抖一抖（快速小幅）。"""
        self.state = 'gesture'
        def step(k=0):
            if not self.gesturing:
                return
            else:
                if k >= 14:
                    self.wiggle = 0.0
                    self._end_gesture()
                    return
                else:
                    self.wiggle = 5.0 if k % 2 else (-5.0)
                    self.root.after(50, lambda: step(k + 1))
        step()
    def _g_sway(self):
        """慢慢左右摇摆，顺便踮两下（只在心情不好的时候做）。"""
        self.state = 'gesture'
        def step(k=0):
            if not self.gesturing:
                return
            else:
                if k >= 36:
                    self.wiggle = 0.0
                    self._end_gesture()
                else:
                    self.wiggle = math.sin(k * 0.35) * 4.5
                    if k % 12 == 0:
                        self.hop = 7
                    self.root.after(45, lambda: step(k + 1))
        step()
    def sleep(self):
        """打盹：站着闭眼（就是原来那套）。"""
        if self.sleeping:
            return
        else:
            if self.edge:
                self.come_out()
            self._interrupt()
            self._close_ask()
            self.sleeping = True
            self.deep_sleep = False
            self.state = 'sleep'
            self.set_pose('front')
            self.say('Zzz… 本鲸先打个盹～', 2200)
            self.expr_photo = None
    def sleep_deep(self):
        """睡沉：换成「睡眠」小表情（抱着鲸鱼玩偶坐着睡）。"""
        if self.sleeping and self.deep_sleep:
            return
        else:
            if not self.sleeping:
                self.sleep()
            self.deep_sleep = True
            self.expr_photo = None
            self.say(random.choice(DEEP_SLEEP_LINES), 2800)
    def wake(self, grumpy=False):
        if not self.sleeping:
            return
        else:
            deep = self.deep_sleep
            self.sleeping = False
            self.deep_sleep = False
            self.state = 'idle'
            self.idle_timer = random.randint(80, 160)
            if deep and (not grumpy):
                self.say(random.choice(DEEP_WAKE_LINES), 3000)
                self.emote('relaxed', 1800)
            else:
                if grumpy:
                    self.grumpy_until = time.time() + 8
                    self.say(self._pick_line(GRUMPY_LINES), 2800)
                    self.emote('angry', 2200)
                else:
                    self.say(random.choice(WAKE_LINES))
                    self.emote('shocked', 1400)
    def _on_follow_toggle(self, *args):
        if self.follow.get():
            if self.edge:
                self.come_out()
            self.follow_said = False
            self.say('本鲸跟上主人啦～', 2600)
        else:
            self.say('唔……那本鲸不跟了。', 2200)
    def _poll_activity(self):
        """每秒看一眼：主人在用什么程序、有没有全屏、还有没有提醒没到。"""
        self.idle_sec = idle_seconds()
        title, exe = active_window()
        if title == APP_NAME:
            title, exe = ('', '')
        if (title, exe) != self.activity:
            self.activity = (title, exe)
            if exe or title:
                self._log_op(f'切到 {exe or '未知程序'}' + (f'（{str(title)[:24]}）' if title else ''))
            self._on_activity_change(exe, title)
        away = self.idle_sec >= IDLE_SLEEP_SEC
        if away and (not self.was_away):
            self.was_away = True
            self._log_op('离开电脑（这段时间没碰键鼠）')
        else:
            if self.was_away and self.idle_sec < 3:
                    self.was_away = False
                    self._log_op('回到电脑前')
        want = bool(self.quiet_mode.get() and exe and is_fullscreen())
        if want != self.quiet:
            self.quiet = want
            if want and self.state in ('walk', 'float'):
                    self._walk_end()
        left = []
        for done_at, what in self.reminders:
            if time.time() >= done_at:
                self.wake()
                self.hop = 14
                self.say(f'叮咚——{what}啦！', 6000)
            else:
                left.append((done_at, what))
        self.reminders = left
    def _on_activity_change(self, exe, title):
        """主人换了程序，偶尔搭两句话（有节流，不会烦）。认得出编程工具就专门应一声。"""
        if self.quiet or not self.quiet_mode.get() or self.sleeping:
            return None
        else:
            if time.time() - self.last_app_talk < 180:
                return
            else:
                dev = detect_dev_tool(exe, title)
                if dev:
                    if dev == self.dev_seen:
                        return None
                    self.dev_seen = dev
                    self.last_app_talk = time.time()
                    self.say(dev_line(dev), 3600)
                    self.emote('desk-coding', 2600)
                    self._log_op(f'在用编程工具：{dev}')
                    return
                self.dev_seen = None
                low = (str(exe) + ' ' + str(title)).lower()
                for keys, lines, emo in APP_HINTS:
                    if any((k in low for k in keys)):
                        self.last_app_talk = time.time()
                        self.say(random.choice(lines), 3200)
                        self.emote(emo, 2200)
                        break
    def where_is_master(self):
        """报告主人现在在干什么。"""
        title, exe = active_window()
        if not exe:
            msg = '本鲸看不到主人在用什么……可能切到别的桌面了吧。'
        else:
            low = (exe + ' ' + title).lower()
            what = '别的事情'
            for keys, _lines, _emo in APP_HINTS:
                if any((k in low for k in keys)):
                    what = {'code.exe': '写代码', 'cursor': '写代码'}.get(exe.lower(), None) or '这件事'
                    break
            msg = f'主人现在在用 {exe}（{what}），窗口标题是「{title}」。'
        self.say(msg, 4200)
        return msg
    def _check_idle_sleep(self):
        """主人长时间没动（键盘鼠标都算）就自己睡：先打盹，再久一点睡沉。"""
        if self.quiet or self.follow.get():
            return None
        else:
            if not self.sleeping:
                if self.idle_sec >= IDLE_SLEEP_SEC:
                    if self.state == 'idle':
                        self.sleep()
                return None
            else:
                if not self.deep_sleep and self.idle_sec >= IDLE_SLEEP_SEC + NAP_TO_SLEEP_SEC:
                        self.sleep_deep()
    def _routine_span(self):
        """作息里配的（入睡分钟, 起床分钟）；没开或填得不对就返回 None。"""
        if not bool(self.cfg.get('routine_on', True)):
            return
        else:
            s = hm_minutes(self.cfg.get('sleep_at'))
            w = hm_minutes(self.cfg.get('wake_at'))
            if s is None or w is None:
                return None
            else:
                return (s, w)
    def _is_night(self):
        """现在是不是作息里的「睡觉时段」（跨零点也算）。"""
        span = self._routine_span()
        if not span:
            return False
        else:
            now = time.localtime()
            return in_span(now.tm_hour * 60 + now.tm_min, span[0], span[1])
    def _check_routine(self):
        """到点了：夜里自己去睡、早上叫你（只在跨过时间点的那一次动作）。"""
        span = self._routine_span()
        if not span:
            self.routine_night = None
            return
        else:
            night = self._is_night()
            if self.routine_night is None:
                self.routine_night = night
                if night and (not self.sleeping):
                        self.sleep()
                        self.sleep_deep()
                return None
            else:
                if night == self.routine_night:
                    return
                else:
                    self.routine_night = night
                    if night:
                        if self.sleeping:
                            return
                        else:
                            self.sleep_deep()
                            self.say(self._pick_line(NIGHT_SLEEP_LINES), 4600)
                    else:
                        if not self.sleeping:
                            return
                        else:
                            self.wake()
                            self.say(self._pick_line(MORNING_LINES), 4200)
    def do_tool(self, name, args):
        """从菜单直接执行一个工具，把结果说出来。"""
        self._log_op(f'让本鲸做事：{name} {args or ''}'.strip())
        out = run_tool(name, args)
        if out == '__CLEAN__':
            self.clean_feed()
            return out
        else:
            self.say(out[:70], 3600)
            return out
    def ask_remind(self):
        """弹个小窗设置提醒。"""
        win = tk.Toplevel(self.root)
        win.title('设置提醒')
        win.configure(bg='#eef3ff')
        win.attributes('-topmost', True)
        win.resizable(False, False)
        tk.Label(win, text='几分钟后提醒？', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 10)).pack(padx=18, pady=(14, 4))
        v_min = tk.StringVar(value='25')
        e1 = Entry(win, textvariable=v_min, width=8, justify='center', font=('Microsoft YaHei', 10))
        e1.pack()
        tk.Label(win, text='提醒什么？', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 10)).pack(pady=(10, 4))
        v_what = tk.StringVar(value='休息一下')
        Entry(win, textvariable=v_what, width=24, justify='center', font=('Microsoft YaHei', 10)).pack()
        def ok():
            try:
                mins = max(1, int(float(v_min.get())))
            except ValueError:
                mins = 25
            self.reminders.append((time.time() + mins * 60, v_what.get().strip() or '时间到'))
            self.say(f'好～{mins} 分钟后本鲸叫主人。', 3200)
            win.destroy()
        row = Frame(win, bg='#eef3ff')
        row.pack(pady=12)
        tk.Button(row, text='确定', width=7, font=('Microsoft YaHei', 10), command=ok).pack(side='left', padx=6)
        tk.Button(row, text='取消', width=7, font=('Microsoft YaHei', 10), command=win.destroy).pack(side='left')
        e1.focus_set()
    def start_pomodoro(self, minutes, label):
        self.pomo_end = time.time() + minutes * 60
        self.pomo_label = label
        self.wake()
        self.say(f'{label}开始！{minutes} 分钟后本鲸叫你～', 3400)
    def cancel_pomodoro(self):
        self.pomo_end = None
        self.say('计时取消啦。', 2000)
    def _check_pomodoro(self):
        if self.pomo_end and time.time() >= self.pomo_end:
                label = self.pomo_label
                self.pomo_end = None
                self.wake()
                self.hop = 14
                self.emote('desk-done', 2600)
                self.say(f'叮咚——{label}结束！主人起来动一动、喝口水吧～', 6000)
    def feed_dir(self):
        d = os.path.join(data_dir(), FEED_DIR)
        os.makedirs(d, exist_ok=True)
        return d
    def open_feed_dir(self):
        d = self.feed_dir()
        try:
            os.startfile(d)
        except Exception:
            pass
        self.say('把不要的东西丢进这个「投喂」文件夹，本鲸打扫时会把它们变成米饭～', 3600)
    def _devour(self, paths):
        """吃掉这些路径（只允许投喂文件夹内的），返回成功个数。"""
        d = os.path.abspath(self.feed_dir())
        eaten = 0
        for p in paths:
            if os.path.dirname(os.path.abspath(p)) != d:
                continue
            else:
                try:
                    if os.path.isdir(p) and (not os.path.islink(p)):
                        shutil.rmtree(p)
                    else:
                        os.remove(p)
                    eaten += 1
                except OSError:
                    pass
        return eaten
    def _after_eat(self, eaten, dropped=False):
        if not eaten:
            return
        else:
            self.add_rice(eaten)
            self.wake()
            self.hop = 10
            self.eating = True
            self.eat_until = time.time() + 8
            self.emote('deepseek-rice', 2600)
            if dropped:
                self.say(f'{eaten} 样东西本鲸都吃掉啦～变成米饭了，谢谢主人！', 4200)
            else:
                self.say(f'{eaten} 样东西都变成米饭啦～本鲸收好了，主人随时可以投喂。', 4000)
    def clean_feed(self, confirm=True):
        """打扫投喂文件夹：删掉里面的东西，换成米饭攒起来。"""
        d = self.feed_dir()
        items = sorted((n for n in os.listdir(d) if not n.startswith(('.', '_'))))
        if not items:
            if confirm:
                self.say('投喂碗是空的～把不要的东西丢进「投喂」文件夹吧。', 3400)
                self.open_feed_dir()
            return 0
        else:
            if confirm:
                names = '、'.join(items[:6]) + ('…' if len(items) > 6 else '')
                if not messagebox.askyesno('大肥鲸要打扫了', f'要把这 {len(items)} 样东西交给大肥鲸处理吗？\n\n{names}\n\n（会被永久删除，无法恢复；大肥鲸会把它们变成米饭）', parent=self.root):
                    self.say('那本鲸先不动啦～', 2000)
                    return 0
            eaten = self._devour([os.path.join(d, n) for n in items])
            if eaten:
                self.mood_add(5)
            self._after_eat(eaten)
            return eaten
    def _enable_pet_dnd(self):
        """让桌宠本体也能接住拖过来的文件。"""
        if not DND_OK:
            return
        else:
            for w in [self.canvas, self.root]:
                try:
                    w.drop_target_register(DND_FILES)
                    w.dnd_bind('<<Drop>>', self._on_pet_drop)
                except Exception:
                    pass
    def _on_pet_drop(self, event):
        try:
            raw = self.root.tk.splitlist(event.data)
        except Exception:
            raw = [str(event.data)]
        got = (p for x in raw for p in raw if p and os.path.exists(p))
        paths = [p for p in got if not is_self_dir(p)]
        if len(paths) < len(got) and (not paths):
            self.emote('skeptical', 2200)
            self.say('这是本鲸自己住的文件夹啦，可不能丢给本鲸自己～', 4000)
        else:
            if paths:
                self.ask_what_to_do(paths)
    def ask_what_to_do(self, paths):
        """主人把东西丢到本鲸身上了：帮忙整理，还是给它吃？"""
        self.wake()
        n = len(paths)
        names = '、'.join((os.path.basename(p.rstrip('\\/')) for p in paths[:4]))
        if n > 4:
            names += f' 等 {n} 样'
        self.say(f'主人丢了 {n} 样东西给本鲸～是要本鲸帮忙整理，还是给本鲸吃？', 4600)
        win = tk.Toplevel(self.root)
        win.title('大肥鲸问一下')
        win.configure(bg='#eef3ff')
        win.attributes('-topmost', True)
        win.resizable(False, False)
        tk.Label(win, text=f'主人丢了 {n} 样东西给大肥鲸：', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 11, 'bold')).pack(padx=18, pady=(14, 2))
        tk.Label(win, text=names, bg='#eef3ff', fg='#6b7a99', wraplength=300, justify='left', font=('Microsoft YaHei', 9)).pack(padx=18)
        tk.Label(win, text='是要大肥鲸帮忙整理，还是给大肥鲸吃？', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 10)).pack(padx=18, pady=(10, 6))
        row = Frame(win, bg='#eef3ff')
        row.pack(pady=(0, 8))
        def pick(kind):
            win.destroy()
            if kind == 'tidy':
                self._do_tidy(paths)
            else:
                if kind == 'eat':
                    self._do_eat_drop(paths)
                else:
                    self.say('那本鲸先不动它们～', 2400)
        tk.Button(row, text='帮忙整理', width=10, font=('Microsoft YaHei', 10), command=lambda: pick('tidy')).pack(side='left', padx=5)
        tk.Button(row, text='给大肥鲸吃', width=10, font=('Microsoft YaHei', 10), command=lambda: pick('eat')).pack(side='left', padx=5)
        tk.Button(row, text='先放着', width=8, font=('Microsoft YaHei', 10), command=lambda: pick('later')).pack(side='left', padx=5)
        tk.Label(win, text='「帮忙整理」按类型归到同目录的分类文件夹；「给本鲸吃」搬进投喂文件夹并永久删除、换成米饭', bg='#eef3ff', fg='#8a97b3', wraplength=310, justify='left', font=('Microsoft YaHei', 8)).pack(padx=18, pady=(0, 12))
        win.update_idletasks()
        sw, _ = self.screen()
        x = int(min(max(4, self.cx - win.winfo_reqwidth() / 2), sw - win.winfo_reqwidth() - 4))
        y = int(max(4, self.foot - self.ground_line - win.winfo_reqheight() - MOOD_SIZE - 26))
        win.geometry(f'+{x}+{y}')
    def _do_tidy(self, paths):
        """帮忙整理：按类型把东西挪进同目录的分类文件夹（一脸不情愿）。"""
        self.force_mood, self.force_until = ('tidy', time.time() + 6)
        self.emote('deepseek-pressure', 2800)
        self.say('唔……本鲸不想动，但主人的吩咐……好吧。', 3200)
        detail, failed = ({}, [])
        for p in paths:
            src = os.path.abspath(p.rstrip('\\/'))
            parent = os.path.dirname(src)
            cat = tidy_category(src)
            if os.path.basename(parent) == cat:
                continue
            else:
                try:
                    dest = os.path.join(parent, cat)
                    os.makedirs(dest, exist_ok=True)
                    shutil.move(src, unique_path(dest, os.path.basename(src)))
                    detail[cat] = detail.get(cat, 0) + 1
                except Exception:
                    failed.append(os.path.basename(src))
        moved = sum(detail.values())
        if not moved:
            self.say('唔……这些东西本鲸不知道该怎么放。', 3000)
            return
        else:
            parts = '、'.join((f'{k} {v} 个' for k, v in detail.items()))
            msg = f'呼……累死本鲸了。{moved} 样都归好类了：{parts}。'
            if failed:
                msg += f'（{len(failed) / 2} 样没搬动）'
            self.say(msg, 5000)
    def _do_eat_drop(self, paths):
        """给本鲸吃：搬进投喂文件夹，然后吃掉变成米饭。"""
        self.force_mood = None
        self.happy_until = time.time() + 10
        self.emote('cheerful', 2400)
        self.say('诶嘿～主人最好啦！本鲸开动咯～', 3000)
        d = self.feed_dir()
        dests = []
        for p in paths:
            try:
                dests.append(shutil.move(p, unique_path(d, os.path.basename(p.rstrip('\\/')))))
            except Exception:
                pass
        self.root.after(1000, lambda: self._after_eat(self._devour(dests), dropped=True))
    def add_rice(self, n):
        st = self.save_data
        st['rice'] = int(st.get('rice', 0)) + n
        st['rice_date'] = date.today().isoformat()
        save_state(st)
    def rice_left_today(self):
        st = self.save_data
        if st.get('feed_day') != date.today().isoformat():
            return FEED_MAX_PER_DAY
        else:
            return max(0, FEED_MAX_PER_DAY - int(st.get('feed_count', 0)))
    def feed(self):
        """投喂：喂一碗米饭（每天有次数上限）。"""
        st = self.save_data
        today = date.today().isoformat()
        if st.get('feed_day') != today:
            st['feed_day'] = today
            st['feed_count'] = 0
            save_state(st)
        if int(st.get('rice', 0)) <= 0:
            self.wake()
            self.say('碗里没有米饭了…主人先「打扫投喂文件夹」换点米饭吧～', 4000)
            return
        else:
            if self.rice_left_today() <= 0:
                self.wake()
                self.say(f'今天已经喂了 {FEED_MAX_PER_DAY} 次啦，明天再来～（本鲸才不是吃太多）', 4000)
                return
            else:
                st['rice'] = int(st['rice']) - 1
                st['feed_count'] = int(st.get('feed_count', 0)) + 1
                st['feed_total'] = int(st.get('feed_total', 0)) + 1
                st['last_feed'] = time.time()
                st['hunger'] = 0.0
                st['hunger_at'] = time.time()
                save_state(st)
                self._hunger_saved = 0.0
                self.mood_add(10)
                self.wake()
                self._log_op('投喂了本鲸一碗米饭')
                self.meet()
                self.say('啊呜——好吃！本鲸开动了～', 3000)
                self._eat_anim(1)
    def _check_rice(self):
        """放太久的米饭会馊掉。"""
        st = self.save_data
        if int(st.get('rice', 0)) <= 0 or not st.get('rice_date'):
            return None
        else:
            try:
                made = date.fromisoformat(st['rice_date'])
            except ValueError:
                return None
            if (date.today() - made).days <= RICE_SPOIL_DAYS:
                return
            else:
                lost = int(st['rice'])
                st['rice'] = 0
                st['rice_date'] = ''
                save_state(st)
                self.wake()
                self.say(f'呜……{lost} 碗米饭放太久馊掉了，主人好久没喂本鲸了。', 5200)
    def _bowl_photo(self, f):
        ck = round(f, 2)
        if ck not in self.bowl_cache:
            im = bowl_image(self.body_h * 0.36)
            w = max(1, int(im.width * f))
            h = max(1, int(im.height * f))
            self.bowl_cache[ck] = ImageTk.PhotoImage(harden(im.resize((w, h), Image.LANCZOS)))
        return self.bowl_cache[ck]
    def _eat_anim(self, bowls=1):
        """吃米饭动画：饭碗从脚边飘到嘴边，一口口变小消失，边吃边嚼。"""
        if self.sleeping or self.dragging:
            return None
        else:
            if self.edge:
                self.come_out()
            self.gesturing = False
            self.turn_id += 1
            self.eat_gen += 1
            gen = self.eat_gen
            self.state = 'idle'
            self.set_pose('front')
            self.emote('deepseek-rice', 2600)
            self.eating = True
            self.eat_until = time.time() + 8
            if self.bowl_item is None:
                self.bowl_item = self.canvas.create_image(0, 0, image=None, state='hidden')
            seq = [(0.5, 0.0), (0.78, 0.05), (0.95, 0.3), (1.0, 0.55), (1.0, 0.85), (0.85, 0.95), (0.6, 0.96), (0.34, 0.96), (0.0, 0.96)]
            full = self._bowl_photo(1.0)
            ground_y = self.ground_line - full.height() // 2 + 2
            mouth_y = self.ground_line - self.body_h * 0.62
            bowls = max(1, min(int(bowls), 3))
            def play(k, i=0):
                if gen != self.eat_gen:
                    return
                else:
                    if k >= bowls:
                        self.canvas.itemconfig(self.bowl_item, state='hidden')
                        self.eating = False
                        return
                    else:
                        if i >= len(seq):
                            play(k + 1, 0)
                            return
                        else:
                            f, p = seq[i]
                            if f <= 0:
                                play(k + 1, 0)
                                return
                            else:
                                ph = self._bowl_photo(f)
                                self.canvas.itemconfig(self.bowl_item, image=ph, state='normal')
                                y = ground_y + (mouth_y - ground_y) * p
                                self.canvas.coords(self.bowl_item, self.canvas_size[0] // 2, y - ph.height() // 2)
                                if i in (5, 7):
                                    self.hop = 5
                                if i >= 4:
                                    self.chew = 3
                                self.root.after(85, lambda: play(k, i + 1))
            play(0)
    def _title(self, text):
        """把台词里的「主人」换成主人自己定的称呼（没改过就是主人）。"""
        t = str(self.cfg.get('user_title') or '主人').strip() or '主人'
        if t == '主人':
            return str(text)
        else:
            return str(text).replace('主人', t)
    def say(self, text, ms=2600):
        text = self._title(text)
        if self.bubble is not None and (not self.bubble.winfo_exists()):
            self.bubble = tk.Toplevel(self.root)
            self.bubble.overrideredirect(True)
            self.bubble.attributes('-topmost', True)
            self.bubble.configure(bg='#ffffff')
            self.blabel = tk.Label(self.bubble, text='', bg='#ffffff', fg='#22315a', font=('Microsoft YaHei', 10), justify='left', padx=10, pady=6, bd=0)
            self.blabel.pack()
        self.blabel.config(text=text)
        self.bubble.update_idletasks()
        bw = self.blabel.winfo_reqwidth()
        bh = self.blabel.winfo_reqheight()
        sw, _ = self.screen()
        left = int(min(max(4, self.cx - bw / 2), sw - bw - 4))
        reserve = MOOD_SIZE + 4 if self._mood_visible() else 0
        top = int(max(4, self.foot - self.ground_line - reserve - bh - 4))
        self.bubble.geometry(f'+{left}+{top}')
        self.bubble.deiconify()
        if self.bubble_job:
            self.root.after_cancel(self.bubble_job)
        self.bubble_job = self.root.after(ms, self._hide_bubble)
    def _hide_bubble(self):
        self.bubble_job = None
        if self.bubble and self.bubble.winfo_exists():
                self.bubble.withdraw()
    def _expr_photo(self, name):
        """按当前大小把表情图缩放成 PhotoImage（按缩放比例缓存复用）。"""
        ck = (name, round(self.scale, 4))
        if ck not in self._expr_cache:
            im = load_emoji(name)
            if im is None:
                return
            else:
                k = self.body_h / im.height
                size = (max(1, int(im.width * k)), max(1, int(im.height * k)))
                self._expr_cache[ck] = ImageTk.PhotoImage(harden(im.resize(size, Image.LANCZOS)))
        return self._expr_cache[ck]
    def _sleep_photo(self):
        """睡沉用的「睡眠」表情：裁掉透明留白再缩放。\n\n这张是坐姿（比较方），所以按「别比站着还高、别被窗口切掉」来缩，\n于是它自己就坐在地面线上，不会飘着。\n"""
        ck = ('sleepy-sit', round(self.scale, 4))
        if ck not in self._expr_cache:
            im = load_emoji('sleepy')
            if im is None:
                return
            else:
                self._expr_cache[ck] = ImageTk.PhotoImage(harden(sleep_sprite(im, self.body_h * 0.95)))
        return self._expr_cache[ck]
    def _sync_sleep_canvas(self):
        """睡沉时把画布临时撑宽，好让「睡眠」表情（坐姿，比较宽）不被切掉；\n醒来 / 被打断就还原。每帧对一下，怎么都能自愈。"""
        on = self.sleeping
        want = self.base_canvas_size[0]
        if on:
            photo = self._sleep_photo()
            if photo is not None:
                want = max(want, photo.width() + 4)
        if self.canvas_size[0] == want:
            return
        else:
            self.canvas_size = (want, self.base_canvas_size[1])
            self.ground_line = self.base_canvas_size[1] - PAD_BOTTOM
            self.canvas.config(width=want, height=self.canvas_size[1])
            self._apply_geometry()
    def emote(self, name, hold=1800, force=False):
        """心情来了就让桌宠本人变成对应的小表情（素材出处见文件头）。\n\n想换就换、连着换也行，没有冷却；hold<=0 表示一直保持这张，不自动收回去。\n"""
        if self.quiet and (not force):
            return
        else:
            photo = self._expr_photo(name)
            if photo is None:
                return
            else:
                self.expr_name = name
                self.expr_photo = photo
                self.expr_until = float('inf') if hold <= 0 else time.time() + hold / 1000.0
                self.emote_until = self.expr_until
    def clear_emote(self):
        """把「一直摆着」的表情收掉，变回平时的立绘。"""
        self.expr_name = None
        self.expr_photo = None
        self.expr_until = 0.0
        self.emote_until = 0.0
        self.say('好啦，本鲸变回原来的样子～', 2200)
    def emote_gallery(self):
        """把所有小表情列出来看（4×4）。"""
        win = tk.Toplevel(self.root)
        win.title('小表情一览（素材：大肥鱼桌宠 DaFeiYu Pet）')
        win.configure(bg='#eef3ff')
        win.attributes('-topmost', True)
        tk.Label(win, text='小表情一览', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=(12, 2))
        tk.Label(win, text='素材来自 GitHub: XiaoHan-612/dafeiyu-pet（未声明 LICENSE，个人自用）', bg='#eef3ff', fg='#6b7a99', font=('Microsoft YaHei', 8)).grid(row=1, column=0, columnspan=4, pady=(0, 8))
        self._gallery_refs = []
        for i, name in enumerate(EMOJI_FILES):
            im = load_emoji(name)
            cell = Frame(win, bg='#eef3ff')
            cell.grid(row=2 + i // 4, column=i % 4, padx=6, pady=6)
            if im is not None:
                ph = ImageTk.PhotoImage(harden(im.resize((96, 96), Image.LANCZOS)))
                self._gallery_refs.append(ph)
                tk.Label(cell, image=ph, bg='#eef3ff', bd=0).pack()
            tk.Label(cell, text=name, bg='#eef3ff', fg='#4a5a7a', font=('Microsoft YaHei', 8)).pack()
            for w in [cell]:
                w.bind('<Button-1>', lambda e, n=name: self.emote(n, 2600, force=True))
        tk.Button(win, text='关闭', width=8, font=('Microsoft YaHei', 10), command=win.destroy).grid(row=6, column=0, columnspan=4, pady=10)
    def _update_expression(self):
        """心情一变，就把桌宠本人换成对应的小表情。"""
        key = self.mood()
        if key == self.mood_seen:
            return
        else:
            self.mood_seen = key
            name = MOOD_EXPR.get(key)
            if name:
                self.emote(name, MOOD_EXPR_HOLD)
    def mood(self):
        """当前心情，决定头顶气泡里显示哪个 emoji。"""
        if self.sleeping:
            return 'sleep' if self.deep_sleep else 'nap'
        else:
            if self.force_mood and time.time() < self.force_until:
                return self.force_mood
            else:
                if time.time() < self.grumpy_until:
                    return 'grumpy'
                else:
                    if self.dragging:
                        return 'scared'
                    else:
                        if self.eating and time.time() < self.eat_until:
                            return 'eat'
                        else:
                            if self.is_sad():
                                return 'sad'
                            else:
                                if time.time() < self.happy_until:
                                    return 'happy'
                                else:
                                    if self.pending:
                                        return 'work'
                                    else:
                                        if self.quiet:
                                            return 'quiet'
                                        else:
                                            if self.state == 'follow':
                                                return 'run'
                                            else:
                                                if self.state in ['walk', 'float']:
                                                    return 'walk'
                                                else:
                                                    return 'idle'
    def status_text(self):
        """给托盘 tooltip 用的一句话状态。"""
        if self.edge:
            return '躲在屏幕边边'
        else:
            return MOOD_TEXT.get(self.mood(), '待机中')
    def hunger(self):
        """饥饿值 0~100（喂一碗米饭就回饱）。\n\n不再是「按上次喂饭的时间算」，而是每秒攒出来的一格 ——\n这样才能做到熟睡 / 打盹长得慢、心情低长得快。\n"""
        return max(0.0, min(100.0, float(self.save_data.get('hunger') or 0.0)))
    def hunger_mult(self):
        """饥饿增长倍率：熟睡 < 打盹 < 平常 < 心情低。"""
        mult = 1.0
        if self.deep_sleep:
            mult *= HUNGER_MULT_SLEEP
        else:
            if self.sleeping:
                mult *= HUNGER_MULT_NAP
        if mood_tier(self.mood_value()) == 'low':
            mult *= HUNGER_MULT_LOW
        return mult
    def _grow_hunger(self):
        """按当前状态攒饥饿值（每秒一次；人不在的那段按平常速度补）。"""
        st = self.save_data
        now = time.time()
        last = float(st.get('hunger_at') or 0.0)
        if not last:
            st['hunger_at'] = now
            save_state(st)
            return
        else:
            gap = now - last
            if gap <= 0:
                return
            else:
                per_hour = 100.0 / HUNGER_FULL_HOURS
                rate = per_hour if gap > 300 else per_hour * self.hunger_mult()
                st['hunger'] = min(100.0, float(st.get('hunger') or 0.0) + min(gap, HUNGER_FULL_HOURS * 3600.0) / 3600.0 * rate)
                st['hunger_at'] = now
                if abs(st['hunger'] - self._hunger_saved) >= 1.0:
                    self._hunger_saved = st['hunger']
                    save_state(st)
    def mood_rate(self):
        """每小时心情掉多少（关掉开关或设成 0 就不掉）。"""
        if not self.cfg.get('mood_decay_on', True):
            return 0.0
        else:
            return max(0.0, float(self.cfg.get('mood_decay', MOOD_DECAY_PER_HOUR) or 0))
    def mood_value(self):
        """心情值 0~100（久不互动会按设定慢慢降）。"""
        st = self.save_data
        return mood_value_of(st.get('mood_val'), st.get('mood_at'), rate=self.mood_rate())
    def mood_add(self, delta):
        """心情涨/跌一点（顺便重置回落计时）。"""
        st = self.save_data
        val = mood_value_of(st.get('mood_val'), st.get('mood_at'), rate=self.mood_rate()) + float(delta)
        st['mood_val'] = max(MOOD_VAL_MIN, min(MOOD_VAL_MAX, val))
        st['mood_at'] = time.time()
        save_state(st)
    def _update_tray_tip(self):
        """鼠标悬浮到托盘小图标上能看到当前状态；右键菜单也顺带更新。"""
        st = self.save_data
        tip = f'{APP_NAME} · {self.status_text()}｜心情 {self.mood_value():.0f}%｜饥饿 {self.hunger():.0f}%｜熟悉度 {familiarity_text(self.familiar_score()[0])}'
        rice = int(st.get('rice', 0) or 0)
        if rice:
            tip += f'｜米饭 {rice}'
        fresh = tip != self._tray_tip
        if fresh:
            self._tray_tip = tip
            self.tray.set_tooltip(tip)
        if fresh or self.t % 30 == 0:
            menu = self._tray_menu()
            if menu != self.tray.menu:
                self.tray.menu = menu
    def _mood_visible(self):
        """气泡现在该不该露出来（只在心情变化时 / 时不时冒一下，不是常驻）。"""
        return bool(self.mood_show.get() and time.time() < self.mood_until)
    def _update_mood(self):
        """头顶气泡：心情一变就冒一下，平时也时不时冒一下，然后自己收起来。"""
        now = time.time()
        key = self.mood()
        if key != self.mood_last:
            self.mood_last = key
            self.mood_next = now + random.uniform(*MOOD_POP_GAP)
            if key in MOOD_NOTABLE:
                self.mood_until = now + MOOD_SHOW_SEC
        else:
            if now >= self.mood_next:
                self.mood_until = now + MOOD_SHOW_SEC
                self.mood_next = now + random.uniform(*MOOD_POP_GAP)
        if not self._mood_visible():
            if self.mood_win is not None and self.mood_win.winfo_exists() and self.mood_win.winfo_viewable():
                        self.mood_win.withdraw()
            return None
        else:
            if self.mood_win is None or not self.mood_win.winfo_exists():
                self.mood_win = tk.Toplevel(self.root)
                self.mood_win.overrideredirect(True)
                self.mood_win.attributes('-topmost', True)
                self.mood_win.configure(bg=KEY)
                self.mood_win.attributes('-transparentcolor', KEY)
                self.mood_canvas = tk.Canvas(self.mood_win, highlightthickness=0, bd=0, width=MOOD_SIZE, height=MOOD_SIZE, bg=KEY)
                self.mood_canvas.pack()
                self.mood_item = self.mood_canvas.create_image(MOOD_SIZE // 2, MOOD_SIZE // 2, image=None)
                self.mood_key = None
            if key != self.mood_key or self.mood_photo is None:
                self.mood_key = key
                self.mood_photo = ImageTk.PhotoImage(harden(mood_bubble_image(MOOD_EMOJI.get(key, '🙂'), MOOD_SIZE)))
                self.mood_canvas.itemconfig(self.mood_item, image=self.mood_photo)
            sw, _ = self.screen()
            left = min(max(2, self.cx - MOOD_SIZE / 2), sw - MOOD_SIZE - 2)
            top = max(2, self.foot - self.ground_line - MOOD_SIZE - 2)
            self.mood_win.geometry(f'{MOOD_SIZE}x{MOOD_SIZE}+{int(left)}+{int(top)}')
            if not self.mood_win.winfo_viewable():
                self.mood_win.deiconify()
    def _icon(self, emoji):
        """菜单小图标：转成 ImageTk 并缓存（否则会被回收变空白）。"""
        if emoji not in self._icon_cache:
            self._icon_cache[emoji] = ImageTk.PhotoImage(menu_icon(emoji))
        return self._icon_cache[emoji]
    def _menu(self):
        self.menu = Menu(self.root, tearoff=0)
        style_menu(self.menu)
        ic = self._icon
        self._menu_header()
        self.menu.add_command(label='跟我聊天（双击也可）', image=ic('💬'), compound='left', command=self.open_chat)
        self.menu.add_command(label='聊天 API 设置…', image=ic('🔧'), compound='left', command=self.open_settings)
        self.menu.add_command(label='应用设置…（大小 / 语音 / 热键 / 自启）', image=ic('⚙️'), compound='left', command=self.app_settings)
        md = Menu(self.menu, tearoff=0)
        style_menu(md)
        md.add_radiobutton(label='本地模式（只用自带的台词，不联网）', image=ic('🐚'), compound='left', variable=self.online_var, value=False, command=self._apply_mode)
        md.add_radiobutton(label='在线模式（让 AI 想，要填 API）', image=ic('🌐'), compound='left', variable=self.online_var, value=True, command=self._apply_mode)
        md.add_separator()
        md.add_checkbutton(label='让 AI 接管它的一举一动', image=ic('🧠'), compound='left', variable=self.ai_brain, command=self._apply_brain)
        self.menu.add_cascade(label='模式', image=ic('🔄'), compound='left', menu=md)
        self.menu.add_checkbutton(label='启用 DeepSeek 余额悬浮窗', image=ic('💰'), compound='left', variable=self.balance_win, command=self.toggle_balance_win)
        self.menu.add_checkbutton(label='余额窗·点击穿透（不挡鼠标）', image=ic('🖱'), compound='left', variable=self.balance_ct, command=self._apply_balance_click_through)
        self.menu.add_checkbutton(label='余额提醒（低余额 / 查询失败变色）', image=ic('🔔'), compound='left', variable=self.balance_alert_on, command=self._apply_balance_alert)
        self.menu.add_command(label='一起猜拳', image=ic('✊'), compound='left', command=self.open_rps)
        vm = Menu(self.menu, tearoff=0)
        style_menu(vm)
        vm.add_checkbutton(label='语音唤醒（喊一声叫大肥鲸）', image=ic('👂'), compound='left', variable=self.voice_wake, command=self._apply_voice)
        vm.add_checkbutton(label='语音对话（听到的话去问大肥鲸）', image=ic('🗣️'), compound='left', variable=self.voice_chat, command=self._apply_voice)
        vm.add_checkbutton(label='朗读大肥鲸的回答', image=ic('🔊'), compound='left', variable=self.voice_speak, command=self._apply_voice)
        vm.add_separator()
        vm.add_command(label='说一句测试', image=ic('🎤'), compound='left', command=self.voice_test)
        vm.add_command(label='停止朗读', image=ic('⏹️'), compound='left', command=self.voice.stop_speak)
        vm.add_command(label='设置唤醒词…', image=ic('✏️'), compound='left', command=self.set_wake_words)
        self.menu.add_cascade(label='语音', image=ic('🎙️'), compound='left', menu=vm)
        mm = Menu(self.menu, tearoff=0)
        style_menu(mm)
        mm.add_checkbutton(label='记下主人今天做的事（会看屏幕）', image=ic('📔'), compound='left', variable=self.mem_on, command=self._apply_memory)
        mm.add_command(label='现在记一笔', image=ic('✍️'), compound='left', command=self.memory_now)
        mm.add_separator()
        mm.add_command(label='看看今天的记录', image=ic('📖'), compound='left', command=self.show_memory)
        mm.add_command(label='打开记录文件夹', image=ic('📂'), compound='left', command=self.open_memory_dir)
        self.menu.add_cascade(label='AI 记录', image=ic('📔'), compound='left', menu=mm)
        pa = Menu(self.menu, tearoff=0)
        style_menu(pa)
        pa.add_checkbutton(label='主动帮忙（合适的时候递几个选项，让你挑）', image=ic('💡'), compound='left', variable=self.ask_on, command=self._apply_proactive)
        pa.add_checkbutton(label='跳过熟悉度（不攒熟悉度也能用）', image=ic('⚡'), compound='left', variable=self.skip_familiar, command=self._apply_proactive)
        pa.add_separator()
        for label, sec in [('每 1 分钟最多一次', 60), ('每 3 分钟最多一次', 180), ('每 5 分钟最多一次', 300), ('每 10 分钟最多一次', 600), ('每 30 分钟最多一次', 1800)]:
            pa.add_radiobutton(label=label, variable=self.ask_gap, value=sec, command=self._apply_proactive)
        pa.add_separator()
        pa.add_command(label='现在就提个议', image=ic('✨'), compound='left', command=self.try_proactive)
        pa.add_separator()
        pa.add_command(label=f'状态 / 熟悉度：{familiarity_text(self.familiar_score()[0])}', image=ic('📊'), compound='left', command=self.show_status)
        self.menu.add_cascade(label='主动智能', image=ic('💡'), compound='left', menu=pa)
        mm2 = Menu(self.menu, tearoff=0)
        style_menu(mm2)
        mm2.add_checkbutton(label='认文本里的 [CMD: …] 这类命令', image=ic('⌨️'), compound='left', variable=self.quick_on, command=self._apply_quick)
        mm2.add_command(label='打开快捷命令输入框', image=ic('⌨️'), compound='left', command=self.quick_show)
        mm2.add_command(label='执行剪贴板里的命令', image=ic('📋'), compound='left', command=self.run_clipboard_quick)
        mm2.add_separator()
        mm2.add_command(label='命令一览…', image=ic('📖'), compound='left', command=self.show_command_help)
        mm2.add_command(label=f'设置热键…（现在：{self.cfg.get('hotkey') or '无'}）', image=ic('🎹'), compound='left', command=self.set_hotkey)
        self.menu.add_cascade(label='快捷命令', image=ic('⌨️'), compound='left', menu=mm2)
        me = Menu(self.menu, tearoff=0)
        style_menu(me)
        me.add_command(label='记一条重要信息…', image=ic('📌'), compound='left', command=self.ask_save_memo)
        me.add_command(label='都记了什么', image=ic('📖'), compound='left', command=self.show_memos)
        me.add_command(label='打开重要信息文件', image=ic('📂'), compound='left', command=self.open_memo_file)
        self.menu.add_cascade(label='重要信息', image=ic('📌'), compound='left', menu=me)
        self.menu.add_separator()
        self.menu.add_checkbutton(label='跟随鼠标', image=ic('🖱️'), compound='left', variable=self.follow)
        self.menu.add_command(label='打个盹 / 叫醒她（点她一下也可以）', image=ic('😴'), compound='left', command=self.toggle_sleep)
        self.menu.add_command(label='睡沉一点（抱着玩偶呼呼大睡）', image=ic('🛌'), compound='left', command=self.sleep_deep)
        ex = Menu(self.menu, tearoff=0)
        style_menu(ex)
        for name in EMOJI_FILES:
            ex.add_command(label=EMOJI_CN.get(name, name), command=lambda n=name: self.emote(n, 0, force=True))
        ex.add_separator()
        ex.add_command(label='看全部表情（大图）', command=self.emote_gallery)
        ex.add_command(label='收起来，恢复原样', command=self.clear_emote)
        self.menu.add_cascade(label='摆个表情（一直保持）', image=ic('🎭'), compound='left', menu=ex)
        hide = Menu(self.menu, tearoff=0)
        style_menu(hide)
        hide.add_command(label='躲到左边（露个头）', image=ic('⬅️'), compound='left', command=lambda: self.hide_at_edge('left'))
        hide.add_command(label='躲到右边（露个头）', image=ic('➡️'), compound='left', command=lambda: self.hide_at_edge('right'))
        hide.add_separator()
        hide.add_command(label='出来吧（点她一下也行）', image=ic('👋'), compound='left', command=self.come_out)
        self.menu.add_cascade(label='躲到屏幕边边', image=ic('🙈'), compound='left', menu=hide)
        self.menu.add_command(label='表演一下（随机小动作）', image=ic('🎭'), compound='left', command=self.gesture)
        self.menu.add_command(label='随机换个小表情', image=ic('😊'), compound='left', command=lambda: self.emote(random.choice(list(EMOJI_FILES)), 2600, force=True))
        self.menu.add_command(label='小表情一览…', image=ic('🖼️'), compound='left', command=self.emote_gallery)
        self.menu.add_checkbutton(label='头顶心情气泡', image=ic('💭'), compound='left', variable=self.mood_show)
        self.menu.add_separator()
        self.menu.add_command(label='现在主人在干什么？', image=ic('🔍'), compound='left', command=self.where_is_master)
        self.menu.add_checkbutton(label='安静模式（主人在全屏时自动回避）', image=ic('🤫'), compound='left', variable=self.quiet_mode)
        self.menu.add_command(label='让本鲸操作电脑…', image=ic('🤖'), compound='left', command=self._cua_menu_start)
        act = Menu(self.menu, tearoff=0)
        style_menu(act)
        act.add_command(label='打开记事本', image=ic('📝'), compound='left', command=lambda: self.do_tool('open_app', {'name': '记事本'}))
        act.add_command(label='打开计算器', image=ic('🧮'), compound='left', command=lambda: self.do_tool('open_app', {'name': '计算器'}))
        act.add_command(label='打开画图', image=ic('🎨'), compound='left', command=lambda: self.do_tool('open_app', {'name': '画图'}))
        act.add_command(label='打开资源管理器', image=ic('📁'), compound='left', command=lambda: self.do_tool('open_app', {'name': '资源管理器'}))
        act.add_separator()
        act.add_command(label='静音 / 取消静音', image=ic('🔇'), compound='left', command=lambda: self.do_tool('volume', {'action': 'mute'}))
        act.add_command(label='音量 +', image=ic('🔊'), compound='left', command=lambda: self.do_tool('volume', {'action': 'up', 'times': 2}))
        act.add_command(label='音量 -', image=ic('🔉'), compound='left', command=lambda: self.do_tool('volume', {'action': 'down', 'times': 2}))
        act.add_command(label='播放 / 暂停', image=ic('🎵'), compound='left', command=lambda: self.do_tool('volume', {'action': 'pause'}))
        act.add_separator()
        act.add_command(label='截个屏', image=ic('📸'), compound='left', command=lambda: self.do_tool('screenshot', {}))
        act.add_command(label='看看内存', image=ic('📊'), compound='left', command=lambda: self.do_tool('system_info', {}))
        act.add_command(label='收起所有窗口', image=ic('🖥️'), compound='left', command=lambda: self.do_tool('show_desktop', {}))
        act.add_command(label='锁定屏幕', image=ic('🔒'), compound='left', command=lambda: self.do_tool('lock_screen', {}))
        act.add_separator()
        act.add_command(label='设置提醒…', image=ic('⏰'), compound='left', command=self.ask_remind)
        self.menu.add_cascade(label='帮我做事', image=ic('🛠️'), compound='left', menu=act)
        self.menu.add_separator()
        rice = int(self.save_data.get('rice', 0))
        left = self.rice_left_today()
        self.menu.add_command(label='打扫投喂文件夹（垃圾变米饭）', image=ic('🧹'), compound='left', command=self.clean_feed)
        self.menu.add_command(label=f'投喂一碗米饭（米饭 {rice} 碗 · 今日 {left}/{FEED_MAX_PER_DAY} · 饥饿 {self.hunger():.0f}%）', image=ic('🍚'), compound='left', command=self.feed)
        self.menu.add_command(label='打开投喂文件夹', image=ic('📂'), compound='left', command=self.open_feed_dir)
        self.menu.add_separator()
        self.menu.add_command(label='番茄钟：专注 25 分钟', image=ic('🍅'), compound='left', command=lambda: self.start_pomodoro(25, '专注'))
        self.menu.add_command(label='番茄钟：休息 5 分钟', image=ic('☕'), compound='left', command=lambda: self.start_pomodoro(5, '休息'))
        self.menu.add_command(label='取消计时', image=ic('❌'), compound='left', command=self.cancel_pomodoro)
        self.menu.add_separator()
        self.menu.add_command(label='放大一点', image=ic('➕'), compound='left', command=lambda: self.set_scale(1.15))
        self.menu.add_command(label='缩小一点', image=ic('➖'), compound='left', command=lambda: self.set_scale(0.87))
        self.menu.add_command(label='回到右下角', image=ic('🏠'), compound='left', command=self.go_home)
        self.menu.add_separator()
        self.menu.add_command(label='退出', image=ic('🚪'), compound='left', command=self.quit)
    def toggle_sleep(self):
        if self.sleeping:
            self.wake(grumpy=True)
        else:
            self.sleep()
    def _hide_photo_for(self, side):
        """躲边用的立绘：往屏幕里侧歪一点，这样只露头、身体藏在屏幕外。"""
        ck = (side, round(self.scale, 4))
        if ck not in self._hide_cache:
            base = self.base['front']
            im = base.resize(self._fit(base), Image.LANCZOS)
            im = im.rotate(-EDGE_TILT if side == 'left' else EDGE_TILT, expand=True, resample=Image.BICUBIC)
            self._hide_cache[ck] = ImageTk.PhotoImage(harden(im))
        return self._hide_cache[ck]
    def _apply_hide(self):
        """换成「躲边」用的画布和图片（歪着的立绘，身体留在屏幕外）。"""
        if self._normal_geo is None:
            self._normal_geo = (self.canvas_size, self.ground_line)
        photo = self._hide_photo_for(self.edge)
        self.canvas_size = (photo.width(), photo.height())
        self.ground_line = photo.height()
        self.canvas.config(width=photo.width(), height=photo.height())
        self._show(photo)
        self._apply_geometry()
    def _snap_to_edge(self):
        """拖到屏幕左右边边上就自动贴过去藏起来。返回 True 表示已经躲好了。"""
        if self.sleeping or not self.edge_snap.get():
            return False
        else:
            sw = self.screen()[0]
            pad = self.canvas_size[0] / 2 + EDGE_SNAP_PAD
            if self.cx <= pad:
                side = 'left'
            else:
                if self.cx >= sw - pad:
                    side = 'right'
                else:
                    return False
            self._log_op('把本鲸拖到屏幕边边，它自己躲进去了')
            self.hide_at_edge(side)
            return True
    def hide_at_edge(self, side):
        if self.edge == side:
            return
        else:
            self._interrupt()
            self.dragging = False
            self.sleeping = False
            self.deep_sleep = False
            self._close_ask()
            self.edge = side
            self.state = 'hide'
            self.foot = float(self.screen()[1] - 40)
            self._apply_hide()
            self.say(random.choice(HIDE_LINES), 2200)
    def _slide_along_edge(self, foot_target):
        """躲边时沿着屏幕边上下滑动换位置（不拽出来）。"""
        self.foot = float(foot_target)
        self._apply_geometry()
    def come_out(self, grumpy=False):
        """从屏幕边边出来。grumpy=True 表示是被硬拽出来的，会不高兴。"""
        if not self.edge:
            return
        else:
            self._interrupt()
            side = self.edge
            self.edge = None
            self.state = 'idle'
            self.idle_timer = random.randint(60, 140)
            if self._normal_geo:
                self.canvas_size, self.ground_line = self._normal_geo
                self._normal_geo = None
                self.canvas.config(width=self.canvas_size[0], height=self.canvas_size[1])
            cw, _ = self.canvas_size
            sw, _ = self.screen()
            self.cx = float(cw / 2 + 20) if side == 'left' else float(sw - cw / 2 - 20)
            self.foot = float(self.screen()[1] - 40)
            self.set_pose('front')
            self._apply_geometry()
            if grumpy:
                self.grumpy_until = time.time() + 8
                self.say(random.choice(COME_OUT_GRUMPY_LINES), 3000)
                self.emote('angry', 2200)
            else:
                self.happy_until = time.time() + 4
                self.say(random.choice(COME_OUT_LINES), 2200)
    def go_home(self):
        if self.edge:
            self.come_out()
        sw, sh = self.screen()
        self.cx = float(sw - self.canvas_size[0] / 2 - 40)
        self.foot = float(sh - 40)
        self.target_cx, self.target_y = (self.cx, self.foot)
        self.state = 'idle'
        self._apply_geometry()
    def _drain_tray(self):
        """把托盘线程丢过来的命令在主线程里执行（tkinter 只能在主线程碰）。"""
        while True:
            try:
                kind, cmd = self.tray_q.get_nowait()
            except queue.Empty:
                return None
            if kind == 'hotkey':
                self._hotkey_state(cmd)
            else:
                self._tray_command(cmd)
    def _hotkey_state(self, ok):
        """热键注册结果：换了热键就回一句；被别人占了也提醒一下。"""
        changing, self.hotkey_changing = (self.hotkey_changing, False)
        if ok:
            if changing:
                self.say('热键换好啦～', 2600)
        else:
            if self.cfg.get('hotkey'):
                self.say(f'热键 {self.cfg['hotkey']} 被别的软件占用了，右键「快捷命令 → 设置热键…」换一个吧。', 6000)
    def _tray_command(self, cmd):
        if cmd in (TRAY_SHOW, 7):
            if self.edge:
                self.come_out()
            self.go_home()
        else:
            if cmd == 1:
                sw, _ = self.screen()
                self.hide_at_edge('left' if self.cx < sw / 2 else 'right')
            else:
                if cmd == 3:
                    self.open_chat()
                else:
                    if cmd == 4:
                        self.feed()
                    else:
                        if cmd == 5:
                            self.open_rps()
                        else:
                            if cmd == TRAY_HOTKEY:
                                self.quick_show()
                            else:
                                if cmd == TRAY_FAM:
                                    self.show_status()
                                else:
                                    if cmd == TRAY_SET:
                                        self.app_settings()
                                    else:
                                        if cmd == 8:
                                            self.quit()
    def quit(self):
        try:
            self.voice.close()
        except Exception:
            pass
        try:
            self.tray.stop()
        except Exception:
            pass
        self.root.destroy()
    def open_rps(self):
        if self.rps and self.rps.winfo_exists():
            self.rps.lift()
            return
        else:
            win = tk.Toplevel(self.root)
            self.rps = win
            win.title('大肥鲸 · 猜拳')
            win.configure(bg='#eef3ff')
            win.resizable(False, False)
            win.attributes('-topmost', True)
            tk.Label(win, text='跟大肥鲸猜拳吧！', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 12, 'bold')).pack(pady=(12, 6))
            row = Frame(win, bg='#eef3ff')
            row.pack(pady=4)
            for name in ['石头', '剪刀', '布']:
                tk.Button(row, text=f'{EMOJI[name]} {name}', width=8, font=('Microsoft YaHei', 10), bg='#ffffff', fg='#22315a', relief='groove', activebackground='#dce6ff', command=lambda n: self.play_rps(n)).pack(side='left', padx=5)
            self.rps_msg = tk.Label(win, text='出拳吧～', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 10), width=30, wraplength=240)
            self.rps_msg.pack(pady=(10, 2))
            self.rps_score = tk.Label(win, text='大肥鲸 0 : 0 你', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 11, 'bold'))
            self.rps_score.pack(pady=2)
            tk.Button(win, text='关闭', width=8, font=('Microsoft YaHei', 10), command=win.destroy).pack(pady=(8, 12))
    def play_rps(self, user):
        pet = random.choice(list(EMOJI))
        if pet == user:
            tone, line = ('平局', random.choice(RPS_DRAW_LINES))
            self.mood_add(2)
        else:
            if BEATS[pet] == user:
                self.score[0] += 1
                tone, line = ('本鲸赢', random.choice(RPS_WIN_LINES))
                self.mood_add(6)
                self.celebrate()
            else:
                self.score[1] += 1
                tone, line = ('你赢', random.choice(RPS_LOSE_LINES))
                self.mood_add((-4))
                self.deject()
        msg = f'你出 {EMOJI[user]}{user}，本鲸出 {EMOJI[pet]}{pet} —— {tone}！'
        if self.rps and self.rps.winfo_exists():
                self.rps_msg.config(text=f'{msg}\n{line}')
                self.rps_score.config(text=f'大肥鲸 {self.score[0]} : {self.score[1]} 你')
        self.say(f'{msg}{line}', 3600)
    def open_chat(self):
        if self.chat and self.chat.winfo_exists():
            self.chat.lift()
            self.chat.focus_force()
            return
        else:
            win = tk.Toplevel(self.root)
            self.chat = win
            win.title('跟大肥鲸聊天')
            win.configure(bg='#eef3ff')
            win.geometry('430x430')
            win.minsize(360, 320)
            win.attributes('-topmost', True)
            top = Frame(win, bg='#eef3ff')
            top.pack(fill='x', padx=10, pady=(10, 0))
            tk.Label(top, text='大肥鲸', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 12, 'bold')).pack(side='left')
            self.chat_status = tk.Label(top, text='', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 9))
            self.chat_status.pack(side='left', padx=8)
            tk.Button(top, text='设置', width=6, font=('Microsoft YaHei', 9), command=self.open_settings).pack(side='right')
            tk.Button(top, text='清空', width=6, font=('Microsoft YaHei', 9), command=self.clear_chat).pack(side='right', padx=6)
            self.history_box = Text(win, wrap='word', height=8, width=1, bg='#ffffff', fg='#22315a', font=('Microsoft YaHei', 10), relief='flat', padx=10, pady=8, state='disabled', spacing1=2, spacing3=6)
            self.history_box.tag_config('me', foreground='#2b6cb0')
            self.history_box.tag_config('pet', foreground='#22315a')
            self.history_box.tag_config('sys', foreground='#b0393a')
            self.history_box.tag_config('who', foreground='#7b88ad')
            self.attach_bar = Frame(win, bg='#eef3ff')
            self.attach_lbl = tk.Label(self.attach_bar, text='', bg='#eef3ff', fg='#9aa6c4', font=('Microsoft YaHei', 9), anchor='w', justify='left', wraplength=310)
            tk.Button(self.attach_bar, text='添加', width=5, font=('Microsoft YaHei', 9), command=self._pick_files).pack(side='right')
            tk.Button(self.attach_bar, text='清除', width=5, font=('Microsoft YaHei', 9), command=self._clear_attachments).pack(side='right', padx=(4, 0))
            self.attach_lbl.pack(side='left', fill='x', expand=True)
            bar = Frame(win, bg='#eef3ff')
            self.chat_input = Text(bar, height=2, width=1, wrap='word', bg='#ffffff', fg='#22315a', font=('Microsoft YaHei', 10), relief='flat', padx=8, pady=6, insertbackground='#22315a')
            self.chat_input.bind('<Return>', self._on_return)
            self.send_btn = tk.Button(bar, text='发送', width=6, font=('Microsoft YaHei', 10), bg='#ffffff', fg='#22315a', command=self.send_chat)
            self.send_btn.pack(side='right', padx=(6, 0), fill='y')
            self.chat_input.pack(side='left', fill='both', expand=True)
            bar.pack(side='bottom', fill='x', padx=10, pady=(6, 10))
            self.attach_bar.pack(side='bottom', fill='x', padx=10)
            self.history_box.pack(fill='both', expand=True, padx=10, pady=8)
            for w in [self.chat_input, self.attach_bar, self.attach_lbl]:
                self._enable_dnd(w)
            self._render_attachments()
            self._append('pet', '主人你来啦～本鲸在的。（Enter 发送，Shift+Enter 换行）')
            if DND_OK:
                self._append('pet', '图片、文件、文件夹都可以直接拖到下面那个框里。')
            else:
                self._append('sys', '没装 tkinterdnd2，拖拽用不了；可以点「添加」选文件（pip install tkinterdnd2 可开启拖拽）。')
            if not self.online():
                self._append('sys', '现在是本地模式：本鲸只用自带的台词回答。想让本鲸动脑子，右键 →「模式」→ 在线模式。')
            else:
                if not self._api_ready():
                    self._append('sys', '在线模式还没配好 API，点右上角「设置」填一下地址、密钥和模型。')
            self._refresh_chat_status()
            self.chat_input.focus_set()
    def _enable_dnd(self, widget):
        if not DND_OK:
            return
        else:
            try:
                widget.drop_target_register(DND_FILES)
                widget.dnd_bind('<<Drop>>', self._on_drop)
            except Exception:
                return None
    def _on_drop(self, event):
        try:
            paths = list(self.root.tk.splitlist(event.data))
        except Exception:
            paths = [event.data]
        self._add_attachments(paths)
        return event.action
    def _add_attachments(self, paths):
        added = 0
        for p in paths:
            p = str(p).strip().strip('{}').strip()
            if not p:
                continue
            p = os.path.normpath(p)
            if p in self.attachments:
                continue
            if self.quick_on.get() and os.path.isfile(p) and (os.path.splitext(p)[1].lower() in TEXT_EXT):
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        body = f.read(400000)
                except OSError:
                    body = ''
                if body and scan_commands(body)[0]:
                    self.say(f'{os.path.basename(p)} 里有命令，本鲸跑一下～', 3000)
                    if self.chat and self.chat.winfo_exists():
                        self._append('sys', f'执行 {os.path.basename(p)} 里的快捷命令')
                        out = self._run_quick(body)
                        if out:
                            self._append('pet', out)
                    else:
                        self._run_quick(body)
                    continue
            if len(self.attachments) >= MAX_ATTACH:
                self.say(f'一次最多带 {MAX_ATTACH} 个啦～', 2200)
                break
            else:
                self.attachments.append(p)
                added += 1
        self._render_attachments()
        if added:
            self.say(f'收到 {added} 个东西啦～', 2200)
    def _pick_files(self):
        paths = filedialog.askopenfilenames(parent=self.chat, title='选给大肥鲸的东西')
        if paths:
            self._add_attachments(paths)
    def _clear_attachments(self):
        self.attachments = []
        self._render_attachments()
    @staticmethod
    def _short_name(p):
        base = os.path.basename(str(p).rstrip('\\/')) or str(p)
        if os.path.isdir(str(p)) is None:
            return base + '\\'
        else:
            return base
    def _render_attachments(self):
        if not self.attach_lbl or not self.attach_lbl.winfo_exists():
            return None
        else:
            if not self.attachments:
                tip = '把图片 / 文件 / 文件夹拖到这里' if DND_OK else '点「添加」选文件'
                self.attach_lbl.config(text=tip, fg='#9aa6c4')
            else:
                names = '、'.join((self._short_name(p) for p in self.attachments))
                self.attach_lbl.config(text=f'附件 {len(self.attachments)} 个：{names}', fg='#3a4a7a')
    @staticmethod
    def _img_data_url(path, max_side=1024):
        """图片压一下再转 base64，免得请求体太大。"""
        im = Image.open(path)
        if im.mode in ['RGBA', 'LA', 'P']:
            im = im.convert('RGBA')
            bg = Image.new('RGB', im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[(-1)])
            im = bg
        else:
            im = im.convert('RGB')
        im.thumbnail((max_side, max_side), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=85)
        return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    def _build_content(self, text, atts):
        """把文字和附件拼成一条 user 消息；图片走多模态。"""
        notes = []
        images = []
        for p in atts:
            name = self._short_name(p)
            ext = os.path.splitext(p)[1].lower()
            if os.path.isdir(p):
                try:
                    items = sorted(os.listdir(p))[:40]
                except OSError:
                    items = []
                notes.append(f'[文件夹 {name}] 里面有：{('、'.join(items) if items else '（空的）')}')
                continue
            else:
                if ext in IMG_EXT:
                    if not self.cfg.get('vision', True):
                        notes.append(f'[图片 {name}]（设置里关掉了发送图片内容）')
                        continue
                    else:
                        try:
                            images.append(self._img_data_url(p))
                        except Exception:
                            notes.append(f'[图片 {name}] 读取失败')
                        else:
                            pass
                else:
                    if ext in TEXT_EXT:
                        try:
                            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                                body = f.read(MAX_FILE_CHARS)
                        except OSError:
                            body = '（读取失败）'
                        notes.append(f'[文件 {name}] 内容：\n{body}')
                    else:
                        try:
                            size = os.path.getsize(p)
                        except OSError:
                            size = 0
                        if ext in AUDIO_EXT or ext in VIDEO_EXT:
                            kind = '视频' if ext in VIDEO_EXT else '音频'
                            notes.append(f'[{kind} {name}] 完整路径：{p}（本鲸可以用 video_summary / identify_music / transcribe_media 处理它）')
                        else:
                            notes.append(f'[文件 {name}]（{size} 字节，看不了内容，只知道名字）')
        ctx = '\n'.join(notes)[:MAX_CTX_CHARS]
        body = text
        if ctx:
            body = (text + '\n\n' if text else '') + '主人丢过来这些东西：\n' + ctx
        if not body:
            body = '（主人发来一个空内容）'
        if not images:
            return body
        else:
            content = [{'type': 'text', 'text': body}]
            content += [{'type': 'image_url', 'image_url': {'url': u}} for u in images]
            return content
    def _strip_images(self, msgs):
        """把消息里的图片换成文件名，用于不支持看图的模型重试。"""
        out = []
        for m in msgs:
            if m.get('role') == 'user' and isinstance(m.get('content'), list):
                texts = [c.get('text', '') for c in m['content'] if c.get('type') == 'text']
                n = sum((1 for c in m['content'] if c.get('type') == 'image_url'))
                out.append({'role': 'user', 'content': '\n'.join(texts) + f'\n（另有 {n} 张图片，当前模型看不了）'})
            else:
                out.append(dict(m))
        return out
    def _on_return(self, e):
        if e.state & 1:
            return
        else:
            self.send_chat()
            return 'break'
    def clear_chat(self):
        self.history = []
        if self.history_box and self.history_box.winfo_exists():
                self.history_box.config(state='normal')
                self.history_box.delete('1.0', 'end')
                self.history_box.config(state='disabled')
        self._append('sys', '对话已清空，本鲸把刚才的事都忘掉啦。')
    def _append(self, tag, text):
        box = self.history_box
        if not box or not box.winfo_exists():
            return None
        else:
            if tag == 'pet':
                text = self._title(text)
            box.config(state='normal')
            if box.index('end-1c') != '1.0':
                box.insert('end', '\n')
            box.insert('end', {'me': '我：', 'pet': '大肥鲸：', 'sys': '提示：'}[tag], 'who')
            box.insert('end', text, tag)
            box.see('end')
            box.config(state='disabled')
    def _begin_stream(self):
        self.emote('thinking', 2000)
        box = self.history_box
        if not box or not box.winfo_exists():
            return None
        else:
            box.config(state='normal')
            if box.index('end-1c') != '1.0':
                box.insert('end', '\n')
            box.insert('end', '大肥鲸：', 'who')
            box.see('end')
            box.config(state='disabled')
    def _delta(self, text):
        box = self.history_box
        if not box or not box.winfo_exists():
            return None
        else:
            box.config(state='normal')
            box.insert('end', text, 'pet')
            box.see('end')
            box.config(state='disabled')
    def send_chat(self):
        if not self.chat or not self.chat.winfo_exists():
            return None
        else:
            text = self.chat_input.get('1.0', 'end').strip()
            atts = list(self.attachments)
            if not text and (not atts):
                return
            else:
                self.chat_input.delete('1.0', 'end')
                shown = text
                if atts:
                    names = '、'.join((self._short_name(p) for p in atts))
                    shown = (text + '  ' if text else '') + f'[附件：{names}]'
                self._append('me', shown)
                self._log_op('跟本鲸说话：' + (text[:24] or '[附件]'))
                self.meet()
                self.mood_add(1)
                self._clear_attachments()
                if self.quick_on.get() and text:
                        cmds, plain = scan_commands(text)
                        if cmds:
                            self._append('sys', f'认出 {len(cmds)} 条快捷命令，本鲸去做～')
                            out = self._run_quick(text)
                            if out:
                                self._append('pet', out)
                            rest = '\n'.join(plain).strip()
                            if not rest:
                                return
                            else:
                                text = rest
                if self.pending:
                    self._append('sys', '本鲸还在想上一个问题呢，稍等一下～')
                    return
                else:
                    self._pending_msg = shown
                    if not atts:
                        hit = match_local(text)
                        if hit:
                            out = run_tool(*hit)
                            if out == '__CLEAN__':
                                self.clean_feed()
                                self._speak_reply = False
                                return
                            else:
                                self._append('pet', out)
                                self.say(out[:70], 3600)
                                self.voice_out(out)
                                return
                    if not self.online():
                        reply = self.reply(text)
                        self._append('pet', reply)
                        self.say(reply, 3200)
                        self.voice_out(reply)
                        return
                    else:
                        if not self._api_ready():
                            self._append('sys', '在线模式还没配好 API（菜单「聊天 API 设置…」填一下），本鲸先用自带的台词回答你。')
                            reply = self.reply(text)
                            self._append('pet', reply)
                            self.say(reply, 3200)
                            self.voice_out(reply)
                            return
                        else:
                            content = self._build_content(text, atts)
                            self._had_images = isinstance(content, list)
                            self._image_retry = False
                            self.tools_on = True
                            self._tool_retry = False
                            self._tool_rounds = 0
                            msgs = [{'role': 'system', 'content': system_prompt(self.cfg)}]
                            mem_ctx = self._memory_context(text)
                            if mem_ctx:
                                msgs.append(mem_ctx)
                            msgs += self.history[-int(self.cfg.get('history', 10)) * 2:]
                            msgs.append({'role': 'user', 'content': content})
                            self._last_msgs = msgs
                            self.pending = True
                            self.stream_buf = ''
                            self.send_btn.config(state='disabled')
                            self._begin_stream()
                            self._refresh_chat_status()
                            self._request(msgs)
    def _request(self, messages, cfg=None, test=False, warmup=False):
        cfg = dict(cfg or self.cfg)
        q = self._q
        tag = 'warmup' if warmup else 'test'
        def worker():
            if not (str(cfg.get('api_key') or '').strip() and str(cfg.get('api_base') or '').strip() and str(cfg.get('model') or '').strip()):
                q.put((tag, False, '请先填写 API 地址、密钥和模型') if test or warmup else ('error', '配置不完整，请点「设置」填写'))
                return
            url = cfg['api_base'].rstrip('/') + '/chat/completions'
            payload = {'model': cfg['model'], 'messages': messages, 'temperature': float(cfg.get('temperature', 0.8)), 'max_tokens': int(cfg.get('max_tokens', 160)), 'stream': not (test or warmup)}
            if not test and (not warmup) and self.tools_on:
                payload['tools'] = SYSTEM_TOOLS
                payload['tool_choice'] = 'auto'
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(cfg.get('api_key', ''))})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    if test or warmup:
                        obj = json.loads(resp.read().decode('utf-8', 'ignore'))
                        got = obj['choices'][0]['message']['content']
                        q.put((tag, True, str(got).strip()))
                        return
                    calls = {}
                    for raw in resp:
                        line = raw.decode('utf-8', 'ignore').strip()
                        if not line.startswith('data:'):
                            continue
                        data = line[5:].strip()
                        if data == '[DONE]':
                            break
                        try:
                            obj = json.loads(data)
                        except ValueError:
                            continue
                        choices = obj.get('choices') or [{}]
                        delta = choices[0].get('delta') or {}
                        piece = delta.get('content')
                        if piece:
                            q.put(('delta', piece))
                        for tc in delta.get('tool_calls') or []:
                            slot = calls.setdefault(tc.get('index', 0), {'id': '', 'name': '', 'args': ''})
                            if tc.get('id'):
                                slot['id'] = tc['id']
                            fn = tc.get('function') or {}
                            if fn.get('name'):
                                slot['name'] += fn['name']
                            if fn.get('arguments'):
                                slot['args'] += fn['arguments']
                    if calls:
                        q.put(('tools', list(calls.values())))
                    else:
                        q.put(('done', None))
            except urllib.error.HTTPError as e:
                detail = e.read().decode('utf-8', 'ignore')[:300]
                msg = f'HTTP {e.code} {detail}'
                q.put((tag, False, msg) if test or warmup else ('error', msg))
            except Exception as e:
                q.put((tag, False, str(e)) if test or warmup else ('error', str(e)))
        threading.Thread(target=worker, daemon=True).start()
    def _drain_queue(self):
        while True:
            try:
                item = self._q.get_nowait()
            except queue.Empty:
                return None
            kind = item[0]
            if kind == 'update':
                self._update_result(item[1], item[2] if len(item) > 2 else False)
                continue
            if kind == 'upd_dl':
                self._update_downloaded(item[1], item[2])
                continue
            if kind == 'cua_goal':
                self.cua_start(item[1])
                continue
            if kind == 'cua_ask':
                self._cua_ask_show(item[1])
                continue
            if kind == 'cua_hud':
                _x, _y = (item[2], item[3])
                _sw, _sh = self.screen()
                _ax = int(_x * _sw) if isinstance(_x, (int, float)) else None
                _ay = int(_y * _sh) if isinstance(_y, (int, float)) else None
                self._cua_say(item[1], _ax, _ay, bool(item[4]))
                continue
            if kind == 'cua_done':
                self.cua_busy = False
                self._cua_hide()
                self.say(item[1], 6000)
                continue
            if kind == 'cua_stop':
                self.cua_busy = False
                self._cua_hide()
                continue
            if kind == 'delta':
                self.stream_buf += item[1]
                self._delta(item[1])
            else:
                if kind == 'done':
                    self._finish_stream()
                else:
                    if kind == 'error':
                        self._fail_stream(item[1])
                    else:
                        if kind == 'test':
                            self._test_result(item[1], item[2])
                        else:
                            if kind == 'tools':
                                self._run_tool_calls(item[1])
                            else:
                                if kind == 'balwin':
                                    self._balance_show(item[1], item[2], item[3] if len(item) > 3 else False, item[4] if len(item) > 4 else '')
                                else:
                                    if kind == 'memory':
                                        self._memory_result(item[1], item[2], item[3])
                                    else:
                                        if kind == 'warmup':
                                            self._warmup_result(item[1], item[2])
                                        else:
                                            if kind == 'decide':
                                                self._decide_result(item[1], item[2])
                                            else:
                                                if kind == 'op':
                                                    self._log_op(f'让本鲸做事：{item[1]} {item[2] or ''}'.strip())
                                                else:
                                                    if kind == 'propose':
                                                        self._propose_result(item[1], item[2])
                                                    else:
                                                        if kind == 'bgdone':
                                                            self._bg_done(item[1], item[2], item[3], item[4])
    def _run_tool_calls(self, calls):
        """模型要求做事：执行，再把结果喂回去让它接着回话。"""
        self._tool_rounds += 1
        use = [c for c in calls if c.get('name')]
        msgs = list(self._last_msgs or [])
        msgs.append({'role': 'assistant', 'content': None, 'tool_calls': [{'id': c['id'] or f'call_{i}', 'type': 'function', 'function': {'name': c['name'], 'arguments': c['args'] or '{}'}} for i, c in enumerate(use)]})
        notes = []
        for i, c in enumerate(use):
            try:
                args = json.loads(c['args'] or '{}')
            except ValueError:
                args = {}
            self._log_op(f'让本鲸做事：{c['name']} {args or ''}'.strip())
            out = run_tool(c['name'], args)
            if isinstance(out, str) and out.startswith('__CUA__'):
                self._q.put(('cua_goal', out[7:]))
                out = '本鲸这就去操作电脑（会先问主人一声）。'
            elif out == '__CLEAN__':
                self.clean_feed()
                out = '已把投喂文件夹里的东西变成米饭'
            notes.append(out)
            msgs.append({'role': 'tool', 'tool_call_id': c['id'] or f'call_{i}', 'content': out})
        self._append('sys', '本鲸去做了：' + '；'.join(notes)[:180])
        if self._tool_rounds >= 3:
            self._append('pet', '（本鲸做完啦～）')
            self.pending = False
            if self.send_btn and self.send_btn.winfo_exists():
                    self.send_btn.config(state='normal')
            self._refresh_chat_status()
        else:
            self._last_msgs = msgs
            self.pending = True
            self.stream_buf = ''
            if self.send_btn and self.send_btn.winfo_exists():
                    self.send_btn.config(state='disabled')
            self._begin_stream()
            self._refresh_chat_status()
            self._request(msgs)
    def _finish_stream(self):
        self.pending = False
        if self.send_btn and self.send_btn.winfo_exists():
                self.send_btn.config(state='normal')
        reply = self.stream_buf.strip()
        if reply:
            self.history += [{'role': 'user', 'content': self._pending_msg}, {'role': 'assistant', 'content': reply}]
            keep = int(self.cfg.get('history', 10)) * 2
            if len(self.history) > keep:
                self.history = self.history[-keep:]
            self.say(reply[:60], 3600)
            self.voice_out(reply)
        else:
            self._delta('（本鲸张了张嘴，什么也没说出来…）')
            self._speak_reply = False
        self._refresh_chat_status()
    def _fail_stream(self, msg):
        if self._had_images and (not self._image_retry):
            self._image_retry = True
            self._had_images = False
            self._append('sys', '这个模型好像看不了图，本鲸把图片换成文件名再试一次…')
            self.pending = True
            self.stream_buf = ''
            if self.send_btn and self.send_btn.winfo_exists():
                    self.send_btn.config(state='disabled')
            self._begin_stream()
            self._refresh_chat_status()
            self._request(self._strip_images(self._last_msgs or []))
        else:
            if self.tools_on and (not self._tool_retry) and self._last_msgs:
                self._tool_retry = True
                self.tools_on = False
                self._append('sys', '这个模型好像不支持工具调用，本鲸先关掉再试一次…')
                self.pending = True
                self.stream_buf = ''
                if self.send_btn and self.send_btn.winfo_exists():
                        self.send_btn.config(state='disabled')
                self._begin_stream()
                self._refresh_chat_status()
                self._request(self._last_msgs)
            else:
                self.pending = False
                if self.send_btn and self.send_btn.winfo_exists():
                        self.send_btn.config(state='normal')
                self._append('sys', f'调用 API 失败：{msg}')
                fallback = self.reply(self._pending_msg)
                self._append('pet', fallback)
                self.emote('apologetic', 2000)
                self.say(fallback, 3200)
                self.voice_out(fallback)
                self._refresh_chat_status()
    def _refresh_chat_status(self):
        if not self.chat_status or not self.chat_status.winfo_exists():
            return None
        else:
            if not self.online():
                text = '本地模式（自带台词，不联网）'
            else:
                if self._api_ready():
                    text = f'在线 · {self.cfg.get('provider', '')} · {self.cfg.get('model', '')}'
                else:
                    text = '在线模式（还没配好 API）'
            if self.pending:
                text += ' · 正在想…'
            self.chat_status.config(text=text)
    def _test_result(self, ok, msg):
        if self.settings_lbl and self.settings_lbl.winfo_exists():
            self.settings_lbl.config(text=('连接成功：' if ok else '连接失败：') + msg[:80])
        else:
            messagebox.showinfo('测试连接', ('成功：' if ok else '失败：') + msg[:200], parent=self.root)
    def toggle_balance_win(self):
        """右键菜单：挂上 / 收起余额小窗。"""
        on = bool(self.balance_win.get())
        self.cfg['balance_win'] = on
        save_config(self.cfg)
        if on:
            self._open_balance_win()
            self.say('好～本鲸把余额小窗挂出来，隔一会儿自己刷新。', 3600)
        else:
            self._close_balance_win()
            self.say('好～本鲸把余额小窗收起来了。', 2600)
    def _balance_reason(self):
        """能不能查余额：能就返回 None，不能就返回一句短提示。"""
        if not self.online():
            return '本地模式看不了'
        else:
            base = str(self.cfg.get('api_base', '')).strip()
            host = (urllib.parse.urlparse(base).hostname or '').lower()
            if 'deepseek' not in host:
                return '只支持 DeepSeek'
            else:
                if not str(self.cfg.get('api_key', '')).strip():
                    return '还没填密钥'
    def _open_balance_win(self):
        """把余额小窗挂出来（无边框、置顶、左右键都能拖、点一下开设置、✕ 收起）。"""
        if self.balance_window and self.balance_window.winfo_exists():
            self.balance_window.lift()
            return
        else:
            win = tk.Toplevel(self.root)
            self.balance_window = win
            win.overrideredirect(True)
            win.attributes('-topmost', True)
            win.configure(bg='#22315a')
            card = tk.Frame(win, bg='#22315a', highlightthickness=1, highlightbackground='#3f5488')
            card.pack(fill='both', expand=True)
            ic = tk.Label(card, image=self._icon('💰'), bg='#22315a')
            ic.pack(side='left', padx=(8, 3), pady=6)
            self.balance_dot = tk.Label(card, text='●', bg='#22315a', fg='#8ea2cc', font=('Microsoft YaHei', 8))
            self.balance_dot.pack(side='left')
            self.balance_lbl = tk.Label(card, text='余额 --', bg='#22315a', fg='#eaf1ff', font=('Microsoft YaHei', 9, 'bold'))
            self.balance_lbl.pack(side='left', padx=(3, 20), pady=6)
            for w in [win, card, ic, self.balance_dot, self.balance_lbl]:
                w.bind('<ButtonPress-1>', lambda e: self._balance_press(e))
                w.bind('<ButtonPress-3>', lambda e: self._balance_press(e))
                w.bind('<B1-Motion>', self._balance_move)
                w.bind('<B3-Motion>', self._balance_move)
                w.bind('<ButtonRelease-1>', self._balance_release)
                w.bind('<ButtonRelease-3>', self._balance_release)
                try:
                    w.configure(cursor='fleur')
                except tk.TclError:
                    pass
            self.balance_alert_btn = tk.Label(card, text='知道了', bg='#22315a', fg='#ffb066', font=('Microsoft YaHei', 8, 'bold'), cursor='hand2')
            self.balance_alert_btn.place(relx=1.0, rely=0.0, anchor='ne', x=(-20), y=3)
            self.balance_alert_btn.place_forget()
            self.balance_alert_btn.bind('<Button-1>', lambda _e: (self._balance_ack_alert(), 'break')[1])
            self.balance_alert_btn.bind('<Enter>', lambda _e: self.balance_alert_btn.config(fg='#ffd28a'))
            self.balance_alert_btn.bind('<Leave>', lambda _e: self.balance_alert_btn.config(fg='#ffb066'))
            self.balance_close = tk.Label(card, text='✕', bg='#22315a', fg='#8ea2cc', font=('Microsoft YaHei', 8, 'bold'), cursor='hand2')
            self.balance_close.place(relx=1.0, rely=0.0, anchor='ne', x=(-2), y=2)
            self.balance_close.bind('<Button-1>', lambda _e: (self._balance_close_by_user(), 'break')[1])
            self.balance_close.bind('<ButtonPress-3>', lambda _e: (self._balance_open_menu(), 'break')[1])
            self.balance_close.bind('<Enter>', lambda _e: self.balance_close.config(fg='#ff8f8f'))
            self.balance_close.bind('<Leave>', lambda _e: self.balance_close.config(fg='#8ea2cc'))
            self._balance_place()
            self._balance_apply_alpha()
            self._set_click_through(win, bool(self.balance_ct.get()))
            self._balance_show_alert_btn(False)
            self.balance_next = time.time() + max(30, int(self.balance_gap.get()))
            self._balance_fetch()
    def _balance_place(self):
        """摆到记住的位置；没记过就默认屏幕右上角，并夹在屏幕内。"""
        win = self.balance_window
        if not win or not win.winfo_exists():
            return None
        else:
            win.update_idletasks()
            w, h = (win.winfo_width(), win.winfo_height())
            sw, sh = self.screen()
            pos = self.cfg.get('balance_pos')
            if pos and len(pos) == 2:
                x, y = (int(pos[0]), int(pos[1]))
            else:
                x, y = (sw - w - 24, 24)
            x = max(0, min(x, sw - w))
            y = max(0, min(y, sh - h))
            win.geometry(f'+{x}+{y}')
    def _balance_press(self, e):
        win = self.balance_window
        if not win or not win.winfo_exists():
            return None
        else:
            self._bal_press = (e.x_root, e.y_root, e.x_root - win.winfo_x(), e.y_root - win.winfo_y())
            self.balance_dragged = False
    def _balance_move(self, e):
        if self._bal_press is None:
            return
        else:
            win = self.balance_window
            if not win or not win.winfo_exists():
                return None
            else:
                rx, ry, ox, oy = self._bal_press
                if abs(e.x_root - rx) + abs(e.y_root - ry) > 3:
                    self.balance_dragged = True
                sw, sh = self.screen()
                nx = max(0, min(e.x_root - ox, sw - win.winfo_width()))
                ny = max(0, min(e.y_root - oy, sh - win.winfo_height()))
                win.geometry(f'+{nx}+{ny}')
    def _balance_release(self, _e):
        if self._bal_press is None:
            return
        else:
            self._bal_press = None
            win = self.balance_window
            if not win or not win.winfo_exists():
                return None
            else:
                if self.balance_dragged:
                    self.balance_dragged = False
                    win.update_idletasks()
                    self.cfg['balance_pos'] = [win.winfo_x(), win.winfo_y()]
                    save_config(self.cfg)
                else:
                    self._balance_open_menu()
    def _balance_btn(self, parent, text, cmd):
        tk.Button(parent, text=text, command=cmd, font=('Microsoft YaHei', 8), bg='#31538f', fg='#eaf1ff', activebackground='#3f5488', relief='flat', padx=8, pady=1).pack(side='left', padx=(0, 5))
    def _balance_open_menu(self):
        """点一下悬浮窗：弹出它自己的小设置（刷新频率 / 穿透 / 回默认位置 / 收起）。"""
        if self.balance_menu and self.balance_menu.winfo_exists():
            self.balance_menu.lift()
            return
        else:
            win = tk.Toplevel(self.root)
            self.balance_menu = win
            win.overrideredirect(True)
            win.attributes('-topmost', True)
            win.configure(bg='#22315a')
            box = tk.Frame(win, bg='#22315a', highlightthickness=1, highlightbackground='#3f5488')
            box.pack(fill='both', expand=True)
            head = Frame(box, bg='#22315a')
            head.pack(fill='x', padx=10, pady=(8, 2))
            tk.Label(head, text='余额悬浮窗设置', bg='#22315a', fg='#eaf1ff', font=('Microsoft YaHei', 9, 'bold')).pack(side='left')
            x = tk.Label(head, text='✕', bg='#22315a', fg='#8ea2cc', font=('Microsoft YaHei', 8, 'bold'), cursor='hand2')
            x.pack(side='right')
            x.bind('<Button-1>', lambda _e: win.destroy())
            x.bind('<Enter>', lambda _e: x.config(fg='#ff8f8f'))
            x.bind('<Leave>', lambda _e: x.config(fg='#8ea2cc'))
            r = Frame(box, bg='#22315a')
            r.pack(anchor='w', padx=10, pady=(2, 0))
            tk.Label(r, text='刷新', bg='#22315a', fg='#9fb0d6', font=('Microsoft YaHei', 8)).pack(side='left', padx=(0, 2))
            for label, sec in [('30秒', 30), ('1分', 60), ('2分', 120), ('5分', 300)]:
                tk.Radiobutton(r, text=label, value=sec, variable=self.balance_gap, command=self._balance_apply_gap, bg='#22315a', fg='#c7d3ef', activebackground='#22315a', selectcolor='#3f5488', font=('Microsoft YaHei', 8), bd=0, highlightthickness=0).pack(side='left')
            ra = Frame(box, bg='#22315a')
            ra.pack(anchor='w', padx=10, pady=(2, 0))
            tk.Label(ra, text='透明度', bg='#22315a', fg='#9fb0d6', font=('Microsoft YaHei', 8)).pack(side='left', padx=(0, 4))
            sc = tk.Scale(ra, from_=100, to=30, orient='horizontal', length=150, variable=self.balance_alpha, command=self._balance_apply_alpha, bg='#22315a', fg='#c7d3ef', troughcolor='#31538f', activebackground='#3f5488', highlightthickness=0, bd=0, sliderrelief='flat', width=10, resolution=5, font=('Microsoft YaHei', 7))
            sc.pack(side='left')
            sc.bind('<ButtonRelease-1>', self._balance_save_alpha)
            tk.Label(ra, text='%', bg='#22315a', fg='#9fb0d6', font=('Microsoft YaHei', 8)).pack(side='left', padx=(2, 0))
            rb = Frame(box, bg='#22315a')
            rb.pack(anchor='w', padx=10, pady=(4, 0))
            tk.Checkbutton(rb, text='余额提醒', variable=self.balance_alert_on, command=self._apply_balance_alert, bg='#22315a', fg='#c7d3ef', activebackground='#22315a', selectcolor='#3f5488', font=('Microsoft YaHei', 8), bd=0, highlightthickness=0).pack(side='left')
            tk.Label(rb, text='低于 ¥', bg='#22315a', fg='#9fb0d6', font=('Microsoft YaHei', 8)).pack(side='left', padx=(6, 0))
            en = tk.Entry(rb, textvariable=self.balance_alert_below, width=5, bg='#31538f', fg='#eaf1ff', insertbackground='#eaf1ff', relief='flat', font=('Microsoft YaHei', 8), justify='center')
            en.pack(side='left', padx=2)
            en.bind('<FocusOut>', self._save_balance_alert_below)
            en.bind('<Return>', self._save_balance_alert_below)
            tk.Label(rb, text='时变色', bg='#22315a', fg='#9fb0d6', font=('Microsoft YaHei', 8)).pack(side='left')
            tk.Checkbutton(box, text='查询失败时也提醒', variable=self.balance_alert_fail, command=self._apply_balance_alert, bg='#22315a', fg='#c7d3ef', activebackground='#22315a', selectcolor='#3f5488', font=('Microsoft YaHei', 8), anchor='w', bd=0, highlightthickness=0).pack(anchor='w', padx=8, pady=(2, 0))
            tk.Checkbutton(box, text='点击穿透（不挡鼠标，这时点不到本窗）', variable=self.balance_ct, command=self._apply_balance_click_through, bg='#22315a', fg='#c7d3ef', activebackground='#22315a', selectcolor='#3f5488', font=('Microsoft YaHei', 8), anchor='w', bd=0, highlightthickness=0).pack(anchor='w', padx=8, pady=(4, 2))
            rr = Frame(box, bg='#22315a')
            rr.pack(anchor='w', padx=10, pady=(2, 8))
            self._balance_btn(rr, '立即刷新', self._balance_fetch)
            self._balance_btn(rr, '回默认位置', self._balance_reset_pos)
            self._balance_btn(rr, '收起悬浮窗', self._balance_close_by_user)
            win.update_idletasks()
            bw = self.balance_window
            sw, sh = self.screen()
            if bw and bw.winfo_exists():
                bx, by = (bw.winfo_x(), bw.winfo_y() + bw.winfo_height() + 4)
            else:
                bx, by = (sw // 2, sh // 3)
            bx = max(4, min(bx, sw - win.winfo_reqwidth() - 4))
            by = max(4, min(by, sh - win.winfo_reqheight() - 4))
            win.geometry(f'+{bx}+{by}')
            self._balance_no_taskbar(win)
    def _balance_apply_gap(self):
        """改自动刷新间隔。"""
        gap = max(30, int(self.balance_gap.get()))
        self.balance_gap.set(gap)
        self.cfg['balance_gap'] = gap
        save_config(self.cfg)
        self.balance_next = time.time() + gap
    def _balance_apply_alpha(self, value=None):
        """调余额悬浮窗的透明度（30%~100%），拖动时即时预览、松手才存。"""
        try:
            a = int(round(float(value))) if value is not None else int(self.balance_alpha.get())
        except (TypeError, ValueError):
            a = 100
        a = max(30, min(100, a))
        win = self.balance_window
        if win and win.winfo_exists():
                try:
                    win.attributes('-alpha', a / 100.0)
                except tk.TclError:
                    return None
    def _balance_save_alpha(self, _e=None):
        """松手时把透明度记进 config.json。"""
        a = max(30, min(100, int(self.balance_alpha.get())))
        self.balance_alpha.set(a)
        self.cfg['balance_alpha'] = a / 100.0
        save_config(self.cfg)
    def _balance_alert_threshold(self):
        """提醒阈值：余额低于它就变警示色。"""
        try:
            return max(0.0, float(str(self.balance_alert_below.get()).strip()))
        except (TypeError, ValueError):
            return 5.0
    def _apply_balance_alert(self):
        """右键菜单 / 设置里：开 / 关余额提醒（低余额、查询失败时变色）。"""
        on = bool(self.balance_alert_on.get())
        self.cfg['balance_alert_on'] = on
        self.cfg['balance_alert_fail'] = bool(self.balance_alert_fail.get())
        save_config(self.cfg)
        if not on:
            self._balance_clear_alert()
        if on:
            self.say('好～余额太低或者查不到，本鲸就给小窗换个颜色提醒主人。', 4200)
        else:
            self.say('好～本鲸不提醒余额了。', 2600)
    def _save_balance_alert_below(self, _e=None):
        """把「低于多少余额提醒」记进 config.json。"""
        try:
            v = float(str(self.balance_alert_below.get()).strip())
        except (TypeError, ValueError):
            v = 5.0
        v = max(0.0, min(100000.0, v))
        self.balance_alert_below.set('%g' % v)
        self.cfg['balance_alert_below'] = v
        save_config(self.cfg)
    def _balance_show_alert_btn(self, on):
        """「知道了」按钮只在提醒时露出来；露出来时给文字右边多留点位置，免得压住它。"""
        btn = self.balance_alert_btn
        if not btn or not btn.winfo_exists():
            return None
        if on:
            btn.place(relx=1.0, rely=0.0, anchor='ne', x=(-20), y=3)
            if self.balance_lbl and self.balance_lbl.winfo_exists():
                self.balance_lbl.pack_configure(padx=(3, 66))
        else:
            btn.place_forget()
            if self.balance_lbl and self.balance_lbl.winfo_exists():
                self.balance_lbl.pack_configure(padx=(3, 20))
    def _balance_clear_alert(self):
        """清掉提醒状态（颜色回到常规）。"""
        self.balance_alert_kind = ''
        self.balance_alert_ack = ''
        self._balance_show_alert_btn(False)
    def _balance_ack_alert(self):
        """点「知道了」：本次提醒关掉、颜色恢复，同一个原因不再反复提醒。"""
        if not self.balance_alert_kind:
            return None
        self.balance_alert_ack = self.balance_alert_kind
        self.balance_alert_kind = ''
        self._balance_show_alert_btn(False)
        self.balance_lbl.config(fg='#eaf1ff')
        self.balance_dot.config(fg='#8ea2cc')
    def _balance_reset_pos(self):
        """把悬浮窗挪回默认位置（屏幕右上角）。"""
        self.cfg['balance_pos'] = None
        save_config(self.cfg)
        self._balance_place()
    def _balance_close_by_user(self):
        self.balance_win.set(False)
        self.cfg['balance_win'] = False
        save_config(self.cfg)
        self._close_balance_win()
        self.say('好～本鲸把余额小窗收起来了。', 2600)
    def _close_balance_win(self):
        win = self.balance_window
        self.balance_window = None
        self.balance_lbl = None
        self.balance_dot = None
        self.balance_close = None
        self.balance_alert_btn = None
        self.balance_alert_kind = ''
        self.balance_alert_ack = ''
        self.balance_busy = False
        self._bal_press = None
        if self.balance_menu:
            try:
                self.balance_menu.destroy()
            except tk.TclError:
                pass
            self.balance_menu = None
        if win:
            try:
                win.destroy()
            except tk.TclError:
                return None
    def _balance_fetch(self):
        """后台查一次余额，结果丢回主线程更新小窗。"""
        win = self.balance_window
        if not win or not win.winfo_exists() or self.balance_busy:
            return None
        else:
            reason = self._balance_reason()
            if reason:
                self._balance_show(False, reason, hint=True)
                return
            else:
                base = str(self.cfg.get('api_base', '')).strip()
                key = str(self.cfg.get('api_key', '')).strip()
                u = urllib.parse.urlparse(base)
                url = f'{u.scheme or 'https'}://{u.netloc}/user/balance'
                self.balance_busy = True
                self._balance_show(None, '查询中…')
                q = self._q
                thr = self._balance_alert_threshold()
                alert_low = bool(self.balance_alert_on.get())
                alert_fail = bool(self.balance_alert_fail.get())
                def worker():
                    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + key, 'Accept': 'application/json'})
                    try:
                        with urllib.request.urlopen(req, timeout=20) as resp:
                            obj = json.loads(resp.read().decode('utf-8', 'ignore'))
                    except urllib.error.HTTPError as e:
                        q.put(('balwin', False, f'查询失败 HTTP {e.code}', False, 'fail' if alert_fail else ''))
                        return None
                    except Exception as e:
                        q.put(('balwin', False, f'查询失败：{e}', False, 'fail' if alert_fail else ''))
                        return None
                    infos = obj.get('balance_infos') or []
                    if not infos:
                        q.put(('balwin', False, '接口没返回余额', False, 'fail' if alert_fail else ''))
                        return
                    else:
                        parts = []
                        low = False
                        for b in infos:
                            sym = {'CNY': '¥', 'USD': '$'}.get(str(b.get('currency', '')).upper(), '')
                            parts.append(f'{sym}{b.get('total_balance', '?')}')
                            try:
                                if float(b.get('total_balance')) < thr:
                                    low = True
                            except (TypeError, ValueError):
                                pass
                        avail = obj.get('is_available', True)
                        tail = '' if avail else '（余额不足）'
                        kind = 'low' if alert_low and (low or not avail) else ''
                        q.put(('balwin', True, '余额 ' + ' / '.join(parts) + tail, False, kind))
                threading.Thread(target=worker, daemon=True).start()
    def _balance_show(self, ok, text, hint=False, kind=''):
        """把结果写进小窗：ok=True 绿、None=查询中黄、False=红（hint 则灰）；\nkind 有值时进入提醒态（低余额 / 查询失败），文字变警示橙色。"""
        self.balance_busy = False
        win = self.balance_window
        if not win or not win.winfo_exists():
            return None
        else:
            self.balance_lbl.config(text=text)
            if not kind:
                self.balance_alert_ack = ''
                self.balance_alert_kind = ''
                self._balance_show_alert_btn(False)
            else:
                alert = bool(self.balance_alert_on.get()) and kind != self.balance_alert_ack
                self.balance_alert_kind = kind if alert else ''
                self._balance_show_alert_btn(alert)
                if alert:
                    self.balance_lbl.config(fg='#ffb066')
                    self.balance_dot.config(fg='#ff8f3f')
                    return
            if ok is True:
                self.balance_lbl.config(fg='#eaf1ff')
                self.balance_dot.config(fg='#5fd38a')
                return
            else:
                if ok is None:
                    self.balance_lbl.config(fg='#c7d3ef')
                    self.balance_dot.config(fg='#e0b64a')
                else:
                    if hint:
                        self.balance_lbl.config(fg='#9fb0d6')
                        self.balance_dot.config(fg='#8ea2cc')
                    else:
                        self.balance_lbl.config(fg='#ffb4b4')
                        self.balance_dot.config(fg='#e06a6a')
    def _balance_tick(self):
        """每秒看一眼：挂着的小窗到点没，到了就刷一次。"""
        win = self.balance_window
        if not win or not win.winfo_exists():
            return None
        else:
            if time.time() < self.balance_next:
                return
            else:
                gap = max(30, int(self.balance_gap.get()))
                self.balance_next = time.time() + gap
                self._balance_fetch()
    def _apply_balance_click_through(self):
        """右键菜单：开 / 关余额小窗的「点击穿透」。"""
        on = bool(self.balance_ct.get())
        self.cfg['balance_click_through'] = on
        save_config(self.cfg)
        self._balance_apply_alpha()
        self._set_click_through(self.balance_window, on)
        if on:
            self.say('好～余额窗不挡鼠标了；想挪它、点它，就把菜单里的「点击穿透」关掉。', 5400)
        else:
            self.say('好～余额窗又能拖、能点了。', 3000)
    def _balance_no_taskbar(self, win):
        """让余额窗只当悬浮窗显示：补 WS_EX_TOOLWINDOW、去掉 WS_EX_APPWINDOW，\n不让它在任务栏和 Alt-Tab 里冒出来（无边框窗加了分层样式后偶尔会漏出去）。"""
        if not win or not win.winfo_exists():
            return None
        try:
            user32 = ctypes.windll.user32
            hwnd = win.winfo_id()
            parent = user32.GetParent(hwnd)
            GWL_EXSTYLE = (-20)
            WS_EX_TOOLWINDOW = 128
            WS_EX_APPWINDOW = 262144
            for h in (hwnd, parent):
                if not h:
                    continue
                style = user32.GetWindowLongW(h, GWL_EXSTYLE)
                user32.SetWindowLongW(h, GWL_EXSTYLE, (style | WS_EX_TOOLWINDOW) & ~WS_EX_APPWINDOW)
            user32.SetWindowPos(parent or hwnd, 0, 0, 0, 0, 0, 39)
        except Exception:
            return None
    def _set_click_through(self, win, on):
        """Windows：给窗口加 / 去 WS_EX_TRANSPARENT，让鼠标点它等于点它下面的窗口。\n\n开了穿透后，这个窗就收不到鼠标事件了（所以不能拖、✕ 也点不到），要操作就先在\n右键菜单里把「点击穿透」关掉。\n"""
        if not win or not win.winfo_exists():
            return None
        else:
            self._balance_no_taskbar(win)
            try:
                user32 = ctypes.windll.user32
                hwnd = win.winfo_id()
                hwnd = user32.GetParent(hwnd) or hwnd
                GWL_EXSTYLE = (-20)
                WS_EX_TRANSPARENT = 32
                WS_EX_LAYERED = 524288
                LWA_ALPHA = 2
                SWP = 39
                style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                if on:
                    style |= WS_EX_TRANSPARENT | WS_EX_LAYERED
                else:
                    style &= ~WS_EX_TRANSPARENT
                user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
                if style & WS_EX_LAYERED:
                    a = max(30, min(100, int(self.balance_alpha.get()))) * 255 // 100
                    user32.SetLayeredWindowAttributes(hwnd, 0, a, LWA_ALPHA)
                user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, SWP)
            except Exception:
                return None
    def wake_words(self):
        raw = str(self.cfg.get('wake_words') or '').strip()
        return [w for w in re.split('[\\s,，、]+', raw) if w][:8] or ['大肥鲸']
    def _apply_voice(self):
        """语音开关变了：要听就起识别进程，不听就关掉。"""
        self.cfg['voice_wake'] = bool(self.voice_wake.get())
        self.cfg['voice_chat'] = bool(self.voice_chat.get())
        self.cfg['voice_speak'] = bool(self.voice_speak.get())
        save_config(self.cfg)
        if not self.voice_wake.get() and (not self.voice_chat.get()):
            self.voice.stop_asr()
            self.voice_arm_until = 0.0
            self.say('耳朵关上啦～', 2200)
            return
        else:
            word = self.wake_words()[0]
            if self.voice.start_asr(self.wake_words()):
                self.say(f'耳朵打开啦，喊「{word}」叫本鲸～', 3600)
                return
            else:
                for v in [self.voice_wake, self.voice_chat]:
                    v.set(False)
                self.cfg['voice_wake'] = self.cfg['voice_chat'] = False
                save_config(self.cfg)
                self.say('本鲸听不见……' + (self.voice.last_error or '系统语音识别起不来'), 4600)
    def _apply_tts(self):
        """换朗读引擎 / 音色。"""
        self.cfg['tts_engine'] = self.tts_engine.get() or 'edge'
        self.cfg['tts_voice'] = self.tts_voice.get().strip() or DEFAULT_TTS_VOICE
        self.tts_voice.set(self.cfg['tts_voice'])
        save_config(self.cfg)
        if self.cfg['tts_engine'] == 'edge' and (not EDGE_TTS_OK):
            self.say('没装 edge-tts，先用系统 SAPI 念着～', 3600)
        else:
            self.say('好～朗读换好啦，试试看。', 2600)
    def _clear_tts_cache(self):
        """清空「语音缓存」文件夹。"""
        n = 0
        try:
            for fn in os.listdir(TTS_CACHE_DIR):
                if fn.lower().endswith('.mp3'):
                    try:
                        os.remove(os.path.join(TTS_CACHE_DIR, fn))
                        n += 1
                    except OSError:
                        pass
        except OSError:
            pass
        self.say(f'清掉 {n} 个语音缓存啦～', 2600)
    def _apply_asr(self):
        """换语音识别引擎 / 按住说话键。"""
        self.cfg['asr_engine'] = self.asr_engine.get() or 'sapi'
        self.cfg['asr_ptt_key'] = self.asr_ptt_key.get().strip()
        save_config(self.cfg)
        self.voice.stop_asr()
        if self.voice_wake.get() or self.voice_chat.get():
            if not self.voice.start_asr(self.wake_words()):
                self.say('语音起不来……' + (self.voice.last_error or ''), 4600)
                return
        if self.cfg['asr_engine'] == 'funasr' and (not asr_model_ready()):
            self.say('本地识别要先下模型哦～点「下载语音模型」（约 200MB，从 ModelScope 下）。', 6200)
        else:
            self.say('好～语音设置改好了。', 2600)
    def _download_asr_model(self):
        """后台下本地识别模型。"""
        if self._asr_dl:
            self.say('本鲸正在下语音模型啦，稍等一下～', 2600)
            return None
        if not ASR_DEPS_OK:
            self.say('缺依赖：先 pip install sherpa-onnx sounddevice numpy', 6200)
            return None
        self._asr_dl = True
        self._asr_result = None
        if self.asr_status and self.asr_status.winfo_exists():
            self.asr_status.config(text='语音模型：正在下载…')
        self.say('好～本鲸去下语音模型了（约 200MB），下好告诉你。', 4600)
        def work():
            self._asr_result = ensure_asr_model()
            self._asr_dl = False
        threading.Thread(target=work, daemon=True).start()
        self._poll_asr_dl(0)
    def _poll_asr_dl(self, n):
        if self._asr_dl:
            if n < 900:
                self.root.after(1000, lambda: self._poll_asr_dl(n + 1))
            return None
        res = self._asr_result
        self._asr_result = None
        ok, err = res if res else (False, '')
        if self.asr_status and self.asr_status.winfo_exists():
            self.asr_status.config(text='语音模型：' + ('已就绪' if asr_model_ready() else '未就绪'))
        if ok:
            self.say('语音模型下好啦，切到「本地 FunASR」就能用了～', 4200)
        else:
            self.say('语音模型没下成……' + str(err), 5600)
    def voice_test(self):
        if not self.voice.speak('本鲸来啦，主人听得见吗？'):
            self.say('念不出来……' + (self.voice.last_error or '系统语音不可用'), 4200)
    def set_wake_words(self):
        new = simpledialog.askstring('唤醒词', '想用什么词叫大肥鲸？（多个用空格隔开）', initialvalue=' '.join(self.wake_words()), parent=self.root)
        if new is None:
            return
        else:
            if not new.strip():
                self.say('那还是用原来的吧～', 2200)
                return
            else:
                self.cfg['wake_words'] = new.strip()
                save_config(self.cfg)
                if self.voice_wake.get() or self.voice_chat.get():
                    self.voice.stop_asr()
                    self.voice.start_asr(self.wake_words())
                self.say(f'好～以后喊「{self.wake_words()[0]}」就行！', 3200)
    def voice_out(self, text):
        """这句话要不要念出来（朗读开关开着，或这次回答本来就是语音问的）。"""
        if self.voice_speak.get() or self._speak_reply:
            self._speak_reply = False
            self.voice.speak(text)
    def ask_voice(self, text):
        """语音提问：走聊天那套流程，回答完念出来。"""
        self.open_chat()
        if not self.chat or not self.chat.winfo_exists():
            return None
        else:
            self.chat_input.delete('1.0', 'end')
            self.chat_input.insert('1.0', text)
            self._speak_reply = True
            self.send_chat()
    def _poll_voice(self):
        while True:
            try:
                ev = self.voice_q.get_nowait()
            except queue.Empty:
                return None
            kind = ev[0]
            if kind == 'v_hyp':
                self._voice_partial(ev[1])
                continue
            if kind == 'v_done':
                self.voice.resume_asr()
            else:
                if kind == 'v_heard':
                    self._voice_heard(ev[1], ev[2], ev[3])
                else:
                    if kind in ['v_error', 'v_closed']:
                        if not self.voice_wake.get() and (not self.voice_chat.get()):
                                continue
                        self.voice.stop_asr()
                        for v in [self.voice_wake, self.voice_chat]:
                            v.set(False)
                        self.cfg['voice_wake'] = self.cfg['voice_chat'] = False
                        save_config(self.cfg)
                        why = str(ev[1])[:60] if kind == 'v_error' else '识别进程掉线了'
                        self.say('本鲸听不见了……' + why, 4600)
    def _voice_heard(self, tag, conf, text):
        text = str(text or '').strip()
        if not text:
            return
        else:
            if tag == 'WAKE' or any((w in text for w in self.wake_words())):
                self._on_wake()
                return
            else:
                if conf < VOICE_CONF:
                    return
                else:
                    if self.voice_chat.get() and time.time() < self.voice_arm_until:
                            self.voice_arm_until = 0.0
                            self.ask_voice(text)
    def _voice_partial(self, text):
        """边听边显示：把识别中的半成品文字丢到气泡里（有节流，不刷屏）。"""
        text = str(text or '').strip()
        if (not text) or self.voice.speaking:
            return None
        now = time.time()
        if now - self._hyp_at < 0.9:
            return None
        self._hyp_at = now
        if self.voice_chat.get() or now < self.voice_arm_until:
            self.say('…' + text[-24:], 1200)
    def _poll_ptt(self):
        """按住说话：按住 asr_ptt_key 指定的键就听，松开出结果（仅本地 FunASR）。"""
        key = str(self.asr_ptt_key.get() or '').strip().lower()
        if (not key) or self.asr_engine.get() != 'funasr':
            if self._ptt_down:
                self._ptt_down = False
                self.voice.set_ptt(False)
            return None
        vk = _PTT_VK.get(key) or _key_code(key) or 0
        if not vk:
            return None
        down = bool(_user32.GetAsyncKeyState(vk) & 32768)
        if down != self._ptt_down:
            self._ptt_down = down
            self.voice.set_ptt(down)
            if down:
                self.voice.arm(True)
                if self.sleeping:
                    self.wake()
                if self.edge:
                    self.come_out()
                self.hop = 8
    def _on_wake(self):
        if self.sleeping:
            self.wake()
        if self.edge:
            self.come_out()
        self.hop = 10
        self.say(random.choice(VOICE_REPLY_LINES), 2800)
        self.emote('cheerful', 1500)
        self.voice_arm_until = time.time() + VOICE_ASK_SEC
    def _apply_memory(self):
        """记录开关变了：存下来，并允许重新试一次看图。"""
        self.cfg['memory_on'] = bool(self.mem_on.get())
        save_config(self.cfg)
        self.mem_vision = True
        if self.mem_on.get():
            self.mem_next = time.time() + 10
            self.say('好～本鲸会悄悄记下主人今天做了什么。', 3400)
        else:
            self.say('好啦，本鲸不看屏幕了。', 2800)
    def memory_now(self):
        """不等间隔，立刻看一次屏幕。"""
        if not self.mem_on.get():
            self.mem_on.set(True)
            self._apply_memory()
        self.mem_next = time.time()
        self.say('本鲸瞄一眼主人在忙什么……', 2400)
        self._check_memory()
    def _check_memory(self):
        """到点了就让后台线程截一张屏，问问模型主人在做什么。"""
        if not self.mem_on.get() or self.mem_busy:
            return None
        else:
            if not self.online() or not self._api_ready():
                return None
            else:
                now = time.time()
                if now < self.mem_next:
                    return
                else:
                    gap = max(60, int(self.cfg.get('memory_interval', 300)))
                    title, exe = self.activity
                    if self.idle_sec and self.idle_sec > 120:
                        self.mem_next = now + 120
                    else:
                        if is_sensitive(title) or is_sensitive(exe):
                            self.mem_next = now + 60
                        else:
                            self.mem_busy = True
                            self.mem_next = now + gap
                            q = self._q
                            use_vision = self.mem_vision and bool(self.cfg.get('vision', True))
                            ops = self._ops_text(8)
                            def worker():
                                text = ''
                                if use_vision:
                                    try:
                                        text = analyze_screen(self.cfg, screen_data_url(ImageGrab.grab()), ops)
                                    except Exception:
                                        self.mem_vision = False
                                        text = ''
                                if not text:
                                    try:
                                        text = analyze_window(self.cfg, exe, title, ops)
                                    except Exception as e:
                                        q.put(('memory', False, str(e), exe))
                                        return None
                                q.put(('memory', True, text, exe))
                            threading.Thread(target=worker, daemon=True).start()
    def _memory_result(self, ok, text, exe):
        self.mem_busy = False
        if not ok:
            return
        else:
            text = str(text or '').strip().strip('「」\"\'')
            if len(text) < 2 or '__SKIP__' in text.upper():
                return None
            else:
                text = redact(text)[:MEMORY_MAX_ENTRY]
                now = time.time()
                if text == self.mem_last and now - self.mem_last_at < MEMORY_DEDUP_SEC:
                    self.mem_last_at = now
                    return
                else:
                    day = time.strftime('%Y-%m-%d')
                    if day != self.mem_day:
                        self.mem_day = day
                        self.mem_last = ''
                        clean_memory()
                    tag = f'[{str(exe or '未知程序')[:24]}] ' if exe else ''
                    if write_memory(f'- {time.strftime('%H:%M')} · {tag}{text}', day):
                        self.mem_last = text
                        self.mem_last_at = now
    def open_memory_dir(self):
        d = memory_dir()
        try:
            os.startfile(d)
        except OSError:
            self.say(f'记录都在这里：{d}', 4600)
    def show_memory(self, day=None):
        """把某天的记录用记事本打开。"""
        day = day or time.strftime('%Y-%m-%d')
        if not read_memory(day).strip():
            self.say(f'{day} 本鲸还什么都没记到呢。', 3400)
            return
        else:
            try:
                os.startfile(memory_path(day))
            except OSError:
                self.say(read_memory(day)[:120], 6000)
    def online(self):
        return str(self.cfg.get('mode', 'local')) == 'online'
    def _api_ready(self):
        """在线模式要的三样东西（地址 / 密钥 / 模型）都填了没。"""
        return all((str(self.cfg.get(k) or '').strip() for k in ['api_base', 'api_key', 'model']))
    def _apply_mode(self):
        """切换模式。切到在线时先跟 AI 对一句话，确认答得上再真的切过去。"""
        if not self.online_var.get():
            self.cfg['mode'] = 'local'
            save_config(self.cfg)
            self._refresh_chat_status()
            self.say('好～本鲸就用自己的小脑袋回答，不联网啦。', 3600)
        else:
            if not self._api_ready():
                self.online_var.set(False)
                self.say('还差 API 设置呢，先把地址、密钥、模型填好～', 4600)
                self.open_settings()
            else:
                if self.warm_busy:
                    return
                else:
                    self.warm_busy = True
                    self.say('本鲸先跟 AI 对一句话试试……', 3200)
                    self._request([{'role': 'user', 'content': '只回两个字：在吗'}], warmup=True)
    def _warmup_result(self, ok, msg):
        """在线模式的试音结果：通了才真的切过去，免得切过去说不了话。"""
        self.warm_busy = False
        if ok:
            self.cfg['mode'] = 'online'
            self.online_var.set(True)
            self.say('对上暗号啦～接下来本鲸动脑子回答主人。', 3600)
            self.happy_until = time.time() + 3
            self.emote('cheerful', 1800)
        else:
            self.cfg['mode'] = 'local'
            self.online_var.set(False)
            self.say('唔……没连上，先留在本地模式：' + str(msg)[:60], 5600)
            self.emote('apologetic', 2000)
        save_config(self.cfg)
        self._refresh_chat_status()
    def _log_op(self, text):
        """记一条主人的操作：既能当 AI 的上下文，也会写进「记录」。"""
        self.ops.append('- ' + time.strftime('%H:%M:%S') + ' ' + str(text))
        del self.ops[:(-20)]
    def _ops_text(self, n=8):
        return '\n'.join(self.ops[-n:])
    def brain_context(self):
        """告诉 AI 现在是什么情况，让它拿主意。"""
        sw, sh = self.screen()
        title, exe = self.activity
        _dev = detect_dev_tool(exe, title)
        dev_txt = f'（编程工具：{_dev}）' if _dev else ''
        return f'时间：{time.strftime('%Y-%m-%d %H:%M')}\n屏幕：{sw}x{sh}，本鲸现在在横向 {self.cx / sw:.2f}、纵向 {min(1.0, self.foot / sh):.2f}（0 最左/最上，1 最右/最下）\n主人正在用：{exe or '（不知道）'}（窗口标题：{title or '无'}）{dev_txt}\n主人已经 {int(self.idle_sec)} 秒没碰键盘鼠标了\n本鲸的心情：{MOOD_TEXT.get(self.mood(), '待机中')}\n主人最近的操作：\n' + (self._ops_text() or '（没记到）')
    def _apply_brain(self):
        self.cfg['ai_brain'] = bool(self.ai_brain.get())
        save_config(self.cfg)
        if self.ai_brain.get():
            self.say('好～本鲸说什么、往哪走，全听脑子安排～', 3600)
        else:
            self.say('那本鲸还按老规矩来～', 2600)
    def _apply_scene_play(self):
        """离线「看画面自己玩」开关。"""
        self.cfg['scene_play'] = bool(self.scene_play.get())
        save_config(self.cfg)
        if self.scene_play.get():
            self.say('好～本鲸会看着主人用啥来应景做动作（写代码就摆 desk-coding…）～', 4200)
        else:
            self.say('好～本鲸不按画面乱比划了。', 2600)
    def _brain_on(self):
        """在线模式 + 开了「让 AI 决定」+ API 配好了。"""
        return bool(self.ai_brain.get() and self.online() and self._api_ready())
    def _ai_decide(self):
        """问 AI 该怎么表现。返回 True 表示「问了，等着」。"""
        if not self._brain_on():
            return False
        else:
            if self.decide_busy or time.time() < self.decide_next:
                return False
            else:
                if self.quiet or self.sleeping or self.dragging or self.edge or self.pending:
                    return False
                else:
                    self.decide_busy = True
                    self.decide_next = time.time() + max(8, int(self.cfg.get('ai_gap', 12)))
                    ctx = self.brain_context()
                    q = self._q
                    def worker():
                        try:
                            msgs = [{'role': 'system', 'content': BRAIN_PROMPT}, {'role': 'user', 'content': ctx}]
                            text, calls = _api_tools_once(self.cfg, msgs, BRAIN_TOOLS)
                            if calls:
                                msgs.append({'role': 'assistant', 'content': None, 'tool_calls': calls})
                                for i, c in enumerate(calls[:2]):
                                    fn = c.get('function') or {}
                                    try:
                                        a = json.loads(fn.get('arguments') or '{}')
                                    except ValueError:
                                        a = {}
                                    q.put(('op', fn.get('name') or '', a))
                                    res = run_tool(fn.get('name'), a)
                                    msgs.append({'role': 'tool', 'tool_call_id': c.get('id') or f'call_{i}', 'content': str(res)[:1500]})
                                text, _ = _api_tools_once(self.cfg, msgs, BRAIN_TOOLS)
                            q.put(('decide', True, text))
                        except Exception as e:
                            q.put(('decide', False, str(e)))
                    threading.Thread(target=worker, daemon=True).start()
                    return True
    def _decide_result(self, ok, text):
        """AI 拿的主意：说话 / 走一步 / 做动作 / 换表情。"""
        self.decide_busy = False
        if not ok:
            self.brain_fails += 1
            if self.brain_fails >= 3 and self.ai_brain.get():
                    self.ai_brain.set(False)
                    self.cfg['ai_brain'] = False
                    save_config(self.cfg)
                    self.say('唔……本鲸的脑子连不上了，先自己乱逛啦。', 4600)
            return None
        else:
            self.brain_fails = 0
            obj = parse_brain(text)
            if not obj:
                return
            else:
                line = str(obj.get('say') or '').strip()
                if line and (not self.quiet) and (not self.sleeping):
                            self.say(line[:60], 3400)
                            self.voice_out(line)
                face = str(obj.get('face') or 'none').strip().lower()
                if face in EMOJI_FILES:
                    self.emote(face, 2600, force=True)
                act = str(obj.get('act') or 'none').strip().lower()
                if act == 'nap':
                    self.sleep()
                else:
                    if act == 'wake':
                        self.wake()
                    else:
                        if act == 'hide':
                            self.hide_at_edge('left' if self.cx < self.screen()[0] / 2 else 'right')
                        else:
                            if act in ['spin', 'hop', 'sway', 'shiver', 'cheer']:
                                self.gesture(act)
                            else:
                                if str(obj.get('move') or 'stay').lower() == 'go':
                                    try:
                                        self._go_to(float(obj.get('x', 0.5)), float(obj.get('y', 0.9)))
                                    except (TypeError, ValueError):
                                        return None
    def _go_to(self, xf, yf):
        """按屏幕比例走过去（AI 说去哪儿就去哪儿）。"""
        sw, sh = self.screen()
        half = max(1, self.sprite_size[0]) / 2
        self.target_cx = max(half + 10, min(sw - half - 10, xf * sw))
        lo, hi = (self.ground_line + 10, max(self.ground_line + 20, sh - 24))
        self.target_y = max(lo, min(hi, yf * sh))
        self._begin_move()
    def familiar_score(self):
        """熟悉度（带 60 秒缓存，别每次都去翻记录文件）。"""
        now = time.time()
        if now - self._fam_cache[1] < 60:
            return (self._fam_cache[0], self._fam_cache[2])
        else:
            st = self.save_data
            score, parts = familiarity(st.get('meet', 0), st.get('days', 0))
            self._fam_cache = (score, now, parts)
            return (score, parts)
    def familiar_ok(self):
        """资料攒够了没（四块都满）；开了「跳过熟悉度」就直接算够。"""
        if self.skip_familiar.get():
            return True
        return self.familiar_score()[0] >= 0.999
    def meet(self, n=1):
        """记一次主人和本鲸的互动（算熟悉度用）。"""
        st = self.save_data
        st['meet'] = int(st.get('meet', 0)) + int(n)
        save_state(st)
        self._fam_cache = (0.0, 0.0, {})
    def status_lines(self):
        """菜单顶部那几行「基础状态」→ [(文字, 是不是标题)]。"""
        st = self.save_data
        return [(f'{APP_NAME} · {self.status_text()}', True), (f'心情 {mood_word(self.mood_value())}　饥饿 {hunger_word(self.hunger())}', False), (f'米饭 {int(st.get("rice", 0) or 0)} 碗（今日还能喂 {self.rice_left_today()} 次）　重要信息 {len(memo_items())} 条', False), (f'熟悉度 {familiarity_text(self.familiar_score()[0])}　陪伴第 {int(st.get("days", 0) or 0)} 天　互动 {int(st.get("meet", 0) or 0)} 次', False), ((('在线模式' if self.online() else '本地模式') + ('·AI 接手' if self._brain_on() else '') + f'　大肥鲸记了 {memory_entry_count()} 条流水'), False)]
    def _menu_header(self):
        """桌宠右键菜单顶部的状态一览（点一下看详细状态）。"""
        lines = self.status_lines()
        for text, _head in lines:
            self.menu.add_command(label=text, command=self.show_status)
        for i, (_text, head) in enumerate(lines):
            try:
                self.menu.entryconfigure(i, font=(MENU_FONT[0], 11, 'bold') if head else (MENU_FONT[0], 9), foreground='#1B2545' if head else '#44557F')
            except tk.TclError:
                pass
        self.menu.add_separator()
    def _tray_menu(self):
        """托盘右键菜单：上面几行是状态（灰的、点不动），下面是操作。"""
        items = [('info', text) for text, _head in self.status_lines()]
        items += [(2, None), (TRAY_SHOW, '叫它出来 / 回到右下角'), (1, '躲到屏幕边边（露个头）'), (TRAY_HOTKEY, f'快捷命令输入框（{self.cfg.get('hotkey') or '没设热键'}）'), (TRAY_FAM, '状态 / 熟悉度…'), (TRAY_SET, '应用设置…'), (2, None), (3, '跟我聊天'), (4, f'投喂一碗米饭（饥饿 {self.hunger():.0f}%）'), (5, '一起猜拳'), (2, None), (8, '退出应用')]
        return items
    def familiar_lines(self):
        score, parts = self.familiar_score()
        lines = [f'大肥鲸对主人的熟悉度：{familiarity_text(score)}']
        for name, (have, need) in parts.items():
            if have >= need:
                lines.append(f'✓ {name}：{need}/{need} 够了')
            else:
                lines.append(f'· {name}：{have}/{need}（还差 {need - have}）')
        lines.append('大肥鲸摸清主人的脾气啦，主动帮忙可以用咯～' if score >= 0.999 else '等完全熟悉了，大肥鲸才会主动递选项打扰主人。')
        return lines
    def show_status(self):
        """状态窗：基础状态 + 熟悉度明细（点菜单顶部、托盘右键都能开）。"""
        win = tk.Toplevel(self.root)
        win.title('大肥鲸的状态')
        win.configure(bg='#eef3ff')
        win.attributes('-topmost', True)
        win.resizable(False, False)
        tk.Label(win, text='大肥鲸的状态', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 12, 'bold')).pack(anchor='w', padx=14, pady=(10, 4))
        for text, _head in self.status_lines()[1:]:
            tk.Label(win, text=text, bg='#eef3ff', fg='#3a4a7a', anchor='w', justify='left', wraplength=420, font=('Microsoft YaHei', 9)).pack(anchor='w', padx=14, pady=1)
        tk.Frame(win, bg='#d3ddf2', height=1).pack(fill='x', padx=14, pady=7)
        for line in self.familiar_lines():
            tk.Label(win, text=line, bg='#eef3ff', fg='#3a4a7a', anchor='w', justify='left', wraplength=420, font=('Microsoft YaHei', 9)).pack(anchor='w', padx=14, pady=1)
        tk.Label(win, text='（记录攒得越多、陪得越久，大肥鲸就越懂主人；点菜单顶部的状态也能开这里）', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8), wraplength=420, justify='left').pack(anchor='w', padx=14, pady=(6, 0))
        tk.Button(win, text='关闭', width=8, font=('Microsoft YaHei', 10), command=win.destroy).pack(pady=(6, 10))
    def autostart_on(self):
        # irreducible cflow, using cdg fallback
        """开机自启开了没（读 HKCU 的 Run 项）。"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_RUN) as k:
                return bool(winreg.QueryValueEx(k, APP_NAME)[0])
        except OSError:
            return False
    def set_autostart(self):
        want = bool(self.autostart_var.get())
        if getattr(sys, 'frozen', False):
            cmd = f'\"{os.path.abspath(sys.executable)}\"'
        else:
            pyw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
            exe = pyw if os.path.exists(pyw) else sys.executable
            cmd = f'\"{exe}\" \"{os.path.abspath(__file__)}\"'
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_RUN, 0, winreg.KEY_ALL_ACCESS) as k:
                if want:
                    winreg.SetValueEx(k, APP_NAME, 0, winreg.REG_SZ, cmd)
                else:
                    try:
                        winreg.DeleteValue(k, APP_NAME)
                    except OSError:
                        pass
        except OSError as e:
            self.autostart_var.set(not want)
            self.say(f'改不了开机自启……（{e}）', 4200)
        self.say('好～以后开机就自动叫本鲸起来。' if want else '那本鲸就不自己起来了。', 3600)
    def _apply_mood_decay(self):
        """心情回落：开关 + 每小时降多少。"""
        try:
            val = int(float(self.mood_decay_var.get()))
        except (tk.TclError, ValueError):
            val = int(self.cfg.get('mood_decay', 6) or 0)
        val = max(0, min(100, val))
        on = bool(self.mood_decay_on.get())
        changed = val != self.cfg.get('mood_decay') or on != self.cfg.get('mood_decay_on')
        self.cfg['mood_decay'] = val
        self.cfg['mood_decay_on'] = on
        self.mood_decay_var.set(val)
        save_config(self.cfg)
        if not changed:
            return
        else:
            if not on or not val:
                self.say('好～以后不管多久不理本鲸，心情都不会掉了。', 4200)
                return
            else:
                self.say(f'好～久不理本鲸的话，心情每小时掉 {val}%，来陪本鲸说说话就涨回来～', 4800)
    def _apply_title(self):
        """改「它该怎么称呼你」。"""
        t = str(self.title_var.get() or '').strip()[:12] or '主人'
        self.title_var.set(t)
        if t == self.cfg.get('user_title'):
            return
        else:
            self.cfg['user_title'] = t
            save_config(self.cfg)
            self.happy_until = time.time() + 2
            self.say(f'好～以后本鲸就叫你「{t}」啦。', 3800)
    def _apply_edge_snap(self):
        self.cfg['edge_snap'] = bool(self.edge_snap.get())
        save_config(self.cfg)
        self.say('好～拖到边上就自己躲起来。' if self.edge_snap.get() else '好～拖到边上不动它了。', 3200)
    def _apply_routine(self):
        """作息：开关 + 入睡 / 起床时间（填错了回退默认）。"""
        s = hm_minutes(self.sleep_var.get())
        w = hm_minutes(self.wake_var.get())
        if s is None:
            s = 1410
        if w is None:
            w = 420
        self.sleep_var.set(hm_text(s))
        self.wake_var.set(hm_text(w))
        on = bool(self.routine_on.get())
        quiet = bool(self.quiet_night.get())
        st, wt = (hm_text(s), hm_text(w))
        changed = on != self.cfg.get('routine_on') or quiet != self.cfg.get('quiet_night') or st != self.cfg.get('sleep_at') or (wt != self.cfg.get('wake_at'))
        self.cfg['routine_on'] = on
        self.cfg['quiet_night'] = quiet
        self.cfg['sleep_at'] = st
        self.cfg['wake_at'] = wt
        save_config(self.cfg)
        self.routine_night = None
        if not changed:
            return
        else:
            if not on:
                self.say('好～本鲸不按作息来了，什么时候睡、什么时候醒都随缘。', 4200)
                return
            else:
                self.say(f'好～本鲸 {st} 去睡、{wt} 起来' + ('，夜里就不吵主人了。' if quiet else '。'), 4600)
    def _apply_mem_gap(self):
        self.cfg['memory_interval'] = max(60, int(self.mem_gap.get()))
        save_config(self.cfg)
        self.say(f'好～记录改成每 {self.cfg['memory_interval'] // 60} 分钟看一眼。', 3400)
    def _apply_pc_control(self):
        """控制电脑：总开关 + 文件 / 跑命令行 / 电源 / 系统设置 四档权限。"""
        on = bool(self.pc_ctrl.get())
        self.cfg['pc_control_on'] = on
        self.cfg['pc_files'] = bool(self.pc_files.get())
        self.cfg['pc_command'] = bool(self.pc_command.get())
        self.cfg['pc_power'] = bool(self.pc_power.get())
        self.cfg['pc_settings'] = bool(self.pc_settings.get())
        save_config(self.cfg)
        set_pc_control(on, {'files': self.cfg['pc_files'], 'command': self.cfg['pc_command'], 'power': self.cfg['pc_power'], 'settings': self.cfg['pc_settings']})
        if on:
            names = [label for label, v in [('文件', self.pc_files), ('跑命令行', self.pc_command), ('电源', self.pc_power), ('系统设置', self.pc_settings)] if v.get()]
            self.say('好～本鲸能替主人操作电脑了：' + ('、'.join(names) if names else '（不过四档权限都还关着，勾一个才有用）') + '。', 5200)
        else:
            self.say('好～本鲸不碰主人的电脑了。', 3200)
    def _on_size_slide(self, value):
        """拖动大小滑条：防抖一下再应用（重建素材比较重）。"""
        try:
            px = int(float(value))
        except (TypeError, ValueError):
            return None
        if hasattr(self, 'size_px_var'):
            self.size_px_var.set(str(px))
        job = getattr(self, '_size_job', None)
        if job:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        self._size_job = self.root.after(90, lambda: self._apply_size_px(px))
    def _apply_size_px(self, px=None):
        """应用大小：从滑条来的 px 或输入框里的 px。"""
        self._size_job = None
        if px is None:
            if not hasattr(self, 'size_px_var'):
                return None
            try:
                px = int(float(self.size_px_var.get()))
            except (TypeError, ValueError):
                return None
        self.set_scale_px(px)
        real = int(self.sprite_size[1])
        if hasattr(self, 'size_px_var'):
            self.size_px_var.set(str(real))
        sc = getattr(self, 'size_scale', None)
        if sc is not None:
            try:
                sc.set(real)
            except Exception:
                pass
    def app_settings(self):
        """应用设置窗：外观 / 行为 / 快捷命令 / 语音 / 智能功能 / 系统。"""
        if self.app_set_win and self.app_set_win.winfo_exists():
            self.app_set_win.lift()
            return
        else:
            win = tk.Toplevel(self.root)
            self.app_set_win = win
            win.title('应用设置')
            win.configure(bg='#eef3ff')
            win.attributes('-topmost', True)
            win.resizable(True, True)
            _sw, _sh = self.screen()
            win.geometry(f'560x{min(620, max(360, _sh - 150))}')
            win.minsize(430, 300)
            tk.Label(win, text='应用设置', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 12, 'bold')).pack(anchor='w', padx=16, pady=(12, 0))
            tk.Label(win, text='这里管桌宠自己怎么玩；AI 的地址 / 密钥 / 模型在右键「聊天 API 设置…」里。内容多的时候可以用滚轮上下翻。', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8), wraplength=500, justify='left').pack(anchor='w', padx=16, pady=(2, 4))
            holder = Frame(win, bg='#eef3ff')
            holder.pack(fill='both', expand=True)
            canvas = tk.Canvas(holder, bg='#eef3ff', highlightthickness=0, bd=0)
            bar = tk.Scrollbar(holder, orient='vertical', command=canvas.yview, width=11)
            canvas.configure(yscrollcommand=bar.set)
            bar.pack(side='right', fill='y')
            canvas.pack(side='left', fill='both', expand=True)
            body = Frame(canvas, bg='#eef3ff')
            body_id = canvas.create_window((0, 0), window=body, anchor='nw')
            body.bind('<Configure>', lambda _e: canvas.configure(scrollregion=canvas.bbox('all')))
            canvas.bind('<Configure>', lambda e: canvas.itemconfigure(body_id, width=e.width))
            def on_wheel(event):
                canvas.yview_scroll((-1) if event.delta > 0 else 1, 'units')
            def on_wheel_linux(event):
                canvas.yview_scroll((-1) if event.num == 4 else 1, 'units')
            win.bind('<MouseWheel>', on_wheel)
            win.bind('<Button-4>', on_wheel_linux)
            win.bind('<Button-5>', on_wheel_linux)
            canvas.bind('<Enter>', lambda _e: canvas.focus_set())
            def head(text):
                tk.Label(body, text=text, bg='#eef3ff', fg='#5A6B93', font=('Microsoft YaHei', 9, 'bold')).pack(anchor='w', padx=16, pady=(9, 1))
            def row():
                f = Frame(body, bg='#eef3ff')
                f.pack(fill='x', padx=16, pady=1)
                return f
            def toggle(parent, text, var, cmd=None):
                tk.Checkbutton(parent, text=text, variable=var, command=cmd, bg='#eef3ff', fg='#2E3A5C', activebackground='#eef3ff', selectcolor='#ffffff', font=('Microsoft YaHei', 9), anchor='w', bd=0, highlightthickness=0).pack(side='left')
            def button(parent, text, cmd):
                tk.Button(parent, text=text, command=cmd, font=('Microsoft YaHei', 9), bg='#dce7fb', fg='#22315a', activebackground='#c9d9f7', relief='flat', padx=8, pady=0).pack(side='left', padx=(0, 5))
            def radio(parent, text, var, value, cmd):
                tk.Radiobutton(parent, text=text, variable=var, value=value, command=cmd, bg='#eef3ff', fg='#3a4a7a', activebackground='#eef3ff', selectcolor='#ffffff', font=('Microsoft YaHei', 9), bd=0, highlightthickness=0).pack(side='left')
            head('外观')
            r = row()
            _ref = max(self.base[k].height for k in ('front', 'side', 'back'))
            _cur = int(self.sprite_size[1])
            tk.Label(r, text='大小：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 4))
            self.size_px_var = tk.StringVar(value=str(_cur))
            self.size_scale = tk.Scale(r, from_=90, to=int(_ref * 0.6), orient='horizontal', length=220, showvalue=False, bg='#eef3ff', fg='#3a4a7a', troughcolor='#dce7fb', activebackground='#c9d9f7', highlightthickness=0, bd=0, sliderrelief='flat', width=12, resolution=4, command=self._on_size_slide)
            self.size_scale.set(_cur)
            self.size_scale.pack(side='left')
            se = tk.Entry(r, textvariable=self.size_px_var, width=6, font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a', justify='center')
            se.pack(side='left', padx=(8, 2))
            se.bind('<Return>', lambda _e: self._apply_size_px())
            se.bind('<FocusOut>', lambda _e: self._apply_size_px())
            tk.Label(r, text='px（拖动滑条或直接输入数值，回车生效）', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            head('行为')
            r = row()
            toggle(r, '跟随鼠标（小跑跟着你）', self.follow)
            r = row()
            toggle(r, '拖到屏幕左右边就自动贴边躲起来', self.edge_snap, self._apply_edge_snap)
            r = row()
            tk.Label(r, text='它该怎么称呼你：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left')
            te = tk.Entry(r, textvariable=self.title_var, width=10, font=('Microsoft YaHei', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a', justify='center')
            te.pack(side='left', padx=(0, 4))
            te.bind('<Return>', lambda _e: self._apply_title())
            te.bind('<FocusOut>', lambda _e: self._apply_title())
            tk.Label(r, text='（默认「主人」，回车生效）', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            head('作息')
            r = row()
            toggle(r, '按作息时间休息（到点自己去睡、早上叫你）', self.routine_on, self._apply_routine)
            r = row()
            tk.Label(r, text='入睡', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            se = tk.Entry(r, textvariable=self.sleep_var, width=7, font=('Microsoft YaHei', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a', justify='center')
            se.pack(side='left')
            se.bind('<Return>', lambda _e: self._apply_routine())
            se.bind('<FocusOut>', lambda _e: self._apply_routine())
            tk.Label(r, text='　起床', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            we = tk.Entry(r, textvariable=self.wake_var, width=7, font=('Microsoft YaHei', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a', justify='center')
            we.pack(side='left')
            we.bind('<Return>', lambda _e: self._apply_routine())
            we.bind('<FocusOut>', lambda _e: self._apply_routine())
            tk.Label(r, text='（例 23:30 / 07:00，回车生效）', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            toggle(r, '睡觉时段里不主动开口打扰', self.quiet_night, self._apply_routine)
            head('心情')
            r = row()
            toggle(r, '久不互动心情会慢慢降低', self.mood_decay_on, self._apply_mood_decay)
            tk.Label(r, text='　每小时降', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9)).pack(side='left')
            sp = tk.Spinbox(r, from_=0, to=100, width=4, textvariable=self.mood_decay_var, font=('Microsoft YaHei', 9), justify='center', bd=0, relief='flat', bg='#ffffff', fg='#22315a', buttonbackground='#dce7fb', command=self._apply_mood_decay)
            sp.pack(side='left', padx=(0, 2))
            sp.bind('<Return>', lambda _e: self._apply_mood_decay())
            sp.bind('<FocusOut>', lambda _e: self._apply_mood_decay())
            tk.Label(r, text='%（0＝不降）', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9)).pack(side='left')
            head('快捷命令')
            r = row()
            toggle(r, '认文本里的 [CMD: …] 这类命令', self.quick_on, self._apply_quick)
            button(r, '命令一览…', self.show_command_help)
            r = row()
            tk.Label(r, text=f'热键：{self.cfg.get('hotkey') or '（没设）'}', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 6))
            button(r, '改热键…', self.set_hotkey)
            button(r, '清空', lambda: self._apply_hotkey(None))
            head('语音')
            r = row()
            toggle(r, '语音唤醒', self.voice_wake, self._apply_voice)
            toggle(r, '语音对话', self.voice_chat, self._apply_voice)
            toggle(r, '朗读回答', self.voice_speak, self._apply_voice)
            r = row()
            button(r, '设置唤醒词…', self.set_wake_words)
            button(r, '说一句测试', self.voice_test)
            button(r, '停止朗读', self.voice.stop_speak)
            r = row()
            tk.Label(r, text='朗读引擎：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            radio(r, 'Edge（在线·好听）', self.tts_engine, 'edge', self._apply_tts)
            radio(r, '系统 SAPI', self.tts_engine, 'sapi', self._apply_tts)
            if not EDGE_TTS_OK:
                tk.Label(r, text='（没装 edge-tts，会自动用 SAPI）', bg='#eef3ff', fg='#b4552f', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            tk.Label(r, text='Edge 音色：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            tv = tk.Entry(r, textvariable=self.tts_voice, width=24, font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            tv.pack(side='left')
            tv.bind('<Return>', lambda _e: self._apply_tts())
            tv.bind('<FocusOut>', lambda _e: self._apply_tts())
            tk.Label(r, text='（如 zh-CN-XiaoxiaoNeural / zh-CN-YunxiNeural）', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            button(r, '清空语音缓存', self._clear_tts_cache)
            tk.Label(r, text='念过的句子会缓存到「语音缓存」文件夹，重复用更快。', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            tk.Label(r, text='识别引擎：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            radio(r, '系统 SAPI', self.asr_engine, 'sapi', self._apply_asr)
            radio(r, '本地 FunASR（更准）', self.asr_engine, 'funasr', self._apply_asr)
            if not ASR_DEPS_OK:
                tk.Label(r, text='（缺 sherpa-onnx / sounddevice / numpy）', bg='#eef3ff', fg='#b4552f', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            button(r, '下载语音模型', self._download_asr_model)
            tk.Label(r, text='（本地识别用，约 200MB，从 ModelScope 下）', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            tk.Label(r, text='按住说话键：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            _pe = tk.Entry(r, textvariable=self.asr_ptt_key, width=10, font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a', justify='center')
            _pe.pack(side='left')
            _pe.bind('<Return>', lambda _e: self._apply_asr())
            _pe.bind('<FocusOut>', lambda _e: self._apply_asr())
            tk.Label(r, text='（如 alt / f2 / space，留空=关；仅本地 FunASR）', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            self.asr_status = tk.Label(r, text='语音模型：' + ('已就绪' if asr_model_ready() else '未就绪'), bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8))
            self.asr_status.pack(side='left')
            head('智能功能')
            r = row()
            toggle(r, 'AI 记录（隔一会儿看一眼屏幕）', self.mem_on, self._apply_memory)
            tk.Label(r, text='　间隔', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9)).pack(side='left')
            for mins in [1, 2, 5, 10]:
                radio(r, f'{mins}分', self.mem_gap, mins * 60, self._apply_mem_gap)
            r = row()
            toggle(r, '主动帮忙（合适的时候递几个选项，让你挑）', self.ask_on, self._apply_proactive)
            toggle(r, '跳过熟悉度（不攒熟悉度也能用主动智能）', self.skip_familiar, self._apply_proactive)
            r = row()
            tk.Label(r, text='　最多隔', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9)).pack(side='left')
            for label, sec in [('1分', 60), ('3分', 180), ('5分', 300), ('10分', 600), ('30分', 1800)]:
                radio(r, label, self.ask_gap, sec, self._apply_proactive)
            r = row()
            toggle(r, '让 AI 接管它的一举一动', self.ai_brain, self._apply_brain)
            button(r, f'状态 / 熟悉度：{familiarity_text(self.familiar_score()[0])}', self.show_status)
            r = row()
            toggle(r, '看画面自己玩（离线时按在用的程序做动作）', self.scene_play, self._apply_scene_play)
            head('控制电脑')
            r = row()
            toggle(r, '允许本鲸操作电脑（总开关）', self.pc_ctrl, self._apply_pc_control)
            tk.Label(r, text='　总开关关着时，下面四档权限都不生效。', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            tk.Label(r, text='权限：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            toggle(r, '文件（读/写/建文件夹/移动/打开）', self.pc_files, self._apply_pc_control)
            toggle(r, '跑命令行', self.pc_command, self._apply_pc_control)
            r = row()
            toggle(r, '电源（关机/重启/睡眠/定时关机）', self.pc_power, self._apply_pc_control)
            toggle(r, '系统设置（音量/亮度/壁纸/回收站/打开设置）', self.pc_settings, self._apply_pc_control)
            r = row()
            tk.Label(r, text='关着的时候本鲸只能做些轻巧的事（开程序、调音量、截图…）；打开对应权限后，它才能替主人改文件、执行命令、关机重启、改系统设置，请在自己看着的时候用。', bg='#eef3ff', fg='#b4552f', font=('Microsoft YaHei', 8), wraplength=520, justify='left').pack(anchor='w')
            head('AI 操作电脑')
            r = row()
            toggle(r, '允许本鲸操作鼠标键盘（自己动手点、拖动、打字）', self.cua_on, self._apply_cua)
            button(r, '现在让它做一件事…', self._cua_menu_start)
            r = row()
            tk.Label(r, text='动手前：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            radio(r, '每步都问', self.cua_ask, 'each', self._apply_cua)
            radio(r, '只问一次', self.cua_ask, 'once', self._apply_cua)
            radio(r, '不问了', self.cua_ask, 'never', self._apply_cua)
            r = row()
            tk.Label(r, text='「只问一次」同意后 ', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9)).pack(side='left')
            for _m in [10, 30, 60]:
                radio(r, f'{_m} 分钟内', self.cua_ask_minutes, _m, self._apply_cua)
            r = row()
            tk.Label(r, text='最多走 ', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9)).pack(side='left')
            for _n in [10, 20, 40]:
                radio(r, f'{_n} 步', self.cua_max_steps, _n, self._apply_cua)
            button(r, '让它停手', self.cua_stop)
            r = row()
            tk.Label(r, text='动手时屏幕上有个悬浮条，写着是哪个 AI 在操作、当前在做什么（移动鼠标 / 点击 / 拖动 / 打字 / 按键 / 滚轮 / 等待 N 秒 / 看屏幕 / 等待主人操作…）；主人一动鼠标键盘它就先停下等你。需要在线模式并配好 API。', bg='#eef3ff', fg='#b4552f', font=('Microsoft YaHei', 8), wraplength=520, justify='left').pack(anchor='w')
            head('音乐 / 视频解析')
            r = row()
            tk.Label(r, text='听歌识曲 ACRCloud host：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            acr_host_var = tk.StringVar(value=str(self.cfg.get('acr_host') or ''))
            eh = tk.Entry(r, textvariable=acr_host_var, width=30, font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            eh.pack(side='left')
            r = row()
            tk.Label(r, text='access_key：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            acr_key_var = tk.StringVar(value=str(self.cfg.get('acr_access_key') or ''))
            ek = tk.Entry(r, textvariable=acr_key_var, width=18, show='*', font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            ek.pack(side='left')
            tk.Label(r, text='　secret：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            acr_sec_var = tk.StringVar(value=str(self.cfg.get('acr_access_secret') or ''))
            es = tk.Entry(r, textvariable=acr_sec_var, width=18, show='*', font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            es.pack(side='left')
            r = row()
            tk.Label(r, text='转写 API 地址：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            stt_base_var = tk.StringVar(value=str(self.cfg.get('stt_base') or ''))
            eb = tk.Entry(r, textvariable=stt_base_var, width=34, font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            eb.pack(side='left')
            r = row()
            tk.Label(r, text='转写 Key：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            stt_key_var = tk.StringVar(value=str(self.cfg.get('stt_key') or ''))
            esk = tk.Entry(r, textvariable=stt_key_var, width=22, show='*', font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            esk.pack(side='left')
            tk.Label(r, text='　模型：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            stt_model_var = tk.StringVar(value=str(self.cfg.get('stt_model') or 'whisper-1'))
            em = tk.Entry(r, textvariable=stt_model_var, width=14, font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            em.pack(side='left')
            r = row()
            tk.Label(r, text='ffmpeg 路径：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            ffmpeg_var = tk.StringVar(value=str(self.cfg.get('ffmpeg_path') or ''))
            ef = tk.Entry(r, textvariable=ffmpeg_var, width=30, font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            ef.pack(side='left')
            def save_media(_e=None):
                self.cfg['acr_host'] = acr_host_var.get().strip()
                self.cfg['acr_access_key'] = acr_key_var.get().strip()
                self.cfg['acr_access_secret'] = acr_sec_var.get().strip()
                self.cfg['stt_base'] = stt_base_var.get().strip()
                self.cfg['stt_key'] = stt_key_var.get().strip()
                self.cfg['stt_model'] = stt_model_var.get().strip() or 'whisper-1'
                self.cfg['ffmpeg_path'] = ffmpeg_var.get().strip()
                save_config(self.cfg)
                if ff_status and ff_status.winfo_exists():
                    ff_status.config(text='ffmpeg：' + (ffmpeg_exe() or '未找到（用到时会自动下载）'))
            for ent in (eh, ek, es, eb, esk, em, ef):
                ent.bind('<Return>', save_media)
                ent.bind('<FocusOut>', save_media)
            r = row()
            button(r, '保存上面的配置', save_media)
            def pick_ff():
                p = filedialog.askopenfilename(parent=win, title='选 ffmpeg.exe', filetypes=[('ffmpeg', 'ffmpeg.exe'), ('可执行文件', '*.exe'), ('所有文件', '*.*')])
                if p:
                    ffmpeg_var.set(p)
                    save_media()
                    self.say('好～记下 ffmpeg 路径了。', 2600)
            def dl_ff():
                if getattr(self, '_ff_dl', False):
                    self.say('本鲸正在下载 ffmpeg 啦，稍等一下～', 2400)
                    return
                self._ff_dl = True
                self._ff_result = None
                ff_status.config(text='ffmpeg：正在下载…')
                self.say('好～本鲸去下载 ffmpeg 了，下好告诉你。', 3000)
                def work():
                    self._ff_result = ensure_ffmpeg()
                    self._ff_dl = False
                threading.Thread(target=work, daemon=True).start()
                self._poll_ff_dl(ff_status, 0)
            button(r, '选 ffmpeg.exe…', pick_ff)
            button(r, '现在下载 ffmpeg', dl_ff)
            r = row()
            ff_status = tk.Label(r, text='ffmpeg：' + (ffmpeg_exe() or '未找到（用到时会自动下载）'), bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8), wraplength=520, justify='left')
            ff_status.pack(anchor='w')
            tk.Label(body, text='听歌识曲用 ACRCloud（host / access_key / access_secret）；转写用 OpenAI 兼容的 /audio/transcriptions（地址 + Key + 模型）。改完按回车、或点「保存上面的配置」即生效。', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8), wraplength=520, justify='left').pack(anchor='w', padx=16, pady=(2, 0))
            head('更新')
            r = row()
            toggle(r, '自动检查更新', self.update_check_on, self._apply_update)
            tk.Label(r, text=f'　当前版本 {APP_VERSION}', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9)).pack(side='left')
            r = row()
            tk.Label(r, text='检查频率：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            for _lb, _hr in [('1小时', 1), ('6小时', 6), ('12小时', 12), ('24小时', 24)]:
                radio(r, _lb, self.update_gap_hours, _hr, self._apply_update)
            r = row()
            tk.Label(r, text='更新版本：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            for _val, _lb in UPDATE_CHANNELS:
                radio(r, _lb, self.update_channel, _val, self._apply_update)
            tk.Label(r, text='（正式版最稳；预览版最新，可能不稳定）', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            toggle(r, '检测到新版本就自动安装（不勾就每次询问）', self.update_auto, self._apply_update)
            tk.Label(r, text='　更新用内置工具：下完自动替换主程序并重启，不用装安装器。', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            r = row()
            tk.Label(r, text='GitHub 仓库：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            self.upd_gh_var = tk.StringVar(value=str(self.cfg.get('update_repo_github') or ''))
            eg = tk.Entry(r, textvariable=self.upd_gh_var, width=32, font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            eg.pack(side='left')
            r = row()
            tk.Label(r, text='Gitee 仓库：', bg='#eef3ff', fg='#2E3A5C', font=('Microsoft YaHei', 9)).pack(side='left', padx=(0, 3))
            self.upd_gitee_var = tk.StringVar(value=str(self.cfg.get('update_repo_gitee') or ''))
            ei = tk.Entry(r, textvariable=self.upd_gitee_var, width=32, font=('Consolas', 9), bd=0, relief='flat', bg='#ffffff', fg='#22315a')
            ei.pack(side='left')
            for _e in (eg, ei):
                _e.bind('<Return>', lambda _ev: self._apply_update())
                _e.bind('<FocusOut>', lambda _ev: self._apply_update())
            r = row()
            button(r, '保存更新设置', self._apply_update)
            button(r, '立即检查更新', lambda: (self._apply_update(), self._check_update(manual=True)))
            tk.Label(r, text='（填 owner/repo；GitHub 拉不到会自动改用 Gitee）', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            head('系统')
            r = row()
            self.autostart_var.set(self.autostart_on())
            toggle(r, '开机自动启动', self.autostart_var, self.set_autostart)
            button(r, '打开数据文件夹', lambda: os.startfile(data_dir()))
            tk.Frame(win, bg='#d3ddf2', height=1).pack(fill='x', padx=16, pady=(10, 0))
            foot = Frame(win, bg='#eef3ff')
            foot.pack(fill='x', padx=16, pady=(6, 10))
            tk.Label(foot, text='改完就生效，设置存在 config.json 里', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(side='left')
            tk.Button(foot, text='关闭', width=8, font=('Microsoft YaHei', 10), bg='#7ba7f0', fg='white', relief='flat', command=win.destroy).pack(side='right')
    def _poll_ff_dl(self, lb, n):
        """在 UI 线程里等后台下载 ffmpeg 的结果，好了就刷新状态。"""
        if getattr(self, '_ff_dl', False):
            if n < 240:
                self.root.after(1000, lambda: self._poll_ff_dl(lb, n + 1))
            return
        p = getattr(self, '_ff_result', None)
        if lb and lb.winfo_exists():
            lb.config(text='ffmpeg：' + (p if p else '下载失败，可以点「选 ffmpeg.exe…」手动指定'))
        if p:
            self.say('ffmpeg 准备好啦，视频解析能用了～', 3600)
        else:
            self.say('ffmpeg 没下成……可以自己放一个 ffmpeg.exe，再在设置里填它的路径。', 5600)
    def _check_update_tick(self):
        """到点了就后台查一次更新。"""
        if (not self.update_check_on.get()) or self.upd_busy:
            return None
        if time.time() < self.upd_next:
            return None
        self.upd_next = time.time() + max(1, int(self.update_gap_hours.get())) * 3600
        self._check_update(manual=False)
    def _check_update(self, manual=False):
        """后台查更新（GitHub / Gitee，一个失败自动换另一个）。"""
        if self.upd_busy:
            return None
        self.upd_busy = True
        q = self._q
        if manual:
            self.say('本鲸去看看有没有新版本～', 2600)
        def worker():
            try:
                info = fetch_update_info()
            except Exception as e:
                info = {'ok': False, 'err': str(e)}
            q.put(('update', info, manual))
        threading.Thread(target=worker, daemon=True).start()
    def _update_result(self, info, manual=False):
        self.upd_busy = False
        if not info or not info.get('ok'):
            if manual:
                self.say('没查到更新信息……' + str((info or {}).get('err') or ''), 5200)
            return None
        new = str(info.get('version') or '')
        ch = dict(UPDATE_CHANNELS).get(str(info.get('channel') or self.cfg.get('update_channel') or 'release'), '')
        if not _ver_gt(new, APP_VERSION):
            if manual:
                self.say(f'已经是最新版本啦（{APP_VERSION} · {ch}）～', 3600)
            return None
        self.upd_pending = info
        note = f'发现新版本 {new}（当前 {APP_VERSION}）· {ch} · 来自 {info.get("source")}'
        self.say(note, 6000)
        if self.update_auto.get():
            self._do_update(info)
            return
        try:
            yes = messagebox.askyesno('发现新版本', f'{note}\n\n现在更新吗？（会自动下载并替换程序、然后重启）')
        except tk.TclError:
            yes = False
        if yes:
            self._do_update(info)
    def _do_update(self, info):
        """下载新 exe；退出后由脚本替换并重启。"""
        url = str(info.get('url') or '')
        if not url:
            self.say('这个版本没有下载地址……', 3600)
            return None
        self.say(f'本鲸开始下载 {info.get("version")} 啦，下好会自动重启～', 6000)
        def worker():
            tmp_exe = os.path.join(tempfile.gettempdir(), 'whale_pet_new.exe')
            ok, err = download_file(url, tmp_exe, str(info.get('sha256') or ''))
            self._q.put(('upd_dl', ok, tmp_exe if ok else err))
        threading.Thread(target=worker, daemon=True).start()
    def _update_downloaded(self, ok, payload):
        if not ok:
            self.say('更新包没下成……' + str(payload), 5200)
            return None
        if not getattr(sys, 'frozen', False):
            self.say(f'新版本已经下到 {payload}（现在是源码运行模式，本鲸就不自动替换了）。', 6000)
            return None
        cur_exe = os.path.abspath(sys.executable)
        bat = os.path.join(tempfile.gettempdir(), 'whale_upd.bat')
        lines = ['@echo off', 'chcp 65001 >nul', 'ping -n 3 127.0.0.1 >nul', f'copy /y "{payload}" "{cur_exe}" >nul', f'start "" "{cur_exe}"', 'del "%~f0"']
        try:
            with open(bat, 'w', encoding='utf-8') as f:
                f.write('\r\n'.join(lines))
            subprocess.Popen(['cmd', '/c', bat], creationflags=_NO_WINDOW | 8)
        except Exception as e:
            self.say(f'写更新脚本失败……（{e}）', 5200)
            return None
        self.say('更新好啦，本鲸这就重启～', 3000)
        self.root.after(900, self._quit_for_update)
    def _quit_for_update(self):
        try:
            self.quit()
        except Exception:
            pass
        os._exit(0)
    def _apply_update(self):
        """保存「更新」设置。"""
        self.cfg['update_check_on'] = bool(self.update_check_on.get())
        self.cfg['update_auto'] = bool(self.update_auto.get())
        self.cfg['update_gap_hours'] = max(1, int(self.update_gap_hours.get()))
        _ch = str(self.update_channel.get() or 'release')
        self.cfg['update_channel'] = _ch if _ch in ('release', 'beta', 'preview') else 'release'
        self.cfg['update_repo_github'] = self.upd_gh_var.get().strip().strip('/')
        self.cfg['update_repo_gitee'] = self.upd_gitee_var.get().strip().strip('/')
        save_config(self.cfg)
        self.upd_next = time.time() + 5
    def _cua_say(self, text, x=None, y=None, waiting=False):
        """操作电脑时的悬浮 HUD：显示是哪个 AI 在操作、当前在做什么。"""
        try:
            w = self.cua_win
            if w is None or not w.winfo_exists():
                w = tk.Toplevel(self.root)
                self.cua_win = w
                w.overrideredirect(True)
                w.attributes('-topmost', True)
                w.configure(bg='#16233c')
                box = tk.Frame(w, bg='#16233c', highlightthickness=1, highlightbackground='#4a86ff')
                box.pack(fill='both', expand=True)
                self.cua_head = tk.Label(box, text='', bg='#16233c', fg='#9fd0ff', font=('Microsoft YaHei', 8, 'bold'))
                self.cua_head.pack(anchor='w', padx=8, pady=(5, 0))
                self.cua_lbl = tk.Label(box, text='', bg='#16233c', fg='#eaf1ff', font=('Microsoft YaHei', 9, 'bold'), justify='left', wraplength=250)
                self.cua_lbl.pack(anchor='w', padx=8, pady=(1, 6))
                self._balance_no_taskbar(w)
            prov = str(self.cfg.get('provider') or 'AI')
            self.cua_head.config(text=f'🤖 由 {prov} 操作中' + ('（暂停）' if waiting else ''))
            self.cua_lbl.config(text=text or '')
            sw, sh = self.screen()
            if x is None:
                px, py = self.root.winfo_pointerxy()
            else:
                px, py = int(x), int(y)
            w.update_idletasks()
            bw, bh = w.winfo_reqwidth(), w.winfo_reqheight()
            w.geometry(f'+{max(4, min(sw - bw - 6, px + 22))}+{max(4, min(sh - bh - 6, py + 22))}')
        except Exception:
            pass
    def _cua_hide(self):
        w = self.cua_win
        self.cua_win = None
        if w is not None:
            try:
                w.destroy()
            except Exception:
                pass
    def _cua_perm(self, text):
        """在 UI 线程问主人同不同意；worker 在这里等结果。"""
        ev = threading.Event()
        self._cua_ask_ev = ev
        self._cua_ask_ok = False
        self._q.put(('cua_ask', text))
        ev.wait()
        return bool(self._cua_ask_ok)
    def _cua_ask_show(self, text):
        try:
            ok = messagebox.askyesno('本鲸想操作电脑', text + '\n\n同意吗？（操作期间主人一动鼠标键盘，本鲸就先停手让边）')
        except Exception:
            ok = False
        self._cua_ask_ok = bool(ok)
        if self._cua_ask_ev is not None:
            self._cua_ask_ev.set()
    def _cua_user_active(self):
        """主人是不是正在动鼠标 / 敲键盘（用来暂停）。"""
        try:
            pt = wintypes.POINT()
            _user32.GetCursorPos(ctypes.byref(pt))
            if abs(pt.x - self._cua_last_pos[0]) + abs(pt.y - self._cua_last_pos[1]) > 24:
                return True
            for vk in (1, 2, 4, 5, 6, 8, 9, 13, 16, 17, 18, 27, 32, 91):
                if _user32.GetAsyncKeyState(vk) & 32768:
                    return True
            return False
        except Exception:
            return False
    def _cua_mark_pos(self):
        try:
            pt = wintypes.POINT()
            _user32.GetCursorPos(ctypes.byref(pt))
            self._cua_last_pos = (pt.x, pt.y)
        except Exception:
            pass
    def cua_stop(self):
        if not self.cua_busy:
            return None
        self._cua_stop = True
        self._cua_hide()
        self.say('好～本鲸停手了。', 2600)
    def cua_start(self, goal):
        """开始让 AI 操作电脑完成一个目标。"""
        goal = str(goal or '').strip()
        if not goal:
            return None
        if not self.cua_on.get():
            self.say('先在「应用设置 → 控制电脑」里打开「允许本鲸操作电脑」哦～', 5200)
            return None
        if self.cua_busy:
            self.say('本鲸手上还有活儿没干完呢～', 3200)
            return None
        if self.mode.get() != 'online' or (not self.api_key.get().strip()):
            self.say('得先切到在线模式并配好 API，本鲸才能动脑子操作电脑～', 5000)
            return None
        if not self._cua_perm(f'主人要本鲸去操作电脑完成：{goal}'):
            self.say('好，那本鲸不动手了。', 2600)
            return None
        self.cua_busy = True
        self._cua_stop = False
        self._cua_goal = goal
        self._cua_until = time.time() + max(1, int(self.cua_ask_minutes.get() or 30)) * 60
        self._cua_mark_pos()
        self.say(f'好～本鲸开始操作电脑：{goal}', 3600)
        threading.Thread(target=self._cua_loop, args=(goal,), daemon=True).start()
    def _cua_need_ask(self):
        tier = str(self.cua_ask.get() or 'each')
        if tier == 'never':
            return False
        if tier == 'once':
            return time.time() >= self._cua_until
        return True
    def _cua_loop(self, goal):
        step = 0
        max_steps = max(1, int(self.cua_max_steps.get() or 20))
        try:
            while (not self._cua_stop) and step < max_steps:
                step += 1
                if self._cua_need_ask() and (not self._cua_perm(f'第 {step} 步：继续操作电脑完成任务「{goal}」吗？')):
                    break
                self._q.put(('cua_hud', f'正在看屏幕…（第 {step} 步）', None, None, False))
                try:
                    url = screen_data_url(ImageGrab.grab(), 1280, 70)
                except Exception:
                    break
                act = self._cua_decide(goal, url, step)
                if not act:
                    break
                name = str(act.get('action') or '').lower()
                desc = str(act.get('desc') or '').strip() or name
                if name in ('done', ''):
                    self._q.put(('cua_done', f'搞定啦～{desc}'))
                    return
                if name == 'fail':
                    self._q.put(('cua_done', f'呜……本鲸做不下去了：{desc}'))
                    return
                self._cua_wait_user()
                if self._cua_stop:
                    break
                self._q.put(('cua_hud', desc, act.get('x'), act.get('y'), False))
                self._cua_perform(name, act)
                time.sleep(0.45)
        finally:
            self.cua_busy = False
            self._q.put(('cua_stop',))
    def _cua_wait_user(self):
        """主人一动鼠标键盘就先暂停，连着 1.2 秒没动再继续。"""
        if not self._cua_user_active():
            return None
        self._q.put(('cua_hud', '等待主人操作…（本鲸先让边）', None, None, True))
        idle_since = None
        while not self._cua_stop:
            if self._cua_user_active():
                idle_since = None
            elif idle_since is None:
                idle_since = time.time()
            elif time.time() - idle_since > 1.2:
                break
            time.sleep(0.12)
        self._cua_mark_pos()
    def _cua_decide(self, goal, data_url, step):
        sw, sh = self.screen()
        sys_p = f'你是「本鲸」的电脑操作大脑。看着屏幕截图，为了完成主人的目标，决定下一步做哪一个动作。只输出一个 JSON 对象，不要解释、不要代码块。\n字段：{{"action":"move|click|double_click|right_click|drag|type|key|scroll|wait|done|fail","x":0.5,"y":0.5,"x2":0.5,"y2":0.5,"text":"要打的字","key":"ctrl+c","amount":3,"seconds":1,"desc":"用中文一句话说这一步在干嘛"}}\n{CUA_HELP}\n现在是第 {step} 步，屏幕 {sw}x{sh}。完成了就 action=done；没把握或做不到就 action=fail，并在 desc 里说明。'
        body = [{'type': 'text', 'text': f'主人的目标：{goal}'}, {'type': 'image_url', 'image_url': {'url': data_url}}]
        try:
            txt = _api_once(self.cfg, [{'role': 'system', 'content': sys_p}, {'role': 'user', 'content': body}], temperature=0.2, max_tokens=300, timeout=60)
        except Exception:
            return None
        return parse_brain(txt)
    def _cua_perform(self, name, act):
        try:
            sw, sh = self.screen()
            def fx(k, d=0.5):
                try:
                    return max(0.0, min(sw - 1.0, float(act.get(k, d)) * sw))
                except (TypeError, ValueError):
                    return d * sw
            def fy(k, d=0.5):
                try:
                    return max(0.0, min(sh - 1.0, float(act.get(k, d)) * sh))
                except (TypeError, ValueError):
                    return d * sh
            if name == 'move':
                cua_move(fx('x'), fy('y'))
            elif name == 'click':
                cua_click(fx('x'), fy('y'), 'left')
            elif name == 'double_click':
                cua_click(fx('x'), fy('y'), 'left', double=True)
            elif name == 'right_click':
                cua_click(fx('x'), fy('y'), 'right')
            elif name == 'drag':
                cua_drag(fx('x'), fy('y'), fx('x2'), fy('y2'))
            elif name == 'type':
                cua_type(str(act.get('text') or ''))
            elif name == 'key':
                cua_key(str(act.get('key') or ''))
            elif name == 'scroll':
                cua_scroll(int(float(act.get('amount', 3) or 3)))
            elif name == 'wait':
                time.sleep(max(0.2, min(120.0, float(act.get('seconds', 1) or 1))))
        except Exception:
            pass
        self._cua_mark_pos()
    def _cua_menu_start(self):
        """右键菜单入口：问主人要做什么，然后开始。"""
        try:
            goal = simpledialog.askstring('让本鲸操作电脑', '想让本鲸做什么？（例如：打开记事本并输入 hello）', parent=self.root)
        except Exception:
            goal = None
        if goal:
            self.cua_start(goal)
    def _apply_cua(self):
        self.cfg['cua_on'] = bool(self.cua_on.get())
        self.cfg['cua_ask'] = str(self.cua_ask.get() or 'each')
        self.cfg['cua_ask_minutes'] = max(1, int(self.cua_ask_minutes.get() or 30))
        self.cfg['cua_max_steps'] = max(1, int(self.cua_max_steps.get() or 20))
        save_config(self.cfg)
    def _apply_proactive(self):
        self.cfg['proactive'] = bool(self.ask_on.get())
        self.cfg['proactive_gap'] = max(30, int(self.ask_gap.get()))
        self.cfg['proactive_skip_familiar'] = bool(self.skip_familiar.get())
        save_config(self.cfg)
        if self.ask_on.get():
            self.ask_next = time.time() + 20
            score, _ = self.familiar_score()
            if self.skip_familiar.get() or score >= 0.999:
                self.say('好～本鲸会在合适的时候递几个选项让主人挑。', 3800)
            else:
                self.say(f'好～不过本鲸还在熟悉主人呢（{familiarity_text(score)}），等完全了解了才敢主动开口。想现在就生效，去「应用设置 → 智能功能」勾上「跳过熟悉度」～', 6800)
        else:
            self._close_ask()
            self.say('那本鲸就不多嘴啦～', 2600)
    def try_proactive(self):
        """立刻试一次（不理冷却）。"""
        if not self.familiar_ok():
            self.say(f'本鲸还没熟悉够主人呢（{familiarity_text(self.familiar_score()[0])}），再让本鲸多看看、多陪陪吧～', 6000)
            self.show_status()
        else:
            self.ask_next = 0.0
            self._check_proactive()
            if not self.ask_win and (not self.ask_busy):
                    self.say('唔……这会儿本鲸没想出什么好提议。', 3600)
    def _check_proactive(self):
        # irreducible cflow, using cdg fallback
        """到点了就看看：现在要不要主动递几个选项。"""
        if not self.ask_on.get() or self.ask_busy:
            return None
        if self.ask_win and self.ask_win.winfo_exists():
            return
        now = time.time()
        if now < self.ask_next:
            return
        if not self.familiar_ok():
            self.ask_next = now + 300
            return
        if (self.quiet_night.get() if hasattr(self, 'quiet_night') else self.cfg.get('quiet_night', True)) and self._is_night():
                    self.ask_next = now + 300
                    return
        if self.quiet or self.sleeping or self.dragging or self.edge or self.pending:
            return None
        else:
            if self.idle_sec > 90:
                self.ask_next = now + 60
            else:
                self.ask_next = now + max(30, int(self.ask_gap.get()))
                if self._brain_on():
                    self._ai_propose()
                else:
                    self._preset_propose()
    def _proactive_context(self):
        title, exe = self.activity
        hour = time.localtime().tm_hour
        _dev = detect_dev_tool(exe, title)
        dev_txt = f'（编程工具：{_dev}）' if _dev else ''
        return f'时间：{time.strftime('%Y-%m-%d %H:%M')}（{hour} 点）\n主人正在用：{exe or '（不知道）'}（窗口标题：{title or '无'}）{dev_txt}\n主人已经 {int(self.idle_sec)} 秒没碰键鼠\n本鲸的心情：{MOOD_TEXT.get(self.mood(), '待机中')}\n主人最近的操作：\n' + (self._ops_text(6) or '（没记到）')
    def _ai_propose(self):
        self.ask_busy = True
        ctx = self._proactive_context()
        q = self._q
        def worker():
            try:
                text = _api_once(self.cfg, [{'role': 'system', 'content': PROACTIVE_PROMPT}, {'role': 'user', 'content': ctx}], temperature=0.8, max_tokens=300, timeout=20)
                q.put(('propose', True, text))
            except Exception as e:
                q.put(('propose', False, str(e)))
        threading.Thread(target=worker, daemon=True).start()
    def _propose_result(self, ok, text):
        self.ask_busy = False
        if not ok:
            self._preset_propose()
            return
        else:
            obj = parse_brain(text)
            if not obj or not obj.get('offer'):
                return None
            else:
                ask = str(obj.get('ask') or '要不要本鲸帮个忙？').strip()[:40]
                opts = []
                for o in (obj.get('options') or [])[:4]:
                    if not isinstance(o, dict):
                        continue
                    else:
                        label = str(o.get('label') or '').strip()[:8]
                        tool = str(o.get('tool') or 'none').strip()
                        arg = o.get('arg') if isinstance(o.get('arg'), dict) else {}
                        if label:
                            opts.append((label, tool, arg))
                if opts:
                    self._show_ask(ask, opts)
    def _preset_propose(self):
        """本地模式：只认几套预设（看窗口标题 / 时间）。"""
        low = (str(self.activity[1]) + ' ' + str(self.activity[0])).lower()
        hour = time.localtime().tm_hour
        now = time.time()
        for i, rule in enumerate(PROACTIVE_PRESETS):
            if rule.get('night'):
                if hour >= 23 or hour < 6:
                    pass
                else:
                    continue
            else:
                if not any((k in low for k in rule['keys'])):
                    continue
            if now - self._preset_seen.get(i, 0) < 7200:
                continue
            self._preset_seen[i] = now
            self._show_ask(rule['ask'], list(rule['opts']))
            break
    def _show_ask(self, ask, opts):
        """在桌宠脑袋上面弹个小面板，让主人单选一个。"""
        if self.ask_win and self.ask_win.winfo_exists():
            return
        else:
            win = tk.Toplevel(self.root)
            self.ask_win = win
            win.overrideredirect(True)
            win.attributes('-topmost', True)
            win.configure(bg='#c7d6f2')
            card = Frame(win, bg='#eef3ff')
            card.pack(padx=1, pady=1)
            tk.Label(card, text=ask, bg='#eef3ff', fg='#22315a', justify='left', wraplength=240, font=('Microsoft YaHei', 10, 'bold')).pack(anchor='w', padx=10, pady=(8, 4))
            row = Frame(card, bg='#eef3ff')
            row.pack(fill='x', padx=8, pady=(0, 8))
            seen_none = False
            for label, tool, arg in list(opts)[:5]:
                if str(tool or 'none').strip() in ('', 'none'):
                    seen_none = True
                tk.Button(row, text=label, font=('Microsoft YaHei', 9), bg='#ffffff', fg='#22315a', relief='groove', activebackground='#dce6ff', padx=6, command=lambda t=tool, a=arg: self._do_ask(t, a)).pack(side='left', padx=3, pady=2)
            if not seen_none:
                tk.Button(row, text='不用啦', font=('Microsoft YaHei', 9), bg='#eef3ff', fg='#7b88ad', relief='flat', activebackground='#e6edfb', padx=6, command=lambda: self._do_ask('none', {})).pack(side='left', padx=(6, 2), pady=2)
            win.update_idletasks()
            w, h = (win.winfo_width(), win.winfo_height())
            sw = self.screen()[0]
            x = int(min(max(6, self.cx - w / 2), sw - w - 6))
            y = int(max(6, self.foot - self.ground_line - h - 6))
            win.geometry(f'+{x}+{y}')
            self.emote('thinking', 2200)
            self.ask_auto = self.root.after(25000, self._close_ask)
    def _close_ask(self):
        if self.ask_auto:
            try:
                self.root.after_cancel(self.ask_auto)
            except Exception:
                pass
            self.ask_auto = None
        try:
            if self.ask_win and self.ask_win.winfo_exists():
                    self.ask_win.destroy()
        except tk.TclError:
            pass
        self.ask_win = None
    def _do_ask(self, tool, arg):
        """主人点了某个选项（tool 为 none 就是不想麻烦本鲸）。"""
        self._close_ask()
        tool = str(tool or 'none').strip()
        if tool in ['', 'none']:
            self.say('好～那本鲸不打扰主人啦。', 2600)
            return
        else:
            if tool not in PROACTIVE_TOOLS:
                self.say('唔……这个本鲸还不会做。', 2600)
                return
            else:
                self._log_op(f'点了本鲸递的选项：{tool}')
                out = str(run_tool(tool, arg or {}))
                if out.startswith('__'):
                    out = '这个本鲸做不了呢。'
                self.say(out[:70], 4200)
                self.voice_out(out)
                self.happy_until = time.time() + 3
    def _apply_quick(self):
        self.cfg['quick_cmd'] = bool(self.quick_on.get())
        save_config(self.cfg)
        if self.quick_on.get():
            self.say('好～本鲸会认文本里的 [CMD: …] 这类命令了。', 3800)
        else:
            self.say('那本鲸就把方括号当普通文字啦～', 3200)
    def quick_show(self):
        """热键唤出的快捷命令输入框。"""
        if self.quick_box and self.quick_box.winfo_exists():
            self.quick_box.deiconify()
            self.quick_box.lift()
            self.quick_box.focus_force()
            self.quick_entry.focus_set()
            return
        else:
            win = tk.Toplevel(self.root)
            self.quick_box = win
            win.title('快捷命令')
            win.configure(bg='#eef3ff')
            win.attributes('-topmost', True)
            win.resizable(False, False)
            tk.Label(win, text=f'写命令，回车执行（热键 {self.cfg.get('hotkey') or '未设置'}）　例：[CMD: 打开计算器]', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 9)).pack(anchor='w', padx=10, pady=(8, 2))
            self.quick_entry = tk.Text(win, width=48, height=4, wrap='word', font=('Consolas', 10), bg='#ffffff', fg='#22315a', relief='flat', padx=8, pady=6, insertbackground='#22315a')
            self.quick_entry.pack(padx=10, pady=(0, 6))
            self.quick_entry.bind('<Return>', self._quick_return)
            self.quick_note = tk.Label(win, text='', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9), wraplength=380, justify='left', anchor='w')
            self.quick_note.pack(fill='x', padx=10)
            bar = Frame(win, bg='#eef3ff')
            bar.pack(fill='x', padx=10, pady=(4, 10))
            tk.Button(bar, text='命令一览', width=8, font=('Microsoft YaHei', 9), command=self.show_command_help).pack(side='left')
            tk.Button(bar, text='粘贴', width=5, font=('Microsoft YaHei', 9), command=self._quick_paste).pack(side='right', padx=(6, 0))
            tk.Button(bar, text='执行', width=6, font=('Microsoft YaHei', 10), bg='#7ba7f0', fg='white', relief='flat', command=self._quick_run_input).pack(side='right', padx=(6, 0))
            win.update_idletasks()
            w, h = (win.winfo_width(), win.winfo_height())
            sw, sh = self.screen()
            win.geometry(f'+{int(min(max(6, self.cx - w / 2), sw - w - 6))}+{int(max(6, min(sh - h - 60, self.foot - self.ground_line - h - 10)))}')
            self.quick_entry.focus_set()
            self.emote('thinking', 1600)
    def _quick_return(self, _e):
        self._quick_run_input()
        return 'break'
    def _quick_paste(self):
        try:
            txt = self.root.clipboard_get()
        except tk.TclError:
            txt = ''
        if not txt.strip():
            self._quick_note('剪贴板里没有文字。')
            return
        else:
            self.quick_entry.insert('end', txt)
            self.quick_entry.focus_set()
    def _quick_note(self, text):
        if self.quick_note is not None and self.quick_note.winfo_exists():
                self.quick_note.config(text=str(text)[:400])
    def _quick_run_input(self):
        if not self.quick_entry or not self.quick_entry.winfo_exists():
            return None
        else:
            text = self.quick_entry.get('1.0', 'end').strip()
            self.quick_entry.delete('1.0', 'end')
            if not text:
                return
            else:
                out = self._run_quick(text)
                self._quick_note(out if out else '没找到本鲸认识的命令（要有完整的 [CMD: …]）。')
    def run_clipboard_quick(self):
        """把剪贴板里的文本当命令跑一遍。"""
        try:
            txt = self.root.clipboard_get()
        except tk.TclError:
            txt = ''
        if not txt.strip():
            self.say('剪贴板里没有文字呀。', 2800)
            return
        else:
            out = self._run_quick(txt)
            if out is None:
                self.say('剪贴板里没找到本鲸认识的命令。', 3600)
                return
            else:
                if self.quick_box and self.quick_box.winfo_exists():
                        self._quick_note(out)
    def _run_quick(self, text):
        """跑一段文本里的快捷命令，回一句总结（没命令返回 None）。"""
        cmds, plain = scan_commands(text)
        if not cmds:
            return
        else:
            said = []
            for cmd in cmds:
                try:
                    kind, payload = self._exec_quick(cmd)
                except Exception as e:
                    kind, payload = ('say', f'[{cmd['prefix']}] 没做成……（{e}）')
                if kind == 'say' and payload:
                    said.append(payload)
                else:
                    if kind == 'ai':
                        self._quick_ai(payload, cmd['params']['quiet'])
                        said.append('（交给 AI 想去了…）')
            self._log_op(f'跑了 {len(cmds)} 条快捷命令')
            self.meet()
            if plain:
                said.append('其余文字没当命令：' + ' '.join(plain)[:40])
            if not said:
                return '做完了。'
            else:
                if len(said) > 1:
                    self.say('；'.join(said)[:80], 5000)
                else:
                    if not cmds[0]['params']['quiet']:
                        self.say(said[0][:80], 4600)
                return '\n'.join(said)
    def _exec_quick(self, cmd):
        """执行一条快捷命令 → (kind, payload)；kind = say / ai / done。"""
        p, body = (cmd['prefix'], cmd['content'])
        if p == 'SAY':
            t = ' '.join(body.split())
            if t and (not cmd['params']['quiet']):
                    self.say(t[:70], 4200)
                    self.voice_out(t)
            return ('done', None)
        else:
            if p == 'OPEN':
                return ('say', self._quick_open(body))
            else:
                if p == 'SAVE':
                    return ('say', save_memo(body))
                else:
                    if p == 'DEL':
                        return ('say', forget_memo(body))
                    else:
                        if p == 'LIST':
                            return ('say', list_memos(body))
                        else:
                            if p == 'CALC':
                                return ('say', calc_expr(body))
                            else:
                                if p == 'TIME':
                                    return ('say', '现在是 ' + time.strftime('%Y-%m-%d %H:%M:%S') + '（周' + '一二三四五六日'[int(time.strftime('%w')) - 1] + '）')
                                else:
                                    if p == 'SHOT':
                                        return ('say', f'截好了，存在 {take_screenshot()}')
                                    else:
                                        if p == 'CLIP':
                                            try:
                                                self.root.clipboard_clear()
                                                self.root.clipboard_append(body)
                                            except tk.TclError as e:
                                                return ('say', f'剪贴板写不进去……（{e}）')
                                            return ('say', f'复制好啦（{len(body)} 个字）。')
                                        else:
                                            if p == 'READ':
                                                return ('say', read_text_file(body))
                                            else:
                                                if p == 'WRITE':
                                                    return ('say', write_text_file(body))
                                                else:
                                                    if p in ['RUN', 'PS', 'DOS']:
                                                        cmd_text = body.strip()
                                                        if not cmd_text:
                                                            return ('say', '要跑什么命令呀？')
                                                        else:
                                                            style = 'cmd' if p == 'DOS' else 'ps' if p == 'PS' else guess_shell(cmd_text)
                                                            self._bg_run(lambda c=cmd_text, s=style: (True, run_shell(c, s)), cmd['params']['quiet'], 'shell')
                                                            return ('say', '')
                                                    else:
                                                        if p == 'GET':
                                                            url = _normalize_url(body)
                                                            if not url:
                                                                return ('say', f'「{body[:24]}」不像个网址……')
                                                            else:
                                                                self._bg_run(lambda u=url: (True, fetch_page(u)), cmd['params']['quiet'], 'get')
                                                                return ('say', '')
                                                        else:
                                                            if p == 'SEARCH':
                                                                q = body.strip()
                                                                if not q:
                                                                    return ('say', '要搜什么呢？')
                                                                else:
                                                                    if not self.online() or not self._api_ready():
                                                                        return ('say', f'本地搜不了「{q}」，要在线模式才行。')
                                                                    else:
                                                                        self._quick_ai(f'帮我联网搜一下「{q}」，然后用一两句话告诉本鲸搜到了什么。', cmd['params']['quiet'])
                                                                        return ('say', '')
                                                            else:
                                                                if p == 'HIDE':
                                                                    self.hide_at_edge('right' if self.cx > self.screen()[0] / 2 else 'left')
                                                                    return ('done', None)
                                                                else:
                                                                    if p == 'SHOW':
                                                                        self.come_out()
                                                                        return ('done', None)
                                                                    else:
                                                                        if p == 'SLEEP':
                                                                            self.sleep()
                                                                            return ('done', None)
                                                                        else:
                                                                            if p == 'WAKE':
                                                                                self.wake()
                                                                                return ('done', None)
                                                                            else:
                                                                                hit = match_local(body)
                                                                                if hit:
                                                                                    out = run_tool(*hit)
                                                                                    if out == '__CLEAN__':
                                                                                        self.clean_feed()
                                                                                        return ('done', None)
                                                                                    else:
                                                                                        if out.startswith('__'):
                                                                                            return ('say', '这个本鲸做不了呢。')
                                                                                        else:
                                                                                            return ('say', out)
                                                                                else:
                                                                                    if not self.online() or not self._api_ready():
                                                                                        return ('say', f'本地口令里没有「{body[:24]}」，而且现在没连 AI。')
                                                                                    else:
                                                                                        return ('ai', body)
    def _quick_open(self, target):
        """[OPEN: …] 打开网址 / 文件夹 / 文件。"""
        t = str(target or '').strip().strip('\"')
        if not t:
            return '要打开什么呢？'
        else:
            looks_path = len(t) > 2 and t[1] == ':' or t.startswith(('\\\\', '/', '.\\'))
            if os.path.exists(t) or looks_path:
                try:
                    os.startfile(t)
                    name = os.path.basename(t.rstrip('\\/')) or t
                    return f'已经打开 {name} 啦～'
                except OSError as e:
                    return f'打不开……（{e}）'
            else:
                url = _normalize_url(t)
                if url:
                    try:
                        os.startfile(url)
                        return f'浏览器打开 {url} 了。'
                    except OSError as e:
                        return f'打不开……（{e}）'
                else:
                    local = os.path.join(data_dir(), t)
                    if os.path.exists(local):
                        try:
                            os.startfile(local)
                            return f'已经打开 {t} 啦～'
                        except OSError as e:
                            return f'打不开……（{e}）'
                    else:
                        return f'本鲸找不到「{t}」，它也不像个网址……'
    def _bg_run(self, work, quiet=False, tag='task'):
        """慢活丢后台跑（跑命令 / 抓网页 / 问 AI），回来再在气泡里说。"""
        self.bg_q.append((work, quiet, tag))
        if not self.bg_busy:
            self._bg_next()
    def _bg_next(self):
        if not self.bg_q:
            self.bg_busy = False
            return
        else:
            work, quiet, tag = self.bg_q.pop(0)
            self.bg_busy = True
            q = self._q
            def runner():
                try:
                    ok, text = work()
                except Exception as e:
                    ok, text = (False, f'{type(e).__name__}: {e}')
                q.put(('bgdone', ok, text, quiet, tag))
            threading.Thread(target=runner, daemon=True).start()
    def _bg_done(self, ok, text, quiet, tag):
        self.bg_busy = False
        text = str(text or '').strip()
        if tag == 'ai' and ok and text:
                    self.history += [{'role': 'user', 'content': '(快捷命令)'}, {'role': 'assistant', 'content': text}]
                    keep = int(self.cfg.get('history', 10)) * 2
                    self.history = self.history[-keep:]
        if not ok:
            self.say('本鲸没做成……' + text[:50], 5200)
        else:
            if text and (not quiet):
                    self.say(text.splitlines()[0][:70], 5200)
                    self.voice_out(text)
        self._quick_note(text or ('做完了' if ok else ''))
        if self.quick_box and self.quick_box.winfo_exists() and text:
                    self.quick_box.deiconify()
        self._bg_next()
    def _ai_answer(self, request):
        """让在线 AI 回答一个请求（它可以自己调工具）。"""
        cfg = dict(self.cfg)
        msgs = [{'role': 'system', 'content': system_prompt(cfg)}] + list(self.history[-int(cfg.get('history', 10)) * 2:]) + [{'role': 'user', 'content': request}]
        text, calls = _api_tools_once(cfg, msgs, SYSTEM_TOOLS, max_tokens=300, timeout=60)
        for _ in range(2):
            if not calls:
                return (True, text)
            else:
                msgs.append({'role': 'assistant', 'content': None, 'tool_calls': calls})
                for i, c in enumerate(calls[:3]):
                    fn = c.get('function') or {}
                    try:
                        a = json.loads(fn.get('arguments') or '{}')
                    except ValueError:
                        a = {}
                    res = str(run_tool(fn.get('name'), a))
                    if res.startswith('__'):
                        res = '（这条得在聊天里做）'
                    msgs.append({'role': 'tool', 'tool_call_id': c.get('id') or f'qc{i}', 'content': res[:1500]})
                text, calls = _api_tools_once(cfg, msgs, SYSTEM_TOOLS, max_tokens=300, timeout=60)
        return (True, text)
    def _quick_ai(self, request, quiet=False):
        """CMD 认不出来的 / SEARCH，都交给在线 AI。"""
        self._bg_run(lambda: self._ai_answer(request), quiet, 'ai')
    def show_command_help(self):
        """快捷命令一览。"""
        win = tk.Toplevel(self.root)
        win.title('快捷命令一览')
        win.configure(bg='#eef3ff')
        win.attributes('-topmost', True)
        tk.Label(win, text='只要文本里有完整的 [前缀: 内容]，就是一条命令', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 10, 'bold')).pack(anchor='w', padx=12, pady=(10, 4))
        body = Frame(win, bg='#eef3ff')
        body.pack(fill='both', expand=True, padx=12)
        for i, (left, desc) in enumerate(COMMAND_HELP):
            tk.Label(body, text=left, bg='#eef3ff', fg='#22315a', width=16, anchor='w', font=('Consolas', 9)).grid(row=i, column=0, sticky='w', pady=1)
            tk.Label(body, text=desc, bg='#eef3ff', fg='#4a5a7a', anchor='w', justify='left', wraplength=330, font=('Microsoft YaHei', 9)).grid(row=i, column=1, sticky='w', pady=1)
        tk.Label(win, text='参数（写在内容末尾）：\\r \\n 内容里换行；\\r2 \\n2 跳过下面 2 行；\\all 整篇每行都是命令；\\ra1 \\na1 上/下 1 行也算进这条；\\rl1 \\nl1 这条完跳到第 1 行；\\end 到此为止；\\loop 重复本行（最多 10 次）；\\quiet 悄悄执行不弹气泡。\n方括号外面单独写的 \\r \\n 也当换行，所以一行能写好几条命令。', bg='#eef3ff', fg='#6b7a99', justify='left', wraplength=470, font=('Microsoft YaHei', 9)).pack(anchor='w', padx=12, pady=(8, 2))
        tk.Label(win, text='例： [CMD: 打开计算器]\\r[OPEN: baidu.com]\\r[SAVE: 周三去医院]\n　　 [CALC: 128*24]\\r[RUN: ipconfig]\\r[CLIP: 一段文字]\n文件里：第一行写 [CMD: 随便什么\\all]，后面每行都是一条命令', bg='#eef3ff', fg='#3a4a7a', justify='left', wraplength=470, font=('Consolas', 9)).pack(anchor='w', padx=12, pady=(0, 10))
        tk.Button(win, text='关闭', width=8, font=('Microsoft YaHei', 10), command=win.destroy).pack(pady=(0, 10))
    def set_hotkey(self):
        """设置热键：不用手敲，直接按下组合键，本鲸记下来再让主人确认。"""
        win = tk.Toplevel(self.root)
        win.title('设置快捷热键')
        win.configure(bg='#eef3ff')
        win.attributes('-topmost', True)
        win.resizable(False, False)
        tk.Label(win, text='请直接按下想用的组合键', bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 11, 'bold')).pack(padx=20, pady=(14, 2))
        tk.Label(win, text='例如 Ctrl+Alt+K；至少要带 Ctrl / Alt / Shift / Win 中的一个。按 Esc 取消。', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).pack(padx=20)
        shown = tk.Label(win, text='等待按键…', bg='#ffffff', fg='#22315a', font=('Consolas', 15), width=22, height=2)
        shown.pack(padx=20, pady=10)
        state = {'combo': None}
        row = Frame(win, bg='#eef3ff')
        row.pack(pady=(0, 14))
        ok_btn = tk.Button(row, text='就用这个', font=('Microsoft YaHei', 10), bg='#7ba7f0', fg='white', relief='flat', padx=14, pady=3, state='disabled')
        ok_btn.pack(side='left', padx=6)
        cancel_btn = tk.Button(row, text='取消', font=('Microsoft YaHei', 10), bg='#dce7fb', fg='#22315a', relief='flat', padx=14, pady=3)
        cancel_btn.pack(side='left', padx=6)
        def mods_of(bits):
            m = []
            if bits & 4:
                m.append('ctrl')
            if bits & 8:
                m.append('alt')
            if bits & 1:
                m.append('shift')
            if bits & 64:
                m.append('win')
            return m
        def on_key(e):
            if e.keysym == 'Escape':
                close()
                return 'break'
            if e.keysym in _HOTKEY_MODNAMES:
                m = mods_of(e.state)
                shown.config(text=('+'.join(m) + '+…') if m else '等待按键…', fg='#7b88ad')
                return 'break'
            else:
                name = _hotkey_name(e.keysym)
                m = mods_of(e.state)
                combo = '+'.join(m + [name]) if name and m else None
                if (not combo) or (not parse_hotkey(combo)):
                    state['combo'] = None
                    ok_btn.config(state='disabled')
                    shown.config(text='要带 Ctrl / Alt / Shift / Win 中的一个', fg='#c94f4f')
                else:
                    state['combo'] = combo
                    ok_btn.config(state='normal')
                    shown.config(text=combo, fg='#22315a')
                return 'break'
        def close():
            if not state.get('done'):
                state['done'] = True
                try:
                    self.tray.set_hotkey(parse_hotkey(self.cfg.get('hotkey')))
                except Exception:
                    pass
            win.destroy()
        def apply():
            combo = state['combo']
            if not combo:
                return None
            else:
                state['done'] = True
                self.cfg['hotkey'] = combo
                save_config(self.cfg)
                self._apply_hotkey(parse_hotkey(combo))
                win.destroy()
        ok_btn.config(command=apply)
        cancel_btn.config(command=close)
        win.protocol('WM_DELETE_WINDOW', close)
        try:
            if self.tray.hwnd:
                self.tray.set_hotkey(None)
        except Exception:
            pass
        win.bind('<KeyPress>', on_key)
        win.grab_set()
        win.focus_force()
        win.update_idletasks()
        try:
            sw, sh = self.screen()
            win.geometry(f'+{int((sw - win.winfo_width()) / 2)}+{int((sh - win.winfo_height()) / 3)}')
        except Exception:
            pass
    def _apply_hotkey(self, hk):
        """换热键（真正注册由托盘线程做，结果从队列回来）。"""
        self.hotkey_changing = True
        if self.tray.hwnd:
            self.tray.set_hotkey(hk)
        else:
            self.tray.hotkey = hk
        if not hk:
            self.say('好，不用热键了。', 2600)
    def ask_save_memo(self):
        """弹个小窗手动记一条重要信息。"""
        try:
            init = self.root.clipboard_get()[:200]
        except tk.TclError:
            init = ''
        text = simpledialog.askstring('记一条重要信息', '要大肥鲸记下什么？', initialvalue=init, parent=self.root)
        if text and text.strip():
                self.say(save_memo(text), 4200)
                self.meet()
    def show_memos(self):
        out = list_memos()
        self.say(out.splitlines()[(-1)][:70] if '\n' in out else out[:70], 5200)
        if self.chat and self.chat.winfo_exists():
                self._append('pet', out)
    def open_memo_file(self):
        p = memo_path()
        if not os.path.exists(p):
            save_memo('（这里记重要信息，本鲸帮主人存着）')
        try:
            os.startfile(p)
        except OSError as e:
            self.say(f'打不开……（{e}）', 4200)
    def _memory_context(self, text):
        """主人问「我今天干了什么」时，把记录塞给模型当参考。"""
        if not any((k in str(text or '') for k in RECALL_KEYS)):
            return
        else:
            parts = [b.strip()[:MEMORY_CTX_CHARS] for b in [read_memory(day_text(0)), read_memory(day_text((-1)))] if b.strip()]
            if not parts:
                return
            else:
                return {'role': 'system', 'content': '下面是本鲸给主人记的流水账（越靠后越新）。主人问起时就照它帮主人回忆，说人话、别编造，记录里没有的就说没看到：\n\n' + '\n\n'.join(parts)}
    def open_settings(self):
        if self.settings_win and self.settings_win.winfo_exists():
            self.settings_win.lift()
            return
        else:
            win = tk.Toplevel(self.root)
            self.settings_win = win
            win.title('大肥鲸 · API 设置')
            win.configure(bg='#eef3ff')
            win.resizable(False, False)
            win.attributes('-topmost', True)
            v_provider = tk.StringVar(value=self.cfg.get('provider', 'DeepSeek'))
            v_base = tk.StringVar(value=self.cfg.get('api_base', ''))
            v_model = tk.StringVar(value=self.cfg.get('model', ''))
            v_key = tk.StringVar(value=self.cfg.get('api_key', ''))
            v_temp = tk.StringVar(value=str(self.cfg.get('temperature', 0.8)))
            def apply_preset(*_):
                base, model = PROVIDERS.get(v_provider.get(), ('', ''))
                if base:
                    v_base.set(base)
                    v_model.set(model)
            v_provider.trace_add('write', apply_preset)
            body = Frame(win, bg='#eef3ff')
            body.pack(padx=14, pady=12)
            def row(r, label, widget, hint=''):
                tk.Label(body, text=label, bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 10), anchor='e', width=9).grid(row=r, column=0, sticky='e', pady=4)
                widget.grid(row=r, column=1, sticky='we', pady=4)
                if hint:
                    tk.Label(body, text=hint, bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8), anchor='w').grid(row=r, column=2, sticky='w', padx=(8, 0))
            opt = tk.OptionMenu(body, v_provider, *PROVIDERS.keys())
            opt.config(font=('Microsoft YaHei', 10), bg='#ffffff', width=16)
            row(0, '提供方', opt, '选一个常见的，或选「自定义」')
            e_base = Entry(body, textvariable=v_base, width=34, font=('Consolas', 9))
            row(1, 'API 地址', e_base, 'OpenAI 兼容的 /v1 地址')
            e_model = Entry(body, textvariable=v_model, width=34, font=('Consolas', 9))
            row(2, '模型', e_model)
            e_key = Entry(body, textvariable=v_key, width=34, show='*', font=('Consolas', 9))
            row(3, 'API Key', e_key, '只保存在本机 config.json')
            e_temp = Entry(body, textvariable=v_temp, width=8, font=('Consolas', 9))
            row(4, '温度', e_temp, '0~2，越大越放飞')
            v_vision = tk.BooleanVar(value=bool(self.cfg.get('vision', True)))
            tk.Checkbutton(body, text='把拖进来的图片按多模态发给模型（模型不支持看图就取消勾选）', variable=v_vision, bg='#eef3ff', fg='#22315a', font=('Microsoft YaHei', 9), anchor='w', activebackground='#eef3ff').grid(row=5, column=1, columnspan=2, sticky='w', pady=2)
            tk.Label(body, text=f'配置文件：{CONFIG_PATH}', bg='#eef3ff', fg='#7b88ad', font=('Microsoft YaHei', 8)).grid(row=6, column=0, columnspan=3, pady=(8, 0), sticky='w')
            self.settings_lbl = tk.Label(body, text='', bg='#eef3ff', fg='#3a4a7a', font=('Microsoft YaHei', 9), wraplength=420, justify='left')
            self.settings_lbl.grid(row=7, column=0, columnspan=3, pady=(6, 0), sticky='w')
            def current():
                try:
                    temp = float(v_temp.get())
                except ValueError:
                    temp = 0.8
                return {'provider': v_provider.get(), 'api_base': v_base.get().strip(), 'api_key': v_key.get().strip(), 'model': v_model.get().strip(), 'temperature': temp, 'vision': bool(v_vision.get())}
            def save():
                self.cfg.update(current())
                save_config(self.cfg)
                self._refresh_chat_status()
                if self.history_box and self.history_box.winfo_exists():
                        self._append('sys', '设置已保存。')
                win.destroy()
            def test():
                cfg = current()
                if not cfg['api_base'] or not cfg['api_key'] or (not cfg['model']):
                    self.settings_lbl.config(text='API 地址、Key、模型都要填哦。')
                else:
                    self.settings_lbl.config(text='正在测试连接…')
                    self._request([{'role': 'system', 'content': system_prompt(cfg)}, {'role': 'user', 'content': '只回两个字：你好'}], cfg=cfg, test=True)
            btns = Frame(body, bg='#eef3ff')
            btns.grid(row=7, column=0, columnspan=3, pady=(10, 0), sticky='e')
            tk.Button(btns, text='测试连接', width=9, font=('Microsoft YaHei', 10), command=test).pack(side='left', padx=(0, 8))
            tk.Button(btns, text='保存', width=7, font=('Microsoft YaHei', 10), command=save).pack(side='left', padx=(0, 8))
            tk.Button(btns, text='取消', width=7, font=('Microsoft YaHei', 10), command=win.destroy).pack(side='left')
    @staticmethod
    def reply(msg):
        """没配 API 时的本地兜底台词。"""
        rules = [(('你好', '在吗', 'hi', 'hello'), '你好呀主人～本鲸一直都在！'), (('名字', '叫什么', '是谁'), '本鲸叫本鲸，是一只住在海里的鲸鱼女仆哦。'), (('吃', '饿', '米饭', '饭', '甜'), '本鲸最喜欢白米饭了！把不要的东西丢进「投喂」文件夹，本鲸就能换米饭吃。'), (('清理', '垃圾', '打扫'), '右键本鲸选「打扫投喂文件夹」，垃圾会变成米饭哦。'), ('投喂', '喂'), f'右键选「投喂一碗米饭」就行～每天最多 {FEED_MAX_PER_DAY} 次，米饭放 {RICE_SPOIL_DAYS} 天会馊掉，要记得喂本鲸。', (('番茄', '专注', '计时'), '右键本鲸可以开番茄钟哦，25 分钟专注，到点本鲸叫你。'), (('帮我', '能做什么', '会做什么', '有什么功能', '会什么'), '这些本鲸会做：开程序、开网址、静音/音量、截图、看内存、收起窗口、锁屏、设提醒。直接跟本鲸说就行～'), (('喜欢', '爱你', '抱'), '诶诶，本鲸也喜欢主人～（害羞）'), (('再见', '拜拜', '晚安'), '晚安主人，记得好好休息，本鲸守着你。'), (('时间', '几点'), '本鲸不太会看表，不过你开心的时候就是好时候～'), (('累', '困', '烦', '难过'), '辛苦啦，摸摸头，本鲸陪主人一起深呼吸。'), (('胖', '重'), '本鲸才不胖！这叫圆润，尾巴很轻的。'), (('笨', '丑', '讨厌'), '呜……主人好过分，本鲸要躲进海里了。'), (('玩', '游戏'), '要不要猜拳？右键本鲸选「一起猜拳」就好啦！')]
        low = msg.lower()
        for keys, ans in rules:
            if any((k in low for k in keys)):
                return ans
        return random.choice(['唔……本鲸还在学说话，听不太懂，不过本鲸在认真听哦。', '咕噜咕噜～主人继续说，本鲸听着呢。', '这个本鲸记下啦！', '诶嘿，跟主人聊天真开心。'])
    def run(self):
        self.root.mainloop()
import winreg
def uninstall_app():
    """从「应用和功能」里点卸载时走这里：删快捷方式、自启项、卸载信息，再删文件。"""
    exe = os.path.abspath(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    home = os.path.dirname(exe)
    root = tk.Tk()
    root.withdraw()
    purge = messagebox.askyesno(f'卸载{APP_NAME}', f'确定要卸载{APP_NAME}吗？\n\n选「是」＝连配置和存档一起删干净\n选「否」＝保留 config.json / state.json / 投喂 文件夹（重装还能接着用）')
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_UNINST) as k:
            lnks = winreg.QueryValueEx(k, 'Shortcuts')[0]
    except OSError:
        lnks = ''
    for p in [x for x in str(lnks).split('|') if x]:
        try:
            os.remove(p)
        except OSError:
            pass
    for hive, path, name in [(winreg.HKEY_CURRENT_USER, REG_RUN, APP_NAME)]:
        try:
            with winreg.OpenKey(hive, path, 0, winreg.KEY_ALL_ACCESS) as k:
                winreg.DeleteValue(k, name)
        except OSError:
            pass
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, REG_UNINST)
    except OSError:
        pass
    root.destroy()
    tail = f'rmdir /s /q \"{home}\"' if purge else f'del /f /q \"{exe}\"'
    try:
        subprocess.Popen(['cmd', '/c', f'timeout /t 2 /nobreak >nul & {tail}'], creationflags=134217728)
    except Exception:
        return None
if __name__ == '__main__':
    if '--uninstall' in sys.argv:
        uninstall_app()
    else:
        WhalePet().run()
