from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy import concatenate_videoclips

from modules.censor import AudioCensorer
from modules.music import MusicHandler


class VideoRenderer:
    def __init__(self):
        pass


    def make_subclip(self, video, segments, segment_id):
        # Grab appropriate segment
        segment = segments[segment_id]

        # Skip if the segment was cut
        if segment.get("cut"):
            return False

        # Create the subclip
        start, end = segment["start"], segment["end"]
        subclip = video.subclipped(start, end)

        # Censor parts of audio if needed
        if segment.get("beeps"):
            subclip = self.audio_censorer.censor_clip(subclip, segment)

        # Overlay music if specified
        if segment.get("music"):
            subclip = self.music_handler.add_music_to_clip(subclip, segments, segment_id)

        # Return the modified subclip
        return subclip


    def stitch_segments(self, video_path, segments, output_path):
        """Stitch together video segments with optional subtitles."""
        try:
            # Load the video file
            video = VideoFileClip(video_path)

            # Instantiate utilities
            self.music_handler = MusicHandler()
            self.audio_censorer = AudioCensorer()

            # Create subclips based on start and end times
            clips = []
            for i,segment in enumerate(segments):
                print(f"Rendering: Segment {i+1}/{len(segments)}")
                if segment.get("external_file"):
                    # External Source
                    subclip = VideoFileClip(segment["external_file"])
                    subclip = subclip.resized(video.size) # Resize external clip to align
                else:
                    # Standard
                    try:
                        subclip = self.make_subclip(video, segments, i)
                    except Exception as e:
                        print(f"Error occurred during subclip creation: {e}")

                if subclip:
                    clips.append(subclip)

            # Stitch the subclips together
            print("Concatenating video clips...")
            final_video = concatenate_videoclips(clips)

            # Write the result to an output file
            print("Saving final video...")
            final_video.write_videofile(output_path, codec="libx264", fps=30, logger="bar")

            print(f"Video successfully saved to {output_path}")
            return {
                "music_attr": self.music_handler.generate_music_attributed_description()
            }

        except Exception as e:
            print(f"Error occured during stitching: {e}")


    def add_subtitles(self):
        """Currently deactivated due to bug in moviepy that makes it take forever to render"""
        pass
        # Add subtitles for each segment if "words" are provided
        # if "words" in segment and segment["words"]:
        #     print(f"Preparing segment video clip ({i}/{len(segments)-1})")
        #     text_clips = []
        #     for word in segment["words"]:
        #         # Create the TextClip for each word
        #         font_size = 100
        #         text_clip = TextClip(
        #             text=word["word"].strip(),
        #             font_size=font_size,
        #             font="arial",
        #             color="white",
        #             stroke_color="black",
        #             stroke_width=2,
        #             duration=word["end"] - word["start"],
        #         ).with_start(word["start"])
        #         x_position = (subclip.w * 0.5) - ((font_size*len(word["word"].strip()))/4)
        #         y_position = subclip.h * 0.8
        #         text_clip.pos = lambda t, x=x_position, y=y_position: (x, y)
        #         text_clips.append(text_clip)

        #     subclip = CompositeVideoClip([subclip, *text_clips], size=subclip.size)