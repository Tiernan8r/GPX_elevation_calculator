import json

import gpxpy
import numpy as np
import requests

BATCH_SIZE = 512  # 512 for paid customers.

PAUSE_INTERVAL = 1

URL = "https://api.open-elevation.com/api/v1/lookup"


def request(lats, lons):
    """Iterate over the coordinates in chunks, querying the GPXZ api to return
    a list of elevations in the same order."""

    print(f"Requesting elevation details for {len(lats)} coordinates...")

    elevations = []
    locations = []
    for lat, lon in zip(lats, lons):
        loc = {
            "latitude": lat,
            "longitude": lon,
        }

        locations.append(loc)

    payload = json.dumps({
        "locations": locations
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", URL, headers=headers, data=payload)

    response.raise_for_status()
    elevations += [r["elevation"] for r in response.json()["results"]]

    return elevations


def _batch_request(lats, lons):
    """Iterate over the coordinates in chunks, querying the GPXZ api to return
    a list of elevations in the same order."""

    print(f"Requesting elevation details for {len(lats)} coordinates...")

    elevations = []
    n_chunks = int(len(lats) // BATCH_SIZE) + 1
    lat_chunks = np.array_split(lats, n_chunks)
    lon_chunks = np.array_split(lons, n_chunks)

    num_chunks = len(lat_chunks)
    print(f"Have {num_chunks} chunks to request over...")

    i = 1
    for lat_chunk, lon_chunk in zip(lat_chunks, lon_chunks):
        print(f"Chunk {i}:")
        i += 1

        elevs = request(lat_chunk, lon_chunk)

        elevations.append(e for e in elevs)

    return elevations


def add_elevation_to_gpx(gpx_path, output_path):

    # Load gpx.
    with open(gpx_path) as f:
        gpx = gpxpy.parse(f)

    # Find points.
    points = list(gpx.walk(only_points=True))
    latitudes = [p.latitude for p in points]
    longitudes = [p.longitude for p in points]

    # Update elevations.
    elevations = _batch_request(latitudes, longitudes)
    for point, elevation in zip(points, elevations):
        point.elevation = elevation

    # Save gpx file.
    with open(output_path, "w") as f:
        f.write(gpx.to_xml())
