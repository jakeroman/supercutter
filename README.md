# AI Video Editing Tool

Welcome to the AI Video Editing Tool! This project automates and streamlines video editing using AI, combining audio and video with modular flexibility. The tool leverages powerful hardware and advanced AI models to achieve optimal results.
Prerequisites

To get started, ensure you have the following:

    Powerful Hardware: High-performance CPU/GPU is required for smooth and efficient operation.
    Ollama: Install Ollama for AI model support.
    Python Environment:
        Ensure Python is installed on your system.
        Install dependencies using pipenv.

## Installation
1. Install Ollama

Follow the official documentation for installing and setting up Ollama on your machine.
2. Set Up Dependencies

Run the following commands to install the required Python packages:

pipenv install

Project Structure

This repository is organized as follows:

.
├── library
│   ├── audio
│   │   └── [custom folders for your audio files]
│   └── video
│       └── outro.mp4 (optional)
├── modules
│   ├── ai.py
│   ├── censor.py
│   ├── music.py
│   ├── prompts.py
│   ├── renderer.py
│   ├── segments.py
│   ├── transcribe.py
│   └── utils.py
├── temp
│   └── transcript.json
├── edit.py
├── Pipfile
├── Pipfile.lock
└── readme.md

    library/:
        audio/: Create custom folders to categorize your audio files. You can name the folders anything you like and have as many as you need.
        video/: Optionally include an outro video (e.g., outro.mp4) if you'd like to append it to the final video.
    modules/: Contains Python scripts for various functionalities, including transcription, rendering, and AI processing.
    temp/: Temporary files and generated outputs (e.g., transcripts).

## Usage
Step 1: Prepare Audio Library

    Organize your audio files under library/audio/ in any folder structure you prefer. For example:
        library/audio/mood1/
        library/audio/energetic/
        library/audio/custom_name/
    Add as many folders as you like, and name them however you want.

Step 2: Run the Project

Execute the edit.py script with your video file as an argument:

pipenv run python edit.py <video filename>

Example:

pipenv run python edit.py input_video.mp4

Step 3: Check Outputs

The generated video files and other outputs will appear in the appropriate directories.
Notes

    This project requires powerful hardware for optimal performance, especially for AI processing.
    Ensure that all dependencies are installed and your audio library is correctly structured for the best results.
    The outro.mp4 file in library/video/ is optional but can be used to append an outro to your final video.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.
## License

This project is licensed under the MIT License. See the LICENSE file for more details.