import argparse
import os
import pdb

from modules.ai import AIHandler
from modules.music import MusicHandler
from modules.renderer import VideoRenderer
from modules.segments import SegmentHandler
from modules.transcribe import VideoTranscriber
from modules.utils import EditorUtils

def main():
    # Argparse
    parser = argparse.ArgumentParser(
        description="A script to process a video file for editing."
    )
    parser.add_argument(
        "video", 
        type=str, 
        help="Path to the video file to be edited."
    )
    parser.add_argument(
        "--start-pad", 
        type=float, 
        help="A number in seconds that is added to the beginning of each segment to pad it",
        default=0.25,
    )
    parser.add_argument(
        "--end-pad", 
        type=float, 
        help="A number in seconds that is added to the end of each segment to pad it",
        default=0.45,
    )
    parser.add_argument(
        "--min-music-segs", 
        type=int, 
        help="How many segments a music track must be playing before allowing a switch",
        default=4,
    )
    parser.add_argument(
        "--outro", 
        type=str, 
        help="A path to an outro video that will be tacked onto the end. Defaults to library/video/outro.mp4",
        default="library/video/outro.mp4",
    )
    parser.add_argument(
        "--filter", 
        type=bool, 
        help="Whether or not to enable the profanity filter, defaults to True",
        default=True,
    )
    
    args = parser.parse_args()
    
    # Prepare
    print(">> Preparing")
    EditorUtils.cleanup_temp() # Cleanup temp folder

    # Transcribe
    print(">> Transcribing")
    transcriber = VideoTranscriber() # Load whisper model
    transcriber.transcribe(video_path=args.video, output_path="temp/transcript.json")
    transcript = EditorUtils.load_json("temp/transcript.json")
    print(f"Generated transcript of {len(transcript["text"])} characters")

    # Pad Segments
    print(">> Padding Segments")
    segments = list(transcript["segments"])
    segments = SegmentHandler.pad_segments(segments, args.start_pad, args.end_pad)
    for i,v in enumerate(segments):
        print(f"#{i}: {v["text"]} [{int(v["start"])}-{int(v["end"])}]")

    # AI Segment Cutting
    print(">> AI Segment Cutting")
    ai = AIHandler()

    for i,v in enumerate(segments):
        keep = ai.decide_to_keep_segment(segments, i)
        if keep == "filter" and args.filter:
            # Filter for profanity
            print(f"Filtering Segment {i}: {v["text"]}")
            beeps = ai.filter_segment_words(segments, i)
            segments[i]["beeps"] = beeps
        elif keep:
            print(f"Keeping Segment {i}: {v["text"]}")
        else:
            print(f"Cutting Segment {i}: {v["text"]}")
            segments[i]["cut"] = True

    # Remove Flagged Segments
    segments = [segment for segment in segments if not segment.get("cut", False)]

    # Add Music with Mood Persistence
    print(">> AI Music Choice")
    moods = MusicHandler().get_moods()

    last_mood = None  # Stores the last chosen mood
    mood_count = 0  # Tracks how long the current mood has been active

    for i, v in enumerate(segments):
        # If the previous mood is still locked, reuse it instead of querying AI
        if last_mood and mood_count < args.min_music_segs:
            choice = last_mood
            mood_count += 1
            print(f"Maintaining mood [{choice}] for Segment {i} (Persistence: {mood_count}/{args.min_music_segs})")
        else:
            # AI determines the mood only when a change is allowed
            choice = ai.pick_mood_from_context(moods, segments, i).strip()
            print(f"New Mood [{choice}] assigned to Segment {i}")

            # Reset mood count for the new selection
            mood_count = 1  

        # Update last mood and assign the mood to the segment
        last_mood = choice
        segments[i]["music"] = choice

        print(f"Music: [{choice}] for Segment {i}: {v['text']}")

    # Add Outro
    if os.path.exists(args.outro):
        segments.append({
            "external_file": args.outro
        })

    # Stitch
    print(">> Rendering")
    stitcher = VideoRenderer()
    render_result = stitcher.stitch_segments(video_path=args.video, segments=segments, output_path="temp/output.mp4") or {}

    # Done
    EditorUtils.cleanup_file_readers()
    print("\n\n\n\n\n ☑️  Video saved to temp/output.mp4\n")

    # Generate Description
    print(">> Generated Description:")
    desc = ai.generate_description(segments)
    print(desc)

    print("\nMusic:")
    print(render_result.get("music_attr","Music attributions unavailable."))

if __name__ == "__main__":
    main()
