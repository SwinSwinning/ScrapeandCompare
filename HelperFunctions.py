import csv


def capitalize_each_word(original_str):
    result = ""
    # Split the string and get all words in a list
    list_of_words = original_str.split()
    # Iterate over all elements in list
    for elem in list_of_words:
        # capitalize first letter of each word and add to a string
        if len(result) > 0:
            result = result + " " + elem.strip().capitalize()
        else:
            result = elem.capitalize()
    # If result is still empty then return original string else returned capitalized.
    if not result:
        return original_str
    else:
        return result


def tocsv(rows):
    with open('new.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

