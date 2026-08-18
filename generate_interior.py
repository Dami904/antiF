import os
import subprocess

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)

os.makedirs("voyage/assets", exist_ok=True)

# Generate high-resolution interior viewpoints
# 1. Base interior forward view
# 2. Derive directional pan/tilt viewpoints with perspective shifts, crops, and ambient lighting

# Forward view
run_cmd('ffmpeg -y -f lavfi -i "color=c=#0d0e12:s=1920x1080" -vf "drawbox=y=ih*0.55:color=#181a22@1:t=fill,drawbox=y=ih*0.52:h=4:color=#38bdf8@0.9:t=fill,drawbox=x=iw*0.32:y=ih*0.38:w=iw*0.36:h=ih*0.28:color=#1e2230@1:t=fill,drawbox=x=iw*0.325:y=ih*0.39:w=iw*0.35:h=ih*0.26:color=#0f172a@1:t=fill,drawbox=x=iw*0.14:y=ih*0.48:w=iw*0.16:h=ih*0.1:color=#0f172a@1:t=fill,drawbox=x=iw*0.18:y=ih*0.56:w=iw*0.08:h=ih*0.35:color=#11131a@1:t=fill,drawbox=y=0:h=ih*0.35:color=#151824@0.6:t=fill" -frames:v 1 voyage/assets/int_forward.png')

# Left 45
run_cmd('ffmpeg -y -i voyage/assets/int_forward.png -vf "crop=iw*0.8:ih:0:0,scale=1920:1080,drawbox=x=0:y=ih*0.2:w=iw*0.25:h=ih*0.8:color=#101218@1:t=fill,drawbox=x=iw*0.05:y=ih*0.45:w=4:color=#38bdf8@0.8:t=fill" -frames:v 1 voyage/assets/int_left45.png')

# Left 90 (Driver Door & Window)
run_cmd('ffmpeg -y -f lavfi -i "color=c=#0c0d12:s=1920x1080" -vf "drawbox=y=ih*0.4:color=#161822@1:t=fill,drawbox=x=iw*0.2:y=ih*0.48:w=iw*0.6:h=ih*0.12:color=#222634@1:t=fill,drawbox=y=ih*0.42:h=4:color=#38bdf8@0.8:t=fill,drawbox=x=iw*0.35:y=ih*0.52:w=iw*0.15:h=ih*0.04:color=#c59d5f@1:t=fill,drawbox=y=0:h=ih*0.38:color=#1a1d2c@0.5:t=fill" -frames:v 1 voyage/assets/int_left90.png')

# Right 45
run_cmd('ffmpeg -y -i voyage/assets/int_forward.png -vf "crop=iw*0.8:ih:iw*0.2:0,scale=1920:1080,drawbox=x=iw*0.75:y=ih*0.2:w=iw*0.25:h=ih*0.8:color=#101218@1:t=fill,drawbox=x=iw*0.95:y=ih*0.45:w=4:color=#38bdf8@0.8:t=fill" -frames:v 1 voyage/assets/int_right45.png')

# Right 90 (Passenger Door & Window)
run_cmd('ffmpeg -y -i voyage/assets/int_left90.png -vf "hflip" -frames:v 1 voyage/assets/int_right90.png')

# Rear view (Back seats & panoramic roof)
run_cmd('ffmpeg -y -f lavfi -i "color=c=#0b0c10:s=1920x1080" -vf "drawbox=y=ih*0.45:color=#161822@1:t=fill,drawbox=x=iw*0.15:y=ih*0.4:w=iw*0.32:h=ih*0.45:color=#202330@1:t=fill,drawbox=x=iw*0.53:y=ih*0.4:w=iw*0.32:h=ih*0.45:color=#202330@1:t=fill,drawbox=y=ih*0.48:h=4:color=#38bdf8@0.7:t=fill,drawbox=x=iw*0.2:y=0:w=iw*0.6:h=ih*0.32:color=#1f2438@0.7:t=fill" -frames:v 1 voyage/assets/int_rear.png')

# Sunroof (Upward looking full glass roof)
run_cmd('ffmpeg -y -f lavfi -i "color=c=#08090d:s=1920x1080" -vf "drawbox=x=iw*0.1:y=ih*0.08:w=iw*0.8:h=ih*0.84:color=#1c2236@0.9:t=fill,drawbox=x=iw*0.1:y=ih*0.08:w=iw*0.8:h=ih*0.84:color=#38bdf8@0.3:t=4,drawbox=x=iw*0.495:y=ih*0.08:w=iw*0.01:h=ih*0.84:color=#0b0c10@1:t=fill" -frames:v 1 voyage/assets/int_sunroof.png')

# Console (Downward looking wireless charge & crystal dial)
run_cmd('ffmpeg -y -f lavfi -i "color=c=#101218:s=1920x1080" -vf "drawbox=x=iw*0.25:y=ih*0.1:w=iw*0.5:h=ih*0.8:color=#181b26@1:t=fill,drawbox=x=iw*0.3:y=ih*0.2:w=iw*0.18:h=ih*0.35:color=#0e1017@1:t=fill,drawbox=x=iw*0.52:y=ih*0.2:w=iw*0.18:h=ih*0.35:color=#0e1017@1:t=fill,drawbox=x=iw*0.42:y=ih*0.65:w=iw*0.16:h=ih*0.18:color=#c59d5f@0.8:t=fill,drawbox=y=ih*0.15:h=3:color=#38bdf8@0.6:t=fill" -frames:v 1 voyage/assets/int_console.png')

print("All interior frames generated successfully!")
