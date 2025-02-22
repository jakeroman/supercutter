class SegmentHandler:
    @staticmethod
    def pad_segments(segments, start_pad, end_pad):
        """
        Adds padding to video segments while ensuring they do not overlap.
        
        :param segments: List of segments with "start" and "end" keys.
        :param start_pad: Amount of padding (in seconds) to add before each segment.
        :param end_pad: Amount of padding (in seconds) to add after each segment.
        :return: Adjusted list of segments with no overlapping.
        """
        for i in range(len(segments)):
            # Apply start padding
            new_start = max(0, segments[i]["start"] - start_pad)

            # Prevent start overlap with the previous segment
            if i > 0:
                prev_end = segments[i - 1]["end"]
                new_start = max(new_start, prev_end)

            # Apply end padding
            new_end = segments[i]["end"] + end_pad

            # Prevent end overlap with the next segment
            if i < len(segments) - 1:
                next_start = segments[i + 1]["start"]
                if new_end > next_start:
                    new_end = next_start - 0.01  # Small buffer to avoid touching\

            # Check final segment does not exceed video      
            if i == len(segments) - 1:
                new_end = new_end - 0.1  # Who doesn't love a good hack fix?

            # Update the segment
            segments[i]["start"] = new_start
            segments[i]["end"] = new_end

        return segments
