import argparse
import os

import spotipy
import spotipy.util as spotipy_util

import utils

output_separator = '‖'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('spotify_username')
    parser.add_argument('dir')
    args = parser.parse_args()

    print(f'getting music from {args.dir}')
    music = {}
    for file_path in utils.get_music_files(args.dir):
        artist, title = utils.get_artist_title(file_path)
        print(file_path, artist, title, sep=output_separator)

        if artist not in music:
            music[artist] = []
        music[artist].append(title)

    print('connecting to spotify')
    spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
    spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    spotify_redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']
    token = spotipy_util.prompt_for_user_token(
        args.spotify_username,
        scope='user-read-private',
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri=spotify_redirect_uri
    )
    spotify = spotipy.Spotify(auth=token)

    print('querying spotify data to start radios from')
    artist_uris = []
    track_uris = []
    for artist in music.keys():
        results = spotify.search(q='artist:' + artist, type='artist')
        for item in results['artists']['items']:
            artist_uri = item['uri']
            spotify_url = item['external_urls']['spotify']
            print(artist, artist_uri, spotify_url, sep=output_separator)
            artist_uris.append(artist_uri)

    print('getting recommendations')
    results = spotify.recommendations(
        seed_artists=artist_uris,
        seed_tracks=track_uris
    )
    for track in results['tracks']:
        artists = ', '.join([artist['name'] for artist in track['artists']])
        album = track['album']['name']
        track_name = track['name']
        spotify_url = track['external_urls']['spotify']
        print(artists, album, track_name, spotify_url, sep=output_separator)


if __name__ == '__main__':
    main()
