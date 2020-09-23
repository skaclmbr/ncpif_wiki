# NC Partners in Flight Wiki
Python code for extracting and reformatting wiki xml export data for the NC Partners in Flight wiki (wiki.ncpif.org)
Python code for extracting and reformatting wiki xml export data for the NC Partners in Flight wiki (wiki.ncpif.org) with Semantic MediaWiki data.

See website at: http://wiki.ncpif.org

## Files
* parse_wiki_xml.py - python code for ingesting wikipedia xml export, and populating an excel spreadsheet for manipulation - being true to semantic media wiki links. 
* build_wiki_xml.py - python code reversing the process - takes excel spreadsheet and creates an xml import file. Also creates recipricol relationships between primary entities (Species, Habitats, Organizations, Projects, Geographies, and Plans)
* 20200429173214_wiki_ncpif.xlsx - example excel spreadsheet created from parse code.
* 20200429173214_wiki_ncpif_of_upload.xlsx - example excel spreadsheet created from build code.


## Known Issues
* there are some...