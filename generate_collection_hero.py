import subprocess
import os

def run_cmd(cmd):
    print("Running:", cmd)
    subprocess.run(cmd, shell=True, check=True)

os.makedirs("assets", exist_ok=True)

# 1. Create a 360 EV rotation clip
with open("assets/voyage_frames.txt", "w") as f:
    for loop in range(2):
        for az in [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]:
            azStr = str(az).zfill(3)
            f.write(f"file '../voyage/assets/ext_az{azStr}_el1.png'\n")
            f.write("duration 0.1\n")
    f.write("file '../voyage/assets/ext_az330_el1.png'\n")

run_cmd('ffmpeg -y -f concat -safe 0 -i assets/voyage_frames.txt -c:v libx264 -pix_fmt yuv420p -vf "scale=1920:1080,fps=30" assets/voyage_clip.mp4')

# 2. Concat the 4 hero clips (Valence, Valkyrie, Aurelia, Voyage)
with open("assets/hero_montage.txt", "w") as f:
    f.write("file '../valence/assets/hero.mp4'\n")
    f.write("file '../valkyrie/assets/hero.mp4'\n")
    f.write("file '../aurelia/assets/hero.mp4'\n")
    f.write("file 'voyage_clip.mp4'\n")

run_cmd('ffmpeg -y -f concat -safe 0 -i assets/hero_montage.txt -vf "scale=1920:1080,fps=30" -c:v libx264 -crf 20 -pix_fmt yuv420p assets/collection_hero.mp4')

print("Master Collection Hero Video Reel generated successfully!")
