import pdb
import re
import ollama

from modules.prompts import AIPrompts


DEFAULT_MODEL = "qwen2.5:14b"

class AIHandler:
    def __init__(self, model: str | None = None):
        self.model = model or DEFAULT_MODEL


    def generate_response(self, prompt):
        # print("---------------------")
        # print("AI Prompt: ",prompt)
        res = ollama.generate(
            model=self.model,
            prompt=prompt,
        )
        # print("AI Response: ",res.response)
        return res.response
    
    
    def decide_to_keep_segment(self, segments, segment_id):
        message = self._build_segment_context(segments, segment_id)
        message += AIPrompts.decide_to_keep_segment

        # Check if segment is empty
        if len(segments[segment_id]["text"].strip()) == 0:
            return False

        # Get response
        while True:
            response = self.generate_response(message)
            if "[YES]" in response:
                return True
            if "[FILTER]" in response:
                return "filter"
            if "[NO]" in response:
                return False
            

    def filter_segment_words(self, segments, segment_id):
        message = self._build_segment_context(segments, segment_id)
        message += AIPrompts.segment_filtering_intro

        # Add word list
        segment = segments[segment_id]
        for i,v in enumerate(segment["words"]):
            message += f"Word #{i}: {v["word"]}\n"
        
        # Inject prompt 
        message += AIPrompts.segment_filtering_prompt

        # Get response
        response = self.generate_response(message)
        censor = self._extract_list_from_text(response)
        
        # Turn that into beeps
        beeps = []
        for i in censor:
            word = segment["words"][i]
            beeps.append({
                "start_time": word["start"] - segment["start"],
                "duration": word["end"] - word["start"]
            })

        return beeps
            

    def pick_mood_from_context(self, moods, segments, segment_id):
        message = self._build_segment_context(segments, segment_id, context_range=20, include_music=True)

        # Inject prompts
        message += AIPrompts.mood_selector_intro
        if segment_id > 0:
            message += f"The mood of the last segment was: {segments[segment_id-1].get("music") or "unknown"}.\n"

        # Add list of mood options
        for i,v in enumerate(moods):
            message += f"Mood [{i}]: {v}\n"
        message += AIPrompts.mood_selector_prompt

        # Get response
        while True:
            res = self.generate_response(message)
            mood_choice = self._extract_list_from_text(res)
            if len(mood_choice) == 1 and mood_choice[0] < len(moods):
                return moods[mood_choice[0]]



    def pick_song_from_options(self, options, segments, segment_id):
        message = self._build_segment_context(segments, segment_id)

        # Inject song options and prompts
        message += AIPrompts.song_selector_intro
        for i,v in enumerate(options):
            message += f"Song [{i}]: {v}\n"
        message += AIPrompts.song_selector_prompt

        # Get response
        while True:
            res = self.generate_response(message)
            song_choice = self._extract_list_from_text(res)
            if len(song_choice) == 1 and song_choice[0] < len(options):
                return options[song_choice[0]]

            
    # Helper methods
    def _build_segment_context(self, segments, segment_id, context_range=10, include_music=False):
        message = AIPrompts.segments_intro

        # Define the range of segments to include
        start_index = max(0, segment_id - context_range)
        end_index = min(len(segments), segment_id + (context_range + 1))  # +11 to include segment_id itself

        for i in range(start_index, end_index):
            if i == segment_id:
                message += "YOUR "

            message += f"Segment {i} [{int(segments[i]['start'])}s to {int(segments[i]['end'])}s]: " # Add base segment

            if include_music:
                message += f"[Music: {segments[i].get("music") or "TBD"}] " # Add music mood indicator
                
            message += segments[i]["text"] + (" [Segment Removed]\n" if segments[i].get("cut") else "\n") # Add indicator if segment removed

        # Add a reminder about the current segment:
        message += AIPrompts.current_segment
        message += f"Segment {segment_id}: {segments[segment_id]['text']}\n"

        return message

    

    def _extract_list_from_text(self, response_text):
        """
        Extracts a list of integers from a given text.

        Args:
            response_text (str): The text from which to extract the list.

        Returns:
            list: A list of integers if found, otherwise an empty list.
        """
        # Use a regex pattern to find something that looks like a Python list
        match = re.search(r'\[(\s*\d+\s*(,\s*\d+\s*)*)\]', response_text)
        if match:
            # Extract the matched portion (e.g., "[1, 3, 6]")
            list_string = match.group(0)
            try:
                # Safely evaluate the string to turn it into a Python list
                extracted_list = eval(list_string)
                # Ensure it's a list of integers
                if isinstance(extracted_list, list) and all(isinstance(x, int) for x in extracted_list):
                    return extracted_list
            except Exception as e:
                print(f"Error evaluating list: {e}")
        return []


    def generate_description(self, segments):
        """Makes a description based on the whole video context"""
        context = ""
        for i in segments:
            context += (i.get("text","") + " ")
        context += ("\n" + AIPrompts.description_generator)
        return self.generate_response(context)