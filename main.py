import ExtractFunctions
from csv import reader, writer

if __name__ == '__main__':
    URL = "https://eumostwanted.eu/"

    # We are first extracting and creating a new CSV file with the extract_all custom function
    ExtractFunctions.extract_all(URL)

    # Lets now compare the original file and the newly created one for differences.
    # open and load records as list of string
    with open('2021-06-25T130338_eu_most_wanted.csv', 'r', encoding="utf-8") as t1, \
            open('new.csv', 'r', encoding="utf-8") as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    # open and load records as list of lists
    with open('2021-06-25T130338_eu_most_wanted.csv', 'r', encoding="utf-8") as t1, \
            open('new.csv', 'r', encoding="utf-8") as t2, \
            open('results.csv', 'w', newline='', encoding="utf-8") as write_obj:

        original_rowlist = [row for row in reader(t1)]
        new_rowlist = [row for row in reader(t2)]

        csv_writer = writer(write_obj)

        # copy headers from the new extracted list, add them to the output file and add a "Changed" column
        headers = new_rowlist[0]
        headers.append("what_has_changed")
        csv_writer.writerow(headers)

        # Let's first check all records in the new file and compare to the original one
        for idx, line in enumerate(filetwo):  # iterate over all the lines in the new file
            if line not in fileone:           # If the line does not exist in the original it is either new or changed
                i = 0
                changed = False

                while i < len(original_rowlist):  # While loops iterates over all the different records in the original file
                    if new_rowlist[idx][8] == original_rowlist[i][8]:  # if the URL exists in both files, there has been a profile change
                        output_to_append = ""
                        # compare all the cells of the matched records in the original and new file to find what changed
                        for j in range(len(new_rowlist[0][:-1])):
                            if new_rowlist[idx][j] != original_rowlist[i][j]: # Check if the compared cells are different
                                output_to_append += ("updated value in column: " + new_rowlist[0][j] + " | ")
                        changed = True
                        new_rowlist[idx].append(output_to_append)
                        break
                    i += 1
                if not changed:  # if the record only exists in the new file, it has been added
                    output_to_append = "profile added"
                    new_rowlist[idx].append(output_to_append)
                csv_writer.writerow(new_rowlist[idx])

        # Now we check which records from the original file do not exist in the new file.
        for idx, line in enumerate(fileone):
            if line not in filetwo:
                i = 0
                exists = False
                # check if there are any records in the old file that do not exist in the new.
                while i < len(new_rowlist):  # While loops iterates over all the different records in the new file
                    if original_rowlist[idx][8] == new_rowlist[i][8]:  # check if the same url exists in both files
                        exists = True
                        break
                    i += 1
                if not exists:  # if the record does not exist in the new file
                    original_rowlist[idx].append("Profile removed")  # add "removed" to output
                    csv_writer.writerow(original_rowlist[idx])  # write to csv
    print("Original file and new file compared\nOutput file created: results.csv")
