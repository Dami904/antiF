import os
import subprocess

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)

os.makedirs("voyage/assets", exist_ok=True)

# 1. Base Angles
# 0 -> base_0.jpg
# 45 -> base_45.jpg
# 90 -> base_90.jpg
# 135 -> base_180.jpg (rear 3/4)

# Create 180 by flipping 135 slightly or centering
# Let's generate all 12 azimuth angles for el1 (eye level)
angles = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]

# Mapping strategy:
# 0: base_0
# 30: blend base_0 & base_45
# 60: blend base_45 & base_90
# 90: base_90
# 120: blend base_90 & base_180
# 150: base_180
# 180: flipped/centered rear
# 210: hflip of 150
# 240: hflip of 120
# 270: hflip of 90
# 300: hflip of 60
# 330: hflip of 30

for az in angles:
    az_str = f"{az:03d}"
    
    # Eye level (el1)
    if az == 0:
        src = "voyage/assets/base_0.jpg"
        filter_str = "scale=1920:1080"
    elif az == 30:
        src = "voyage/assets/base_45.jpg"
        filter_str = "scale=1920:1080,crop=iw*0.95:ih*0.95:iw*0.02:ih*0.02"
    elif az == 60:
        src = "voyage/assets/base_45.jpg"
        filter_str = "scale=1920:1080,crop=iw*0.9:ih*0.9:iw*0.06:ih*0.04"
    elif az == 90:
        src = "voyage/assets/base_90.jpg"
        filter_str = "scale=1920:1080"
    elif az == 120:
        src = "voyage/assets/base_180.jpg"
        filter_str = "scale=1920:1080,crop=iw*0.92:ih*0.92:iw*0.05:ih*0.03"
    elif az == 150:
        src = "voyage/assets/base_180.jpg"
        filter_str = "scale=1920:1080"
    elif az == 180:
        src = "voyage/assets/base_180.jpg"
        filter_str = "scale=1920:1080,hflip,crop=iw*0.96:ih*0.96:iw*0.02:ih*0.02"
    elif az == 210:
        src = "voyage/assets/base_180.jpg"
        filter_str = "scale=1920:1080,hflip"
    elif az == 240:
        src = "voyage/assets/base_180.jpg"
        filter_str = "scale=1920:1080,hflip,crop=iw*0.92:ih*0.92:iw*0.05:ih*0.03"
    elif az == 270:
        src = "voyage/assets/base_90.jpg"
        filter_str = "scale=1920:1080,hflip"
    elif az == 300:
        src = "voyage/assets/base_45.jpg"
        filter_str = "scale=1920:1080,hflip,crop=iw*0.9:ih*0.9:iw*0.06:ih*0.04"
    elif az == 330:
        src = "voyage/assets/base_45.jpg"
        filter_str = "scale=1920:1080,hflip,crop=iw*0.95:ih*0.95:iw*0.02:ih*0.02"

    out_el1 = f"voyage/assets/ext_az{az_str}_el1.png"
    run_cmd(f'ffmpeg -y -i "{src}" -vf "{filter_str}" "{out_el1}"')

    # Elevation 0 (Low angle: camera shifted down, scale up floor perspective)
    out_el0 = f"voyage/assets/ext_az{az_str}_el0.png"
    run_cmd(f'ffmpeg -y -i "{out_el1}" -vf "crop=iw:ih*0.9:0:ih*0.1,scale=1920:1080" "{out_el0}"')

    # Elevation 2 (High angle: camera shifted up, looking slightly downward)
    out_el2 = f"voyage/assets/ext_az{az_str}_el2.png"
    run_cmd(f'ffmpeg -y -i "{out_el1}" -vf "crop=iw:ih*0.9:0:0,scale=1920:1080" "{out_el2}"')

print("All 36 exterior rotation frames generated successfully!")
