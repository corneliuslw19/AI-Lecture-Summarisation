# AI-Lecture-Summarisation 
This project processes English-language lecture recordings and generates
revision-oriented material using multiple pre-trained AI models.

The processing pipeline consists of:
1. OpenAI Whisper Base - speech-to-text transcription
2. BART-large-CNN - lecture summarisation
3. KeyBERT - key concept extraction
4. Structured revision-note generation
5. Tkinter graphical user interface

# REQUIREMENTS
- Python 3.11
- FFmpeg
- Python packages listed in requirements.txt

# INSTALLATION
Install the required Python packages using:

pip install -r requirements.txt

FFmpeg must also be installed separately and accessible from the system PATH.

RUNNING THE APPLICATION
Run:

python gui.py

Select a supported lecture audio file (MP3, WAV or M4A) and click
"Process Lecture".

# OUTPUT
The system generates the following files in the output folder:

- transcript.txt
- summary.txt
- key_concepts.txt
- revision_notes.txt
