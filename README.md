GPX Elevation Calculator:
===

A simple CLI utility to add elevation data to a GPX file using the [Open Elevation](open-elevation.com) API.

## Setup:

Clone the repo to your system, and `cd` to it using the CLI

Setup a python virtualenvironment

```console
$ python -m venv venv
```

Activate the new virtual environment

```console
$ . venv/bin/activate
```

Install the required python modules

```console
$ pip install -r requirements.txt
```

## Usage

Once the environment is setup and ready to go, the program can be run using:

```console
$ python main.py
```

This will result in the help message being displayed:

```console
main.py - a utility to add elevation data to a GPX file:
USAGE:
main.py [FLAGS] <gpx_file>
ARGUMENTS:
<gpx_file>       Path to target GPX file.
FLAGS:
-o/--output      Specify the output GPX file location.
-h/--help        Show this message
```

The usage is straight forward, call the program with the GPX file you want to add elevation data to as an argument, by default the program will calculate the elevation data to a new file with the same path as the original, with a "-elevation" suffix appended.

This behaviour can overridden using the `--output` flag, with the desired path to your new GPX file.

## Notes:

Depending on the number of nodes in your GPX file, the calculation of the elevations may take a while. Requests to the [open-elevation.com](open-elevation.com) API are batched in sets of 512 nodes, with an interval of 1 second between completed requests, to not overload the API.