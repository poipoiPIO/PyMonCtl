#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import time

import pymonctl as pmc  # type: ignore[import]
import pywinctl as pwc  # type: ignore[import]


def countChanged(names, screensInfo):
    for name in names:
        print("MONITORS COUNT CHANGED:", name, screensInfo[name])


def propsChanged(names, screensInfo):
    for name in names:
        print("MONITORS PROPS CHANGED:", name, screensInfo[name])


print("ALL MONITORS:")
monitors = pmc.getMonitors()
for monitor in monitors:
    print(monitor, monitors[monitor])
print()

win = pwc.getActiveWindow()
if win is not None:
    dpy = win.getDisplay()
    print("CURRENT MONITOR:", dpy)
    print("MONITOR SIZE:", pmc.getSize(dpy))
    print("WORKAREA:", pmc.getWorkArea(dpy))
    print("POSITION:", pmc.getPosition(dpy))
    print("AREA:", pmc.getRect(dpy))
    print("FIND FROM POINT", pmc.findMonitorName(win.center.x, win.center.y))
    print()

    currMode = pmc.getCurrentMode(dpy)
    print("CURRENT MODE:", currMode)
    print()

    print("ALLOWED MODES:")
    modes = pmc.getAllowedModes(dpy)
    modeIndex = len(modes)
    for i, mode in enumerate(modes):
        print(mode)
        if mode == currMode:
            modeIndex = i
    print()

    targetMode = currMode
    if currMode is not None:
        for i, mode in enumerate(modes):
            if mode == currMode:
                # Choosing a random allowed, different from current screen mode
                targetMode = modes[(i + 3) if (i + 3) < len(modes) else ((i - 3) if (i - 3) >= 0 else 0)]
                break

    pmc.enableUpdate(monitorPropsChanged=propsChanged)
    print("UPDATE DETECTION ENABLED:", pmc.isUpdateEnabled())
    print("DETECTING CHANGES. PLEASE WAIT...")
    i = 0
    while True:
        if i == 5 and targetMode is not None:
            print("CHANGE MODE TO:", dpy, targetMode)
            pmc.changeMode(targetMode.width, targetMode.height, targetMode.frequency, dpy)
        if i == 10 and currMode is not None:
            print("RESTORING MODE TO:", dpy, currMode)
            pmc.changeMode(currMode.width, currMode.height, currMode.frequency, dpy)
        if i == 15:
            break
        i += 1
        time.sleep(1)
    pmc.disableUpdate()
    print("UPDATE DETECTION ENABLED:", pmc.isUpdateEnabled())
else:
    print("NO ACTIVE WINDOW?!?!?!" + (" GUESS WE ARE IN WAYLAND..." if sys.platform == "linux" else ""))
