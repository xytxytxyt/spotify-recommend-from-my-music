import argparse

import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir')
    args = parser.parse_args()
    for file_path in utils.get_music_files(args.dir):
        artist, title = utils.get_artist_title(file_path)
        print(file_path, artist, title)


if __name__ == '__main__':
    main()
