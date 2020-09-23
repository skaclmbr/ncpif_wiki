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
## End idea: provide a tool to convert wiki data to table format
## 	-Entities
## 	-Properties
## 	-Build and Parse Wiki XML imports/exports

###################################################################
## WIKITEXT STRUCTURE
## There are three main components to the wikitext on a page:
## 	1. Intro Template (includes list of linked items, formatted properties)
##  2. Supplementary information (description, etc.)
##  3. File link (if applicable)
##  4. Category declaration(s)
##  5. Property declaration(s)


###################################################################
## EXCEL
## results are stored in an excel workbook with the following structure:
## - entities (type, title)
## - categories (title, category)
## - properties (title, property, value)
## - wikitext (title, wikitext)



###################################################################
## QUESTIONS
## 	-What is the best storage/management database for input/output?
## 	-Should this be stored in MySQL online?

import xml.dom.minidom
from openpyxl import Workbook #allows connecting to databases
# from openpyxl import load_workbook #allows connecting to databases
from openpyxl.worksheet.table import Table, TableStyleInfo

def fRemoveBadChars(t):
	r = t.replace("'","").replace(";","").replace(",","").replace("/","")
	return r


def fNodeLabel(t):
	#Node Label: Camel case beginning with upper-case character (:VehicleOwner)
	r = t.title().replace(" ","").replace("'","")
	r = ":"+r
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
	r = t.title().replace(" ","").replace("'","").replace("-","")
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
		r = "'" + fRemoveBadChars(t) + "'"

	return r


def main():

	nl = '\n'
	propDelim = '|'

	# PRIMARY CATEGORIES
	types = ['Species','Habitat','Organization','Project','Plan','Geography','Priority'] #defines primary category for the entity

	# # DEFAULT COLUMNS
	# colsEnt = {'type':'A','title':'B'}
	# colsCat = {'title':'A','category':'B'}
	# colsPro = {'title':'A','property':'B','value':'C'}
	# colsWik = {'title':'A','wikitext':'B'}

	# ROW COUNTERS
	rowEnt = 1
	rowCat = 1
	rowPro = 1
	rowWik = 1


	###################################################################
	# CREATE EXCEL FOR STORING DATA
	# NOT NEEDED

	# wb = Workbook()

	# wsEnt = wb.active #get the first sheet
	# wsEnt.title = "entities"
	# wsCat = wb.create_sheet("categories")
	# wsPro = wb.create_sheet("properties")
	# wsWik = wb.create_sheet("wikitext")

	# Add headers
	# wsEnt[colsEnt['type']+str(rowEnt)] = 'type'
	# wsEnt[colsEnt['title']+str(rowEnt)] = 'title'
	rowEnt +=1

	# wsCat[colsCat['title']+str(rowCat)] = 'title'
	# wsCat[colsCat['category']+str(rowCat)] = 'category'
	rowCat +=1

	# wsPro[colsPro['title']+str(rowPro)] = 'title'
	# wsPro[colsPro['property']+str(rowPro)] = 'property'
	# wsPro[colsPro['value']+str(rowPro)] = 'value'
	rowPro +=1

	# wsWik[colsWik['title']+str(rowWik)] = 'title'
	# wsWik[colsWik['wikitext']+str(rowWik)] = 'wikitext'
	rowWik +=1

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
		title = fRemoveBadChars(page.getElementsByTagName("title")[0].childNodes[0].nodeValue)
		print (nl+"======" + str(title) + "======")
		currNodeName = fNodeName(title)
		createText = "CREATE (" + currNodeName

		#################
		# GET WIKITEXT
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
					# nodeLabels.append(priCat)
					# wsEnt[colsEnt['type']+str(rowEnt)]=priCat
					# wsEnt[colsEnt['title']+str(rowEnt)]=title
					rowEnt +=1

				# wsCat[colsCat['title']+str(rowCat)]=title
				# wsCat[colsCat['category']+str(rowCat)]=currCat
				nodeLabels.append(fNodeLabel(currCat))
				rowCat +=1

				#advance cursor
				currPos = wt.find("[[Category:",cEnd)+11 #find next category
			createText += "".join(nodeLabels)
			# print (createText)

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
				propOutput.append("name: '" + title + "'") #add page title as name property
				for p in propList: #loop through list
					itemValue=p.replace("\n","").split("=")
					# DETERMINE if property is a relationship (e.g., Has Species)
					noun = itemValue[0][itemValue[0].find(" ")+1:]
					# print(itemValue)
					# print (noun)
					#check if it is a relationship
					if noun in types:
						itemValue.append(noun)
						rel = {'typeA':priCat,'typeB':noun,'nodeA':currNodeName,'nodeB':fNodeName(itemValue[1]),'nameA':title,'nameB':itemValue[1],'relType':fRelationshipLabel(itemValue[0])}
						relList.append(rel)

					else: #not a relationship, add as property
						propOutput.append(fPropertyLabel(itemValue[0]) + ": " + fBoolNumString(itemValue[1]))

					rowPro +=1
				# print (", ".join(propOutput))
				#close createText
				createText += " { " + ", ".join(propOutput) + "})"
				print(createText +nl)

			#################
			# WIKITEXT
			# SKIP WIKITEXT FOR CYPHER OUTPUT

			# wsWik[colsWik['title']+str(rowWik)]=title
			# wsWik[colsWik['wikitext']+str(rowWik)]=wt[:wtEnd] #get wikitext until categories start

			rowWik +=1

			## OUTPUT
			# WRITE CREATE for node
			o.write(createText + nl)

			# Includes Template, Supplementary Information, and File Links (#s 1-3 above)


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
	

	# print (outJoinDelim.join(outRelText))
	o.write(nl + "CREATE" + nl + outJoinDelim.join(outRelText))

	# SAVE EXCEL FILE
	# format/define tables
	# style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,showLastColumn=False, showRowStripes=True, showColumnStripes=True)

	# tabEnt = Table(displayName="entities",ref="A1:"+colsEnt['title']+str(rowEnt-1))
	# tabEnt.tableStyleInfo = style
	# wsEnt.add_table(tabEnt)
	# tabCat = Table(displayName="categories",ref="A1:"+colsCat['category']+str(rowCat-1))
	# tabCat.tableStyleInfo = style
	# wsCat.add_table(tabCat)
	# tabPro = Table(displayName="properties",ref="A1:"+colsPro['value']+str(rowPro-1))
	# tabPro.tableStyleInfo = style
	# wsPro.add_table(tabPro)
	# tabWik = Table(displayName="wikitext",ref="A1:"+colsWik['wikitext']+str(rowWik-1))
	# tabWik.tableStyleInfo = style
	# wsWik.add_table(tabWik)



	# wb.save(timestamp + '_wiki_ncpif.xlsx')

	print(str(count) + " Pages Found")


if __name__=="__main__":
	main();