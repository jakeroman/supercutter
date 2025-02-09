class AIPrompts(str):
    segments_intro = "Each one of these segments represents a potential part of the video:\n"
    current_segment = "The segment you are currently considering is: "
    decide_to_keep_segment = (
        "Please evaluate whether this segment enhances the video’s quality and aligns with appropriate content standards. "
        "Classify it as follows:\n\n"
        "- [YES] – The segment is engaging, relevant, and appropriate for inclusion.\n"
        "- [FILTER] – The segment contains strong profanity, explicit language, or content that is clearly inappropriate for the audience.\n"
        "- [NO] – The segment is uninteresting, redundant, or does not add value to the video.\n\n"
        "Use [FILTER] only for strong profanity or content that is clearly inappropriate. Mild informal language (e.g., 'idiot', 'crap') should generally not be filtered unless it is used in a derogatory or offensive way."
        "Respond with only the classification for the segment you are currently considering."
    )
    segment_filtering_intro = (
        "Here's a list of words, each labeled with a number. Your task is to review the list and identify any words that might need to be censored. "
        "Focus on filtering only explicit profanity, offensive language, or sensitive information if absolutely necessary.\n"
    )
    segment_filtering_prompt = (
        "Please review the provided words and decide which, if any, should be censored. This should only include things like excessive profanity, explicit language, etc. Regular conversational english words should never be censored"
        "or sensitive personal information. Respond with the list of word numbers to censor, formatted as [1, 3, 6]. If no words need to be censored, simply respond with an empty list: []"
    )
    song_selector_intro = "Here's a list of songs you can choose from to be background music for this part of the video. Your task is to pick the one best suited to the context and mood.\n"
    song_selector_prompt = "Please respond with the number associated with the song you would like to choose in the format [5] for example."
    mood_selector_intro = "Here's a list of music categories you can choose from to be background music for this part of the video. Your task is to pick the one best suited to the context and overall energy.\n"
    mood_selector_prompt = (
        "Each segment above has a corresponding music mood."
        "To ensure a smooth viewing experience, avoid changing the mood too frequently—"
        "try to maintain the same mood for at least **5-20 segments** unless a significant shift in tone or energy justifies a change."
        "Mood changes should feel **natural and intentional**, not abrupt or random."
        "Prioritize consistency, but adapt when the pacing, energy, or emotions in the scene clearly call for a shift."
        "When selecting a new mood, consider whether the previous mood is still appropriate."
        "Please respond with the number associated with the mood you would like to choose in the format [0], and **only choose from the provided options**."
    )
