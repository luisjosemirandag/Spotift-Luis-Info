# Import pandas to read the csv
import pandas as pd

# Read the csv to get the artist already processed
all_dataset = pd.read_csv('Spotify project/Scrobber history plays/search_info_spotify.csv')

# Separate them in each variable
id_song = all_dataset.iloc[:,0]
id_artist = all_dataset.iloc[:,1]
id_album = all_dataset.iloc[:,2]

# Put the data in lists so it's easier to process
id_song_list = [id_song[x] for x in range(0,len(id_song))]
id_artist_list = [id_artist[x] for x in range(0,len(id_artist))]
id_album_list = [id_album[x] for x in range(0,len(id_album))]
