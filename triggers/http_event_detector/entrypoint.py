import os

from event_detector import run

def event_detector():
    default_pattern = "A(.*).gz"
    pattern = os.environ.get("FILE_PATTERN") or default_pattern
    run(pattern)

if __name__ == "__main__":
    event_detector()