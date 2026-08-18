import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFilter

os.makedirs("scratch/lego_frames", exist_ok=True)
os.makedirs("assets", exist_ok=True)

W, H = 1920, 1080
TOTAL_FRAMES = 180  # 6 seconds at 30fps

print("Generating 180-frame Lego build timelapse animation...")

# Helper to draw isometric 3D Lego brick
def draw_lego_brick(draw, x, y, w, h, depth, color_top, color_front, color_side, studs_x=2, studs_y=4, glowing=False, alpha=1.0):
    # Front face
    draw.polygon([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill=color_front)
    # Side face
    draw.polygon([(x + w, y), (x + w + depth, y - int(depth*0.5)), (x + w + depth, y + h - int(depth*0.5)), (x + w, y + h)], fill=color_side)
    # Top face
    draw.polygon([(x, y), (x + depth, y - int(depth*0.5)), (x + w + depth, y - int(depth*0.5)), (x + w, y)], fill=color_top)
    
    # Highlight edge
    edge_col = (255, 255, 255) if not glowing else (100, 220, 255)
    draw.line([(x, y), (x + w, y), (x + w + depth, y - int(depth*0.5))], fill=edge_col, width=2 if not glowing else 3)

    # Studs on top face
    stud_r = max(2, int(w / (studs_x * 3.2)))
    for sx in range(studs_x):
        for sy in range(studs_y):
            u = (sx + 0.5) / studs_x
            v = (sy + 0.5) / studs_y
            st_x = x + u * w + v * depth
            st_y = y - v * int(depth*0.5) - 6
            
            draw.ellipse([st_x - stud_r, st_y - int(stud_r*0.6), st_x + stud_r, st_y + int(stud_r*0.6)], 
                         fill=color_top, outline=(200, 220, 255) if glowing else color_side, width=1)
            draw.ellipse([st_x - int(stud_r*0.7), st_y - int(stud_r*0.4), st_x + int(stud_r*0.7), st_y + int(stud_r*0.4)], 
                         fill=(80, 220, 255) if glowing else color_top)

def ease_out_bounce(t):
    if t < (1 / 2.75):
        return 7.5625 * t * t
    elif t < (2 / 2.75):
        t -= (1.5 / 2.75)
        return 7.5625 * t * t + 0.75
    elif t < (2.5 / 2.75):
        t -= (2.25 / 2.75)
        return 7.5625 * t * t + 0.9375
    else:
        t -= (2.625 / 2.75)
        return 7.5625 * t * t + 0.984375

def ease_out_cubic(t):
    return 1 - math.pow(1 - t, 3)

# Render each frame of the assembly timelapse
for frame_idx in range(TOTAL_FRAMES):
    progress = frame_idx / TOTAL_FRAMES  # 0.0 to 1.0

    img = Image.new("RGB", (W, H), (10, 12, 16))
    draw = ImageDraw.Draw(img)

    # Ambient spotlight with subtle breathing
    spot_pulse = math.sin(frame_idx * 0.05) * 5
    for r in range(int(W * 0.7), 0, -15):
        intensity = int((1 - r / (W * 0.7)) * (38 + spot_pulse))
        draw.ellipse([W*0.5 - r, H*0.45 - r*0.6, W*0.5 + r, H*0.45 + r*0.6], fill=(10 + intensity, 14 + int(intensity*1.2), 22 + int(intensity*1.7)))

    # Studio table surface reflection plane
    table_y = int(H * 0.58)
    for y in range(table_y, H):
        ratio = (y - table_y) / (H - table_y)
        shade = int(8 + ratio * 12)
        draw.line([(0, y), (W, y)], fill=(shade, shade + 2, shade + 6))

    # Grid lines on cutting mat
    for x in range(0, W, 80):
        draw.line([(x, table_y), (int(W*0.5 + (x - W*0.5)*1.8), H)], fill=(22, 28, 42), width=1)
    for y in range(table_y, H, 45):
        draw.line([(0, y), (W, y)], fill=(22, 28, 42), width=1)

    # =========================================================================
    # LEGO ASSEMBLY TIMELINE PIECES
    # =========================================================================
    
    # 1. Baseplate Assembly (Frames 0 - 25)
    if frame_idx >= 5:
        p1 = min(1.0, (frame_idx - 5) / 18.0)
        drop_y = int(H*0.62 - (1 - ease_out_bounce(p1)) * 300)
        draw_lego_brick(draw, int(W*0.28), drop_y, int(W*0.44), 30, 140, (30, 34, 46), (22, 25, 34), (16, 18, 26), 8, 4)

    # 2. Main Chassis Bricks (Frames 25 - 55)
    if frame_idx >= 25:
        p2 = min(1.0, (frame_idx - 25) / 20.0)
        drop_y = int(H*0.56 - (1 - ease_out_bounce(p2)) * 350)
        draw_lego_brick(draw, int(W*0.32), drop_y, int(W*0.36), 35, 120, (45, 52, 68), (34, 38, 50), (26, 30, 40), 6, 3)

    # 3. Technic Cross Beams (Frames 55 - 85)
    if frame_idx >= 55:
        p3 = min(1.0, (frame_idx - 55) / 20.0)
        drop_y = int(H*0.50 - (1 - ease_out_bounce(p3)) * 350)
        draw_lego_brick(draw, int(W*0.36), drop_y, int(W*0.28), 35, 100, (60, 68, 88), (48, 54, 70), (38, 42, 56), 5, 2)

    # 4. Translucent Neon Cyan Energy Core Bricks (Frames 85 - 115)
    if frame_idx >= 85:
        p4 = min(1.0, (frame_idx - 85) / 20.0)
        drop_y = int(H*0.44 - (1 - ease_out_bounce(p4)) * 400)
        draw_lego_brick(draw, int(W*0.40), drop_y, int(W*0.20), 30, 80, (56, 189, 248), (30, 140, 210), (15, 95, 160), 4, 2, glowing=True)

    # 5. Gold Wing & Exhaust Trim Bricks (Frames 115 - 145)
    if frame_idx >= 110:
        p5 = min(1.0, (frame_idx - 110) / 20.0)
        drop_y = int(H*0.46 - (1 - ease_out_bounce(p5)) * 380)
        draw_lego_brick(draw, int(W*0.35), drop_y, int(W*0.08), 25, 60, (212, 163, 89), (180, 135, 65), (140, 100, 45), 2, 2)
        draw_lego_brick(draw, int(W*0.57), drop_y, int(W*0.08), 25, 60, (212, 163, 89), (180, 135, 65), (140, 100, 45), 2, 2)

    # 6. Aerodynamic Sloped Roof Canopy & Final Snap (Frames 140 - 175)
    if frame_idx >= 135:
        p6 = min(1.0, (frame_idx - 135) / 22.0)
        drop_y = int(H*0.39 - (1 - ease_out_bounce(p6)) * 450)
        draw_lego_brick(draw, int(W*0.43), drop_y, int(W*0.14), 25, 60, (230, 235, 245), (180, 190, 205), (140, 150, 165), 3, 2)
        
        # Snap Alignment Lasers
        if p6 < 1.0:
            target_x = int(W*0.43)
            draw.line([(target_x, drop_y + 25), (target_x, int(H*0.39) + 25)], fill=(56, 189, 248), width=2)
            draw.line([(target_x + int(W*0.14), drop_y + 25), (target_x + int(W*0.14), int(H*0.39) + 25)], fill=(56, 189, 248), width=2)

    # Scattered loose precision parts on table (diminishing as they are used!)
    if frame_idx < 140:
        draw_lego_brick(draw, int(W*0.18), int(H*0.68), 70, 20, 40, (56, 189, 248), (30, 140, 210), (15, 95, 160), 2, 1, glowing=True)
    if frame_idx < 115:
        draw_lego_brick(draw, int(W*0.74), int(H*0.66), 85, 22, 50, (212, 163, 89), (180, 135, 65), (140, 100, 45), 2, 2)
    if frame_idx < 60:
        draw_lego_brick(draw, int(W*0.78), int(H*0.74), 60, 20, 35, (45, 52, 68), (34, 38, 50), (26, 30, 40), 2, 1)

    # Laser particle sparkles
    for i in range(40):
        px = int((i * 97 + frame_idx * 3) % W)
        py = int((i * 61 + frame_idx * 2) % H)
        pr = 1 + (i % 2)
        draw.ellipse([px, py, px+pr, py+pr], fill=(160, 210, 255))

    frame_path = f"scratch/lego_frames/frame_{frame_idx:04d}.png"
    img.save(frame_path)

print("Compiling frames to MP4 using FFmpeg...")
subprocess.run('ffmpeg -y -framerate 30 -i scratch/lego_frames/frame_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p -vf "scale=1920:1080" assets/lego_build_timelapse.mp4', shell=True, check=True)
print("assets/lego_build_timelapse.mp4 successfully created!")
