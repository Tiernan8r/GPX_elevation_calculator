import gpxpy
import numpy as np
import requests
import time
import datetime

API_KEY = 'ak_xIO8pzCi_ugMbNElpl1MXJVEq'  # Get a free key from www.gpxz.io.
BATCH_SIZE = 50  # 512 for paid customers.

PAUSE_INTERVAL = 1


def gpxz_elevation(lats, lons):
    '''Iterate over the coordinates in chunks, querying the GPXZ api to return
    a list of elevations in the same order.'''
    elevations = []
    n_chunks = int(len(lats) // BATCH_SIZE) + 1
    lat_chunks = np.array_split(lats, n_chunks)
    lon_chunks = np.array_split(lons, n_chunks)

    num_chunks = len(lat_chunks)
    print(f"Have {num_chunks} to request over...")

    eta = datetime.timedelta(seconds=num_chunks*PAUSE_INTERVAL)
    print(f"This will take ~{eta}")

    for lat_chunk, lon_chunk in zip(lat_chunks, lon_chunks):
        latlons = '|'.join(f'{lat},{lon}' for lat,
                           lon in zip(lat_chunk, lon_chunk))
        response = requests.post(
            'https://api.gpxz.io/v1/elevation/points',
            headers={'x-api-key': API_KEY},
            data={'latlons': latlons},
        )
        response.raise_for_status()
        elevations += [r['elevation'] for r in response.json()['results']]

        print(f"Waiting {PAUSE_INTERVAL} secs for next request...")
        time.sleep(PAUSE_INTERVAL)
    return elevations


def add_elevation_to_gpx(gpx_path, output_path='with_elevation.gpx'):
    # Load gpx.
    # gpx_path = 'run.gpx'
    with open(gpx_path) as f:
        gpx = gpxpy.parse(f)

    # Find points.
    points = list(gpx.walk(only_points=True))
    latitudes = [p.latitude for p in points]
    longitudes = [p.longitude for p in points]

    # Update elevations.
    elevations = gpxz_elevation(latitudes, longitudes)
    for point, elevation in zip(points, elevations):
        point.elevation = elevation

    # Save gpx file.
    with open(output_path, 'w') as f:
        f.write(gpx.to_xml())
