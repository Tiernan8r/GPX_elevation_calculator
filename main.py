import os
import re
import sys
from typing import List, Tuple

import gpx_elev
import ticker

GPX_FILES = ["./gpxs/LEJOG.gpx",
             "./gpxs/_LEJOG_2019___My_15_day_routemerged_into_one.gpx",
             "./gpxs/end_to_end_example_main_route.gpx",
             "./gpxs/LEJOG_minimal_climbing.gpx"]

OUTPUT_EXTENSION = "-elevation"


def usage():
    print(sys.argv[0], "- a utility to add elevation data to a GPX file:")
    print("USAGE:")
    print(sys.argv[0], "[FLAGS] <gpx_file>")
    print("ARGUMENTS:")
    print("<gpx_file>       Path to target GPX file.")
    print("FLAGS:")
    print("-o/--output      Specify the output GPX file location.")
    print("-h/--help        Show this message")
    sys.exit(0)


def parse_cli(args: List[str]) -> Tuple[str, str]:
    """Parses the CLI input

    Parameters:
        args (List[str]): The CLI arguments
    Returns:
        Tuple[str, str]: A tuple of the GPX file to add
            elevation to, and the associated output file name.
    """

    # The CLI argument values
    values = []
    # The output flag value
    output = ""

    # Num args provided
    n = len(args)

    # Iterate over all args
    i = 0
    while i < n:
        arg = args[i]

        # Assume a flag was given, and try find flag val
        flag_val = ""
        if i + 1 < n:
            flag_val = args[i + 1]

        # Show help and exit if requested
        if arg == "-h" or arg == "--help":
            usage()

        # If output flag used, set output var value
        if arg == "-o" or arg == "--output":

            # If no value for flag provided, need to exit
            if flag_val == "":
                print("Missing output filename value!")
                sys.exit(1)

            # Save value to output, and skip flag/val pair
            output = flag_val
            i += 2
            continue

        # Error on unrecognised flag
        if re.match("--.+", arg) or re.match("-.+", arg):
            print(f"unrecognised flag '{arg}'")
            sys.exit(1)

        # Store all non flag args in the values list
        values.append(arg)
        i += 1

    print("ARGS:")
    print(args)
    print("VALS:")
    print(values)

    # Need one GPX file
    if len(values) < 1:
        print("Must provide a GPX file to operate on!")
        sys.exit(1)

    # Ignore extra 'files' if given
    target_val = values[0]
    if len(values) > 1:
        print(f"Too many args provided, ignoring all but '{target_val}'")

    target = os.path.abspath(target_val)
    # Default the output name if not overridden
    if output == "":
        target_fname, target_ext = os.path.splitext(target)

        output = target_fname + OUTPUT_EXTENSION + target_ext

    return target, output


def main():

    # Parse the CLI input, dropping the program name
    target, output = parse_cli(sys.argv[1:])

    # Verify target file exists:
    if not os.path.exists(target):
        print(f"GPX file '{target}' not found!")
        sys.exit(1)

    print(f"Adding elevation data to GPX file: {target}")
    print(f"Output GPX file will is: {output}")

    progress_bar = ticker.threaded_progress_bar()

    # Add elevation to GPX file
    gpx_elev.add_elevation_to_gpx(target, output)

    progress_bar.terminate()


if __name__ == "__main__":
    main()
