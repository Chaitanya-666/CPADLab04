import http.server
import socketserver
import threading
import time
import subprocess
from pathlib import Path

PORT = 8992
DIR = Path("Lab04/scripts").resolve()
OUT_DIR = Path("Lab04/images").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIR), **kwargs)
    def log_message(self, *args):
        pass

# Start Server
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
thread = threading.Thread(target=httpd.serve_forever, daemon=True)
thread.start()
print(f"HTTP Server started on 127.0.0.1:{PORT}")

SCENARIOS = [
    ("01_map_initial_view_mobile.png", "01", 414, 896),
    ("02_permission_request_dialog.png", "02", 414, 896),
    ("03_user_location_locked.png", "03", 414, 896),
    ("04_poi_marker_infowindow.png", "04", 414, 896),
    ("05_marker_bottom_detail_sheet.png", "05", 414, 896),
    ("06_recenter_fab_camera_animation.png", "06", 414, 896),
    ("07_map_type_satellite_view.png", "07", 414, 896),
    ("08_map_type_terrain_view.png", "08", 414, 896),
    ("09_tablet_portrait_overview.png", "09", 800, 1066),
    ("10_tablet_landscape_splitview.png", "10", 1200, 800),
    ("11_desktop_web_target.png", "11", 1280, 800),
    ("12_gps_disabled_fallback_snack.png", "12", 414, 896),
]

try:
    for filename, state, w, h in SCENARIOS:
        out_path = OUT_DIR / filename
        url = f"http://127.0.0.1:{PORT}/app_view.html?state={state}"
        cmd = [
            "/usr/bin/chromium",
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--window-size={w},{h}",
            "--virtual-time-budget=2500",
            f"--screenshot={str(out_path)}",
            url
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if out_path.exists():
            print(f"Captured {filename} ({w}x{h}) - {out_path.stat().st_size} bytes")
        else:
            print(f"Failed to capture {filename}: {res.stderr.decode()}")
finally:
    httpd.shutdown()
    httpd.server_close()
    print("HTTP Server stopped.")
