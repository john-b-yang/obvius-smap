## sMAP Building Management Tool
Maintained by Gabe Fierro, Albert Goto, and John Yang  

#### Overview


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
* <i>python download.py -d &lt;MM-DD-YYYY&gt;</i>: Downloads all building data on a specific day.
* <i>python crawl_bmo.py -l</i>: Generates configuration file (config.ini) that specifies which buildings' data to retrieve.
* <i>python bmo_import.py config.ini &lt;start date&gt; &lt;days&gt;</i>: Creates and gathers the URLs pointing at data within the date range specified by the "start date" and "days" arguments for each building
* <i>python parse_bmo.py bmo-output.txt [-u] [-d folder]</i>: Downloads data per URL into a directory specified by the "folder" parameter

#### Progress Track

| To Do | Description |
| ----- | ----------- |
| Data Ingestion | Set up how building data is parsed, interpreted, and stored. |
| Unnecessary Files | bmo_import's dependencies are from sMAP. sensordb, obvius, bmo files may not be necessary (bmo_import.py) |
| Parsing Error | Many parsing errors when downloading files (parse_bmo.py) |

#### Issues
- (text-files/bmo-output.txt): Purpose of Starting Day URLs? - Data per day?

#### Relevant Links:
- sMAP Documentation: https://pythonhosted.org/Smap/en/2.0/core.html
