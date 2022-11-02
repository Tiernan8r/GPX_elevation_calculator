"""
File containing the code to add an animated progress bar
"""
import multiprocessing
import sys
import time

#: List of the ASCII art tickers
_ticks = ["-", "\\", "|", "/"]


def ticker(tick_rate=0.2, prefix="", file=sys.stdout):
    """
    Shows a swirling ticker on the terminal to indicate that an operation
    is in progress.
    :param float tick_rate: The interval to sleep between refreshes in seconds.
    :parma str prefix: An optional prefix to show before the ticker.
    :param TextIO file: Override for the default I/O printed to.
    """

    def show(j):
        i = j % len(_ticks)  # Loop through the ticks
        file.write(f"{prefix}{_ticks[i]}\r")  # write to the same line
        file.flush()

    i = 0
    while True:
        show(i)
        i += 1
        time.sleep(tick_rate)

def threaded_progress_bar() -> multiprocessing.Process:
    """
    Run the progress bar ticker in a separate process so that
    we can sleep the process without hanging the main API request
    returns:
        multiprocessing.Process: The reference to the process running
            the progress bar
    """
    ticker_process = multiprocessing.Process(
        target=ticker,
        args=(0.5, "",)
    )
    ticker_process.start()

    return ticker_process
