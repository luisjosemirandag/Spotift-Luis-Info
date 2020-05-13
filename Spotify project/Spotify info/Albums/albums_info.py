# import libraries
import http
import requests
import pandas as pd
import codecs
# Read de songs ids csv
albums = pd.read_csv('Spotify project/Scrobber history plays/search_info_spotify.csv')
# Separate the csv in the columns in need
albums_id = albums.iloc[:,2]

# Insert the column artust into a list so it's easier to process
albums_id_list = [albums_id[x] for x in range(0,len(albums_id))]

# Remove the duplicates from the list song_id_list
albums_id_list = list(dict.fromkeys(albums_id_list))
# Creating an int for the number of items on the list
album_length = len(albums_id_list)

# Declare the current index so it's easier to re-execute
a = open('Spotify project/Spotify info/Albums/current_index.txt','r')
current_index = int(a.read())

try:
    # Use the separated data to look for in Spotify's web API
    for x in range(current_index,album_length):
        # to declare the header and parameters for the spotify's http look up
        # it may be necessary to update the token
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer BQDIdIjTTdz8gO-8Lzm9JP74dS_oD2CkdD6iLBr11ogHdb5syB3fQeg4UJLoJJFPf958-hcoa6sEysLZERW-RlcWr5KFYTxJWmwhXJSgmr9Cn3DlIWF_co4LhW-X0HrqysttY1cjX43jHjhS1F0oGPg3Zu7No_8Yk7Wnfg17kGKHC5gWsjcEUxgDP3Ax33IjMpbXbNRATmNQTj4148TwiwmcfFcVsEm2jkdaF5yUR-qnZOV0d7txPlSwtz6HBWoQoNaf8Dho0CJ6YB4g984BpQjp_4X6GZL4hQ',
        }
        
        # The page with the id defined:

        web_with_id = str("https://api.spotify.com/v1/albums/")+str(albums_id_list[x])+str('?market=AR')

        # request the info's page
        pagina = requests.get(web_with_id,headers=headers)

        # turn it into a json file so python reads it as dictionaries
        pagina_data = pagina.json()
        
        # album's attributes
        album_name = pagina_data.get('name')
        if ',' in album_name:
            album_name = album_name.replace(',','')
        album_popularity = pagina_data.get('popularity')
        album_release_date = pagina_data.get('release_date')

        # Function to get the genre of the artist:
        
        def album_picture(page):
            images_1 = pagina_data.get("images")
            images_3 = images_2[0]
            images_final = images_3.get("url")
            return images_final

        # write all in a csv file
        b = open('Spotify project/Spotify info/Albums/scrobber_info_spotify_albums.csv', 'a',encoding='utf-8')
        b.write(
        str(albums_id[x]) + "," +
        str(album_name) + ", " +
        str(album_popularity) + "," +
        str(album_release_date) + "," +
        str(album_picture(pagina_data)) + '\n')
        b.close()
except:
    f = open('Spotify project/Spotify info/Albums/current_index.txt','w')
    f.write(str(x))
    f.close()
    a.close()

a.close()
c = open('Spotify project/Spotify info/Albums/current_index.txt','w')
c.write('0')
c.close()
