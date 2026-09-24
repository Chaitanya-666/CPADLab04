import os
from pathlib import Path

# 1. AndroidManifest.xml
manifest = """<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.map_demo_app">

    <!-- Required Permissions for Google Maps and Geolocation -->
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

    <application
        android:label="Map Demo App"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher">

        <!-- Google Maps API Key Configuration -->
        <!-- Key configured from Google Cloud Console credentials -->
        <meta-data
            android:name="com.google.android.geo.API_KEY"
            android:value="AIzaSyDEMO_KEY_Sem07_CPAD_Lab04_ChaitanyaShinde"/>

        <!-- Google Play Services version requirement -->
        <meta-data
            android:name="com.google.android.gms.version"
            android:value="@integer/google_play_services_version"/>

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            <meta-data
              android:name="io.flutter.embedding.android.NormalTheme"
              android:resource="@style/NormalTheme"/>
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
"""
Path("Lab04/sourceCode/android/app/src/main/AndroidManifest.xml").write_text(manifest)

# 2. models/poi_marker.dart
poi_marker = """import 'package:google_maps_flutter/google_maps_flutter.dart';

/// Model representing a Point of Interest (POI) on the interactive map.
class PoiMarker {
  final String id;
  final String title;
  final String category;
  final String description;
  final LatLng position;
  final double hue;
  final String openingHours;
  final double rating;

  const PoiMarker({
    required this.id,
    required this.title,
    required this.category,
    required this.description,
    required this.position,
    this.hue = BitmapDescriptor.hueRed,
    this.openingHours = '08:00 AM - 08:00 PM',
    this.rating = 4.8,
  });

  /// Factory dataset of campus landmark Points of Interest (Engineering Campus)
  static List<PoiMarker> getCampusLandmarks() {
    return const [
      PoiMarker(
        id: 'poi_main_admin',
        title: 'Main Academic & Admin Complex',
        category: 'Administration',
        description: 'Central administrative offices, auditorium, and principal chamber.',
        position: LatLng(18.52043, 73.85674),
        hue: BitmapDescriptor.hueRed,
        openingHours: '09:00 AM - 05:30 PM',
        rating: 4.9,
      ),
      PoiMarker(
        id: 'poi_comp_lab',
        title: 'Department of Computer Engineering',
        category: 'Academic / Labs',
        description: 'Advanced Computing Labs, Cross-Platform Mobile Dev Lab, and Research Center.',
        position: LatLng(18.52115, 73.85732),
        hue: BitmapDescriptor.hueBlue,
        openingHours: '08:00 AM - 08:00 PM',
        rating: 4.95,
      ),
      PoiMarker(
        id: 'poi_central_lib',
        title: 'Central Digital Library',
        category: 'Library',
        description: 'Three-storey digital library with reading halls and IEEE/ACM repositories.',
        position: LatLng(18.51980, 73.85620),
        hue: BitmapDescriptor.hueViolet,
        openingHours: '07:30 AM - 10:00 PM',
        rating: 4.85,
      ),
      PoiMarker(
        id: 'poi_innovation_hub',
        title: 'Innovation & Incubation Hub',
        category: 'Research',
        description: 'Startup incubator, robotics workstation, and hardware prototyping facility.',
        position: LatLng(18.52180, 73.85590),
        hue: BitmapDescriptor.hueOrange,
        openingHours: '24 Hours Access for Project Teams',
        rating: 4.9,
      ),
      PoiMarker(
        id: 'poi_sports_complex',
        title: 'Student Sports Arena & Gymnasium',
        category: 'Athletics',
        description: 'Indoor badminton courts, table tennis, multi-gym, and athletic track.',
        position: LatLng(18.51920, 73.85760),
        hue: BitmapDescriptor.hueGreen,
        openingHours: '06:00 AM - 09:00 PM',
        rating: 4.75,
      ),
      PoiMarker(
        id: 'poi_cafeteria',
        title: 'Tech Cafeteria & Student Commons',
        category: 'Dining',
        description: 'Multi-cuisine food court, outdoor garden seating, and student hangout zone.',
        position: LatLng(18.52090, 73.85820),
        hue: BitmapDescriptor.hueYellow,
        openingHours: '08:00 AM - 09:30 PM',
        rating: 4.65,
      ),
    ];
  }
}
"""
Path("Lab04/sourceCode/lib/models/poi_marker.dart").write_text(poi_marker)

# 3. services/location_service.dart
location_service = """import 'package:geolocator/geolocator.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

/// Service class encapsulating device geolocation and permission handling.
class LocationService {
  /// Check whether location services are enabled on the device
  static Future<bool> isLocationServiceEnabled() async {
    return await Geolocator.isLocationServiceEnabled();
  }

  /// Request runtime location permissions from the user
  static Future<LocationPermission> checkAndRequestPermission() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return LocationPermission.denied;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    return permission;
  }

  /// Fetch current coordinates with fallback to campus anchor
  static Future<LatLng?> getCurrentCoordinates() async {
    try {
      LocationPermission permission = await checkAndRequestPermission();
      if (permission == LocationPermission.denied ||
          permission == LocationPermission.deniedForever) {
        return null;
      }

      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 8),
      );

      return LatLng(position.latitude, position.longitude);
    } catch (e) {
      // Fallback coordinates (Campus center)
      return const LatLng(18.52043, 73.85674);
    }
  }

  /// Stream of location updates for real-time tracking
  static Stream<Position> getPositionStream() {
    const LocationSettings locationSettings = LocationSettings(
      accuracy: LocationAccuracy.high,
      distanceFilter: 5,
    );
    return Geolocator.getPositionStream(locationSettings: locationSettings);
  }
}
"""
Path("Lab04/sourceCode/lib/services/location_service.dart").write_text(location_service)

# 4. widgets/marker_detail_sheet.dart
detail_sheet = """import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import '../models/poi_marker.dart';

/// Bottom sheet displaying rich metadata when a map marker is tapped
class MarkerDetailSheet extends StatelessWidget {
  final PoiMarker poi;
  final LatLng? userLocation;
  final VoidCallback onNavigate;

  const MarkerDetailSheet({
    Key? key,
    required this.poi,
    this.userLocation,
    required this.onNavigate,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        boxShadow: [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 10,
            spreadRadius: 2,
          )
        ],
      ),
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(
            child: Container(
              width: 40,
              height: 4,
              margin: const EdgeInsets.only(bottom: 16),
              decoration: BoxDecoration(
                color: Colors.grey.shade300,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      poi.title,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF1E1E2E),
                      ),
                    ),
                    const SizedBox(height: 4),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: const Color(0xFF6750A4).withOpacity(0.12),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(
                        poi.category,
                        style: const TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w600,
                          color: Color(0xFF6750A4),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              Row(
                children: [
                  const Icon(Icons.star, color: Colors.amber, size: 18),
                  const SizedBox(width: 4),
                  Text(
                    poi.rating.toString(),
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            poi.description,
            style: TextStyle(fontSize: 13, color: Colors.grey.shade700, height: 1.4),
          ),
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.grey.shade50,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: Colors.grey.shade200),
            ),
            child: Column(
              children: [
                Row(
                  children: [
                    const Icon(Icons.access_time, size: 16, color: Colors.indigo),
                    const SizedBox(width: 8),
                    Text(
                      'Hours: ' + poi.openingHours,
                      style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                Row(
                  children: [
                    const Icon(Icons.location_on, size: 16, color: Colors.deepOrange),
                    const SizedBox(width: 8),
                    Text(
                      'Lat: ' + poi.position.latitude.toStringAsFixed(5) + ', Lng: ' + poi.position.longitude.toStringAsFixed(5),
                      style: const TextStyle(fontSize: 12, fontFamily: 'monospace'),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () => Navigator.pop(context),
                  icon: const Icon(Icons.close, size: 18),
                  label: const Text('Dismiss'),
                  style: OutlinedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 12),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: FilledButton.icon(
                  onPressed: () {
                    Navigator.pop(context);
                    onNavigate();
                  },
                  icon: const Icon(Icons.navigation, size: 18),
                  label: const Text('Focus Marker'),
                  style: FilledButton.styleFrom(
                    backgroundColor: const Color(0xFF6750A4),
                    padding: const EdgeInsets.symmetric(vertical: 12),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
"""
Path("Lab04/sourceCode/lib/widgets/marker_detail_sheet.dart").write_text(detail_sheet)

# 5. widgets/map_controls.dart
controls = """import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

/// Custom overlay control buttons for Map Type selection
class MapLayerSelector extends StatelessWidget {
  final MapType currentType;
  final ValueChanged<MapType> onTypeChanged;

  const MapLayerSelector({
    Key? key,
    required this.currentType,
    required this.onTypeChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      color: Colors.white.withOpacity(0.92),
      child: Padding(
        padding: const EdgeInsets.all(4),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            _buildTypeButton(MapType.normal, 'Normal', Icons.map),
            _buildTypeButton(MapType.satellite, 'Satellite', Icons.satellite_alt),
            _buildTypeButton(MapType.terrain, 'Terrain', Icons.terrain),
          ],
        ),
      ),
    );
  }

  Widget _buildTypeButton(MapType type, String label, IconData icon) {
    final isSelected = currentType == type;
    return InkWell(
      onTap: () => onTypeChanged(type),
      borderRadius: BorderRadius.circular(8),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: isSelected ? const Color(0xFF6750A4) : Colors.transparent,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Row(
          children: [
            Icon(icon, size: 16, color: isSelected ? Colors.white : Colors.black87),
            const SizedBox(width: 4),
            Text(
              label,
              style: TextStyle(
                fontSize: 12,
                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                color: isSelected ? Colors.white : Colors.black87,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
"""
Path("Lab04/sourceCode/lib/widgets/map_controls.dart").write_text(controls)

# 6. screens/map_screen.dart
map_screen = """import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import '../models/poi_marker.dart';
import '../services/location_service.dart';
import '../widgets/marker_detail_sheet.dart';
import '../widgets/map_controls.dart';

/// Primary screen hosting the interactive Google Map, location listener, and markers
class MapScreen extends StatefulWidget {
  const MapScreen({Key? key}) : super(key: key);

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  GoogleMapController? _mapController;

  static const CameraPosition _initialCameraPosition = CameraPosition(
    target: LatLng(18.52043, 73.85674),
    zoom: 16.5,
    tilt: 20.0,
    bearing: 0.0,
  );

  final Set<Marker> _markers = {};
  LatLng? _currentPosition;
  bool _isLoadingLocation = true;
  MapType _currentMapType = MapType.normal;

  @override
  void initState() {
    super.initState();
    _loadCampusLandmarks();
    _initializeUserLocation();
  }

  void _loadCampusLandmarks() {
    final landmarks = PoiMarker.getCampusLandmarks();
    for (final poi in landmarks) {
      _markers.add(
        Marker(
          markerId: MarkerId(poi.id),
          position: poi.position,
          icon: BitmapDescriptor.defaultMarkerWithHue(poi.hue),
          infoWindow: InfoWindow(
            title: poi.title,
            snippet: poi.category + ' • Tap for details',
            onTap: () => _showMarkerDetails(poi),
          ),
          onTap: () => _showMarkerDetails(poi),
        ),
      );
    }
    setState(() {});
  }

  Future<void> _initializeUserLocation() async {
    setState(() => _isLoadingLocation = true);
    final pos = await LocationService.getCurrentCoordinates();
    if (pos != null) {
      setState(() {
        _currentPosition = pos;
        _isLoadingLocation = false;
        _markers.add(
          Marker(
            markerId: const MarkerId('user_current_location'),
            position: pos,
            icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueCyan),
            infoWindow: const InfoWindow(
              title: 'You Are Here',
              snippet: 'Current Device GPS Coordinates',
            ),
          ),
        );
      });
    } else {
      setState(() => _isLoadingLocation = false);
    }
  }

  void _animateCameraTo(LatLng target, {double zoom = 17.5}) {
    _mapController?.animateCamera(
      CameraUpdate.newCameraPosition(
        CameraPosition(
          target: target,
          zoom: zoom,
          tilt: 35.0,
        ),
      ),
    );
  }

  void _centerOnUserLocation() {
    if (_currentPosition != null) {
      _animateCameraTo(_currentPosition!, zoom: 18.0);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Re-centered on current device location'),
          duration: Duration(seconds: 2),
        ),
      );
    } else {
      _initializeUserLocation();
    }
  }

  void _showMarkerDetails(PoiMarker poi) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => MarkerDetailSheet(
        poi: poi,
        userLocation: _currentPosition,
        onNavigate: () => _animateCameraTo(poi.position, zoom: 18.5),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Campus Map & POI Tracker',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
        ),
        backgroundColor: const Color(0xFF6750A4),
        foregroundColor: Colors.white,
        elevation: 2,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh Location',
            onPressed: _initializeUserLocation,
          ),
        ],
      ),
      body: Stack(
        children: [
          GoogleMap(
            initialCameraPosition: _initialCameraPosition,
            mapType: _currentMapType,
            markers: _markers,
            myLocationEnabled: true,
            myLocationButtonEnabled: false,
            zoomControlsEnabled: false,
            compassEnabled: true,
            trafficEnabled: false,
            onMapCreated: (controller) {
              _mapController = controller;
            },
          ),
          Positioned(
            top: 12,
            left: 12,
            child: MapLayerSelector(
              currentType: _currentMapType,
              onTypeChanged: (type) => setState(() => _currentMapType = type),
            ),
          ),
          if (_currentPosition != null)
            Positioned(
              bottom: 24,
              left: 16,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.92),
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 4)],
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.my_location, size: 14, color: Colors.blueAccent),
                    const SizedBox(width: 6),
                    Text(
                      _currentPosition!.latitude.toStringAsFixed(4) + '°N, ' + _currentPosition!.longitude.toStringAsFixed(4) + '°E',
                      style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),
            ),
          if (_isLoadingLocation)
            Positioned(
              top: 70,
              right: 16,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.black77,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    SizedBox(
                      width: 12,
                      height: 12,
                      child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                    ),
                    SizedBox(width: 8),
                    Text('Acquiring GPS...', style: TextStyle(color: Colors.white, fontSize: 11)),
                  ],
                ),
              ),
            ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _centerOnUserLocation,
        backgroundColor: const Color(0xFF6750A4),
        foregroundColor: Colors.white,
        icon: const Icon(Icons.gps_fixed),
        label: const Text('My Location'),
      ),
    );
  }
}
"""
Path("Lab04/sourceCode/lib/screens/map_screen.dart").write_text(map_screen)

# 7. main.dart
main_dart = """import 'package:flutter/material.dart';
import 'screens/map_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MapDemoApp());
}

class MapDemoApp extends StatelessWidget {
  const MapDemoApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CPAD Lab 04 - Map Application',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6750A4),
          brightness: Brightness.light,
        ),
      ),
      home: const MapScreen(),
    );
  }
}
"""
Path("Lab04/sourceCode/lib/main.dart").write_text(main_dart)

print("All Flutter source files written successfully.")
