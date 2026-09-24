import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CODE_DIR = Path("Lab04/sourceCode")
OUT_DIR = Path("Lab04/images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

APPENDIX_FILES = [
    ("13_code_main.png", "lib/main.dart", "Entry Point & Theming (lib/main.dart)"),
    ("14_code_map_screen.png", "lib/screens/map_screen.dart", "Map Screen & State Management (lib/screens/map_screen.dart)"),
    ("15_code_location_service.png", "lib/services/location_service.dart", "Geolocation & Permission Service (lib/services/location_service.dart)"),
    ("16_code_poi_marker.png", "lib/models/poi_marker.dart", "Point of Interest Model (lib/models/poi_marker.dart)"),
    ("17_code_detail_sheet.png", "lib/widgets/marker_detail_sheet.dart", "POI Details Bottom Sheet (lib/widgets/marker_detail_sheet.dart)"),
    ("18_code_map_controls.png", "lib/widgets/map_controls.dart", "Map Controls & Layer Switcher (lib/widgets/map_controls.dart)"),
    ("19_code_android_manifest.png", "android/app/src/main/AndroidManifest.xml", "Android Manifest Permissions & API Key (AndroidManifest.xml)"),
]

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# Check fonts
if not Path(FONT_PATH).exists():
    # Search for any monospace font
    for p in Path("/usr/share/fonts").glob("**/*Mono*.ttf"):
        FONT_PATH = str(p)
        BOLD_FONT_PATH = str(p)
        break

def render_code_to_png(src_rel_path, out_name, title):
    full_path = CODE_DIR / src_rel_path
    if not full_path.exists():
        print(f"File not found: {full_path}")
        return
    text = full_path.read_text()
    lines = text.split("\n")
    MAX_LINES = 85
    if len(lines) > MAX_LINES:
        lines = lines[:MAX_LINES] + ["", f"  // ... ({len(lines) - MAX_LINES} more lines truncated for appendix; see full code in source directory) ..."]

    font_size = 13
    try:
        title_font = ImageFont.truetype(BOLD_FONT_PATH, 16)
        code_font = ImageFont.truetype(FONT_PATH, font_size)
    except Exception:
        title_font = ImageFont.load_default()
        code_font = ImageFont.load_default()

    longest = max((len(l) for l in lines), default=0)
    longest = max(longest, len(title) + 12)
    
    char_w = 8.5
    line_h = font_size + 5
    pad_x = 24
    pad_y = 20
    
    img_w = int(char_w * longest + 2 * pad_x)
    img_w = max(img_w, 900)
    img_h = int(line_h * (len(lines) + 4) + 2 * pad_y)

    img = Image.new("RGB", (img_w, img_h), color=(250, 250, 252))
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (img_w, 48)], fill=(240, 242, 248))
    draw.line([(0, 48), (img_w, 48)], fill=(210, 215, 230), width=1)
    
    # Title
    draw.text((pad_x, 14), f"Source Code: {title}", fill=(40, 45, 65), font=title_font)

    # Line numbers and Code
    curr_y = 65
    for i, line in enumerate(lines, 1):
        # Line number
        lineno_str = f"{i:3d}  "
        draw.text((pad_x, curr_y), lineno_str, fill=(160, 165, 180), font=code_font)
        # Line text
        draw.text((pad_x + 45, curr_y), line, fill=(30, 35, 45), font=code_font)
        curr_y += line_h

    # Border
    draw.rectangle([(0, 0), (img_w - 1, img_h - 1)], outline=(210, 215, 230), width=1)
    out_file = OUT_DIR / out_name
    img.save(out_file, quality=95)
    print(f"Generated {out_file} ({img_w}x{img_h})")

for out_name, src_path, title in APPENDIX_FILES:
    render_code_to_png(src_path, out_name, title)

print("All code appendix images generated successfully.")
