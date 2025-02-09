from moviepy import AudioClip, concatenate_audioclips
import numpy as np


class AudioCensorer:
    def censor_clip(self, subclip, segment):
        # Get the original audio
        original_audio = subclip.audio

        # Process each beep in the segment
        for beep in segment["beeps"]:
            beep_start = beep["start_time"]  # Relative to the subclip start
            beep_end = beep_start + beep["duration"]

            # Ensure beep_start and beep_end are within valid ranges
            beep_start = max(0, beep_start)
            beep_end = min(subclip.duration, beep_end)

            # Split the audio into parts: before, during, and after the beep
            before_beep = original_audio.subclipped(0, beep_start)
            after_beep = original_audio.subclipped(beep_end, subclip.duration)

            # Generate the beep sound
            nchannels = original_audio.nchannels if hasattr(original_audio, "nchannels") else 2
            beep_clip = self.generate_beep(frequency=1000, duration=beep["duration"], fps=44100, nchannels=nchannels)

            # Combine the audio components
            audio_components = [before_beep, beep_clip, after_beep]
            original_audio = concatenate_audioclips(audio_components)

        # Set the new audio to the subclip
        subclip = subclip.with_audio(original_audio)
        return subclip


    def generate_beep(self, frequency=800, duration=1, fps=44100, nchannels=2, amplitude = 0.2):
        """
        Generates a beep sound of a given frequency and duration.
        Supports mono (nchannels=1) and stereo (nchannels=2).
        """
        if nchannels == 1:
            frame_function = lambda t: np.sin(2 * np.pi * frequency * t) * amplitude
        else:  # Stereo: Same beep in both channels
            frame_function = lambda t: np.array([np.sin(2 * np.pi * frequency * t) * amplitude,
                                                np.sin(2 * np.pi * frequency * t) * amplitude]).T.copy(order="C")
        return AudioClip(frame_function, duration=duration, fps=fps)