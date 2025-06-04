"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.


"""

import csv
import math
import pygal


# --- Helper functions from previous weeks ---

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file. The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            table[row[keyfield]] = row
    return table


# --- Week 4 Project Functions ---

def read_csv_file(file_name, separator, quote):
    """
    Given a CSV file, read the data into a nested list.
    Input: String corresponding to comma-separated CSV file
    Output: Nested list consisting of the fields in the CSV file
    """
    with open(file_name, 'r', newline='', encoding='utf-8') as csv_file:
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=separator, quotechar=quote)
        for row in csv_reader:
            csv_table.append(row)
    return csv_table


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    joined_codes = {}
    reader = read_csv_file(codeinfo["codefile"], codeinfo["separator"],
                           codeinfo["quote"])

    # Find column indices for plot codes and data codes from header
    header = reader[0]
    plot_code_idx = header.index(codeinfo["plot_codes"])
    data_code_idx = header.index(codeinfo["data_codes"])

    # Iterate through data rows (skipping header)
    for row in reader[1:]:
        plot_code = row[plot_code_idx]
        data_code = row[data_code_idx]
        if plot_code and data_code: # Ensure codes are not empty
            joined_codes[plot_code] = data_code
    return joined_codes


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set. The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries. The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way. However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    matched_plot_to_gdp_codes = {}
    unmatched_plot_codes = set()

    # Build a converter from plot codes to World Bank (data) codes (original casing)
    original_plot_to_data_converter = build_country_code_converter(codeinfo)

    # Create a lowercase version of the converter for case-insensitive lookup
    plot_to_data_converter_lower_keys = {
        k.lower(): v for k, v in original_plot_to_data_converter.items()
    }

    # Create a reverse lookup for gdp_countries: lowercase World Bank code to original World Bank code
    gdp_code_lower_to_original_map = {
        gdp_code.lower(): gdp_code for gdp_code in gdp_countries.keys()
    }

    for plot_code_orig, _ in plot_countries.items(): # Used '_' for unused plot_country_name
        # Get the World Bank data code corresponding to the plot code
        # Use lowercase plot_code_orig for lookup in the lowercase-keyed converter
        data_code_from_plot_map_orig = plot_to_data_converter_lower_keys.get(plot_code_orig.lower())

        if data_code_from_plot_map_orig:
            # Check if this World Bank code exists in the gdp_countries (case-insensitive)
            if data_code_from_plot_map_orig.lower() in gdp_code_lower_to_original_map:
                # Get the original casing of the GDP country code from gdp_countries
                gdp_code_actual_case = \
                    gdp_code_lower_to_original_map[data_code_from_plot_map_orig.lower()]
                matched_plot_to_gdp_codes[plot_code_orig] = gdp_code_actual_case
            else:
                unmatched_plot_codes.add(plot_code_orig)
        else:
            unmatched_plot_codes.add(plot_code_orig)

    return (matched_plot_to_gdp_codes, unmatched_plot_codes)


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets. The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year. The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file. The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_data_map = {}
    missing_from_gdp_file = set()
    no_gdp_data_for_year = set()

    # 1. Read all GDP data, keyed by World Bank Country Code
    all_gdp_data_by_code = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                                   gdpinfo["country_code"],
                                                   gdpinfo["separator"],
                                                   gdpinfo["quote"])

    # 2. Reconcile plot_countries to GDP country codes
    # This gives us a dict like {'us': 'USA', 'gb': 'GBR'} and a set of unmatched plot codes
    reconciled_plot_gdp_codes, truly_unmatched_plot_codes = \
        reconcile_countries_by_code(codeinfo, plot_countries, all_gdp_data_by_code)

    missing_from_gdp_file.update(truly_unmatched_plot_codes)

    # 3. Iterate through the reconciled codes to build the map dictionary
    for plot_code_orig, gdp_code_orig in reconciled_plot_gdp_codes.items():
        country_record = all_gdp_data_by_code.get(gdp_code_orig)

        if country_record:
            gdp_value_str = country_record.get(year, '').strip()

            if gdp_value_str:
                try:
                    gdp_value = float(gdp_value_str)
                    if gdp_value > 0: # Ensure positive GDP for log calculation
                        gdp_data_map[plot_code_orig] = math.log10(gdp_value)
                    else:
                        # GDP is non-positive or zero but exists, so mark as no data
                        no_gdp_data_for_year.add(plot_code_orig)
                except ValueError:
                    # GDP value is not a valid number
                    no_gdp_data_for_year.add(plot_code_orig)
            else:
                # No GDP data for this year for this country (empty string)
                no_gdp_data_for_year.add(plot_code_orig)
        else:
            # This case should ideally be covered by reconcile_countries_by_code,
            # but as a fallback for defensive programming, add to missing.
            missing_from_gdp_file.add(plot_code_orig)

    return (gdp_data_map, missing_from_gdp_file, no_gdp_data_for_year)


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = (f'GDP by country for {year} (log scale), '
                            'unified by common country Code')

    gdp_datas = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)

    worldmap_chart.add(f'GDP For {year}', gdp_datas[0])
    worldmap_chart.add('Missing from World Bank Data', gdp_datas[1])
    worldmap_chart.add('No GDP Data', gdp_datas[2])

    # For CodeSkulptor, uncomment render_to_file() for submission.
    # For local testing, you might use render_in_browser().
    # worldmap_chart.render_in_browser()
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    print("Generating maps for various years...")
    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")
    print("Maps generated successfully!")


# Make sure the following call to test_render_world_map is commented out
# when submitting to OwlTest/CourseraTest.

# test_render_world_map()
