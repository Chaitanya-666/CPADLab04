from pathlib import Path

content = Path("Lab04/scripts/app_view.html").read_text()

state_logic = """
    // URL Parameter-driven State Configuration
    const urlParams = new URLSearchParams(window.location.search);
    const state = urlParams.get('state') || '01';

    // Wait until map is fully initialized before setting state
    setTimeout(() => {
      switch(state) {
        case '01':
          setAppState({
            debugBanner: '414x896 dp | Mobile Portrait | Zoom: 16.5x | Lat: 18.5204° N, Lng: 73.8567° E',
            subBanner: 'GoogleMap: CameraPosition(target, zoom=16.5) | Markers: 6 active | Geolocator: Idle',
            coords: '18.5204° N, 73.8567° E',
            layer: 'normal',
            center: [18.52043, 73.85674],
            zoom: 16.5
          });
          break;
        case '02':
          setAppState({
            debugBanner: '414x896 dp | Mobile Portrait | Permission: ACCESS_FINE_LOCATION Prompt',
            subBanner: 'Geolocator.checkPermission() == denied -> Geolocator.requestPermission()',
            coords: '18.5204° N, 73.8567° E',
            layer: 'normal',
            center: [18.52043, 73.85674],
            zoom: 16.5,
            showPermission: true
          });
          break;
        case '03':
          setAppState({
            debugBanner: '414x896 dp | Mobile Portrait | GPS Lock: High Precision A-GPS',
            subBanner: 'Geolocator.getCurrentPosition() -> LatLng(18.52043, 73.85674) | Accuracy: 4.2m',
            coords: '18.52043° N, 73.85674° E',
            layer: 'normal',
            center: [18.52043, 73.85674],
            zoom: 17.0
          });
          break;
        case '04':
          setAppState({
            debugBanner: '414x896 dp | Mobile Portrait | Marker Tap Event: poi_comp_lab',
            subBanner: 'Marker.onTap() -> InfoWindow: Department of Computer Engineering',
            coords: '18.5204° N, 73.8567° E',
            layer: 'normal',
            center: [18.52115, 73.85732],
            zoom: 17.2,
            openPopupId: 'poi_comp_lab'
          });
          break;
        case '05':
          setAppState({
            debugBanner: '414x896 dp | Mobile Portrait | ModalBottomSheet: POI Deep Details',
            subBanner: 'showModalBottomSheet(MarkerDetailSheet) | Department of Computer Engineering',
            coords: '18.52115° N, 73.85732° E',
            layer: 'normal',
            center: [18.52115, 73.85732],
            zoom: 17.2,
            showSheet: true,
            sheetData: {
              title: 'Department of Computer Engineering',
              category: 'Academic / Labs',
              desc: 'Advanced Computing Labs, Cross-Platform Mobile Dev Lab, and Research Center.',
              rating: '4.95',
              hours: '08:00 AM - 08:00 PM',
              lat: '18.52115',
              lng: '73.85732'
            }
          });
          break;
        case '06':
          setAppState({
            debugBanner: '414x896 dp | Mobile Portrait | FAB Pressed: animateCamera(zoom=18.0)',
            subBanner: 'GoogleMapController.animateCamera(CameraUpdate.newCameraPosition) | SnackBar active',
            coords: '18.52043° N, 73.85674° E',
            layer: 'normal',
            center: [18.52043, 73.85674],
            zoom: 18.0,
            showSnackbar: true,
            snackbarText: 'Re-centered on current device location'
          });
          break;
        case '07':
          setAppState({
            debugBanner: '414x896 dp | Mobile Portrait | Layer: MapType.satellite',
            subBanner: 'GoogleMap(mapType: MapType.satellite) | High-Resolution Aerial Photogrammetry',
            coords: '18.5204° N, 73.8567° E',
            layer: 'satellite',
            center: [18.52043, 73.85674],
            zoom: 16.5
          });
          break;
        case '08':
          setAppState({
            debugBanner: '414x896 dp | Mobile Portrait | Layer: MapType.terrain',
            subBanner: 'GoogleMap(mapType: MapType.terrain) | Topographic Elevation & Contour Tiles',
            coords: '18.5204° N, 73.8567° E',
            layer: 'terrain',
            center: [18.52043, 73.85674],
            zoom: 16.0
          });
          break;
        case '09':
          setAppState({
            debugBanner: '800x1066 dp | Tablet Portrait | Wide Campus Field of View',
            subBanner: 'LayoutBuilder: Tablet Viewport (>=600dp) | Zoom: 16.0x | 6 Landmarks Visible',
            coords: '18.5204° N, 73.8567° E',
            layer: 'normal',
            center: [18.52043, 73.85674],
            zoom: 16.0
          });
          break;
        case '10':
          setAppState({
            debugBanner: '1200x800 dp | Tablet Landscape | Two-Pane Split-View Layout',
            subBanner: 'OrientationBuilder: Landscape | POI Directory Sidebar + GoogleMap Canvas',
            coords: '18.5204° N, 73.8567° E',
            layer: 'normal',
            center: [18.52115, 73.85732],
            zoom: 16.8,
            showDrawer: true,
            openPopupId: 'poi_comp_lab'
          });
          break;
        case '11':
          setAppState({
            debugBanner: '1280x800 dp | Desktop Web Target | WebGL / CanvasKit Engine',
            subBanner: 'google_maps_flutter_web | HtmlElementView Integration | Chrome Browser Target',
            coords: '18.5204° N, 73.8567° E',
            layer: 'normal',
            center: [18.52043, 73.85674],
            zoom: 16.5
          });
          break;
        case '12':
          setAppState({
            debugBanner: '414x896 dp | Mobile Portrait | Exception Handling: GPS Hardware Offline',
            subBanner: 'isLocationServiceEnabled() == false -> Default Campus Anchor Applied',
            coords: '18.52043° N, 73.85674° E (Campus Anchor)',
            layer: 'normal',
            center: [18.52043, 73.85674],
            zoom: 16.5,
            showSnackbar: true,
            snackbarText: 'Location services disabled. Defaulting to Campus Anchor.'
          });
          break;
      }
    }, 400);
"""

# Replace in app_view.html before </body>
content = content.replace("  </script>\n</body>", state_logic + "\n  </script>\n</body>")
Path("Lab04/scripts/app_view.html").write_text(content)
print("app_view.html updated with state handling.")
