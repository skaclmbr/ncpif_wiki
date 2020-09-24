# Used to process xml for the NCPIF Conservation Connections Wiki
# and convert to cypher query language for import into graph db
#This is an initial test
# Scott Anderson Sep 23, 2020
# NC Wildlife Resources Commission
# scott.anderson@ncwildlife.org
# python 3.8

###################################################################
## CYPHER NAMING RULES
#	Node Label: Camel case beginning with upper-case character (:VehicleOwner)
#	Relationship Label: Upper case, using underscore to separate words (:OWNS_VEHICLE)
#	Property: Lower camel case, beginning with lower-case character (:firstName)


###################################################################
## Retrieving XML from wiki
#	1. Go to wiki.ncpif.org/index.php?title=Special:Export
#	2. Enter each category for inclusion in export file (e.g., 'Category:Species', 'Category:Species'). Make sure to include all primary entitites: 'Species','Habitat','Organization','Project','Plan','Geography','Priority'
#	3. Export file to folder with this python script
#	4. Change import_fn below to match export xml.

###################################################################
## WIKITEXT STRUCTURE
## There are three main components to the wikitext on a page:
## 	1. Intro Template (includes list of linked items, formatted properties)
##  2. Supplementary information (description, etc.)
##  3. File link (if applicable)
##  4. Category declaration(s)
##  5. Property declaration(s)

###################################################################
## QUESTIONS
## 	-What is the best storage/management database for input/output?
## 	-Should this be stored in MySQL online?

import xml.dom.minidom
from openpyxl import Workbook #allows connecting to databases
# from openpyxl import load_workbook #allows connecting to databases
from openpyxl.worksheet.table import Table, TableStyleInfo

def fRemoveBadChars(t):
	r = t.replace("'","").replace(";","").replace(",","").replace("/","").replace("-","").replace("–","").replace("’","").replace("&","").replace(".","").replace(":","")
	return r


def fNodeLabel(t):
	#Node Label: Camel case beginning with upper-case character (:VehicleOwner)
	r = t.title().replace(" ","").replace("'","")
	r = ":"+fRemoveBadChars(r)
	# print (r)
	return r

def fRelationshipLabel(t):
	#Relationship Label: Upper case, using underscore to separate words (:OWNS_VEHICLE)
	r = t.replace(" ","_").upper()
	r= ":"+r
	# print (r)
	return r

def fPropertyLabel(t):
	#Property: Lower camel case, beginning with lower-case character (:firstName)
	tCase = t.title()
	modTcase = tCase[0].lower()+tCase[1:]
	r = modTcase.replace(" ","")
	# print (r)
	return r

def fNodeName(t):
	# r = t.title().replace(" ","").replace("'","").replace("-","")
	r = fRemoveBadChars(t).title().replace(" ","")
	# r = t.lower().replace(" ","")
	# print (r)
	return r

def fBoolNumString(t):
	#determine type of text, output accordingly
	if isinstance(t,(int,float)):
		r = t
	elif t.lower()=='true' or t.lower()=='false':
		r = t.lower()
	else:
		# r = '"' + fRemoveBadChars(t) + '"'
		r = '"' + t + '"'

	return r


def main():

	nl = '\n'
	propDelim = '|'

	# PRIMARY CATEGORIES
	types = ['Species','Habitat','Organization','Project','Plan','Geography','Priority'] #defines primary category for the entity

	# LOAD XML FILE
	import_fn = "NC+Bird+Conservation-All-20200907141341.xml"
	timestamp = import_fn[25:39]
	o_fn = "NCBirdConservation.cypher"
	o = open('output_files/' + o_fn, 'w', encoding="utf-8")

	doc = xml.dom.minidom.parse(import_fn)

	# LOOP THROUGH PAGES
	count = 1
	pages = doc.getElementsByTagName("page")
	relList = [] #stores relationships between nodes

	for page in pages: #loop through all Wiki pages - each page represents a node entity 

		#start node text
		nodeName = ""

		#################
		# TITLE - the key value for each page
		title = page.getElementsByTagName("title")[0].childNodes[0].nodeValue
		print (nl+"======" + str(title) + "======")
		currNodeName = fNodeName(title)
		createText = "CREATE (" + currNodeName

		#################
		# GET WIKITEXT
		# USED TO EXTRACT CATEGORIES AND PROPERTIES
		wt = page.getElementsByTagName("text")[0].childNodes[0].nodeValue
		# wt = wt_raw.replace("{{#set:"+nl+"}}","")
		# print (wt)

		#################
		# REJECT TEMPLATES AND OTHER PAGES FOR NOW
		
		if "category:" not in title.lower():
		
			#################
			# CATEGORIES
			# loop to capture all categories
			# PRIMARY CATEGORY FIRST, OTHERS AS LABELS

			nodeLabels = []
			priCat = ''
			startPos = wt.find("[[Category:")+11 #find first category
			currPos = startPos
			wtEnd = currPos-11 #define end of wikitext

			while currPos>=startPos:
				cEnd = wt.find("]]",currPos)
				currCat = wt[currPos:cEnd]
				if currCat in types: #check to see if one of main spp, add to entities sheet
					priCat = fNodeLabel(currCat)

				nodeLabels.append(fNodeLabel(currCat))

				#advance cursor
				currPos = wt.find("[[Category:",cEnd)+11 #find next category

			# THIS IS FOR INCLUDING ALL CATEGORIES AS NODE LABELS
			# createText += "".join(nodeLabels)
			# THIS INCLUDES ONLY THE PRIMARY CATEGORY AS NODE LABEL
			createText += priCat

			cEnd +=2 # set end of category declaration

			#################
			# PROPERTIES
			# work with wikitext to extract properties
			# find #set declaration
			# NOTE:
			# 	- must find the properties that represent links
			#	- all other properties represented as cypher properties

			propDict = {}
			pStart = wt.find("{{#set:",cEnd)+7
			pEnd = wt.find("}}",pStart)
			
			if pEnd - pStart>5: #make sure there are some properties set

				propText = wt[pStart:pEnd] #get full property text
				propList = propText.split(propDelim) #create list from property text
				propOutput = []
				propOutput.append('name: "' + title + '"') #add page title as name property
				for p in propList: #loop through list
					itemValue=p.replace('\n','').split('=')
					#clean up the name of the value
					# itemValue[1] = fBoolNumString(itemValue[1])
					# DETERMINE if property is a relationship (e.g., Has Species)
					noun = itemValue[0][itemValue[0].find(' ')+1:] #strip off the verb in the relationship to get to the noun
					print (itemValue)
					if noun in types:
						itemValue.append(noun)
						rel = {'typeA':priCat,'typeB':noun,'nodeA':currNodeName,'nodeB':fNodeName(itemValue[1]),'nameA':title,'nameB':itemValue[1],'relType':fRelationshipLabel(itemValue[0])}
						relList.append(rel)

					else: #not a relationship, add as property
						propOutput.append(fPropertyLabel(itemValue[0]) + ": " + fBoolNumString(itemValue[1]))

				createText += " { " + ", ".join(propOutput) + "}"
				print(createText +nl)

			## OUTPUT
			# WRITE CREATE for node
			createText += ")"
			o.write(createText + nl)

		## FINISH UP PAGE
		count +=1
		# if count>3:
		# 	break #TESTING

	## CREATE RELATIONSHIPS ONCE NODES HAVE BEEN CREATED
	# print (relList)
	# LOOP THROUGH RELATIONSHIPS, GENERATE CYPHER TEXT
	outRelText = []
	outJoinDelim = "," + nl
	for i in relList:

		outRelText.append("(" + i['nodeA'] + ")-[" + i['relType'] + "]->(" + i['nodeB'] + ")")
		#FIRST TRY - COMMENT OUT FOR NOW
		# outRelText = "MATCH (" + i['nodeA'] + i['typeA'] + "),(" + i['nodeB'] + ":" + i['typeB'] + ")" + nl
		# outRelText += "WHERE " + i['nodeA'] + ".name = '" + i['nameA'] + "' AND " + i['nodeB'] + ".name = '" + i['nameB'] + "'" + nl
		# outRelText += "CREATE (" + i['nodeA'] + ")-[r" + i['relType'] + " { name:" + i['nodeA'] + ".name + '<->' + " + i['nodeB'] + ".name }]->(" + i['nameB'] + ")" + nl
		# outRelText += "RETURN type (r), r.name" + nl

	# OUTPUT ALL RELATIONSHIP CYPHER TEXT
	o.write(nl + "CREATE" + nl + outJoinDelim.join(outRelText) + nl + ";")

	print(nl + str(count) + " Pages Found")

if __name__=="__main__":
	main();