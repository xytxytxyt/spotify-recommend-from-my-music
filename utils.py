import os
from tinytag import TinyTag

supported_extensions = [
    'mp3',
]


def get_music_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if any([filename.endswith(f'.{ext}') for ext in supported_extensions]):
                yield os.path.join(root, filename)


def get_artist_title(file_path):
    tag = TinyTag.get(file_path)
    return tag.artist, tag.title
