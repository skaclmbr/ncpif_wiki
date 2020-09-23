### finds matches from keyword list in text files in given folder
### INPUT:
###		keywords.txt: csv file containing search_term, id values
###		plandir: folder path to location of text files to be searched
### OUTPUT: 3 files
###		- list of wikipages of type Priority
###		- list of properties (Has Habitat, Has Habitat Index, Has Species, Has Organization, etc.)
###		- wikitext for each page: {{Priority Page}} [[Category:Priority]]
###		These can be copy/pasted into excel sheets for import


import os
import sys
import datetime
import msvcrt as m

now = datetime.datetime.utcnow()
t = str(now.strftime('%Y-%m-%d'))+'T'+ str(now.strftime('%X'))+'Z' #run date - to be used in file name
print (t)
ts = t.replace("-","").replace(":","")


def main():

	rootdir= os.path.dirname(os.path.abspath(__file__)) #retrieves the current file location as the base folder
	#plandir= rootdir + '\\plans_txt\\' #search through text files in this folder
	

	def slugify(t,d='-'):
		#pass text and delimiter
		#insert delimiter into spaces in text
		t.replace(' ', d)
		t.replace('_', d)
		return t

	def wikify(t,d=' '):
		#pass text and delimiter
		#insert delimiter into spaces in text
		t.replace('_',d)
		t.title()
		return t
		
	def save_unique_match(f,k):
		#pass:
		#	k = keyword id
		#	f = filename slug
		#check to see if pair already exists in matches, if not, add
		fk = [f,kd[k]]
		if fk not in matches: matches.append(fk)
		# if [f,k] not in matches: kwd_link.write(f + delim + k + nl)

	def get_leading_search_term(t):
		#parse passed text with space, return everything except the last item
		print(t)
		tArray = t.split(" ")
		print(tArray)
		if len(tArray) > 1: #passed text 
			return " ".join(tArray[:-1]) #return everything except last item
		else:
			return False

	def build_wikilink(t,wp):
		#pass search text, return formatted wikilink text
		if t==wp:
			#text is the same, just add brackets
			return '[[' + wp + ']]'
		else:
			if get_leading_search_term(wp)==t:
				#text is part of a list (e.g., Cerulean and Kentucky warblers)
				pass
			if t[-1]=='s': #pluralized
				pass



	def wait(): #for debugging, pauses program until keypress
		print ("press any key to continue...")
		m.getch()
	
	delim = ','
	in_delim = '|'
	out_delim = '\t'
	nl = '\n'
	priList = {} #array of priority text, used to remove duplicates
	searchTerms = {} # key = search term, value = [wikipage, wikipage category, match ] (match is a binary if search term is same as wikipage)
	common_categories = ['Priority','NCWAP15 Priority']
	common_wikitext = '{{Priority Page}}'
	

	###############################################################################################
	#OUTPUT FILES - each file corresponds to sheet in excel book
	print (str(ts))
	pwp = open(rootdir + '\\' + str(ts) + '_priority_wikipages.txt','w') #wikipages
	pcat = open(rootdir + '\\' + str(ts) + '_priority_categories.txt','w') #categories
	pprop = open(rootdir + '\\' + str(ts) + '_priority_properties.txt','w') #properties
	pwt = open(rootdir + '\\' + str(ts) + '_priority_wikitext.txt','w') #wikitext

	###############################################################################################
	#INPUT FILES
	p_fn = rootdir + '\\ncwap15_priorities.txt'
	wp = open(rootdir + '\\wikipages_20200429.txt','r').read()
	sFile = open(rootdir + '\\search_terms.txt','r').read()

	###############################################################################################
	#build search dictionaries
	wikipages = {} #dict of all wikipages (key = wikipage, value = Type/Primary Category)
	wpl = wp.splitlines()
	for ln, l in enumerate(wpl):
		r = l.split(in_delim)
		
		if ln==0:
			pass #skip first line
		else:
			currPage = r[1].strip()
			currType = r[0].strip()
			print(currPage	+ currType)
			wikipages[currPage] = currType
			if currType != 'Habitat':
					searchTerms[currPage] = [currPage,currType,True] #add all non-Habitat wikipages to search terms  

	searchl = sFile.splitlines()
	for ln, l in enumerate(searchl):
		r = l.split(in_delim)
		if ln==0:pass #skip first line
		else:
			currTerm = r[0].strip()
			currPage = r[1].strip()

			if currTerm not in searchTerms:

				if currPage in wikipages: #make sure page exists!
					currPageType = wikipages[currPage] # use to determine property to set 
					searchTerms[currTerm] = [currPage,currPageType,False]

					#add derived search terms
					#use all but last term (if more than one word)
					altTerm = get_leading_search_term(currTerm)
					if altTerm: searchTerms[altTerm] = [currPage, currPageType, False]

	print(searchTerms)

	count = 1
	row_data = {}
	h = [] #holds headers
	newRecord = True
	with open(p_fn, 'r', encoding='utf-8') as f:
		for line in f:
			line = line.replace("\n","")
			r = line.split(in_delim)

			if count==1: #collect header info
				for i,d in enumerate(r):
					h.append(d)
				print(h)

			else:
				#add store row data in dictionary
				for i,d in enumerate(r): row_data[h[i]] = d
				currP = row_data['pri_wikipage']
				currText = row_data['text']

				#check for duplicates
				for k,v in priList.items():
					# print (nl+'================='+nl+k + ": " + v)
					# print (currText)
					if currText == v:
						# print ('match!')
						# wait()
						newRecord = False
						currP = k
						break
				if newRecord: priList[currP]=currText #add new record to list



				#SEARCH FOR MATCHES HERE


				#SAVE DATA
				if newRecord:
					#add record to entities
					pwp.write(out_delim.join(['Priority',currP])+nl)

					#add record(s) to categories
					outCat = common_categories + [row_data['type'].title() + ' Priority']
					for c in outCat: pcat.write(out_delim.join([currP,c])+nl)

					##loop through searchHits
					for k,v in searchTerms.items():
						if k in currText: #search hit! add property and change text to be a link
							#value array = [wikipage, wikipage category, match ] (match is true if search term is same as wikipage)
							leadChar = ''
							pprop.write(out_delim.join([currP,'Has '+v[1],v[0]])+nl)
							if v[0][4]=='Cate': leadChar=':'
							if v[2]: #search term is a wikipage
								currText= currText.replace(k,'[['+leadChar+v[0]+']]')
							else:
								currText=currText.replace(k,'[['+leadChar+v[0]+'|'+k+']]')

					#add record to properties (title, property, value)
					#first common properties
					pprop.write(out_delim.join([currP,'Has Plan','North Carolina Wildlife Action Plan 2015'])+nl)
					pprop.write(out_delim.join([currP,'Has Priority Type',row_data['type'].title()+' Priority'])+nl)
					pprop.write(out_delim.join([currP,'Has Text',currText])+nl)
				
					#add record to wiktext
					pwt.write(out_delim.join([currP,common_wikitext])+nl)
			

				#add property links to habitat
				pprop.write(out_delim.join([currP,'Has NCWAP15 Index',row_data['hab_section']])+nl)
				pprop.write(out_delim.join([currP,'Has Habitat',row_data['hab_wikipage']])+nl)



			newRecord = True
			count+=1
	print (str(count) + " records found")

if __name__ == "__main__":
	main()