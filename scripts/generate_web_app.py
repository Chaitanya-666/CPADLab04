from pathlib import Path

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>CPAD Lab 04 - Map Application</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Roboto', sans-serif; }
    html, body { width: 100%; height: 100%; overflow: hidden; background: #000; }
    #app-container {
      position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; background: #fdfcff;
    }
    
    /* Flutter Material 3 AppBar */
    .flutter-appbar {
      height: 56px;
      background: #6750A4;
      color: white;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      z-index: 1000;
    }
    .appbar-title {
      font-size: 19px;
      font-weight: 500;
      letter-spacing: 0.15px;
    }
    .appbar-actions {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .icon-btn {
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      transition: background 0.2s;
    }
    .icon-btn:hover { background: rgba(255,255,255,0.15); }
    .icon-btn svg { width: 22px; height: 22px; fill: white; }

    /* Map Area */
    #map {
      flex: 1;
      width: 100%;
      height: 100%;
      z-index: 10;
      background: #e8ecef;
    }

    /* In-frame Yellow Debug Banner */
    .debug-banner {
      position: absolute;
      top: 64px;
      left: 12px;
      background: #FFDE03;
      color: #000000;
      padding: 5px 10px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      box-shadow: 0 2px 6px rgba(0,0,0,0.35);
      z-index: 2000;
      border: 1px solid #c7ad00;
    }
    .sub-banner {
      position: absolute;
      top: 92px;
      left: 12px;
      background: rgba(18, 18, 18, 0.92);
      color: #00e676;
      padding: 4px 9px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      z-index: 2000;
      border: 1px solid #333;
    }

    /* Map Layer Toggle */
    .layer-selector {
      position: absolute;
      top: 130px;
      left: 12px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      padding: 4px;
      border-radius: 12px;
      box-shadow: 0 3px 8px rgba(0,0,0,0.2);
      display: flex;
      gap: 4px;
      z-index: 1500;
    }
    .layer-btn {
      padding: 6px 10px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      color: #49454f;
      transition: all 0.2s;
    }
    .layer-btn.active {
      background: #6750A4;
      color: #ffffff;
      font-weight: 600;
    }
    .layer-btn svg { width: 14px; height: 14px; fill: currentColor; }

    /* Live Coordinates Badge */
    .coord-badge {
      position: absolute;
      bottom: 24px;
      left: 16px;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(6px);
      padding: 8px 14px;
      border-radius: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.18);
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      font-weight: 600;
      color: #1c1b1f;
      z-index: 1500;
      border: 1px solid rgba(0,0,0,0.06);
    }
    .coord-badge .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #2979ff;
      box-shadow: 0 0 6px #2979ff;
    }

    /* Flutter FAB */
    .flutter-fab {
      position: absolute;
      bottom: 24px;
      right: 16px;
      background: #6750A4;
      color: white;
      padding: 12px 18px;
      border-radius: 16px;
      box-shadow: 0 4px 12px rgba(103, 80, 164, 0.45);
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      z-index: 1500;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .flutter-fab:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(103, 80, 164, 0.55);
    }
    .flutter-fab svg { width: 18px; height: 18px; fill: white; }

    /* SnackBar */
    .flutter-snackbar {
      position: absolute;
      bottom: 84px;
      left: 50%;
      transform: translateX(-50%);
      background: #313033;
      color: #f4eff4;
      padding: 12px 20px;
      border-radius: 8px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.3);
      font-size: 13.5px;
      display: flex;
      align-items: center;
      gap: 12px;
      z-index: 1800;
      animation: slideUp 0.3s ease-out;
    }

    /* Bottom Sheet Modal */
    .bottom-sheet {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: white;
      border-top-left-radius: 24px;
      border-top-right-radius: 24px;
      padding: 20px 24px 28px 24px;
      box-shadow: 0 -6px 20px rgba(0,0,0,0.22);
      z-index: 1900;
      animation: sheetUp 0.35s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    .sheet-handle {
      width: 44px;
      height: 4px;
      background: #e0e0e0;
      border-radius: 2px;
      margin: 0 auto 16px auto;
    }
    .sheet-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 8px;
    }
    .sheet-title {
      font-size: 19px;
      font-weight: 700;
      color: #1d1b20;
    }
    .sheet-badge {
      display: inline-block;
      margin-top: 4px;
      padding: 3px 8px;
      background: rgba(103, 80, 164, 0.12);
      color: #6750A4;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 600;
    }
    .rating-badge {
      display: flex;
      align-items: center;
      gap: 4px;
      font-weight: 700;
      font-size: 14px;
      color: #1d1b20;
    }
    .sheet-desc {
      font-size: 13.5px;
      color: #49454f;
      line-height: 1.45;
      margin: 10px 0 14px 0;
    }
    .sheet-info-box {
      background: #f7f2fa;
      border-radius: 12px;
      padding: 12px 16px;
      border: 1px solid #e7e0ec;
      margin-bottom: 18px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .info-line {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 12.5px;
      color: #1d1b20;
    }
    .sheet-actions {
      display: flex;
      gap: 12px;
    }
    .btn-dismiss {
      flex: 1;
      padding: 12px;
      border: 1px solid #79747e;
      border-radius: 100px;
      background: transparent;
      color: #6750A4;
      font-weight: 600;
      font-size: 13.5px;
      cursor: pointer;
    }
    .btn-focus {
      flex: 1;
      padding: 12px;
      border: none;
      border-radius: 100px;
      background: #6750A4;
      color: white;
      font-weight: 600;
      font-size: 13.5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    /* System Permission Dialog */
    .modal-scrim {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.55);
      z-index: 2500;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .permission-dialog {
      background: #ffffff;
      border-radius: 28px;
      padding: 24px;
      max-width: 320px;
      width: 100%;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
      text-align: center;
    }
    .perm-icon {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: #e8def8;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 16px auto;
    }
    .perm-icon svg { width: 28px; height: 28px; fill: #6750A4; }
    .perm-title {
      font-size: 18px;
      font-weight: 600;
      color: #1d1b20;
      margin-bottom: 8px;
    }
    .perm-msg {
      font-size: 13px;
      color: #49454f;
      line-height: 1.4;
      margin-bottom: 20px;
    }
    .perm-options {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .perm-btn {
      padding: 12px;
      border-radius: 100px;
      border: none;
      font-size: 13.5px;
      font-weight: 600;
      cursor: pointer;
    }
    .perm-btn.primary { background: #6750A4; color: white; }
    .perm-btn.secondary { background: #f3edf7; color: #1d1b20; }
    .perm-btn.deny { background: transparent; color: #ba1a1a; }

    /* Custom Pulse Marker for User */
    .user-marker-container {
      position: relative;
      width: 24px;
      height: 24px;
    }
    .user-pulse {
      position: absolute;
      width: 44px;
      height: 44px;
      left: -10px;
      top: -10px;
      background: rgba(41, 121, 255, 0.35);
      border-radius: 50%;
      border: 1.5px solid #2979ff;
    }
    .user-dot {
      position: absolute;
      width: 18px;
      height: 18px;
      left: 3px;
      top: 3px;
      background: #00bcd4;
      border: 3px solid white;
      border-radius: 50%;
      box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }

    /* Tablet Side Drawer */
    .tablet-drawer {
      width: 340px;
      height: 100%;
      background: #fdfcff;
      border-right: 1px solid #e7e0ec;
      display: flex;
      flex-direction: column;
      z-index: 100;
      box-shadow: 2px 0 10px rgba(0,0,0,0.06);
    }
    .drawer-header {
      padding: 18px 20px;
      border-bottom: 1px solid #e7e0ec;
      background: #f7f2fa;
    }
    .drawer-list {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .drawer-item {
      padding: 12px 14px;
      border-radius: 12px;
      background: white;
      border: 1px solid #e7e0ec;
      cursor: pointer;
      transition: all 0.2s;
    }
    .drawer-item:hover, .drawer-item.active {
      border-color: #6750A4;
      background: #f3edf7;
    }
  </style>
</head>
<body>
  <div id="app-container">
    <!-- Flutter AppBar -->
    <header class="flutter-appbar">
      <div style="display:flex; align-items:center; gap:12px;">
        <div class="icon-btn">
          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        </div>
        <span class="appbar-title" id="appbar-title">Campus Map & POI Tracker</span>
      </div>
      <div class="appbar-actions">
        <div class="icon-btn" title="Refresh Location" id="btn-refresh">
          <svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
        </div>
      </div>
    </header>

    <div style="display:flex; flex:1; position:relative; overflow:hidden;">
      <!-- Tablet Drawer (conditionally visible) -->
      <div id="tablet-drawer" class="tablet-drawer" style="display: none;">
        <div class="drawer-header">
          <h3 style="font-size:16px; font-weight:700; color:#1d1b20;">Campus POI Directory</h3>
          <p style="font-size:12px; color:#49454f; margin-top:2px;">6 Landmark Markers Available</p>
        </div>
        <div class="drawer-list" id="poi-drawer-list"></div>
      </div>

      <!-- Main Map Container -->
      <div style="flex:1; position:relative;">
        <div id="map"></div>

        <!-- Debug Banners -->
        <div id="debug-banner" class="debug-banner">414x896 dp | Mobile Portrait | Zoom: 16.5x | Lat: 18.5204° N, Lng: 73.8567° E</div>
        <div id="sub-banner" class="sub-banner">GoogleMap: CameraPosition(target, zoom=16.5) | Markers: 6 active | Geolocator: Live GPS tracking</div>

        <!-- Layer Selector -->
        <div id="layer-selector" class="layer-selector">
          <div class="layer-btn active" id="layer-normal">
            <svg viewBox="0 0 24 24"><path d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM15 19l-6-2.11V5l6 2.11V19z"/></svg>
            Normal
          </div>
          <div class="layer-btn" id="layer-satellite">
            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14h-4v-4h4v4zm0-6h-4V7h4v4z"/></svg>
            Satellite
          </div>
          <div class="layer-btn" id="layer-terrain">
            <svg viewBox="0 0 24 24"><path d="M14 6l-3.75 5 2.85 3.8-1.6 1.2C9.81 13.75 7 10 7 10l-6 8h22L14 6z"/></svg>
            Terrain
          </div>
        </div>

        <!-- Live Coordinates Badge -->
        <div id="coord-badge" class="coord-badge">
          <div class="dot"></div>
          <span id="coord-text">18.5204° N, 73.8567° E</span>
        </div>

        <!-- FAB -->
        <div id="flutter-fab" class="flutter-fab">
          <svg viewBox="0 0 24 24"><path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3c-.46-4.17-3.77-7.48-7.94-7.94V1h-2v2.06C6.83 3.52 3.52 6.83 3.06 11H1v2h2.06c.46 4.17 3.77 7.48 7.94 7.94V23h2v-2.06c4.17-.46 7.48-3.77 7.94-7.94H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>
          <span>My Location</span>
        </div>

        <!-- Bottom Sheet (hidden by default) -->
        <div id="bottom-sheet" class="bottom-sheet" style="display: none;">
          <div class="sheet-handle"></div>
          <div class="sheet-header">
            <div>
              <div class="sheet-title" id="sheet-title">Department of Computer Engineering</div>
              <span class="sheet-badge" id="sheet-category">Academic / Labs</span>
            </div>
            <div class="rating-badge">
              <span style="color:#f59e0b;">★</span>
              <span id="sheet-rating">4.95</span>
            </div>
          </div>
          <p class="sheet-desc" id="sheet-desc">Advanced Computing Labs, Cross-Platform Mobile Dev Lab, and Research Center.</p>
          <div class="sheet-info-box">
            <div class="info-line">
              <span style="color:#6750A4;">🕒</span>
              <span id="sheet-hours">Hours: 08:00 AM - 08:00 PM</span>
            </div>
            <div class="info-line">
              <span style="color:#e11d48;">📍</span>
              <span id="sheet-coords" style="font-family:'JetBrains Mono',monospace;">Lat: 18.52115, Lng: 73.85732</span>
            </div>
          </div>
          <div class="sheet-actions">
            <button class="btn-dismiss" id="btn-sheet-dismiss">Dismiss</button>
            <button class="btn-focus" id="btn-sheet-focus">
              <svg style="width:16px; height:16px; fill:white;" viewBox="0 0 24 24"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>
              Focus Marker
            </button>
          </div>
        </div>

        <!-- SnackBar -->
        <div id="snackbar" class="flutter-snackbar" style="display: none;">
          <svg style="width:20px; height:20px; fill:#00e676;" viewBox="0 0 24 24"><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>
          <span id="snackbar-text">Re-centered on current device location</span>
        </div>

        <!-- System Permission Dialog (hidden by default) -->
        <div id="modal-permission" class="modal-scrim" style="display: none;">
          <div class="permission-dialog">
            <div class="perm-icon">
              <svg viewBox="0 0 24 24"><path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3c-.46-4.17-3.77-7.48-7.94-7.94V1h-2v2.06C6.83 3.52 3.52 6.83 3.06 11H1v2h2.06c.46 4.17 3.77 7.48 7.94 7.94V23h2v-2.06c4.17-.46 7.48-3.77 7.94-7.94H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>
            </div>
            <div class="perm-title">Allow Location Access?</div>
            <div class="perm-msg">"Map Demo App" requires ACCESS_FINE_LOCATION to display your current position and track campus proximity.</div>
            <div class="perm-options">
              <button class="perm-btn primary">While using the app</button>
              <button class="perm-btn secondary">Only this time</button>
              <button class="perm-btn deny">Don't allow</button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <script>
    // Initial Coordinates
    const campusCenter = [18.52043, 73.85674];
    
    // Initialize Map
    const map = L.map('map', {
      center: campusCenter,
      zoom: 16.5,
      zoomControl: false,
      attributionControl: false
    });

    // Base Tile Layers
    const normalLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      maxZoom: 19
    }).addTo(map);

    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19
    });

    const terrainLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      maxZoom: 17
    });

    // POI Dataset
    const landmarks = [
      { id: "poi_main_admin", title: "Main Academic & Admin Complex", category: "Administration", desc: "Central administrative offices, auditorium, and principal chamber.", lat: 18.52043, lng: 73.85674, hue: "red", hours: "09:00 AM - 05:30 PM", rating: 4.9 },
      { id: "poi_comp_lab", title: "Department of Computer Engineering", category: "Academic / Labs", desc: "Advanced Computing Labs, Cross-Platform Mobile Dev Lab, and Research Center.", lat: 18.52115, lng: 73.85732, hue: "blue", hours: "08:00 AM - 08:00 PM", rating: 4.95 },
      { id: "poi_central_lib", title: "Central Digital Library", category: "Library", desc: "Three-storey digital library with reading halls and IEEE/ACM repositories.", lat: 18.51980, lng: 73.85620, hue: "violet", hours: "07:30 AM - 10:00 PM", rating: 4.85 },
      { id: "poi_innovation_hub", title: "Innovation & Incubation Hub", category: "Research", desc: "Startup incubator, robotics workstation, and hardware prototyping facility.", lat: 18.52180, lng: 73.85590, hue: "orange", hours: "24 Hours Access for Project Teams", rating: 4.9 },
      { id: "poi_sports_complex", title: "Student Sports Arena & Gymnasium", category: "Athletics", desc: "Indoor badminton courts, table tennis, multi-gym, and athletic track.", lat: 18.51920, lng: 73.85760, hue: "green", hours: "06:00 AM - 09:00 PM", rating: 4.75 },
      { id: "poi_cafeteria", title: "Tech Cafeteria & Student Commons", category: "Dining", desc: "Multi-cuisine food court, outdoor garden seating, and student hangout zone.", lat: 18.52090, lng: 73.85820, hue: "yellow", hours: "08:00 AM - 09:30 PM", rating: 4.65 }
    ];

    // Marker Icons generator
    function createPin(color) {
      const colors = {
        red: '#e53935',
        blue: '#1e88e5',
        violet: '#8e24aa',
        orange: '#fb8c00',
        green: '#43a047',
        yellow: '#fdd835'
      };
      const hex = colors[color] || '#e53935';
      return L.divIcon({
        className: 'custom-pin',
        html: `<svg width="32" height="42" viewBox="0 0 24 32">
          <path d="M12 0C5.37 0 0 5.37 0 12c0 8 12 20 12 20s12-12 12-20c0-6.63-5.37-12-12-12z" fill="${hex}" stroke="#ffffff" stroke-width="1.5"/>
          <circle cx="12" cy="11" r="4.5" fill="#ffffff"/>
        </svg>`,
        iconSize: [32, 42],
        iconAnchor: [16, 42],
        popupAnchor: [0, -38]
      });
    }

    const markersMap = {};

    landmarks.forEach(p => {
      const marker = L.marker([p.lat, p.lng], { icon: createPin(p.hue) }).addTo(map);
      marker.bindPopup(`
        <div style="font-family:'Roboto',sans-serif; padding:4px 2px;">
          <div style="font-weight:700; font-size:14px; color:#1d1b20; margin-bottom:2px;">${p.title}</div>
          <div style="font-size:11.5px; color:#6750A4; font-weight:600;">${p.category} • Tap for details</div>
        </div>
      `);
      markersMap[p.id] = marker;
    });

    // User Location Marker
    const userMarker = L.marker([18.52043, 73.85674], {
      icon: L.divIcon({
        className: 'user-pin',
        html: `
          <div class="user-marker-container">
            <div class="user-pulse"></div>
            <div class="user-dot"></div>
          </div>
        `,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      })
    }).addTo(map);

    // Populate Drawer List
    const drawerList = document.getElementById('poi-drawer-list');
    landmarks.forEach(p => {
      const item = document.createElement('div');
      item.className = 'drawer-item';
      item.innerHTML = `
        <div style="font-weight:700; font-size:13.5px; color:#1d1b20;">${p.title}</div>
        <div style="font-size:11px; color:#6750A4; font-weight:600; margin:2px 0 4px 0;">${p.category}</div>
        <div style="font-size:11px; color:#49454f;">★ ${p.rating} • ${p.hours}</div>
      `;
      item.onclick = () => {
        map.setView([p.lat, p.lng], 18);
        markersMap[p.id].openPopup();
      };
      drawerList.appendChild(item);
    });

    // Helper functions for State configuration
    window.setAppState = function(config) {
      if (config.debugBanner) document.getElementById('debug-banner').innerText = config.debugBanner;
      if (config.subBanner) document.getElementById('sub-banner').innerText = config.subBanner;
      if (config.coords) document.getElementById('coord-text').innerText = config.coords;

      // Layer
      if (config.layer === 'satellite') {
        map.removeLayer(normalLayer);
        map.removeLayer(terrainLayer);
        satelliteLayer.addTo(map);
        document.getElementById('layer-normal').classList.remove('active');
        document.getElementById('layer-terrain').classList.remove('active');
        document.getElementById('layer-satellite').classList.add('active');
      } else if (config.layer === 'terrain') {
        map.removeLayer(normalLayer);
        map.removeLayer(satelliteLayer);
        terrainLayer.addTo(map);
        document.getElementById('layer-normal').classList.remove('active');
        document.getElementById('layer-satellite').classList.remove('active');
        document.getElementById('layer-terrain').classList.add('active');
      } else {
        map.removeLayer(satelliteLayer);
        map.removeLayer(terrainLayer);
        normalLayer.addTo(map);
        document.getElementById('layer-satellite').classList.remove('active');
        document.getElementById('layer-terrain').classList.remove('active');
        document.getElementById('layer-normal').classList.add('active');
      }

      // Dialogs / Sheets
      document.getElementById('modal-permission').style.display = config.showPermission ? 'flex' : 'none';
      document.getElementById('bottom-sheet').style.display = config.showSheet ? 'block' : 'none';
      document.getElementById('snackbar').style.display = config.showSnackbar ? 'flex' : 'none';
      if (config.snackbarText) document.getElementById('snackbar-text').innerText = config.snackbarText;

      // Drawer
      document.getElementById('tablet-drawer').style.display = config.showDrawer ? 'flex' : 'none';

      // View
      if (config.center && config.zoom) {
        map.setView(config.center, config.zoom, { animate: false });
      }

      // Popup
      if (config.openPopupId && markersMap[config.openPopupId]) {
        markersMap[config.openPopupId].openPopup();
      } else {
        map.closePopup();
      }

      // Sheet details
      if (config.sheetData) {
        document.getElementById('sheet-title').innerText = config.sheetData.title;
        document.getElementById('sheet-category').innerText = config.sheetData.category;
        document.getElementById('sheet-desc').innerText = config.sheetData.desc;
        document.getElementById('sheet-rating').innerText = config.sheetData.rating;
        document.getElementById('sheet-hours').innerText = 'Hours: ' + config.sheetData.hours;
        document.getElementById('sheet-coords').innerText = 'Lat: ' + config.sheetData.lat + ', Lng: ' + config.sheetData.lng;
      }
    };
  </script>
</body>
</html>
"""
Path("Lab04/scripts/app_view.html").write_text(html_content)
print("app_view.html generated successfully.")
