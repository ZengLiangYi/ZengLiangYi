"""
Terminal Lumina — Business Card Generator v4
Bigger text + real QR code linking to GitHub profile.
"""

from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

W, H = 1800, 1020
BG = "#0D1117"
GREEN = "#00FF41"
BLUE = "#3178C6"
WHITE = "#E6EDF3"
GRAY = "#8B949E"
DIM = "#484F58"
DIMMER = "#2A2F38"
FAINT = "#161B22"
SUBTLE = "#1A1F27"

FONTS = os.path.expanduser(r"~\.claude\skills\canvas-design\canvas-fonts")
CN = r"C:\Windows\Fonts\msyh.ttc"
CN_BD = r"C:\Windows\Fonts\msyhbd.ttc"

def ft(name, sz): return ImageFont.truetype(os.path.join(FONTS, name), sz)
def cn(sz, bold=False): return ImageFont.truetype(CN_BD if bold else CN, sz)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ── Background: dot matrix ──
for x in range(20, W, 40):
    for y in range(20, H, 40):
        if (x // 40 + y // 40) % 5 == 0:
            d.ellipse([x, y, x+2, y+2], fill=FAINT)

for y in range(0, H, 4):
    if y % 12 == 0:
        d.line([(0, y), (W, y)], fill="#0F1419", width=1)

# ── Corner brackets ──
for cx, cy, dx, dy in [(55,45,1,1),(W-55,45,-1,1),(55,H-45,1,-1),(W-55,H-45,-1,-1)]:
    d.line([(cx, cy), (cx+22*dx, cy)], fill=DIM, width=2)
    d.line([(cx, cy), (cx, cy+22*dy)], fill=DIM, width=2)

# ── Vertical divider (dashed) ──
DIV = 900
for y in range(80, H-80, 10):
    if y % 20 == 0:
        d.line([(DIV, y), (DIV, y+6)], fill=DIMMER, width=1)

# ══════════════════════════════════════════
# LEFT COLUMN
# ══════════════════════════════════════════
L = 120
Y = 100

# Green accent bar + cursor dot
d.rectangle([(L-32, Y+12), (L-26, Y+420)], fill=GREEN)
d.ellipse([L-35, Y-2, L-21, Y+12], fill=GREEN)

# Name — BIGGER
d.text((L, Y), "曾亮懿", font=cn(120, True), fill=WHITE)
Y += 148
d.text((L+2, Y), "ZENG LIANGYI", font=ft("GeistMono-Bold.ttf", 32), fill=DIM)

# Title — BIGGER
Y += 68
d.text((L, Y), "前端开发工程师", font=cn(46, True), fill=GREEN)

# Company — BIGGER
Y += 65
d.text((L, Y), "深圳市鑫钰晖科技有限公司", font=cn(30), fill=GRAY)

# Separator
Y += 58
d.line([(L, Y), (L+540, Y)], fill=DIMMER, width=1)

# Tagline — BIGGER
Y += 25
d.text((L, Y), "构建企业级 Web 应用与 AI 产品", font=cn(26), fill="#6E7681")

# Tech pills — BIGGER
Y += 60
techs = ["React", "Vue", "Next.js", "Flutter", "TypeScript"]
ftch = ft("GeistMono-Regular.ttf", 24)
tx = L
for t in techs:
    bb = ftch.getbbox(t)
    tw = bb[2] - bb[0] + 32
    d.rounded_rectangle([(tx, Y), (tx+tw, Y+42)], radius=7, fill=FAINT, outline=DIMMER, width=1)
    d.text((tx+16, Y+8), t, font=ftch, fill=GRAY)
    tx += tw + 12

# Code fragment (bottom-left)
Y += 80
fc = ft("JetBrainsMono-Regular.ttf", 16)
for i, line in enumerate([
    "const dev = {",
    "  stack: ['React','Vue','Next'],",
    "  builds: 'enterprise + AI',",
    "  status: 'always shipping'",
    "};"
]):
    d.text((L, Y + i*24), line, font=fc, fill=DIMMER)

# ══════════════════════════════════════════
# RIGHT COLUMN
# ══════════════════════════════════════════
RX = DIV + 65
RY = 120

fl = ft("GeistMono-Regular.ttf", 20)
fv = ft("GeistMono-Regular.ttf", 27)

contacts = [
    ("TEL",  "134 8086 0940"),
    ("WX",   "134 8086 0940（微信同号）"),
    ("MAIL", "1361209507@qq.com"),
    ("WEB",  "zengliangyi.cn"),
]

# Blue accent bar
d.rectangle([(RX-18, RY+4), (RX-14, RY + len(contacts)*82 - 20)], fill=BLUE)

for i, (label, val) in enumerate(contacts):
    cy = RY + i * 82
    d.text((RX, cy), label, font=fl, fill=BLUE)
    has_cn = any('\u4e00' <= c <= '\u9fff' for c in val)
    d.text((RX, cy+30), val, font=cn(27) if has_cn else fv, fill=WHITE)

# ── Real QR Code → GitHub profile ──
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=1)
qr.add_data("https://github.com/ZengLiangYi")
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#00FF41", back_color="#0D1117").convert("RGB")
qr_size = 200
qr_img = qr_img.resize((qr_size, qr_size), Image.NEAREST)

qr_x = RX + 20
qr_y = 560
img.paste(qr_img, (qr_x, qr_y))

# QR border frame
d.rectangle([(qr_x-4, qr_y-4), (qr_x+qr_size+4, qr_y+qr_size+4)], outline=DIMMER, width=1)

# Label
d.text((qr_x, qr_y + qr_size + 14), "扫码访问 GitHub 主页", font=cn(18), fill=DIM)

# GH label next to QR
d.text((qr_x + qr_size + 30, qr_y + 70), "GH", font=fl, fill=BLUE)
d.text((qr_x + qr_size + 30, qr_y + 100), "github.com/", font=ft("GeistMono-Regular.ttf", 22), fill=WHITE)
d.text((qr_x + qr_size + 30, qr_y + 130), "ZengLiangYi", font=ft("GeistMono-Bold.ttf", 22), fill=WHITE)

# ── Circuit traces (top-right) ──
for i, yy in enumerate([58, 72, 86]):
    xs = W - 160 + i * 35
    d.line([(xs, yy), (W-60, yy)], fill=DIMMER, width=1)
    d.ellipse([W-63, yy-2, W-57, yy+4], fill=DIMMER)

# ── Bottom bar ──
ff = ft("GeistMono-Regular.ttf", 16)
d.text((L-30, H-55), "SZ  22.5431°N  114.0579°E", font=ff, fill=DIMMER)
d.text((W-370, H-55), "// BUILDING THE FUTURE", font=ff, fill=DIMMER)
d.rectangle([(W-125, H-53), (W-113, H-39)], fill=GREEN)

# ── OUTPUT ──
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "business-card.png")
img.save(out, "PNG", quality=100)
print(f"Done: {out} ({W}x{H})")
