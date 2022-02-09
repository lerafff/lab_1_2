# Lab_1_2

# Introduction
Our task was to make a map with at least three layers on
the map. By Argparse we get desired year of films, point where we should
start (lattitude and longtitude) and path to the file with information.
The program works with a file full of names of films,
years, locations and additional information. I used for it file 
like on the site (locations.list), for documentation I made smaller 
file.
Finally we get map with location markers that indicate 10 nearest locations where 
the films of a certain year were filmed

## Functions description
``` diff
-  Function to get info by argparse input_user()  
```

User inputs information in such an order: year, lattitude, longtitude, path to the file
(example below)
``` python 
>>> python main.py 2017 50.000678 -86.000977 1.txt
```
This function return all this info

``` diff
-  Function to read info from entered file read_file(path_file, entered_year)
```
We get path and year, and read all file. But as we know, it has a lot of extra information
for us, so we process information and get only useful things for us

```python 
>>> for i in range(len(one_string[0])):
        if one_string[0][i] == '(':
            name_film = one_string[0][:i].strip()
```
As a result we will get list with smaller lists that include name, year and location of the film
(like at example)
``` python 
['#Hashtag Travel UK', 2017, 'England, UK']
```
 
``` diff
-  Function finds locations of the films find_location(list_data)
```
Function gets list with info from previous one and converts locations to lattitude and longtitude, 
then make a tupple with it and appends to info
We do it in such a way 
``` python 
location = Nominatim(user_agent='app_name').geocode(tupple[-1])
```
But we have extra cases, when module can`t find the location, then I just remove first part
of the location and try again. Let's have a look at the example. As we can see, at first part of the location we have a mistake, so we remove it
##### BronsФon Canyon, Griffith Park - 4730 Crystal Springs Drive, Los Angeles, California, USA -> Griffith Park - 4730 Crystal Springs Drive, Los Angeles, California, USA
It helps us to be correct and accurate as far as possible
``` python
['#Mittelfingerspitzengehl', 2017, 'Germany'], (51.0834196, 10.4234469)]
```
This function returns all previous information plus tupple with lattitude and longtitude

``` diff
- Function finds distance between location of the user and film location find_distance(loc, lattitude, longtitude)
```
 
The function gets all info and works with lattitude and longtitude, as a result we get distance and append it to all previous info
 ``` python 
 distance = geodesic(first_point, second_point).kilometers
 ```
 And then we sort all films with lambda by distance, and return 10 films that have smallest distance. 
 Our function returns list with such elements
 ``` python
 ([['#Murder', 2017, 'Knoxville, Tennessee, USA'], (35.9603948, -83.9210261)], 1568.8069021285557)
 ```
``` diff
- Function makes map with three layers and markers mapp(list_with_all, lattitude, longtitude)
```
This function gets all info and adds markers with short information about film
``` diff
- Function makes map with three layers and markers mapp(list_with_all, lattitude, longtitude)
```
The main function that includes all previous


## Conclusion

___This task was really interesting and useful, because I have learn a lot of new information about making maps with markers and approved my skills of working with big data. Also I had some problems with reading data file and finding locations which had mistakes in name, but I learnt how to cope with that and how to fix, so it was a cool experience___

