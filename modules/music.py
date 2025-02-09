import pdb
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut, MultiplyVolume
from moviepy import AudioFileClip, CompositeAudioClip
from modules.ai import AIHandler
from modules.utils import EditorUtils
import os

LIBRARY_DIR = "library/audio/"

class MusicHandler:
    def __init__(self):
        self.mood_state = {}  # Keeps track of moods and their respective song positions
        self.last_mood = None  # Track the last mood for crossfading


    def get_moods(self):
        return EditorUtils.get_folders_in_directory(LIBRARY_DIR)


    def add_music_to_clip(self, subclip, segments, segment_id, fade_duration=2, volume=0.05):
        """
        Add music to a subclip based on the segment's mood.
        Handles crossfading when moods change.
        """
        # Grab correct segments
        segment = segments[segment_id]
        next_segment = segments[segment_id + 1] if segment_id + 1 < len(segments) else None

        # Determine moods
        mood = segment.get("music")
        next_mood = next_segment.get("music") if next_segment else None

        # Choose or resume song
        audio_data, song_name = self.choose_music(mood, segments, segment_id)

        # Get starting position for the song
        start_position = self.get_song_state(mood, song_name, "position")
        song_duration = audio_data.duration  # Get the full length of the song
        segment_duration = segment["end"] - segment["start"]

        # Ensure we don't exceed the song's duration
        if start_position + segment_duration > song_duration:
            segment_duration = song_duration - start_position  # Adjust duration
            finished = True  # Mark the song as finished
        else:
            finished = False

        # Trim the song to match the (possibly adjusted) segment duration
        music_clip = audio_data.subclipped(start_position, start_position + segment_duration)

        # Ensure fade duration does not exceed half of the clip length
        max_fade_duration = min(fade_duration, segment_duration / 2)

        # Apply fade-in if the mood changes
        if self.last_mood != mood and max_fade_duration > 0:
            music_clip = music_clip.with_effects([AudioFadeIn(max_fade_duration)])

        # Apply fade-out if the next mood changes or song is finishing
        if (next_mood != mood or finished) and max_fade_duration > 0:
            music_clip = music_clip.with_effects([AudioFadeOut(max_fade_duration)])


        # Adjust music volume (to ensure speech is clear)
        music_clip = music_clip.with_effects([MultiplyVolume(volume)])

        # Combine subclip audio and music
        final_audio = CompositeAudioClip([music_clip, subclip.audio])

        # Set the combined audio back to the subclip
        subclip = subclip.with_audio(final_audio)

        # Update mood state for resuming or resetting if the song finished
        self.mood_state[mood][song_name] = {
            "position": 0 if finished else start_position + segment_duration,
            "finished": finished
        }
        self.last_mood = mood  # Update the last mood

        return subclip


    def choose_music(self, mood, segments, segment_id):
        # Prepare mood state dict
        if self.mood_state.get(mood) is None:
            self.mood_state[mood] = {}

        # Check current song
        current_song = self.mood_state[mood].get("_current_song")
        if self.get_song_state(mood, current_song, "finished") is False:
            # We have an active song and it's not over yet
            next_song = current_song
        else:
            # Search for options
            options = EditorUtils.get_filenames_in_directory(LIBRARY_DIR + mood)
            next_song = self.pick_next_song(options, segments, segment_id, mood)
            self.mood_state[mood]["_current_song"] = next_song

        # Load song into memory
        path = os.path.join(f"{LIBRARY_DIR}{mood}", next_song)
        if not os.path.exists(path):
            print("Error accessing:",path)
            pdb.set_trace()

        audio_data = AudioFileClip(path)
        return audio_data, next_song


    def pick_next_song(self, options, segments, segment_id, mood):
        # Filter out songs that have already been finished
        filtered_options = []
        for song in options:
            if self.get_song_state(mood, song, "finished") != True:
                # Song has not been played yet
                filtered_options.append(song)

        if len(filtered_options) == 0:
            # No songs remaining, disabling played filter
            filtered_options = options

        selected = AIHandler().pick_song_from_options(filtered_options, segments, segment_id)
        return selected


    def get_song_state(self, mood, song, param, default=0):
        return self.mood_state[mood].get(song, {}).get(param, default)