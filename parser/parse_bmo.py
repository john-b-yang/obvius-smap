from auth import *
import io
import os
import pandas as pd
import re
import sys
import requests
from optparse import OptionParser

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print "Error encountered when creating directory"
        os._exit(1)

# Given the output from the bmo-import.py file, requests data per URL
def request_urls(input_name, dirname):
    login = requests.auth.HTTPBasicAuth(AUTH[0], AUTH[1])
    last_location = ""
    buildingURLDict = {} # Map Buildings to unique URL
    urlCountDict = {} # Count number of appearances per URL

    newDir = "./" + dirname + "/"
    createFolder(dirname)

    with open(input_name) as in_file:
        for _, line in enumerate(in_file):
            line = re.sub("Loading section", "", line)
            line = re.sub("loading", "", line)
            line = re.sub(r"\s+", "", line)

            if line[:4] == "http":
                ### Part 1: Bookkeeping
                pattern = "DELIMITER=TAB"
                pos = line.index(pattern)
                identifier = line[:(pos + len(pattern))]

                # Grouping together URLs referring to same location
                if identifier not in urlCountDict:
                    urlCountDict[identifier] = 0
                else:
                    urlCountDict[identifier] += 1

                # Identify which URL corresponds to which building
                if last_location not in buildingURLDict:
                    buildingURLDict[last_location] = identifier

                ### Part 2: Download data from URL
                download = requests.get(url=line, auth=login)
                if download.status_code >= 400:
                    print "Received", download.status_code, "response for request:", line
                else:
                    decoded = download.content.decode('utf-8')
                    csv_filename = re.sub(r"[\\\.:/]", "", last_location) + "-day" + str(urlCountDict[identifier])
                    csv_path = dirname + "/" + csv_filename
                    try:
                        csv_df = pd.read_csv(io.StringIO(decoded))
                        csv_df.to_csv(csv_path)
                        print "Downloaded data for", last_location, " (Day", urlCountDict[identifier], ")"
                    except pd.errors.ParserError as err:
                        print "Parsing Error encountered with file", csv_path, ". Skipping..."
                        continue
            elif len(line) >= 0:
                last_location = line

    return None

# Given the output from the bmo-import.py file, groups data URLs by building
def get_urls(input_name, output_name):
    buildingURLDict = {} # Map Buildings to unique URL
    urlListDict = {} # Group common URLs together

    output = open(output_name, "w+")
    last_location = ""
    with open(input_name) as in_file:
        for _, line in enumerate(in_file):
            line = re.sub("Loading section", "", line)
            line = re.sub("loading", "", line)
            line = re.sub(r"\s+", "", line)

            if line[:4] == "http":
                try:
                    pattern = "DELIMITER=TAB"
                    pos = line.index(pattern)
                    identifier = line[:(pos + len(pattern))]

                    # Grouping together URLs referring to same location
                    if identifier not in urlListDict:
                        urlListDict[identifier] = [line]
                    else:
                        urlListDict[identifier] += [line]

                    # Identify which URL corresponds to which building
                    if last_location not in buildingURLDict:
                        buildingURLDict[last_location] = identifier
                except ValueError as err:
                    continue
            elif len(line) >= 0:
                last_location = line

    if len(buildingURLDict) < 2 or len(urlListDict) < 2:
        print "[Warning] The input file may not have been generated from a call to bmo-import.py"

    for building in buildingURLDict:
        location = str("Location:" + building + "\n")
        output.write(location)
        urlList = urlListDict[buildingURLDict[building]]
        urls = str("URLS:" + "\n".join(urlList) + "\n\n")
        output.write(urls)

    print "Generated", output_name, "file with buildings grouped by URLs successfully"

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-u', '--urls', dest='urls', action='store_true', default=False, help='generates text file grouping URLs by building')
    parser.add_option('-d', '--data', dest='data', action='store', default=None, help='downloads building data per URL (specify name of directory to store files as argument)')
    (opts, args) = parser.parse_args()

    if len(sys.argv) < 3:
        print "\n\tMust include bmo output text file and at least one option (-u, -d)"
        print "\t%s <BMO output text file> [-u] [-d folder]" % sys.argv[0]
        print "\tUse the --help argument to learn more about each option.\n"
    if opts.urls:
        get_urls(sys.argv[1], "bmo-parsed.txt")
    if opts.data and len(opts.data) > 0:
        request_urls(sys.argv[1], opts.data)
