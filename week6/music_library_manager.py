print("\nWelcome to Music Library Manager!")

song_list = []
genre_count = {}

for i in range(1,6,1):
    print(f"\n- Enter Song {i} -")
    song_name = input("Song name: ")
    genre = input("Genre: ")

    song_tuple = (song_name, genre)   # what makes a tuple is the comma (,) so no parantheses could also work here.
    song_list.append(song_tuple)
    genre_count[genre] = genre_count.get(genre, 0) + 1

print("\n=== YOUR MUSIC LIBRARY ===\n")
for i in range(0,5,1):
    print(f"{i+1}. {song_list[i][0]} ({song_list[i][1]})")

print("\n=== GENRE STATISTICS ===\n")
for genre_name, genre_sum in genre_count.items():  #first variable in for loop of a dict always gets the keyname. 
    print(f"{genre_name}: {genre_sum} songs")

most_popular = max(genre_count, key=genre_count.get)    # "key" is a built-in setting for max() function. It has to be like that. Can't be changed to another name. 
print(f"\nMost popular genre: {most_popular}\n")

'''
- max(genre_count, key=genre_count.get) --> returns the dict key that has the max value in the dictionary genre_count. 
- IF the value is tied, max() will return the one it saw FIRST.
- "keys= " tells max() to calculate the dictionary value instead of the dict keys. 
- Without "keys", max() sort the highest/furthest genre names alphabetically (if the keys are in strings).
'''