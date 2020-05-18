# import libraries
import pandas as pd
import statistics as stats

artist_listened = pd.read_csv('Projects/Spotify project/final_join.csv')

artist_nm_px = artist_listened.iloc[:,11]
artist_name = artist_listened.iloc[:,19].dropna().reset_index().iloc[:,1]
artist_name_nan = artist_listened.iloc[:,19]
main_band = artist_listened.iloc[:,27]
artist_age = artist_listened.iloc[:,20].dropna().reset_index().iloc[:,1] 
artist_zodiac = artist_listened.iloc[:,23].dropna().reset_index().iloc[:,1]
artist_zodiac_nan = artist_listened.iloc[:,23]
band_age = artist_listened.iloc[:,-6].dropna().reset_index().iloc[:,1]
band_zodiac = artist_listened.iloc[:,31].dropna().reset_index().iloc[:,1]
band_zodiac_nan = artist_listened.iloc[:,31]
artist_px = artist_listened.iloc[:,14]
len_age = range(0,len(band_age))
len_zodiac = range(0,len(band_zodiac))

artist_dict = [{'artist':artist_name_nan[x],'sign':artist_zodiac_nan[x]} for x in range(0,len(artist_name))]
band_dict = [{'artist':main_band[x],'sign':band_zodiac_nan[x]} for x in range(0,len(main_band))]
artist_age_list = [int(artist_age[x]) for x in range(0,len(artist_age))]
artist_zodiac_list = [artist_zodiac[x] for x in range(0,len(artist_zodiac))]
band_age_list = [int(band_age[x]) for x in len_age]
band_zodiac_list = [band_zodiac[x] for x in len_zodiac]
artist_px_list = [{'artist':artist_nm_px[x],'picture':artist_px[x]} for x in range(0,len(artist_px))]
ages = artist_age_list + band_age_list
zodiacs = artist_zodiac_list + band_zodiac_list
artists = artist_dict + band_dict

ages_avg = int(round(stats.mean(ages),0))
zodiacs_top = str(stats.mode(zodiacs))

artist_top_sign = [artists[x]['artist'] for x in range(0,len(artists)) if artists[x]['sign'] == zodiacs_top]
artist_top = str(stats.mode(artist_top_sign))
artist_top_pic = [artist_px_list[x]['picture'] for x in range(0,len(artist_px_list)) if artist_px_list[x]['artist'] == artist_top][0]

f = open("Projects/Spotify project/Web artists info/sign_age_top.csv","w")
f.write("artist_top_age,artist_mode_zodiac,top_artist_sign,top_artist_pic\n"+str(ages_avg)+","+zodiacs_top+","+artist_top+","+artist_top_pic)
f.close