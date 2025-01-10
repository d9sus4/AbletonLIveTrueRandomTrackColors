# Ableton Live Better Track Colors

An experimental Ableton Live control surface script that assigns true random colors to any new tracks (including return tracks, nested tracks) created + some other cool abilities.

## Why

Starting from Live 10, new track colors are not truly random, even if `Theme-Colors->Auto-Assign Track Colors` is enabled in preferences. Instead, new colors are always picked from a fixed color sequence in cycling order. It never uses all 70 colors in Ableton's color palette.

Also, I don't like how Ableton always matches new track color to the container in a grouped track.

Though not backed up by science or anything, I personally believe how the working environment looks and feels can always impact one's creativity, so you may want true random new track colors.

## Requirements

Nothing. Just Ableton Live on Windows or macOS.

Theoretically it should work in all 3 recent versions of Live (10, 11 and 12).

## How to use

1. Copy `BetterTrackColors` folder into the `Remote Scripts` directory under your Ableton Live User Library (if no such directory, create it)
2. Restart Live.
3. Go to `Link, Tempo & MIDI` tab in preferences, add `BetterTrackColors` to the Control Surface list. Leave both Input and Output as None.
4. It should work now.

## Customizable behaviors

See `BetterTrackColors/config.py`.

Remember to always restart Live after modifications.

## Reference

- [AbletonAutoColor](https://github.com/CoryWBoris/AbletonAutoColor/tree/main): many thanks to this similar project that does auto color assignment. Code structure is basically borrowed from it.
- [Live 12 Remote Scripts](https://github.com/gluon/AbletonLive12_MIDIRemoteScripts): decompiled factory scripts.
- [Live 11 API](https://structure-void.com/PythonLiveAPI_documentation/Live11.0.xml): Reverse-engineered unofficial Python API. Live 12 didn't change much.
- [This reddit post](https://www.reddit.com/r/ableton/comments/vtc8s7/writing_my_own_control_surface_script/) helped in debugging.

## TODO

- ~~If `Theme-Colors->Auto-Assign Track Colors` is not checked, disable the plugin.~~ Looks impossible for now.
- Allow user customized palette. ✅
- Skip copied tracks. ✅
- Skip certain group tracks if name matches certain rules. ✅
- Allow diffferent sets of color palettes based on matching track names.