import requests
from bs4 import BeautifulSoup
from HelperFunctions import capitalize_each_word, tocsv
from datetime import datetime


def extract_single(website, index):
    url = website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    main = soup.find('div', class_="view-content")

    links = main.find_all('a')
    # Define some of the field label names for which we want to extract information from the profile.
    labelsToUse = ['Crime', 'Sex', 'Date of birth', 'Nationality']

    # define the column headers to inject in the CSV file
    rows_to_csv = [["last_name", "first_name", "name", "crime", "gender",
               "dob", "nationality", "state_of_case", "url"]]

    # Open the individual profile link
    itemUrl = links[index].get('href')
    print(itemUrl)
    profilePage = requests.get(itemUrl)
    profSoup = BeautifulSoup(profilePage.content, "html.parser")

    # Load the individual profile information into a scrapable object
    mainProf = profSoup.find('div', class_="wanted_top_right")

    # Create the row and add the lastname, firstname and fullname values
    nameVal = mainProf.find('h2').text.strip()
    row = [capitalize_each_word(nameVal.split(',')[0].strip()),
           capitalize_each_word(nameVal.split(',')[1].strip()),
           nameVal]

    # create a list of additional elements excluding the 'State of case' field.
    elemsFound = mainProf.find_all(['h2', 'div'], {"class": "field-label"})[:-1]

    # Loop through all the field label names to check ....
    for c in labelsToUse:
        i = 0
        labelExists = False
        while i < len(elemsFound):
            if c == elemsFound[i].text.split(":")[0]:  # ... if it exists in the scraped profile information.
                labelExists = True  # Label is found so set it to true.

                # always Save values associated to the Crime label as a list.
                if c == "Crime":
                    valsToAppend = [f.text for f in elemsFound[i].next_sibling.findChildren()]
                    row.append(valsToAppend)
                # Make sure the output_to_append format is correctly set to date in the "Date of birth" column.
                elif c == "Date of birth":
                    row.append(datetime.strptime(elemsFound[i].next_sibling.text, '%b %d, %Y').date())
                else:
                    # If the associated values contain more than 1 entry, separate entries with a slash.
                    if len(elemsFound[i].next_sibling.findChildren()) > 1:
                        valsToAppend = [f.text for f in elemsFound[i].next_sibling.findChildren()]
                        row.append('/'.join(valsToAppend))

                    else:  # Else save the values as a single string
                        row.append(elemsFound[i].next_sibling.text)
            i += 1

        # If the label is not found in the found elements just add an empty string
        if not labelExists:
            row.append("")

    # Try to add the description in the state of case.
    try:
        row.append(mainProf.find('div', {"class": "comma-separated field-items"}).text.strip())

    # if adding state of case fails, add an empty string.
    except:
        row.append("")

    # Add the URL
    row.append(itemUrl)

    # Add the complete row to a list of rows
    rows_to_csv.append(row)
    print(rows_to_csv)
    tocsv(rows_to_csv)


def extract_all(website):
    url = website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    main = soup.find('div', class_="view-content")

    links = main.find_all('a')

    labelsToUse = ['Crime', 'Sex', 'Date of birth', 'Nationality']

    # define the column headers to inject in the CSV file
    rows_to_csv = [["last_name", "first_name", "name", "crime", "gender",
                "dob", "nationality", "state_of_case", "url"]]
    # Loop through all the profile links
    for link in links:
        itemUrl = link.get('href')
        print("checking: ", itemUrl)
        try:
            profilePage = requests.get(itemUrl)
            profSoup = BeautifulSoup(profilePage.content, "html.parser")
        except requests.ConnectionError as exception:
            print("URL does not exist on Internet", itemUrl)

        # Load the individual profile information into a scrapeable object
        mainProf = profSoup.find('div', class_="wanted_top_right")

        # Create the row and add the lastname, firstname and fullname values
        nameVal = mainProf.find('h2').text.strip()
        row = [capitalize_each_word(nameVal.split(',')[0].strip()),
               capitalize_each_word(nameVal.split(',')[1].strip()),
               nameVal]

        # create a list of additional elements excluding the 'State of case' field.
        elemsFound = mainProf.find_all(['h2', 'div'], {"class": "field-label"})[:-1]

        # Loop through all the field label names to check ....
        for c in labelsToUse:
            i = 0
            labelExists = False
            while i < len(elemsFound):
                if c == elemsFound[i].text.split(":")[0]:  # ... if it exists in the scraped profile information.
                    labelExists = True  # Label is found so set it to true.

                    # always Save values associated to the Crime label as a list.
                    if c == "Crime":
                        valsToAppend = [f.text for f in elemsFound[i].next_sibling.findChildren()]
                        row.append(valsToAppend)
                    # Make sure the output_to_append format is correctly set to date in the "Date of birth" column.
                    elif c == "Date of birth":
                        row.append(datetime.strptime(elemsFound[i].next_sibling.text, '%b %d, %Y').date())
                    else:
                        # If the associated values contain more than 1 entry, separate entries with a slash.
                        if len(elemsFound[i].next_sibling.findChildren()) > 1:
                            valsToAppend = [f.text for f in elemsFound[i].next_sibling.findChildren()]
                            row.append('/'.join(valsToAppend))

                        else:  # Else save the values as a single string
                            row.append(elemsFound[i].next_sibling.text)
                i += 1

            # If the label is not found in the found elements just add an empty string
            if not labelExists:
                row.append("")

        # Try to add the description in the state of case.
        try:
            row.append(mainProf.find('div', {"class": "comma-separated field-items"}).text.strip())
        # if adding state of case fails, add an empty string.
        except:
            row.append("")

        # Add the URL
        row.append(itemUrl)

        # Add the complete row to a list of rows
        rows_to_csv.append(row)
    tocsv(rows_to_csv)
