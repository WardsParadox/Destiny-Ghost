#!/bin/bash

CONFIGPATH="/Library/Application Support/com.github.wardsparadox.destiny-ghost"
/usr/bin/python "/Library/Application Support/com.github.wardsparadox.destiny-ghost/ghost.py" --computername --assettag --config "$CONFIGPATH"
