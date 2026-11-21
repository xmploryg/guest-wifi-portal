#!/usr/bin/env python3
"""Generate QR code for WiFi network: Go Noles / FirstYearDown"""
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# WiFi QR code format: WIFI:T:WPA;S:<SSID>;P:<PASSWORD>;;
wifi_config = "WIFI:T:WPA;S:Go Noles;P:FirstYearDown;;"

# Generate QR code
qr = qrcode.QRCode(
    version=3,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=4,
)
qr.add_data(wifi_config)
qr.make(fit=True)

# Create QR image with high contrast
qr_img = qr.make_image(fill_color="#002147", back_color="#FFFFFF").convert("RGBA")

# Create printable card (4x6 inch at 300 DPI = 1200x1800)
card_w, card_h = 1200, 1800
card = Image.new("RGBA", (card_w, card_h), "#FFFFFF")
draw = ImageDraw.Draw(card)

# Background gradient approximation - FSU colors
for y in range(card_h):
    ratio = y / card_h
    r = int(0 * (1-ratio) + 206 * ratio)
    g = int(33 * (1-ratio) + 17 * ratio)
    b = int(71 * (1-ratio) + 38 * ratio)
    draw.line([(0, y), (card_w, y)], fill=(r, g, b, 255))

# Gold accent bar at top
draw.rectangle([0, 0, card_w, 120], fill="#FFD700")

# Title
try:
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    font_pwd = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 42)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_pwd = ImageFont.load_default()
    font_small = ImageFont.load_default()

# "Go Noles" title
title_text = "Go Noles"
title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
title_w = title_bbox[2] - title_bbox[0]
draw.text(((card_w - title_w) // 2, 160), title_text, font=font_title, fill="#002147")

# Subtitle
sub_text = "Guest WiFi Access"
sub_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
sub_w = sub_bbox[2] - sub_bbox[0]
draw.text(((card_w - sub_w) // 2, 250), sub_text, font=font_sub, fill="#002147")

# QR code centered
qr_size = 500
qr_resized = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
qr_x = (card_w - qr_size) // 2
qr_y = 320
# White background behind QR for scanability
draw.rectangle([qr_x - 20, qr_y - 20, qr_x + qr_size + 20, qr_y + qr_size + 20], fill="#FFFFFF")
card.paste(qr_resized, (qr_x, qr_y), qr_resized)

# Network details below QR
details_y = qr_y + qr_size + 40

# SSID
ssid_label = "Network Name (SSID)"
ssid_val = "Go Noles"
draw.text((card_w // 2, details_y), ssid_label, font=font_small, fill="#FFFFFF", anchor="mm")
details_y += 40
draw.text((card_w // 2, details_y), ssid_val, font=font_pwd, fill="#FFD700", anchor="mm")
details_y += 60

# Password
pwd_label = "Password"
pwd_val = "FirstYearDown"
draw.text((card_w // 2, details_y), pwd_label, font=font_small, fill="#FFFFFF", anchor="mm")
details_y += 40
draw.text((card_w // 2, details_y), pwd_val, font=font_pwd, fill="#FFD700", anchor="mm")
details_y += 80

# Instructions
instructions = [
    "📱 Open Camera app",
    "📷 Point at QR code",
    "👆 Tap to join network"
]
for inst in instructions:
    draw.text((card_w // 2, details_y), inst, font=font_small, fill="#FFFFFF", anchor="mm")
    details_y += 38

# Footer
footer_text = "FSU • Go Noles • Guest Network"
footer_bbox = draw.textbbox((0, 0), footer_text, font=font_small)
footer_w = footer_bbox[2] - footer_bbox[0]
draw.text(((card_w - footer_w) // 2, card_h - 80), footer_text, font=font_small, fill="#FFD700")

# Save print-ready PNG
output_path = "/opt/data/guest-wifi/wifi-qr-print.png"
card.save(output_path, "PNG", dpi=(300, 300))
print(f"✅ Saved print-ready QR card: {output_path}")
print(f"   Dimensions: {card_w}x{card_h}px @ 300 DPI (4x6 inch)")
print(f"   WiFi config: {wifi_config}")

# Also save just the QR code for web use
qr_web = qr_img.resize((400, 400), Image.LANCZOS)
qr_web.save("/opt/data/guest-wifi/wifi-qr-web.png")
print(f"✅ Saved web QR: /opt/data/guest-wifi/wifi-qr-web.png")