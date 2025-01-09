import Live
from ableton.v2.control_surface import ControlSurface
import random
from functools import partial
from .config import *

color_indices = range(70)

def assign_random_track_color(track):
    """Assigns a random color to a track"""
    track.color_index = random.choice(color_indices)

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

class TrueRandomTrackColors(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        app = Live.Application.get_application()
        self.doc = app.get_document()
        self.previous_track_ids = set(track._live_ptr for track in get_all_tracks(self.doc))
        self.previous_return_track_ids = set(track._live_ptr for track in self.doc.return_tracks)
        # assign random colors to existing tracks on initialization
        # self.assign_colors_to_existing_tracks()

        # register the listener functions
        self.doc.add_tracks_listener(self.on_tracks_changed)
        self.doc.add_return_tracks_listener(self.on_return_tracks_changed)

        # for track in get_all_tracks(self.doc):
        #     track.add_name_listener(partial(self.on_track_name_changed, track))

    def on_tracks_changed(self):
        """Listener function called when a track is added or deleted"""
        current_track_ids = set(track._live_ptr for track in self.doc.tracks)
        self.schedule_message(0, lambda: self.handle_track_change(current_track_ids))

    def on_return_tracks_changed(self):
        """Listener function called when a return track is added or deleted"""
        current_return_track_ids = set(track._live_ptr for track in self.doc.return_tracks)
        self.schedule_message(0, lambda: self.handle_return_track_change(current_return_track_ids))

    def handle_track_change(self, current_track_ids):
        new_track_id = current_track_ids - self.previous_track_ids
        deleted_track_id = self.previous_track_ids - current_track_ids

        if new_track_id:
            new_track_id = new_track_id.pop()
            new_track = None
            for track in self.doc.tracks:
                if track._live_ptr == new_track_id:
                    new_track = track
                    break
            if new_track is not None:
                assign_random_track_color(new_track)
                # Attach the event listener to the new track
                # new_track.add_name_listener(lambda: self.track_name_changed_listener(new_track))

        self.previous_track_ids = current_track_ids

    def handle_return_track_change(self, current_return_track_ids):
        new_return_track_id = current_return_track_ids - self.previous_return_track_ids
        deleted_return_track_id = self.previous_return_track_ids - current_return_track_ids

        if new_return_track_id:
            new_return_track_id = new_return_track_id.pop()
            new_return_track = None
            for return_track in self.doc.return_tracks:
                if return_track._live_ptr == new_return_track_id:
                    new_return_track = return_track
                    break
            if new_return_track is not None:
                assign_random_track_color(new_return_track)
                # attach the event listener to the new track
                # new_track.add_name_listener(lambda: self.track_name_changed_listener(new_track))

        self.previous_return_track_ids = current_return_track_ids

    def assign_colors_to_existing_tracks(self):
        """Assigns colors to existing tracks based on their names"""
        for track in self.doc.tracks:
            assign_random_track_color(track)

    # def on_track_name_changed(self, track):
    #     """Listener function called when a track's name is changed"""
    #     self.schedule_message(0, lambda: assign_track_color(track))