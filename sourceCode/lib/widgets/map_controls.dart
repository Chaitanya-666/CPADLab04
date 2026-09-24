import 'package:flutter/material.dart';
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
