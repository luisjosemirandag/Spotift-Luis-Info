# import the library we use to open URLs
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
from unicodedata import normalize
import requests
# Pandas read csv
artist_info_csv = pd.read_csv('Spotify project/Spotify info/Artists/scrobber_info_spotify_artists.csv',encoding = "ISO-8859-1")

# Separate the values in variables
artist = artist_info_csv.iloc[:,1]
ids = artist_info_csv.iloc[:,0]

# Insert the column artust into a list so it's easier to process
artist_list = [artist[x] for x in range(0,len(artist))]
id_list = [ids[x] for x in range(0,len(ids))]
# Clean the ´ out of the input so it can be looked up in Wikipedia
artist_list_wiki = [normalize("NFD",artist_list[x]).encode("ascii","ignore").decode("ascii").title() for x in range(0,len(artist_list))]
# Number of artists
artist_length = len(artist_list_wiki)

# Both links to check
links = ["https://en.wikipedia.org/wiki/","https://www.grammy.com/search/"]

# Iterate the artists
for b in range(0,artist_length):
    artist_name = str(artist_list_wiki[b])
    # Specific hardcode for Tini because her Wikipedia page does not recognize her as Tini
    if artist_name == 'Tini':
        artist_name = 'Martina Stoessel'
    # Separate the spaces with _ so it can be looked up
    artist_name_mod = artist_name.replace(" ", "_")
    # The url plus the artist's name
    url = str(links[0]) + str(artist_name_mod)
    # Define variables
    global birthday
    global origin
    global city
    global birthday_split
    global origin_split
    global country
    # Try to see if it's a singer or a band by checking if the webpage has a class named birthday
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        birthday = soup.find(class_="bday").get_text()
    except:
        try:
            # Trying again but hardcoding singer because it could happen that it's an ambiguous search
            url += '_(singer)'
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, "lxml")
            birthday = soup.find(class_="bday").get_text()
        except:
            try:
                # Setting the url again as the beginning to treat the variable as a band
                url = str(links[0]) + str(artist_name_mod)
                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page, "lxml")
                origin_raw = soup.find(class_="infobox vcard plainlist").get_text()
            except:
                try:
                # Hardcoding band because the search can be ambiguous
                    url = str(links[0]) + str(artist_name_mod) + '_(band)'
                    page = urllib.request.urlopen(url)
                    soup = BeautifulSoup(page, "lxml")
                    origin_raw = soup.find(class_="infobox vcard plainlist").get_text()
                except:
                    continue
    # Some wikipages have a class for the occupation, so it can tell us if it's about a singer or a band
    try:
        description = soup.find(class_="role").get_text()
    except:
        try:
            description = soup.find(class_="shortdescription nomobile noexcerpt noprint searchaux").get_text()
        except:
            description = 'Not found'
    if 'singer' in description:
        band_singer = 'singer'
    elif 'Singer' in description:
        band_singer = 'singer'
    elif 'band' in description:
        band_singer = 'band'
    elif 'Band' in description:
        band_singer = 'band'
    elif 'dj' in description:
        band_singer = 'singer'
    elif 'DJ' in description:
        band_singer = 'singer'
    else:
        try:
            # Some wikipages don't have the description that we need, so if the birthday is a date, it's a singer
            birthday = soup.find(class_="bday").get_text()
            if len(birthday) == 10:
                band_singer = 'singer'
            else:
                band_singer = 'band'
            # Getting the all the text from the vcard on Wikipedia
            members_raw = soup.find(class_="infobox vcard plainlist").get_text()
            # Indexing the word 'members'
            members_index = members_raw.index('Members') + 8
            # Getting all the members
            members_cut = members_raw[members_index:]
            members_list = members_cut.split('\n')
            try:
                if len(members_list) > 1:
                    band_singer = 'band'
                else:
                    band_singer = 'singer'
            except:
                continue
        except:
            band_singer = 'band'
    # Let's get the variables we want out of the singers
    if band_singer == 'singer':
        try:
            #Let's get the origin out of a class named birthplace
            origin = soup.find(class_="birthplace").get_text()
            #Spitting the origin so we can get the city and the country in two different variables
            origin_split = origin.split(", ")
            country = origin_split[-1]
            city = origin_split[0:-1]
            city_fix = ''
            # Also let's split the birthday so we can get the day, month and year separately
            birthday_split = birthday.split("-")
        except:
            try:
                # Some wikipages don't have the class birthplace, so we look for that info in the card
                origin_raw = soup.find(class_="infobox vcard plainlist").get_text()
                # Looking for the words that cover the origin and get their indexes
                index_origin = origin_raw.find("(age") + 8
                index_genre = origin_raw.find('Genre')
                origin = origin_raw[index_origin:index_genre]
                # Removing the extra characters
                if origin[2] == ']':
                    origin = origin[3:]
                if origin[-1] == ']':
                    origin = origin[:-3]
                # Splitting the origin to separate the city and the country
                origin_split = origin.split(", ")
                country = origin_split[-1]
                city = origin_split[0:-1]
                city_fix = ''
                # Also let's split the birthday so we can get the day, month and year separately
                birthday_split = birthday.split("-")
            except:
                continue
        
        # Now let's move to the grammy's page
        url = str(links[1]) + str(artist_name_mod)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        # If the artist is not found, then it does not have any nominations
        try:
            global wins
            global nominations
            grammy_wins = soup.find(class_="group-artist-wins-noms field-group-div").get_text()
            grammy_wins_split = grammy_wins.split("\n")
            wins = int(grammy_wins_split[3])
            nominations = int(grammy_wins_split[-4])
        except:
            wins = 0
            nominations = 0
        # This is a function that returns the zodiac sign
        def astrology(month,day):
            if month == 12:
                astro_sign = 'Sagittarius' if (day < 22) else 'Capricorn'
            elif month == 1:
                astro_sign = 'Capricorn' if (day < 20) else 'Aquarius'
            elif month == 2:
                astro_sign = 'Aquarius' if (day < 19) else 'Pisces'
            elif month == 3:
                astro_sign = 'Pisces' if (day < 21) else 'Aries'
            elif month == 4:
                astro_sign = 'Aries' if (day < 20) else 'Taurus'
            elif month == 5:
                astro_sign = 'Taurus' if (day < 21) else 'Geminis'
            elif month == 6:
                astro_sign = 'Gemini' if (day < 21) else 'Cancer'
            elif month == 7:
                astro_sign = 'Cancer' if (day < 23) else 'Leo'
            elif month == 8:
                astro_sign = 'Leo' if (day < 23) else 'Virgo'
            elif month == 9:
                astro_sign = 'Virgo' if (day < 23) else 'Libra'
            elif month == 10:
                astro_sign = 'Libra' if (day < 23) else 'Scorpio'
            elif month == 11:
                astro_sign = 'Scorpio' if (day < 22) else 'Sagittarius'
            return astro_sign
        
        # This is a function that returns the age
        def calculateAge(dateofbirth): 
            today = date.today() 
            age = today.year - dateofbirth.year - ((today.month, today.day) < (dateofbirth.month, dateofbirth.day)) 
            return age

    # to insert everything in a csv file
    if band_singer == 'singer':
        a = open('Spotify project/Web artists info/artist_info_singers.csv', 'a')
        a.write(str(id_list[b]) + "," + str(artist_list[b]) + "," +
        str(calculateAge(date(int(birthday_split[0]),int(birthday_split[1]),int(birthday_split[2])))) + "," +
        str(country) + "," +
        str(birthday) + "," +
        str(astrology(int(birthday_split[1]),int(birthday_split[2])))+","+
        str(wins)+","+
        str(nominations)+'\n')
        a.close()


    # Now let's work for the bands:
    if band_singer == 'band':
        # Getting the all the text from the vcard on Wikipedia
        members_raw = soup.find(class_="infobox vcard plainlist").get_text()
        # Indexing the word 'members'
        members_index = members_raw.index('Members') + 8
        # Getting all the members
        members_cut = members_raw[members_index:]
        members_list = members_cut.split('\n')
        # The main member should be the first one
        main_member = members_list[0]
        # Getting the data from Wikipedia
        main_member_mod = main_member.replace(" ", "_")
        url = str(links[0]) + main_member_mod
        try:
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, "lxml")
            birthday = soup.find(class_="bday").get_text()
        except:
            try:
        # Trying again but hardcoding singer because it could happen that it's an ambiguous search
                url += '_(singer)'
                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page, "lxml")
                birthday = soup.find(class_="bday").get_text()
            except:
                birthday = 'NULL'
        try:
            #Let's get the origin out of a class named birthplace
            origin = soup.find(class_="birthplace").get_text()
            #Spitting the origin so we can get the city and the country in two different variables
            origin_split = origin.split(", ")
            country = origin_split[-1]
            city = origin_split[0:-1]
            city_fix = ''
            # Also let's split the birthday so we can get the day, month and year separately
            birthday_split = birthday.split("-")
        except:
            try:
                # Some wikipages don't have the class birthplace, so we look for that info in the card
                origin_raw = soup.find(class_="infobox vcard plainlist").get_text()
                # Looking for the words that cover the origin and get their indexes
                index_origin = origin_raw.find("(age") + 8
                index_genre = origin_raw.find('Genre')
                origin = origin_raw[index_origin:index_genre]
                # Removing the extra characters
                if origin[2] == ']':
                    origin = origin[3:]
                if origin[-1] == ']':
                    origin = origin[:-3]
                # Splitting the origin to separate the city and the country
                origin_split = origin.split(", ")
                country = origin_split[-1]
                city = origin_split[0:-1]
                city_fix = ''
                # Also let's split the birthday so we can get the day, month and year separately
                birthday_split = birthday.split("-")
            except:
                continue
            # Now let's move to the grammy's page
        
        url = str(links[1]) + str(artist_name_mod)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        # If the artist is not found, then it does not have any nominations
        try:
            grammy_wins = soup.find(class_="group-artist-wins-noms field-group-div").get_text()
            grammy_wins_split = grammy_wins.split("\n")
            wins = int(grammy_wins_split[3])
            nominations = int(grammy_wins_split[-4])
        except:
            wins = 0
            nominations = 0
        # This is a function that returns the zodiac sign
        try:
            def astrology(month,day):
                if month == 12:
                    astro_sign = 'Sagittarius' if (day < 22) else 'Capricorn'
                elif month == 1:
                    astro_sign = 'Capricorn' if (day < 20) else 'Aquarius'
                elif month == 2:
                    astro_sign = 'Aquarius' if (day < 19) else 'Pisces'
                elif month == 3:
                    astro_sign = 'Pisces' if (day < 21) else 'Aries'
                elif month == 4:
                    astro_sign = 'Aries' if (day < 20) else 'Taurus'
                elif month == 5:
                    astro_sign = 'Taurus' if (day < 21) else 'Geminis'
                elif month == 6:
                    astro_sign = 'Gemini' if (day < 21) else 'Cancer'
                elif month == 7:
                    astro_sign = 'Cancer' if (day < 23) else 'Leo'
                elif month == 8:
                    astro_sign = 'Leo' if (day < 23) else 'Virgo'
                elif month == 9:
                    astro_sign = 'Virgo' if (day < 23) else 'Libra'
                elif month == 10:
                    astro_sign = 'Libra' if (day < 23) else 'Scorpio'
                elif month == 11:
                    astro_sign = 'Scorpio' if (day < 22) else 'Sagittarius'
                return astro_sign
        except:
            continue
        
        # This is a function that returns the age
        try:
            def calculateAge(dateofbirth):
                today = date.today() 
                age = today.year - dateofbirth.year - ((today.month, today.day) < (dateofbirth.month, dateofbirth.day)) 
                return age
        except:
            continue

        try:
            age_of_the_artist = str(calculateAge(date(int(birthday_split[0]),int(birthday_split[1]),int(birthday_split[2]))))
            astrology_of_the_artist = str(astrology(int(birthday_split[1]),int(birthday_split[2])))
        except:
            age_of_the_artist = 'NULL'
            astrology_of_the_artist = 'NULL'
        # to insert everything in a csv file
    if band_singer == 'band':
        a = open('Spotify project/Web artists info/artist_info_bands.csv', 'a')
        a.write(str(id_list[b]) + "," + str(artist_list[b]) + "," +
        str(main_member) + "," + 
        age_of_the_artist + "," +
        str(country) + "," +
        str(birthday) + "," +
        astrology_of_the_artist +","+
        str(wins)+","+
        str(nominations)+'\n')
        a.close()