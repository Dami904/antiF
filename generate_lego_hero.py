import os
import math
from PIL import Image, ImageDraw, ImageFilter

os.makedirs("assets", exist_ok=True)
W, H = 1920, 1080

def create_lego_hero():
    # Base dark studio backdrop with moody spotlight
    img = Image.new("RGB", (W, H), (10, 12, 16))
    draw = ImageDraw.Draw(img)

    # Ambient radial lighting gradient
    for r in range(int(W * 0.7), 0, -10):
        intensity = int((1 - r / (W * 0.7)) * 40)
        draw.ellipse([W*0.5 - r, H*0.45 - r*0.6, W*0.5 + r, H*0.45 + r*0.6], fill=(12 + intensity, 16 + int(intensity*1.3), 26 + int(intensity*1.8)))

    # Studio table surface reflection plane
    table_y = int(H * 0.58)
    for y in range(table_y, H):
        ratio = (y - table_y) / (H - table_y)
        shade = int(8 + ratio * 12)
        draw.line([(0, y), (W, y)], fill=(shade, shade + 2, shade + 6))

    # Grid lines on building surface / cutting mat
    for x in range(0, W, 80):
        draw.line([(x, table_y), (int(W*0.5 + (x - W*0.5)*1.8), H)], fill=(25, 32, 48), width=1)
    for y in range(table_y, H, 45):
        draw.line([(0, y), (W, y)], fill=(25, 32, 48), width=1)

    # Helper to draw isometric 3D Lego brick with studs
    def draw_lego_brick(x, y, w, h, depth, color_top, color_front, color_side, studs_x=2, studs_y=4, glowing=False):
        # 1. Front face
        draw.polygon([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill=color_front)
        
        # 2. Side face (Right isometric extrusion)
        draw.polygon([(x + w, y), (x + w + depth, y - int(depth*0.5)), (x + w + depth, y + h - int(depth*0.5)), (x + w, y + h)], fill=color_side)
        
        # 3. Top face
        draw.polygon([(x, y), (x + depth, y - int(depth*0.5)), (x + w + depth, y - int(depth*0.5)), (x + w, y)], fill=color_top)
        
        # Highlight edge
        draw.line([(x, y), (x + w, y), (x + w + depth, y - int(depth*0.5))], fill=(255, 255, 255) if not glowing else (100, 220, 255), width=2 if not glowing else 3)

        # Studs on top face
        stud_r = int(w / (studs_x * 3.2))
        for sx in range(studs_x):
            for sy in range(studs_y):
                u = (sx + 0.5) / studs_x
                v = (sy + 0.5) / studs_y
                st_x = x + u * w + v * depth
                st_y = y - v * int(depth*0.5) - 6
                
                # Stud cylinder
                draw.ellipse([st_x - stud_r, st_y - int(stud_r*0.6), st_x + stud_r, st_y + int(stud_r*0.6)], fill=color_top, outline=(200, 220, 255) if glowing else (color_side), width=1)
                # Stud top highlight
                draw.ellipse([st_x - int(stud_r*0.7), st_y - int(stud_r*0.4), st_x + int(stud_r*0.7), st_y + int(stud_r*0.4)], fill=(80, 220, 255) if glowing else color_top)

    # =========================================================================
    # LAYER 1: BASEPLATE & MODULAR FOUNDATION BRICKS
    # =========================================================================
    # Large Dark Charcoal Baseplate
    draw_lego_brick(int(W*0.28), int(H*0.62), int(W*0.44), 30, 140, (30, 34, 46), (22, 25, 34), (16, 18, 26), 8, 4)

    # Layer 2: Main Chassis Bricks (Matte Obsidian & Gunmetal)
    draw_lego_brick(int(W*0.32), int(H*0.56), int(W*0.36), 35, 120, (45, 52, 68), (34, 38, 50), (26, 30, 40), 6, 3)
    
    # Layer 3: Technic Cross Beams & Structural Core
    draw_lego_brick(int(W*0.36), int(H*0.50), int(W*0.28), 35, 100, (60, 68, 88), (48, 54, 70), (38, 42, 56), 5, 2)

    # Layer 4: Translucent Neon Cyan Energy Core Bricks (Glowing)
    draw_lego_brick(int(W*0.40), int(H*0.44), int(W*0.20), 30, 80, (56, 189, 248), (30, 140, 210), (15, 95, 160), 4, 2, glowing=True)

    # Layer 5: Gold Accents & Cockpit Wings
    draw_lego_brick(int(W*0.35), int(H*0.46), int(W*0.08), 25, 60, (212, 163, 89), (180, 135, 65), (140, 100, 45), 2, 2)
    draw_lego_brick(int(W*0.57), int(H*0.46), int(W*0.08), 25, 60, (212, 163, 89), (180, 135, 65), (140, 100, 45), 2, 2)

    # Layer 6: Aerodynamic Sloped Wing Roof Bricks
    draw_lego_brick(int(W*0.43), int(H*0.39), int(W*0.14), 25, 60, (230, 235, 245), (180, 190, 205), (140, 150, 165), 3, 2)

    # =========================================================================
    # SUSPENDED "SNAP-IN" PIECE (The Assembly in Action!)
    # =========================================================================
    # Floating top brick descending into position with alignment laser glow
    float_x, float_y = int(W*0.48), int(H*0.28)
    draw_lego_brick(float_x, float_y, int(W*0.12), 25, 50, (56, 189, 248), (30, 150, 220), (20, 100, 170), 3, 1, glowing=True)
    
    # Connecting Snap Guides / Laser Projection Lines
    draw.line([(float_x, float_y + 25), (int(W*0.45), int(H*0.39))], fill=(56, 189, 248), width=2)
    draw.line([(float_x + int(W*0.12), float_y + 25), (int(W*0.55), int(H*0.39))], fill=(56, 189, 248), width=2)
    draw.line([(float_x + 50, float_y - 25), (int(W*0.50) + 50, int(H*0.34))], fill=(56, 189, 248), width=1)

    # Scattered loose precision bricks on the table (Realistic build setting!)
    draw_lego_brick(int(W*0.18), int(H*0.68), 70, 20, 40, (56, 189, 248), (30, 140, 210), (15, 95, 160), 2, 1, glowing=True)
    draw_lego_brick(int(W*0.74), int(H*0.66), 85, 22, 50, (212, 163, 89), (180, 135, 65), (140, 100, 45), 2, 2)
    draw_lego_brick(int(W*0.78), int(H*0.74), 60, 20, 35, (45, 52, 68), (34, 38, 50), (26, 30, 40), 2, 1)

    # Soft glowing ambient particles / dust
    for i in range(80):
        px = int((i * 73) % W)
        py = int((i * 47) % H)
        pr = 1 + (i % 3)
        draw.ellipse([px, py, px+pr, py+pr], fill=(180, 220, 255))

    # Apply subtle film glow filter
    glow = img.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.blend(img, glow, 0.25)

    img.save("assets/lego_build.jpg", quality=95)
    print("Cinematic Lego build hero image generated successfully!")

create_lego_hero()
