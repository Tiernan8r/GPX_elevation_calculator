import gpx_elev
import time

GPX_FILES = ["./gpxs/LEJOG.gpx",
             "./gpxs/_LEJOG_2019___My_15_day_routemerged_into_one.gpx",
             "./gpxs/end_to_end_example_main_route.gpx",
             "./gpxs/LEJOG_minimal_climbing.gpx"]


def main():

    for gpx in GPX_FILES:
        print("WORKING ON:")
        print(gpx)
        gpx_elev.add_elevation_to_gpx(gpx, gpx)
        print("Waiting 10s for next request...")
        time.sleep(10)

if __name__ == "__main__":
    main()
