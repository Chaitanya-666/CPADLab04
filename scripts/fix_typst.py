from pathlib import Path

content = Path("Lab04/typst/CpadLabAssignment04ChaitanyaShinde231070066.typ").read_text()

# 1. Fix raw code block inside key_box
old_xml = """    ```xml
    <meta-data
        android:name="com.google.android.geo.API_KEY"
        android:value="AIzaSy...YOUR_SECURE_KEY..."/>
    ```"""
new_xml = """#code_block("<meta-data\\n    android:name=\\"com.google.android.geo.API_KEY\\"\\n    android:value=\\"AIzaSy...YOUR_SECURE_KEY...\\"/>", lang: "xml")"""
content = content.replace(old_xml, new_xml)

# 2. Fix animateCamera code block
old_dart = """```dart
_mapController?.animateCamera(
  CameraUpdate.newCameraPosition(
    CameraPosition(target: _currentPosition!, zoom: 18.0, tilt: 35.0),
  ),
);
```"""
new_dart = """#code_block("_mapController?.animateCamera(\\n  CameraUpdate.newCameraPosition(\\n    CameraPosition(target: _currentPosition!, zoom: 18.0, tilt: 35.0),\\n  ),\\n);", lang: "dart")"""
content = content.replace(old_dart, new_dart)

# 3. Fix math dash errors
content = content.replace("($approx 150$--$250$ mA additional current draw)", "(approximately 150--250 mA additional current draw)")
content = content.replace("($approx 200$--$500$ ms)", "(approximately 200--500 ms)")

Path("Lab04/typst/CpadLabAssignment04ChaitanyaShinde231070066.typ").write_text(content)
print("Typst file updated.")
