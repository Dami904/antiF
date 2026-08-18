import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
                elif "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    if "GEMINI" in k.upper() or "API_KEY" in k.upper():
                        return v.strip().strip('"').strip("'")
    return None

def generate_omni_video(
    api_key: str,
    img_path: str,
    prompt: str,
    output_mp4_path: str
) -> bool:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-omni-flash-preview:generateContent"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with open(img_path, "rb") as img_f:
            b64_img = base64.b64encode(img_f.read()).decode("utf-8")
        mime = "image/jpeg" if img_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
    except Exception as e:
        print(f"Error opening image '{img_path}': {e}", file=sys.stderr)
        return False

    payload = {
        "model": "models/gemini-omni-flash-preview",
        "generation_config": {"thinking_level": "high"},
        "response_format": {"type": "video", "aspect_ratio": "16:9", "duration": "10s"},
        "input": [
            {"type": "text", "text": prompt + " Smooth continuous slow cinematic camera tracking pan across the motherboard surface and crystalline silicon die. Crisp metallic reflections, light technical aesthetic. No text, no titles, no subtitles, no overlays."},
            {"type": "image", "mime_type": mime, "data": b64_img}
        ]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
    )
    
    try:
        print("Contacting gemini-omni-flash-preview API for video synthesis...")
        with urllib.request.urlopen(req, context=ctx) as response:
            res = json.loads(response.read().decode("utf-8"))
            for step in res.get("steps", []):
                for item in step.get("content", []):
                    if item.get("type") == "video" or "video" in str(item.get("mime_type")):
                        os.makedirs(os.path.dirname(output_mp4_path) or ".", exist_ok=True)
                        with open(output_mp4_path, "wb") as f:
                            f.write(base64.b64decode(item["data"]))
                        print(f"Successfully generated video: {output_mp4_path}")
                        return True
            if "candidates" in res:
                for cand in res["candidates"]:
                    for part in cand.get("content", {}).get("parts", []):
                        if "inlineData" in part and "video" in part["inlineData"].get("mimeType", ""):
                            os.makedirs(os.path.dirname(output_mp4_path) or ".", exist_ok=True)
                            with open(output_mp4_path, "wb") as f:
                                f.write(base64.b64decode(part["inlineData"]["data"]))
                            print(f"Successfully generated video from parts: {output_mp4_path}")
                            return True
            print("Response received without video stream:", json.dumps({k: type(v).__name__ for k, v in res.items()}))
            return False
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"API HTTP Error {e.code} ({e.reason}): {error_body}", file=sys.stderr)
        return False
    except urllib.error.URLError as e:
        print(f"Network / URL Error: {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error during video generation: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    key = get_api_key()
    if not key:
        print("No GEMINI_API_KEY found in .env.", file=sys.stderr)
        sys.exit(1)
    
    prompt = "Cinematic slow glide camera shot over a high performance ceramic motherboard with exposed silicon accelerator die and gold micro traces. Ultra clean laboratory lighting, natural reflections."
    success = generate_omni_video(
        api_key=key,
        img_path="assets/hero_ref.jpg",
        prompt=prompt,
        output_mp4_path="assets/hero.mp4"
    )
    if success:
        print("Hero video generation complete!")
    else:
        print("Omni video generation could not be completed directly.")
