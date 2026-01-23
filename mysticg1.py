#!/usr/bin/env python3
import hid
import time
import signal
import sys

VID = 0xaa88
PID = 0x8666
TEMP_PATH = "/sys/class/thermal/thermal_zone0/temp"
INTERVAL = 0.5  # seconds


def shutdown(signum, frame):
    try:
        device.close()
    except Exception:
        pass
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

device = hid.device()
device.open(VID, PID)

while True:
    try:
        with open(TEMP_PATH, "r") as f:
            temp = int(f.read().strip()) // 1000
    except Exception:
        temp = 0

    if temp > 99:
        temp = 99
    elif temp < 0:
        temp = 0

    frame = [0x00, temp, 0x00, 0x00, 0x00]
    frame.append(sum(frame) & 0xFF)

    device.write(bytes(frame))
    time.sleep(INTERVAL)
