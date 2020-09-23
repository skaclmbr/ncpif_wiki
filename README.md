# NC Partners in Flight Wiki
Python code for extracting and reformatting wiki xml export data for the NC Partners in Flight wiki (wiki.ncpif.org) with Semantic MediaWiki data.

Recent update converts wiki xml output to cypher query languate for import into graph database like Neo4j.

See website at: http://wiki.ncpif.org

## Files
* parse_wiki_xml.py - python code for ingesting wikipedia xml export, and populating an excel spreadsheet for manipulation - being true to semantic media wiki links.
* wiki_xml_to_cypher.py - intests wikipedia xml export (with Semantic MediaWiki notation), and creates a cypher query language output
* build_wiki_xml.py - python code reversing the process - takes excel spreadsheet and creates an xml import file. Also creates recipricol relationships between primary entities (Species, Habitats, Organizations, Projects, Geographies, and Plans)
* 20200429173214_wiki_ncpif.xlsx - example excel spreadsheet created from parse code.
* 20200429173214_wiki_ncpif_of_upload.xlsx - example excel spreadsheet created from build code.
* NCBirdConservation.cypher - example output file from wiki_xml_to_cypher.py
* NC+Bird+Conservation+All+20200901141341.xml - example wiki xml export file
