import 'package:google_maps_flutter/google_maps_flutter.dart';

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
