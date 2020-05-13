# import libraries
import http
import requests
import pandas as pd
# Read de artist ids csv
artist = pd.read_csv('Spotify project/Scrobber history plays/search_info_spotify.csv')
# Separate the csv in the columns in need
artist_id = artist.iloc[:,1]

# Insert the column artust into a list so it's easier to process
artist_id_list = [artist_id[x] for x in range(0,len(artist_id))]

# Remove the duplicates from the list artist_id_list
artist_id_list = list(dict.fromkeys(artist_id_list))
# Creating an int for the number of items on the list
artist_length = len(artist_id_list)

# Use the separated data to look for in Spotify's web API
for x in range(0,artist_length):
    # to declare the header and parameters for the spotify's http look up
    # it may be necessary to update the token
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer BQAN54Zq-afCNnJRF87uNrVi1Xv3prZyDAry9aj62Zu42MChoMN1dI6dR90Y8a6pvB2skLurcRll_l3XctDmGeTT13Acz_iYxEsb4kms8-grCkOBt6trxgojiRoYDJ538V749accYHMvM_WvmkYdfTJGKeI6pd-xiJJgP1f1KVjMuIoIKkFaNTo6y3FQ4_l7mwEvrIO0J4cjZzLL4UTYlRYyGua7WYI21oXBfKxH-BzrKQa5KN8xVlZULNL7Nft43vhCmU90ZO77A3drRrPAkJOEGmTYSBjGrg',
    }
    
    # The page with the id defined:

    web_with_id = str("https://api.spotify.com/v1/artists/")+str(artist_id_list[x])

    # request the info's page
    pagina = requests.get(web_with_id,headers=headers)

    # turn it into a json file so python reads it as dictionaries
    pagina_data = pagina.json()
    
    # artist's name
    artist_name = pagina_data.get("name")
    artist_popularity = pagina_data.get("popularity")

    # Function to get the genre of the artist:
    def genre(page):
        genre_1 = pagina_data.get("genres")
        try:
            genre_final = genre_1[0]
            return genre_final
        except:
            genre_final = 'NULL'
    
    def artist_picture(page):
        images_1 = pagina_data.get("images")
        images_2 = images_1[0]
        images_final = images_2.get("url")
        return images_final

    # write all in a csv file
    b = open('Spotify project/Spotify info/Artists/scrobber_info_spotify_artists.csv', 'a')
    b.write(
    str(artist_id_list[x]) + "," +
    str(artist_name) + "," +
    str(artist_popularity) + "," +
    str(genre(pagina_data)) + "," +
    str(artist_picture(pagina_data)) + '\n')
    b.close()
