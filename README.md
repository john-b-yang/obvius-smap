## sMAP Building Management Tool
Maintained by Gabe Fierro, Albert Goto, and John Yang  

#### Installation + Setup
1. "git clone" this repository onto your local machine, then change directory into this repository
2. Fill out and create necessary authentication file:  
    a. Fill out the fields in the "sample-auth.py" field.  
    b. Rename this file to "auth.py"  
    c. Place copies of this file in the "crawler" and "parser" folders
3. Run "docker build -t smap:latest ." (Include the period).
    * Ensure the image was successfully generated from this Dockerfile by running "docker image ls" and checking for it.
4. Run "docker run -it --name smap-container --rm smap".
    * Creates a container for running the code and commands listed below.

#### Commands
* <i>python crawl_bmo.py -l</i>;
    - Within "obvius" directory
    - Purpose: Generates configuration file (config.ini) that specifies which buildings' data to retrieve.
    - Output Example: crawl_urls.txt
    - Include the "--help" option to check out other configurations
* <i>python bmo-import.py config.ini &lt;start date&gt; &lt;days&gt;</i>;
    - Within "bmo" directory
    - Purpose: Creates and gathers the URLs pointing at data within the date range specified by the "start date" and "days" arguments for each building
    - Output Example: bmo_output.txt
* <i>python parse_bmo.py bmo-output.txt [-u] [-d folder]</i>
    - Within "parser" directory
    - Purpose
        * [-u]: Generates a text file that groups the URLs from <i>bmo-import.py</i>'s output by building
        * [-d folder]: Downloads data per URL into a directory specified by the "folder" parameter
    - Output Example: bmo-parsed.txt

#### Progress Track

| To Do | Description |
| ----- | ----------- |
| Data Ingestion | Set up how building data is parsed, interpreted, and stored. |
| Unnecessary Files | bmo-import's dependencies are from sMAP. sensordb, obvius, bmo files may not be necessary (bmo-import.py) |
| Parsing Error | Many parsing errors when downloading files (parse_bmo.py) |

#### Issues
- (text-files/bmo-output.txt): Purpose of Starting Day URLs? - Data per day?

#### Relevant Links:
- sMAP Documentation: https://pythonhosted.org/Smap/en/2.0/core.html
