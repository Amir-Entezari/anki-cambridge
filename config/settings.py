import os.path
from os import getcwd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
AUDIO_DIR = os.path.join(MEDIA_DIR, 'audio')
