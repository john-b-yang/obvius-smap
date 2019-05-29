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

#### Download Command
python download.py -s &lt;start date&gt; -e &lt;end date&gt; -d(evices) -c(onfig)
* Purpose: Returns data for all buildings + meters within the context of a single BMO (Building Management Online)
* -s (YYYY-MM-DD): [Required] Start Date of Query
* -e (YYYY-MM-DD): [Required] End Date of Query
* -d: [Optional] If passed, program outputs a JSON file containing building + meter information
* -c: [Optional] If passed, program outputs a Config (INI) file containing building + meter information
* Example: python download.py -s 2019-04-01 -e 2019-04-03 | Returns all data for buildings + meters between April 1st, 2019, and April 3rd, 2019 (inclusive range)

#### Progress Track
* Data Ingestion: Set up how building data is parsed, interpreted, and stored.

#### Relevant Links:
- sMAP Documentation: https://pythonhosted.org/Smap/en/2.0/core.html
