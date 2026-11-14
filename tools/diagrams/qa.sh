#!/bin/sh
# render every SVG under docs to /tmp/qa for visual review: ./qa.sh docs/theory/diagrams/03*.svg
mkdir -p /tmp/qa
for f in "$@"; do rsvg-convert -w 1360 "$f" -o /tmp/qa/$(basename "$f" .svg).png; done
