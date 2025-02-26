class AIPrompts(str):
    segments_intro = "Each one of these segments represents a potential part of the video:\n"
    current_segment = "The segment you are currently considering is: "
    decide_to_keep_segment = (
        "Please evaluate whether this segment enhances the video’s quality. "
        "Classify it as follows:\n"
        "- [YES] – The segment is engaging, relevant, and appropriate for inclusion.\n"
        "- [FILTER] – The segment contains strong profanity, explicit language, or content that is clearly inappropriate for the audience.\n"
        "- [NO] – The segment is uninteresting, redundant, or does not add value to the video.\n"
        "Use [FILTER] only for strong profanity or content that is clearly inappropriate. Mild informal language (e.g., 'idiot', 'crap') should not be filtered. "
        "The speech probability can be used as metric of how clear the speech in this segment is, higher values are better. "
        "Think through it for a moment, then respond with the classification for the segment you are currently considering."
    )
    segment_filtering_intro = (
        "Here's a list of words, each labeled with a number. Your task is to review the list and identify any words that might need to be censored. "
        "Focus on filtering only explicit profanity, offensive language, or sensitive information if absolutely necessary.\n"
    )
    segment_filtering_prompt = (
        "Review the provided words and identify only those that should be censored. "
        "Censorship should apply strictly to the following categories:\n"
        "- Strong profanity or obscene language.\n"
        "- Explicit or highly offensive terms.\n"
        "- Sensitive personal information (e.g., full names, addresses, phone numbers).\n"
        "Do NOT censor regular conversational English words, including:\n"
        "- Mild negative words (e.g., 'dumb', 'stupid', 'kill', 'steal' in non-explicit contexts).\n"
        "- Informal expressions and slang that are not offensive.\n"
        "Respond with a list of word indices that should be censored, formatted as a Python list (e.g., [1, 3, 6]). "
        "If no words need to be censored, respond with an empty list: []."
    )
    song_selector_intro = "Here's a list of songs you can choose from to be background music for this part of the video. Your task is to pick the one best suited to the context and mood.\n"
    song_selector_prompt = "Think through it for a moment, then respond with the number associated with the song you would like to choose in the format [5] for example."
    mood_selector_intro = "Here's a list of music categories you can choose from to be background music for this part of the video. Your task is to pick the one best suited to the context and overall energy.\n"
    mood_selector_prompt = (
        "Each segment above has a corresponding music mood. "
        "To ensure a smooth viewing experience, avoid changing the mood too frequently. "
        "try to maintain the same mood for at least **5-20 segments** unless a significant shift in tone or energy justifies a change. "
        "Mood changes should feel **natural and intentional**, not abrupt or random. "
        "Prioritize consistency, but adapt when the pacing, energy, or emotions in the scene clearly call for a shift. "
        "When selecting a new mood, consider whether the previous mood is still appropriate. "
        "Think through it for a moment, then respond with the number associated with the mood you would like to choose in the format [0], and **only choose from the provided options**.\n"
    )
    description_generator = "Write a concise YouTube description that clearly explains what the video is about, using natural language. Avoid being cringy, inappropriate, or overly sensational. Incorporate relevant keywords for SEO and summarize key elements of the video without adding timestamps or fabricating specific moments. End with a brief call to action. Respond with only the description."