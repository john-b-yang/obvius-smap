### Parsing
Sends out HTTP requests for each URL from the 'bmo' module, then retrieves, processes, and downloads the response and data, distinguished by the building and time the data comes from.

#### Command
* <i>python parse_bmo.py bmo-output.txt [-u] [-d folder]</i>
    - Within "parser" directory
    - Purpose
        * [-u]: Generates a text file that groups the URLs from <i>bmo_import.py</i>'s output by building
        * [-d folder]: Downloads data per URL into a directory specified by the "folder" parameter
    - Output Example: bmo-parsed.txt
