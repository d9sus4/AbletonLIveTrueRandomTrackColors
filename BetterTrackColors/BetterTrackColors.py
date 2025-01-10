import Live
from ableton.v2.control_surface import ControlSurface
import random
from functools import partial
from .config import *

LISTEN_TO_TRACK_CHANGES = RANDOMIZE_NEW_TRACK_COLORS
LISTEN_TO_RETURN_TRACK_CHANGES = RANDOMIZE_NEW_RETURN_TRACK_COLORS
STORE_EXISTING_TRACK_MARK = SKIP_COLOR_COPIED_TRACKS

def assign_random_track_color(track):
    """Assigns a random color to a track"""
    if SKIP_COLOR_COPIED_TRACKS and track.get_data("i_am_an_existing_track", False): # a marker to mark already existing tracks, to enable skipping copied tracks
        return
    track.color_index = random.choice(COLOR_INDICES)
    if STORE_EXISTING_TRACK_MARK:
        track.set_data("i_am_an_existing_track", True) # atttention: this field will be stored persistently in your live set file
        # which may conflict with future updates of live
        # if you have concerns, disable related functionality in config

def get_all_tracks(doc):
    all_tracks = []
    for track in doc.tracks:
        all_tracks.append(track)
        if hasattr(track, 'is_foldable') and track.is_foldable:
            all_tracks.extend(get_nested_tracks(track))
    return all_tracks

def get_nested_tracks(group_track):
    nested_tracks = []
    for track in group_track.canonical_parent.tracks:
        if hasattr(track, 'is_grouped') and track.is_grouped and track.group_track == group_track:
            nested_tracks.append(track)
            if hasattr(track, 'is_foldable') and track.is_foldable:
                nested_tracks.extend(get_nested_tracks(track))
    return nested_tracks

class BetterTrackColors(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        app = Live.Application.get_application()
        self.doc = app.get_document()
        if LISTEN_TO_TRACK_CHANGES:
            self.previous_tracks = set(self.doc.tracks)
            self.doc.add_tracks_listener(self.on_tracks_changed)
        if LISTEN_TO_RETURN_TRACK_CHANGES:
            self.previous_return_tracks = set(self.doc.return_tracks)
            self.doc.add_return_tracks_listener(self.on_return_tracks_changed)
            
        if STORE_EXISTING_TRACK_MARK:
            for track in self.doc.tracks + self.doc.return_tracks:
                track.set_data("i_am_an_existing_track", True)

    def on_tracks_changed(self):
        """Listener function called when a track is added or deleted"""
        # current_track_ids = set(track._live_ptr for track in self.doc.tracks)
        current_tracks = set(self.doc.tracks)
        self.schedule_message(0, lambda: self.handle_track_change(current_tracks)) # a change to view can't be triggered by notification and must be deferred

    def on_return_tracks_changed(self):
        """Listener function called when a return track is added or deleted"""
        current_return_tracks = set(self.doc.return_tracks)
        self.schedule_message(0, lambda: self.handle_return_track_change(current_return_tracks))

    def handle_track_change(self, current_tracks):
        new_tracks = current_tracks - self.previous_tracks
        for new_track in new_tracks:
            # find the outermost container
            now_track = new_track
            while now_track.is_grouped:
                now_track = now_track.group_track
            skip_flag = False
            for keyword in SKIP_COLOR_IF_TRACK_NAME_CONTAINS:
                if keyword.lower() in str(now_track.name).lower():
                    skip_flag = True
                    break
            if new_track is not None and not skip_flag:
                assign_random_track_color(new_track)
        self.previous_tracks = current_tracks

    def handle_return_track_change(self, current_return_tracks):
        new_return_tracks = current_return_tracks - self.previous_return_tracks

        for new_return_track in new_return_tracks:
            if new_return_track is not None:
                assign_random_track_color(new_return_track)
        self.previous_return_tracks = current_return_tracks

    def assign_colors_to_existing_tracks(self):
        """Assigns colors to existing tracks based on their names"""
        for track in self.doc.tracks:
            assign_random_track_color(track)