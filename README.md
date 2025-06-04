# Plotting GDP Data on a World Map - Part 2

This project focuses on enhancing the quality of world map GDP plots created with Pygal by improving the mapping between Pygal country codes and World Bank country
names. The goal is to use multiple data sources to resolve discrepancies, clean data, and unify conflicting information. We will gain experience working with
multiple dictionaries and handling real-world data integration challenges.

------

# Project description

The project consists of multiple problems. Each problem will utilize functions you wrote for the previous problems. You can also download all of the files used when testing your code as a zip file.

### Working with the CSV Files
As with the last project, we will again use a gdpinfo dictionary to specify information about the GDP data file. The gdpinfo dictionary is exactly the same as before and contains the following keys, all of which are strings (the use of these keys will become apparent as you work on the project, you may want to refer back to this information as you work on the different parts of the project):

🔹"gdpfile": the name of the CSV file that contains GDP data.
🔹"separator": the delimiter character used in the CSV file.
🔹"quote": the quote character used in the CSV file.
🔹"min_year": the oldest year for which there is data in the CSV file.
🔹"max_year": the most recent year for which there is data in the CSV file.
🔹"country_name": the name of the column header for the country names.
🔹"country_code": the name of the column header for the country codes.

If you look in the template file, you will see an example of such an "gdpinfo" dictionary that is used to access the GDP data from the World Bank discussed above.

As the format of the CSV file that stores the country codes could change (or you could acquire data from somewhere else), the functions that operate directly on the country code data will all take a "codeinfo" dictionary that provides information about the file. That way, you do not need to use constants within your code to access the CSV file and their columns. The codeinfo dictionary contains the following keys, all of which are strings (the use of these keys will become apparent as you work on the project, you may want to refer back to this information as you work on the different parts of the project):

🔹"codefile": the name of the CSV file that contains country codes.
🔹"separator": the delimiter character used in the CSV file.
🔹"quote": the quote character used in the CSV file.
🔹"plot_codes": the name of the column header that holds the country codes used by the plot library.
🔹"data_codes": the name of the column header that holds the country codes used by the GDP data.

### Problem 1: Generate a dictionary that maps different country codes to each other
The main task of this project is to process the World Bank GDP data and build a Pygal map dictionary whose values represented the GDP data for a given year. In this week's version of the project, the key step in this process is reconciling Pygal country codes/names with the World Bank country codes. In order to do this, you will first write a function called build_country_code_converter that takes codeinfo, a country code info dictionary, and returns a dictionary that maps plot country codes to data country codes.

### Problem 2: Create a dictionary that maps Pygal country codes to World Bank country codes
Next, you first must write a function called reconcile_countries_by_code which takes codeinfo, a country code information dictionary, plot_countries, a dictionary mapping country codes used by a plot library (such as Pygal) to the corresponding country name, and gdp_countries, a dictionary whose keys are the country codes used within the GDP data. The values in the gdp_countries dictionary are irrelevant for this function, but presumably contain GDP data for each country. The 
reconcile_countries_by_code function should return a dictionary and a set. The dictionary should map the country codes from plot_countries to country codes from 
gdp_countries that correspond to the same country (given the country code equivalencies specified by codeinfo). It should not contain key-value pairs for the countries within plot_countries that do not appear in gdp_countries. The set should contain all of the country codes within plot_countries that did not match any countries in gdp_countries, so is effectively the set of countries that the plot library knows about but cannot be found within the GDP data.

### Problem 3: Transform GDP data for given year into a form suitable for a world map plot
Your next task is to implement the main function that processes GDP data. You must write a function called build_map_dict_by_code which takes gdpinfo, a GDP information dictionary (as used in the previous projects), codeinfo, a country code information dictionary, plot_countries, a dictionary mapping country codes used by a plot library (such as Pygal) to the corresponding country name, and year, the year for which to create a GDP map dictionary, expressed as a string. The 
build_map_dict_by_code function should return a dictionary and two sets. The dictionary should map the country codes from plot_countries to the log (base 10) ofthe GDP for the associated country in the given year. (The logarithmic scaling is chosen to yield a better distribution of color shades in the final plot.) The first set should contain the country codes from plot_countries that were not found in the GDP data file. The second set contains the country codes from plot_countries that were found in the GDP data file, but have no GDP information for the specified year.

### Problem 4: Create an SVG image of the GDP data plotted on the world map
As the final part of this project, your task is to write a function that takes the GDP map information computed using build_map_dict_by_code and create a world map plot using Pygal. You should write a function called render_world_map which takes gdpinfo, a GDP information dictionary, codeinfo, a country code information dictionary, plot_countries, a dictionary mapping country codes used by Pygal to the corresponding country name, and year, the string year for which to create a GDP map dictionary, and map_file, the string name of the file to write the output plot to.

Using these inputs, you should use Pygal to plot the logarithmically-scaled GDP data on a world map. Review Pygal's documentation on world maps for more details. Make sure that you plot not only the GDP data, but also the countries which are missing from the GDP data entirely and the countries that are contained within the GDP data, but have no data for the given year.

The output plot should be stored in an SVG file with the name specified by the map_file input.

# Key features

1. Use GDP and country code CSV files with flexible formats.
2. Build a converter from Pygal codes to GDP data codes.
3. Match Pygal country codes with GDP data codes.
4. Create a log-scaled GDP dictionary by country for a given year.
5. Generate an SVG world map showing GDP data using Pygal.


------------





