import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFilter

os.makedirs("aura/assets", exist_ok=True)
os.makedirs("scratch/aura_frames", exist_ok=True)
W, H = 1920, 1080

print("Generating Aura Planar-1 headphone video and photography assets...")

# 1. Generate 120-frame (4s @ 30fps) exploded headphone assembly video
for f_idx in range(120):
    progress = f_idx / 120.0
    img = Image.new("RGB", (W, H), (8, 10, 14))
    draw = ImageDraw.Draw(img)

    # Ambient studio radial spotlight
    for r in range(int(W * 0.6), 0, -15):
        intensity = int((1 - r / (W * 0.6)) * 45)
        draw.ellipse([W*0.5 - r, H*0.48 - r*0.6, W*0.5 + r, H*0.48 + r*0.6], fill=(10 + intensity, 14 + int(intensity*1.2), 22 + int(intensity*1.8)))

    # Acoustic wave ripples in background
    for w_i in range(5):
        wave_r = int((f_idx * 4 + w_i * 90) % (W*0.7))
        alpha = max(0, int(255 * (1 - wave_r / (W*0.7))))
        draw.ellipse([W*0.5 - wave_r, H*0.48 - wave_r*0.6, W*0.5 + wave_r, H*0.48 + wave_r*0.6], outline=(30, 45, 65), width=1)

    # Headphone Exploded Stage Center
    cx, cy = int(W * 0.5), int(H * 0.48)
    
    # Explode distance based on smooth sine oscillation
    explode = math.sin(progress * math.pi) * 160

    # 1. Carbon Fiber & Beryllium Arch Headband (Top)
    hb_y = int(cy - 200 - explode * 0.4)
    draw.arc([cx - 220, hb_y, cx + 220, hb_y + 360], 190, 350, fill=(40, 48, 62), width=18)
    draw.arc([cx - 215, hb_y + 4, cx + 215, hb_y + 360], 190, 350, fill=(212, 163, 89), width=2)
    # Suspension leather strap
    draw.arc([cx - 180, hb_y + 25, cx + 180, hb_y + 340], 200, 340, fill=(25, 28, 36), width=14)

    # 2. Left & Right Ear Cup Sub-Assemblies (Exploded layers)
    for side, sign in [('left', -1), ('right', 1)]:
        base_x = cx + sign * int(220 + explode * 0.8)
        
        # Layer A: Lambskin Memory Foam Cushion (Innermost)
        pad_x = base_x - sign * int(explode * 0.6)
        draw.ellipse([pad_x - 70, cy - 110, pad_x + 70, cy + 110], fill=(22, 25, 34), outline=(45, 52, 68), width=12)
        draw.ellipse([pad_x - 35, cy - 65, pad_x + 35, cy + 65], fill=(10, 12, 16), outline=(30, 35, 48), width=2)

        # Layer B: Planar Magnetic Trace Diaphragm (Golden etched ultra-thin film)
        diag_x = base_x
        draw.ellipse([diag_x - 60, cy - 95, diag_x + 60, cy + 95], fill=(18, 22, 30), outline=(212, 163, 89), width=3)
        # Etched gold trace lines
        for l_y in range(-70, 75, 14):
            draw.line([(diag_x - 45, cy + l_y), (diag_x + 45, cy + l_y)], fill=(212, 163, 89), width=2)

        # Layer C: Neodymium N52 Magnet Matrix
        mag_x = base_x + sign * int(explode * 0.4)
        draw.ellipse([mag_x - 62, cy - 98, mag_x + 62, cy + 98], outline=(56, 189, 248), width=2)
        for m_y in range(-65, 70, 24):
            draw.rounded_rectangle([mag_x - 48, cy + m_y - 6, mag_x + 48, cy + m_y + 6], radius=3, fill=(35, 42, 56), outline=(56, 189, 248), width=1)

        # Layer D: Open-Back Aerodynamic Grill (Outermost)
        grill_x = base_x + sign * int(explode * 0.8)
        draw.ellipse([grill_x - 65, cy - 102, grill_x + 65, cy + 102], fill=(18, 20, 28), outline=(60, 70, 90), width=4)
        for gx in range(-45, 50, 15):
            draw.line([(grill_x + gx, cy - 75), (grill_x + gx, cy + 75)], fill=(40, 48, 64), width=2)
        # Brand Logo on Center Cap
        draw.ellipse([grill_x - 18, cy - 18, grill_x + 18, cy + 18], fill=(212, 163, 89), outline=(255, 255, 255), width=1)

        # Silver-plated 4.4mm audio cable exiting base
        cab_start_x = grill_x
        cab_start_y = cy + 105
        draw.line([(cab_start_x, cab_start_y), (cab_start_x - sign * 40, cab_start_y + 80), (cx, H - 40)], fill=(180, 190, 210), width=4)

    # Ambient audio pulse wave
    freq_text = f"{20 + int(progress * 39980):,} Hz // PLANAR RESPONSE"
    draw.text((cx - 100, H - 90), freq_text, fill=(56, 189, 248))

    img.save(f"scratch/aura_frames/frame_{f_idx:04d}.png")

# Compile hero.mp4 and showcase.mp4
subprocess.run('ffmpeg -y -framerate 30 -i scratch/aura_frames/frame_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p aura/assets/hero.mp4', shell=True, check=True)
subprocess.run('ffmpeg -y -i aura/assets/hero.mp4 -vf "scale=1280:720,fps=30" -c:v libx264 -crf 20 -pix_fmt yuv420p aura/assets/showcase.mp4', shell=True, check=True)

# 2. Generate High-Res Macro Photography Assets
# Macro Diaphragm Detail
img_macro = Image.new("RGB", (W, H), (12, 14, 18))
draw_macro = ImageDraw.Draw(img_macro)
for y in range(0, H, 20):
    draw_macro.line([(0, y), (W, y)], fill=(212, 163, 89), width=4)
    draw_macro.line([(0, y+10), (W, y+10)], fill=(30, 36, 48), width=2)
for x in range(0, W, 100):
    draw_macro.line([(x, 0), (x, H)], fill=(56, 189, 248), width=1)
draw_macro.ellipse([W*0.3, H*0.2, W*0.7, H*0.8], outline=(255, 255, 255), width=6)
img_macro = img_macro.filter(ImageFilter.GaussianBlur(radius=2))
img_macro.save("aura/assets/frame_macro.jpg", quality=95)

# Stand Lifestyle Photo
img_stand = Image.new("RGB", (W, H), (14, 16, 22))
draw_stand = ImageDraw.Draw(img_stand)
draw_stand.polygon([(W*0.4, H*0.8), (W*0.6, H*0.8), (W*0.65, H), (W*0.35, H)], fill=(45, 35, 25))
draw_stand.line([(W*0.5, H*0.15), (W*0.5, H*0.8)], fill=(70, 75, 90), width=22)
draw_stand.arc([W*0.38, H*0.12, W*0.62, H*0.45], 180, 360, fill=(35, 40, 52), width=24)
img_stand = img_stand.filter(ImageFilter.GaussianBlur(radius=3))
img_stand.save("aura/assets/cockpit.jpg", quality=95)

print("Aura Planar-1 assets generated successfully!")
