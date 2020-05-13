# import libraries
import http
import requests
import pandas as pd

# Read de last.fm csv
songs_listened = pd.read_csv('Spotify project/Raw csv/Luisjosemiran.csv')

# Separate the csv in the columns in need
artist = songs_listened.iloc[:,0]
album = songs_listened.iloc[:,1]
song = songs_listened.iloc[:,2]
datetime_listened = songs_listened.iloc[:,-1]

# Insert the columns into lists so it's easier to separate
artist_list = [artist[x] for x in range(0,len(artist))]
album_list = [album[x] for x in range(0,len(album))]
song_list = [song[x] for x in range(0,len(song))]
datetime_list = [datetime_listened[x] for x in range(0,len(datetime_listened))]
artist_length = len(artist_list)

# Declare the current index so it's easier to re-execute
a = open('Spotify project/Scrobber history plays/current_index.txt','r')
current_index = int(a.read())

if current_index == 0:
    # Overwrite the csv output file to only the firts row that indicates the columns
    b = open('Spotify project/Scrobber history plays/search_info_spotify.csv', 'w')
    b.write('id_song,id_artist,id_album,datetime\n')
    b.close()


try:
    # Use the separated data to look for in Spotify's web API
    for x in range(current_index,artist_length):
        # to declare the header and parameters for the spotify's http look up
        # it may be necessary to update the token
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer BQAN54Zq-afCNnJRF87uNrVi1Xv3prZyDAry9aj62Zu42MChoMN1dI6dR90Y8a6pvB2skLurcRll_l3XctDmGeTT13Acz_iYxEsb4kms8-grCkOBt6trxgojiRoYDJ538V749accYHMvM_WvmkYdfTJGKeI6pd-xiJJgP1f1KVjMuIoIKkFaNTo6y3FQ4_l7mwEvrIO0J4cjZzLL4UTYlRYyGua7WYI21oXBfKxH-BzrKQa5KN8xVlZULNL7Nft43vhCmU90ZO77A3drRrPAkJOEGmTYSBjGrg',
        }
        params = (
            ('q', str(song_list[x])+", "+str(artist_list[x])),
            ('type', 'track,artist'),
            ('market', 'AR'),
            ('limit','1'))

        # request the info's page
        pagina = requests.get("https://api.spotify.com/v1/search",headers=headers,params=params)

        # turn it into a json file so python reads it as dictionaries
        pagina_data = pagina.json()

        #these functions return the ids spotify uses to get more data out of it
        def id_song(song):
            id_1 = pagina_data.get('tracks')
            id_2 = id_1.get('items')
            id_3 = id_2[0]
            id_4 = id_3.get('id')
            return id_4

        def id_artist(artist):
            id_1 = pagina_data.get('tracks')
            id_2 = id_1.get('items')
            id_3 = id_2[0]
            id_4 = id_3.get('artists')
            id_5 = id_4[0]
            id_6 = id_5.get('id')
            return id_6

        def id_album(album):
            id_1 = pagina_data.get('tracks')
            id_2 = id_1.get('items')
            id_3 = id_2[0]
            id_4 = id_3.get('album')
            id_5 = id_4.get('id')
            return id_5

        # write all in a csv file
        b = open('Spotify project/Scrobber history plays/search_info_spotify.csv', 'a')
        b.write(
        str(id_song(pagina_data)) + "," +
        str(id_artist(pagina_data)) + "," +
        str(id_album(pagina_data)) + "," + str(datetime_list[x] + '\n'))
        b.close()
except:
    f = open('Spotify project/Scrobber history plays/current_index.txt','w')
    f.write(str(x))
    f.close()
    a.close()

a.close()
c = open('Spotify project/Scrobber history plays/current_index.txt','w')
c.write('0')
c.close()