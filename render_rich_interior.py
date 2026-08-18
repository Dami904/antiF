import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs("voyage/assets", exist_ok=True)
W, H = 1920, 1080

def create_base_canvas():
    # Subtle studio dark atmospheric background
    img = Image.new("RGB", (W, H), (14, 16, 22))
    draw = ImageDraw.Draw(img)
    
    # Windshield / outdoor view gradient
    for y in range(0, int(H * 0.45)):
        ratio = y / (H * 0.45)
        r = int(18 + ratio * 8)
        g = int(22 + ratio * 10)
        b = int(32 + ratio * 15)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    return img, draw

# =========================================================================
# 1. FORWARD INTERIOR (Full Luxury Cockpit View)
# =========================================================================
def render_interior_forward():
    img, draw = create_base_canvas()

    # Horizon road reflection through windshield
    draw.polygon([(W*0.2, H*0.42), (W*0.8, H*0.42), (W*0.9, H*0.1), (W*0.1, H*0.1)], fill=(24, 28, 38))
    # A-Pillars
    draw.polygon([(0, 0), (W*0.12, 0), (W*0.06, H*0.5), (0, H*0.5)], fill=(18, 20, 26))
    draw.polygon([(W, 0), (W*0.88, 0), (W*0.94, H*0.5), (W, H*0.5)], fill=(18, 20, 26))

    # Main Sweeping Leather Dashboard (Layered)
    draw.polygon([(0, H*0.46), (W, H*0.46), (W, H), (0, H)], fill=(20, 22, 30))
    # Open-pore dark wood trim strip
    draw.polygon([(W*0.05, H*0.48), (W*0.95, H*0.48), (W*0.95, H*0.53), (W*0.05, H*0.53)], fill=(32, 28, 24))
    
    # Ambient Light Strip (Vibrant Cyan / Teal LED Bar)
    for i in range(4):
        alpha_color = (56, 189, 248)
        draw.line([(W*0.05, H*0.478 + i), (W*0.95, H*0.478 + i)], fill=alpha_color, width=1)
    
    # Air Vents Line
    draw.line([(W*0.08, H*0.525), (W*0.92, H*0.525)], fill=(45, 50, 65), width=3)

    # 1. Center Floating 15.6-inch OLED Screen (3D Bevel)
    cx, cy, cw, ch = int(W*0.38), int(H*0.32), int(W*0.32), int(H*0.32)
    # Screen chassis / aluminum bezel
    draw.rounded_rectangle([cx-6, cy-6, cx+cw+6, cy+ch+6], radius=14, fill=(35, 40, 52), outline=(70, 80, 100), width=2)
    # Screen Glass Active Area
    draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=10, fill=(10, 14, 22))
    
    # Screen UI: Map Navigation on Left
    draw.rounded_rectangle([cx+12, cy+12, cx+int(cw*0.58), cy+ch-12], radius=8, fill=(18, 24, 38))
    # Simulated GPS route line
    draw.line([(cx+30, cy+ch-30), (cx+80, cy+100), (cx+180, cy+60), (cx+260, cy+40)], fill=(56, 189, 248), width=4)
    draw.ellipse([cx+76, cy+96, cx+84, cy+104], fill=(255, 255, 255))
    draw.text((cx+30, cy+25), "NAVIGATION // SHANGHAI AUTOPILOT", fill=(180, 200, 230))

    # Screen UI: Media & EV Telemetry on Right
    draw.rounded_rectangle([cx+int(cw*0.62), cy+12, cx+cw-12, cy+int(ch*0.52)], radius=8, fill=(16, 20, 30))
    draw.text((cx+int(cw*0.65), cy+25), "84% // 608 KM", fill=(52, 211, 153))
    draw.text((cx+int(cw*0.65), cy+50), "VOYAGE SOUNDSTREAM", fill=(140, 150, 175))
    draw.text((cx+int(cw*0.65), cy+75), "Spatial Audio 7.1.4", fill=(212, 163, 89))
    
    # Screen Climate Bar at bottom
    draw.rounded_rectangle([cx+int(cw*0.62), cy+int(ch*0.56), cx+cw-12, cy+ch-12], radius=8, fill=(16, 20, 30))
    draw.text((cx+int(cw*0.65), cy+int(ch*0.66)), "CLIMATE 21.5°C AUTO", fill=(220, 230, 245))

    # 2. Driver 10.25-inch Digital Cluster
    dx, dy, dw, dh = int(W*0.14), int(H*0.42), int(W*0.16), int(H*0.12)
    draw.rounded_rectangle([dx-4, dy-4, dx+dw+4, dy+dh+4], radius=8, fill=(28, 32, 42), outline=(50, 60, 80), width=1)
    draw.rounded_rectangle([dx, dy, dx+dw, dy+dh], radius=6, fill=(8, 10, 16))
    draw.text((dx+20, dy+15), "108 KM/H", fill=(255, 255, 255))
    draw.text((dx+20, dy+45), "PILOT ASSIST ACTIVE", fill=(56, 189, 248))
    draw.text((dx+20, dy+75), "PWR 24 kW  |  BAT 84%", fill=(140, 150, 175))

    # 3. Two-Spoke Capacitive Steering Wheel (Detailed)
    sx, sy, sr = int(W*0.22), int(H*0.75), int(W*0.13)
    # Outer Ring
    draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], outline=(24, 26, 34), width=32)
    draw.ellipse([sx-sr+8, sy-sr+8, sx+sr-8, sy+sr-8], outline=(40, 44, 56), width=4)
    # Center Hub & Spokes
    draw.rounded_rectangle([sx-int(sr*0.6), sy-int(sr*0.25), sx+int(sr*0.6), sy+int(sr*0.25)], radius=12, fill=(22, 24, 32), outline=(60, 65, 80), width=2)
    draw.ellipse([sx-14, sy-14, sx+14, sy+14], fill=(56, 189, 248))
    draw.text((sx-38, sy+25), "VOYAGE", fill=(200, 210, 230))
    # Left/Right capacitive touch buttons
    draw.rounded_rectangle([sx-int(sr*0.52), sy-10, sx-int(sr*0.25), sy+10], radius=4, fill=(35, 40, 52))
    draw.rounded_rectangle([sx+int(sr*0.25), sy-10, sx+int(sr*0.52), sy+10], radius=4, fill=(35, 40, 52))

    # 4. Center Console (Bottom Center)
    draw.polygon([(W*0.36, H*0.68), (W*0.64, H*0.68), (W*0.72, H), (W*0.28, H)], fill=(22, 25, 34))
    # Dual 50W wireless charging pads
    draw.rounded_rectangle([W*0.42, H*0.74, W*0.48, H*0.88], radius=8, fill=(14, 16, 22), outline=(45, 50, 65), width=2)
    draw.rounded_rectangle([W*0.52, H*0.74, W*0.58, H*0.88], radius=8, fill=(14, 16, 22), outline=(45, 50, 65), width=2)
    draw.text((W*0.43, H*0.80), "50W Qi", fill=(80, 90, 110))
    draw.text((W*0.53, H*0.80), "50W Qi", fill=(80, 90, 110))
    # Crystal rotary gear dial
    draw.ellipse([W*0.47, H*0.91, W*0.53, H*0.99], fill=(212, 163, 89), outline=(255, 255, 255), width=2)

    # 5. Front Passenger Seat (Right)
    draw.polygon([(W*0.75, H*0.55), (W*0.96, H*0.65), (W*0.98, H), (W*0.68, H)], fill=(26, 29, 38))
    # Headrest
    draw.rounded_rectangle([W*0.78, H*0.45, W*0.88, H*0.56], radius=14, fill=(28, 32, 42), outline=(50, 55, 70), width=2)

    img.save("voyage/assets/int_forward.png")

# =========================================================================
# 2. INTERIOR LEFT 45° (Driver Door & Mirror View)
# =========================================================================
def render_interior_left45():
    img, draw = create_base_canvas()
    
    # Left Door Window
    draw.polygon([(0, H*0.1), (W*0.55, H*0.18), (W*0.5, H*0.48), (0, H*0.48)], fill=(22, 26, 36))
    # Mirror Camera Display
    draw.rounded_rectangle([W*0.46, H*0.38, W*0.54, H*0.48], radius=6, fill=(10, 14, 20), outline=(56, 189, 248), width=2)
    draw.text((W*0.47, H*0.42), "DIGITAL MIRROR", fill=(56, 189, 248))

    # Driver Door Panel Structure
    draw.polygon([(0, H*0.48), (W*0.58, H*0.48), (W*0.65, H), (0, H)], fill=(22, 25, 34))
    # Ambient Light Strip along door
    draw.line([(0, H*0.51), (W*0.55, H*0.51)], fill=(56, 189, 248), width=3)
    # Perforated Speaker Grille
    draw.ellipse([W*0.15, H*0.68, W*0.35, H*0.88], outline=(60, 68, 85), width=3)
    draw.text((W*0.20, H*0.77), "DOLBY ATMOS 7.1.4", fill=(140, 150, 175))
    # Seat adjustment controls on door
    draw.rounded_rectangle([W*0.35, H*0.54, W*0.48, H*0.60], radius=4, fill=(35, 40, 52))
    draw.text((W*0.37, H*0.56), "MEMORY 1 2 3", fill=(200, 210, 230))

    # Steering Wheel partially in view on right
    sx, sy, sr = int(W*0.85), int(H*0.75), int(W*0.18)
    draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], outline=(24, 26, 34), width=36)
    
    img.save("voyage/assets/int_left45.png")

# =========================================================================
# 3. INTERIOR LEFT 90° (Pure Driver Side Window)
# =========================================================================
def render_interior_left90():
    img, draw = create_base_canvas()
    
    # Large Frameless Acoustic Glass Window
    draw.polygon([(W*0.08, H*0.1), (W*0.92, H*0.1), (W*0.88, H*0.52), (W*0.12, H*0.52)], fill=(20, 24, 34))
    # B-Pillar
    draw.polygon([(W*0.88, 0), (W*0.96, 0), (W*0.96, H), (W*0.88, H)], fill=(16, 18, 24))
    
    # Lower Door Armrest
    draw.polygon([(0, H*0.52), (W, H*0.52), (W, H), (0, H)], fill=(22, 25, 34))
    draw.line([(W*0.05, H*0.54), (W*0.95, H*0.54)], fill=(56, 189, 248), width=3)
    # Power window switches & handle
    draw.rounded_rectangle([W*0.35, H*0.62, W*0.65, H*0.72], radius=8, fill=(32, 36, 48), outline=(60, 70, 90), width=1)
    draw.text((W*0.42, H*0.66), "POWER WINDOWS // LOCK", fill=(180, 190, 210))

    img.save("voyage/assets/int_left90.png")

# =========================================================================
# 4. INTERIOR RIGHT 45° (Passenger Side View)
# =========================================================================
def render_interior_right45():
    # Mirror of left45 with passenger dashboard adjustments
    img = Image.open("voyage/assets/int_left45.png").transpose(Image.FLIP_LEFT_RIGHT)
    img.save("voyage/assets/int_right45.png")

# =========================================================================
# 5. INTERIOR RIGHT 90° (Passenger Door View)
# =========================================================================
def render_interior_right90():
    img = Image.open("voyage/assets/int_left90.png").transpose(Image.FLIP_LEFT_RIGHT)
    img.save("voyage/assets/int_right90.png")

# =========================================================================
# 6. INTERIOR REAR (Back Seats & Panoramic Canopy)
# =========================================================================
def render_interior_rear():
    img, draw = create_base_canvas()
    
    # Panoramic Rear Windshield
    draw.polygon([(W*0.25, H*0.15), (W*0.75, H*0.15), (W*0.85, H*0.45), (W*0.15, H*0.45)], fill=(22, 26, 36))
    
    # Rear Lounge Seats (Executive 3-Seat Bench)
    # Left Rear Seat
    draw.rounded_rectangle([W*0.14, H*0.42, W*0.42, H*0.95], radius=16, fill=(26, 29, 38), outline=(48, 54, 70), width=2)
    draw.rounded_rectangle([W*0.22, H*0.32, W*0.34, H*0.44], radius=12, fill=(30, 34, 44))
    # Right Rear Seat
    draw.rounded_rectangle([W*0.58, H*0.42, W*0.86, H*0.95], radius=16, fill=(26, 29, 38), outline=(48, 54, 70), width=2)
    draw.rounded_rectangle([W*0.66, H*0.32, W*0.78, H*0.44], radius=12, fill=(30, 34, 44))
    
    # Center Armrest with Touch Controls
    draw.rounded_rectangle([W*0.44, H*0.52, W*0.56, H*0.95], radius=8, fill=(20, 22, 30), outline=(56, 189, 248), width=1)
    draw.text((W*0.46, H*0.62), "REAR HVAC\n22.0°C", fill=(56, 189, 248))

    # Ambient Light running across roofline
    draw.line([(W*0.1, H*0.12), (W*0.9, H*0.12)], fill=(56, 189, 248), width=3)
    
    img.save("voyage/assets/int_rear.png")

# =========================================================================
# 7. INTERIOR SUNROOF (Upward Panoramic Glass View)
# =========================================================================
def render_interior_sunroof():
    img = Image.new("RGB", (W, H), (12, 14, 20))
    draw = ImageDraw.Draw(img)
    
    # Massive 2.1m² Glass Roof Frame
    draw.rounded_rectangle([W*0.12, H*0.08, W*0.88, H*0.92], radius=24, fill=(18, 24, 38), outline=(40, 48, 65), width=6)
    
    # Electrochromic tint starlight glow
    for i in range(120):
        sx = int(W*0.15 + (i * 37) % int(W*0.7))
        sy = int(H*0.12 + (i * 53) % int(H*0.75))
        draw.ellipse([sx, sy, sx+2, sy+2], fill=(200, 230, 255))

    # Ambient LED Contour Halo
    draw.rounded_rectangle([W*0.13, H*0.09, W*0.87, H*0.91], radius=20, outline=(56, 189, 248), width=2)
    draw.text((W*0.42, H*0.48), "2.1 m² ELECTROCHROMIC GLASS", fill=(212, 163, 89))
    draw.text((W*0.44, H*0.52), "99.9% UV REJECTION", fill=(140, 150, 175))

    img.save("voyage/assets/int_sunroof.png")

# =========================================================================
# 8. INTERIOR CONSOLE (Downward View)
# =========================================================================
def render_interior_console():
    img = Image.new("RGB", (W, H), (16, 18, 25))
    draw = ImageDraw.Draw(img)
    
    # Center Tunnel Leather Console
    draw.polygon([(W*0.22, 0), (W*0.78, 0), (W*0.86, H), (W*0.14, H)], fill=(22, 26, 36))
    
    # Dual 50W Fast Wireless Charging Pads
    draw.rounded_rectangle([W*0.28, H*0.12, W*0.48, H*0.48], radius=14, fill=(14, 16, 22), outline=(56, 189, 248), width=2)
    draw.rounded_rectangle([W*0.52, H*0.12, W*0.72, H*0.48], radius=14, fill=(14, 16, 22), outline=(56, 189, 248), width=2)
    draw.text((W*0.34, H*0.28), "WIRELESS 50W (AIR COOLED)", fill=(56, 189, 248))
    draw.text((W*0.58, H*0.28), "WIRELESS 50W (AIR COOLED)", fill=(56, 189, 248))
    
    # Handcrafted Diamond-Cut Crystal Gear Selector
    cx, cy, cr = int(W*0.5), int(H*0.68), 65
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(212, 163, 89), outline=(255, 255, 255), width=3)
    draw.text((cx-28, cy-10), "PRND", fill=(10, 12, 16))
    
    # Dual Cupholders with sliding cover
    draw.ellipse([W*0.32, H*0.75, W*0.42, H*0.92], outline=(50, 58, 75), width=3)
    draw.ellipse([W*0.58, H*0.75, W*0.68, H*0.92], outline=(50, 58, 75), width=3)

    img.save("voyage/assets/int_console.png")

print("Rendering all 8 luxury interior viewpoints...")
render_interior_forward()
render_interior_left45()
render_interior_left90()
render_interior_right45()
render_interior_right90()
render_interior_rear()
render_interior_sunroof()
render_interior_console()
print("All 8 rich luxury interior frames successfully generated!")
