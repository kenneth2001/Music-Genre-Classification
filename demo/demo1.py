import spotipy
SPOTIFY_CLIENT_ID = 
SPOTIFY_CLIENT_SECRET = 

# Create Spotify Search Engine object
def get_spotify_engine(client_id, client_secret):
    return spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# fetch song information from spotify
def fetch_song_info(sp, song_name):
    results = sp.search(q=song_name, type='track')
    items = results['tracks']['items']
    
    album_genre = sp.album(items[0]["album"]["external_urls"]["spotify"])['genres']
    artist_genre = sp.artist(items[0]["artists"][0]["external_urls"]["spotify"])['genres']
    print(f"Song Name: {items[0]['name']}")
    print(f"Song Artist: {items[0]['artists'][0]['name']}")
    print(f"Song Album: {items[0]['album']['name']}")
    print(f"Album Genre: {album_genre}")
    print(f"Artist Genre: {artist_genre}")
    print(f"Track id: {items[0]['id']}")
    print("-- -- -- -- -- -- --")
    
    features = sp.audio_features(tracks = items[0]['id'])
    print(f"Danceability: {features[0]['danceability']}")
    print(f"Energy: {features[0]['energy']}")
    print(f"Key: {features[0]['key']}")
    print(f"Lounness: {features[0]['loudness']}")
    print(f"Mode: {features[0]['mode']}")
    print(f"Speechiness: {features[0]['speechiness']}")
    print(f"Acousticness: {features[0]['acousticness']}")
    print(f"Instrumentalness: {features[0]['instrumentalness']}")
    print(f"Liveness: {features[0]['liveness']}")
    print(f"Valence: {features[0]['valence']}")
    print(f"Tempo: {features[0]['tempo']}")
    print(f"Duration: {features[0]['duration_ms']//1000}s")
    print(f"Time signature: {features[0]['time_signature']}")

print('This program helps fetch song metadata using Spotify API')
songname = input("Please enter the name of the song: ")    

print("")

sp = get_spotify_engine(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
fetch_song_info(sp, songname)