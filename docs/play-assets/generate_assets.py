#!/usr/bin/env python3
"""Generate Google Play Store graphics for ForeverBetter Connect.

Brand palette (from website/src/app/globals.css):
  paper  #fbf8f4   ink #080808   accent #b51730
Outputs into ./ (run from play-assets dir).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

PAPER = (251, 248, 244)
PAPER2 = (246, 241, 235)
INK = (8, 8, 8)
ACCENT = (181, 23, 48)
ACCENT_DK = (140, 16, 36)
MUTED = (95, 92, 87)

HERE = os.path.dirname(os.path.abspath(__file__))

def font(size, bold=True):
    candidates = [
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_pulse(d, cx, cy, w, amp, color, width, n=280):
    """Draw a stylized heartbeat / sync pulse line centered vertically at cy."""
    pts = []
    for i in range(n + 1):
        x = cx - w / 2 + (w * i / n)
        t = i / n
        # baseline with a single QRS-like spike near the middle
        y = cy
        d0 = t - 0.5
        spike = math.exp(-(d0 * 22) ** 2)
        wobble = 0.12 * math.sin(t * math.pi * 6)
        y = cy - amp * (spike * 1.0) + amp * 0.10 * wobble
        # small dip right before the spike
        y += amp * 0.5 * math.exp(-((t - 0.44) * 40) ** 2)
        y += amp * 0.35 * math.exp(-((t - 0.56) * 34) ** 2)
        pts.append((x, y))
    d.line(pts, fill=color, width=width, joint="curve")

# ---------------------------------------------------------------- ICON 512
def make_icon(path, size=512):
    scale = 4
    S = size * scale
    img = Image.new("RGB", (S, S), PAPER)
    d = ImageDraw.Draw(img)
    # subtle vertical gradient
    for y in range(S):
        t = y / S
        r = int(PAPER[0] * (1 - t) + PAPER2[0] * t)
        g = int(PAPER[1] * (1 - t) + PAPER2[1] * t)
        b = int(PAPER[2] * (1 - t) + PAPER2[2] * t)
        d.line([(0, y), (S, y)], fill=(r, g, b))
    # accent ring
    margin = int(S * 0.14)
    d.ellipse([margin, margin, S - margin, S - margin],
              outline=ACCENT, width=int(S * 0.018))
    # inner faint ring
    m2 = int(S * 0.20)
    d.ellipse([m2, m2, S - m2, S - m2],
              outline=(int(ACCENT[0]), int(ACCENT[1]), int(ACCENT[2])), width=int(S * 0.006))
    # heartbeat pulse
    draw_pulse(d, S / 2, S / 2, w=S * 0.52, amp=S * 0.16,
               color=ACCENT, width=int(S * 0.028))
    # small filled node at the pulse peak
    d.ellipse([S/2 - S*0.02, S*0.5 - S*0.185 - S*0.02,
               S/2 + S*0.02, S*0.5 - S*0.185 + S*0.02], fill=ACCENT_DK)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(path)
    print("wrote", path, img.size)

# ---------------------------------------------------------------- FEATURE 1024x500
def make_feature(path, w=1024, h=500):
    scale = 2
    W, H = w * scale, h * scale
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    # dark gradient background
    for y in range(H):
        t = y / H
        r = int(12 * (1 - t) + 26 * t)
        g = int(12 * (1 - t) + 12 * t)
        b = int(14 * (1 - t) + 16 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    # faint pulse across full width
    draw_pulse(d, W * 0.5, H * 0.52, w=W * 1.15, amp=H * 0.16,
               color=(60, 26, 32), width=int(H * 0.02))
    draw_pulse(d, W * 0.5, H * 0.52, w=W * 0.9, amp=H * 0.20,
               color=ACCENT, width=int(H * 0.012))
    # title
    tf = font(int(H * 0.15), bold=True)
    sf = font(int(H * 0.062), bold=False)
    d.text((int(W * 0.07), int(H * 0.30)), "ForeverBetter", font=tf, fill=PAPER)
    d.text((int(W * 0.07), int(H * 0.30 + H * 0.155)), "Connect", font=tf, fill=ACCENT)
    d.text((int(W * 0.07), int(H * 0.70)),
           "Sync your Health Connect data, securely.", font=sf, fill=(210, 205, 198))
    img = img.resize((w, h), Image.LANCZOS)
    img.save(path)
    print("wrote", path, img.size)

# ---------------------------------------------------------------- PHONE SCREENSHOTS
def rounded_panel(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def make_screenshot(path, kind, w=1080, h=2160):
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(PAPER[0] * (1 - t) + PAPER2[0] * t)
        g = int(PAPER[1] * (1 - t) + PAPER2[1] * t)
        b = int(PAPER[2] * (1 - t) + PAPER2[2] * t)
        d.line([(0, y), (w, y)], fill=(r, g, b))
    pad = 70
    # status bar mock
    sf_small = font(34, bold=False)
    d.text((pad, 40), "9:41", font=font(34, bold=True), fill=INK)
    d.text((w - pad - 120, 40), "5G  100%", font=sf_small, fill=MUTED)
    # header
    d.text((pad, 150), "ForeverBetter", font=font(64, bold=True), fill=INK)
    d.text((pad, 226), "Connect", font=font(64, bold=True), fill=ACCENT)

    title_f = font(52, bold=True)
    body_f = font(38, bold=False)
    label_f = font(34, bold=False)

    if kind == "connect":
        caption = "Connect your account"
        y = 380
        rounded_panel(d, [pad, y, w - pad, y + 640], 40, (255, 255, 255), (229, 221, 212), 2)
        d.text((pad + 50, y + 50), "Host", font=label_f, fill=MUTED)
        rounded_panel(d, [pad + 50, y + 100, w - pad - 50, y + 200], 20, PAPER2, (229, 221, 212), 2)
        d.text((pad + 80, y + 130), "https://api.foreverbetter.xyz", font=body_f, fill=INK)
        d.text((pad + 50, y + 250), "Sign-in code", font=label_f, fill=MUTED)
        rounded_panel(d, [pad + 50, y + 300, w - pad - 50, y + 400], 20, PAPER2, (229, 221, 212), 2)
        d.text((pad + 80, y + 330), "••••••••", font=body_f, fill=INK)
        rounded_panel(d, [pad + 50, y + 470, w - pad - 50, y + 580], 26, ACCENT)
        d.text((w / 2, y + 525), "Connect", font=title_f, fill=PAPER, anchor="mm")
    elif kind == "permissions":
        caption = "You choose what to share"
        rows = ["Steps & distance", "Heart rate & HRV", "Sleep", "Active energy",
                "Blood oxygen", "Workouts"]
        y = 380
        d.text((pad, y), "Health Connect permissions", font=title_f, fill=INK)
        y += 110
        for r in rows:
            rounded_panel(d, [pad, y, w - pad, y + 130], 28, (255, 255, 255), (229, 221, 212), 2)
            d.text((pad + 50, y + 42), r, font=body_f, fill=INK)
            # toggle on
            rounded_panel(d, [w - pad - 150, y + 38, w - pad - 40, y + 92], 27, ACCENT)
            d.ellipse([w - pad - 90, y + 40, w - pad - 42, y + 90], fill=PAPER)
            y += 160
    else:  # syncing
        caption = "Syncing in the background"
        cx, cy = w / 2, 900
        d.ellipse([cx - 220, cy - 220, cx + 220, cy + 220], outline=ACCENT, width=16)
        draw_pulse(d, cx, cy, w=360, amp=120, color=ACCENT, width=14)
        d.text((cx, cy + 330), "Sync active", font=title_f, fill=INK, anchor="mm")
        d.text((cx, cy + 410), "Last synced just now", font=body_f, fill=MUTED, anchor="mm")
        rounded_panel(d, [pad, cy + 520, w - pad, cy + 640], 26, (255, 255, 255), (229, 221, 212), 2)
        d.text((cx, cy + 580), "Disconnect", font=body_f, fill=ACCENT, anchor="mm")

    # caption band bottom
    d.text((pad, h - 220), caption, font=font(56, bold=True), fill=INK)
    img.save(path)
    print("wrote", path, img.size)

if __name__ == "__main__":
    make_icon(os.path.join(HERE, "icon-512.png"))
    make_feature(os.path.join(HERE, "feature-graphic-1024x500.png"))
    make_screenshot(os.path.join(HERE, "screenshot-1-connect.png"), "connect")
    make_screenshot(os.path.join(HERE, "screenshot-2-permissions.png"), "permissions")
    make_screenshot(os.path.join(HERE, "screenshot-3-syncing.png"), "syncing")
