# import libraries
import http
import requests
import pandas as pd
import codecs
# Read de songs ids csv
song = pd.read_csv('Spotify project/Scrobber history plays/search_info_spotify.csv')
# Separate the csv in the columns in need
song_id = song.iloc[:,0]

# Insert the column artust into a list so it's easier to process
song_id_list = [song_id[x] for x in range(0,len(song_id))]

# Remove the duplicates from the list song_id_list
song_id_list = list(dict.fromkeys(song_id_list))
# Creating an int for the number of items on the list
song_length = len(song_id_list)

# Declare the current index so it's easier to re-execute
a = open('Spotify project/Spotify info/Songs/current_index.txt','r')
current_index = int(a.read())

try:
    # Use the separated data to look for in Spotify's web API
    for x in range(0,song_length):
        # to declare the header and parameters for the spotify's http look up
        # it may be necessary to update the token
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer BQAEcvXIOznwAIQ8Fwycvfy90F-lI3W9FbP2Zg5JWR86JOsnInTbJ9e83x_gL21W6tMTmk2w_NfPz-Pgbp_Uis4Bo6WYRvekhaLCT1Fo65d6p4q1MUzOi-TZxAN1AA1ZRkv6EHFWCqCCIW-LxuevnWp8Z_x-OL4AePJw4Zvx11aTsd-sZMLOxpbJrrAAAZFpiDrhXXnJXpWXRkjBfxf7htbxJAXJLw8NXyL6qmyf9PpDxBAVDwR2tWcccI2HGpmf4LpdED8IZ08OdLsJyAdUsYHpLn8_-bvP3w',
        }
        
        # The page with the id defined:

        web_with_id = str("https://api.spotify.com/v1/tracks/")+str(song_id_list[x])+str('?market=AR')

        # request the info's page
        pagina = requests.get(web_with_id,headers=headers)

        # turn it into a json file so python reads it as dictionaries
        pagina_data = pagina.json()
        
        # song's attributes
        song_name = pagina_data.get("name")
        song_popularity = pagina_data.get("popularity")

        # Function to get the genre of the artist:
        
        def song_picture(page):
            images_1 = pagina_data.get("album")
            images_2 = images_1.get("images")
            images_3 = images_2[0]
            images_final = images_3.get("url")
            return images_final

        headers_2 = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer BQAEcvXIOznwAIQ8Fwycvfy90F-lI3W9FbP2Zg5JWR86JOsnInTbJ9e83x_gL21W6tMTmk2w_NfPz-Pgbp_Uis4Bo6WYRvekhaLCT1Fo65d6p4q1MUzOi-TZxAN1AA1ZRkv6EHFWCqCCIW-LxuevnWp8Z_x-OL4AePJw4Zvx11aTsd-sZMLOxpbJrrAAAZFpiDrhXXnJXpWXRkjBfxf7htbxJAXJLw8NXyL6qmyf9PpDxBAVDwR2tWcccI2HGpmf4LpdED8IZ08OdLsJyAdUsYHpLn8_-bvP3w',
        }
        
        # The page with the id defined:

        web_with_id_2 = str("https://api.spotify.com/v1/audio-features/")+str(song_id_list[x])

        # request the info's page
        pagina_2 = requests.get(web_with_id_2,headers=headers_2)

        # turn it into a json file so python reads it as dictionaries
        pagina_data_2 = pagina_2.json()

        # song's attributes
        song_danceability = pagina_data_2.get("danceability")
        song_energy = pagina_data_2.get("energy")
        song_liveness = pagina_data_2.get("liveness")
        song_duration_ms = pagina_data_2.get("duration_ms")

        # write all in a csv file
        b = open('Spotify project/Spotify info/Songs/scrobber_info_spotify_songs.csv', 'a',encoding='utf-8')
        b.write(
        str(song_id_list[x]) + "," +
        str(song_name) + ", " +
        str(song_popularity) + "," +
        str(song_danceability) + "," +
        str(song_energy) + "," +
        str(song_liveness) + "," + 
        str(song_duration_ms) + "," + 
        str(song_picture(pagina_data)) + '\n')
        b.close()
except:
    f = open('Spotify project/Spotify info/Songs/current_index.txt','w')
    f.write(str(x))
    f.close()
    a.close()

a.close()
c = open('Spotify project/Spotify info/Songs/current_index.txt','w')
c.write('0')
c.close()