import 'package:flutter/material.dart';
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
