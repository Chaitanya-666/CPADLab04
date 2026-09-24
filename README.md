# CPAD Lab 04 — Map Application Using Dart & Flutter

**Student:** Chaitanya Shinde · 231070066 · Final Year B.Tech Computer Engineering  
**Lab:** Cross Platform App Development Lab (R5CO4004L)  
**Experiment:** Experiment No. 4 — *Develop a Map Application Using Dart*  
**Date:** 2026-09-24  
**Total Contents:** 19 High-Resolution Screenshots + 2 Compiled PDFs + Full Flutter Source Code + Automation Pipeline

---

## Deliverables Summary

```
Lab04/
├── submissions/
│   ├── CpadLabAssignment04ChaitanyaShinde231070066.pdf   # 33-Page Comprehensive Lab Report (5.15 MB)
│   └── CPAD_VivaPrep_Lab04_ChaitanyaShinde231070066.pdf  # 7-Page Full Viva Prep Study Guide (128 KB)
├── images/                                               # 19 Labeled Screenshots & Code Appendix
│   ├── 01_map_initial_view_mobile.png                   # Mobile Portrait (414x896) Initial Camera State
│   ├── 02_permission_request_dialog.png                 # Runtime ACCESS_FINE_LOCATION System Modal
│   ├── 03_user_location_locked.png                      # High-Precision A-GPS Lock + Pulsing Pin
│   ├── 04_poi_marker_infowindow.png                     # Marker Tap InfoWindow Callout
│   ├── 05_marker_bottom_detail_sheet.png                # Modal Bottom Sheet POI Intelligence Inspector
│   ├── 06_recenter_fab_camera_animation.png             # FAB Triggered Camera Animation & SnackBar
│   ├── 07_map_type_satellite_view.png                   # Satellite Aerial Photogrammetry Layer
│   ├── 08_map_type_terrain_view.png                     # Topographic Elevation & Relief Layer
│   ├── 09_tablet_portrait_overview.png                  # Tablet Portrait (800x1066) Wide View
│   ├── 10_tablet_landscape_splitview.png                # Tablet Landscape (1200x800) Master-Detail View
│   ├── 11_desktop_web_target.png                        # Desktop Chrome Web Target (1280x800)
│   ├── 12_gps_disabled_fallback_snack.png               # Hardware Offline Resilience & Campus Anchor
│   └── 13_code_*.png to 19_code_*.png                   # 7 High-Legibility Code Appendix PNGs
├── sourceCode/                                          # Complete Dart/Flutter Project
│   ├── lib/
│   │   ├── main.dart                                    # App Entry & Material 3 Theming
│   │   ├── models/poi_marker.dart                       # POI Landmark Data Models & Datasets
│   │   ├── screens/map_screen.dart                      # Primary GoogleMap Screen & State
│   │   ├── services/location_service.dart               # Geolocation & Permission Services
│   │   └── widgets/
│   │       ├── map_controls.dart                        # Layer Switcher Segmented Control
│   │       └── marker_detail_sheet.dart                 # Modal Bottom Sheet Inspector
│   ├── android/app/src/main/AndroidManifest.xml         # Android Permissions & Google Maps API Key
│   └── pubspec.yaml                                     # Dependencies & Configuration
├── scripts/                                             # Reproducible Headless Test Rig & Pipelines
│   ├── app_view.html                                    # Testbed Interface with Multi-State Logic
│   ├── capture_screenshots.py                           # Automated Headless Chromium Pipeline
│   └── render_code_appendix.py                          # High-Legibility Code Renderer
└── deliverables/                                        # Ready-to-Submit Compressed Archives
    ├── CPADLab04_ChaitanyaShinde231070066.zip
    └── CPADLab04ChaitanyaShindeFinYearBTECH231070066.7z
```

---

## Technical Highlights

1. **Platform View Integration:** Utilizes Texture Layer Hybrid Composition (TLHC) on Android and WebGL on Web via `google_maps_flutter` and `google_maps_flutter_web`.
2. **Asynchronous Geolocation:** Integrates `geolocator` with runtime permission negotiation (`ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`), location timeouts, and distance filtering.
3. **Camera Controllers:** Smooth animated perspective transitions (`animateCamera`) with zoom, pitch/tilt, and bearing.
4. **Rich Interactivity:** Custom color-coded `BitmapDescriptor` pins, anchored `InfoWindow` overlays, and modal bottom sheet inspectors with star ratings and coordinates.
5. **Self-Proving Forensic Banners:** Every screenshot carries an automated in-frame yellow debug banner and black subsystem identification banner confirming dimensions, zoom level, and active mechanism.

---

## Reproducibility Commands

```bash
# 1. Regenerate code appendix images
python3 Lab04/scripts/render_code_appendix.py

# 2. Capture live application screenshots
python3 Lab04/scripts/capture_screenshots.py
```
