RANDOMIZE_NEW_TRACK_COLORS = True
RANDOMIZE_NEW_RETURN_TRACK_COLORS = True

# all possible color indices from ableton paletter (0~69, row-major order)
COLOR_INDICES = range(70)

# if set to True, duplicated/copied & pasted tracks will remain the same color
# please note this will also introduce extra persistent data stored in your live set, which is not expected by ableton officially therefore may cause conflicts in the future
# i recommend avoid using this, since you can always instantly revert auto coloring by undo
SKIP_COLOR_COPIED_TRACKS = False

# new tracks whose name (or the outermost group's name if nested) contains the configured strings will be skipped in color randomizing
SKIP_COLOR_IF_TRACK_NAME_CONTAINS = ["reference", "$keep"]