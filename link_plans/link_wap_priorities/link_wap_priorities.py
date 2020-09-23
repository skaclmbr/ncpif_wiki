### finds matches from keyword list in WAP Priorities text files in given folder
### INPUT:
###		keywords.txt: csv file containing search_term, id values
###		priorities.txt: file containing priorities and their ids
###			0: id
###			1: pri-id
###			2: h_id
###			3: habitat
###			4: p_type
###			5: category
###			6: priority - text of priority to be searched
### OUTPUT:
###		priority_link.txt: csv file containing keyword key and slugified text file title

import os
import sys
import msvcrt as m

def main():
	rootdir='C:/data/@projects/conservation_database/link_wap_priorities/'

	def slugify(t,d='-'):
		#pass text and delimiter
		#insert delimiter into spaces in text
		t.replace(' ', d)
		t.replace('_', d)
		return t
		
	def save_unique_match(f,k):
		#pass:
		#	k = keyword id
		#	f = filename slug
		#check to see if pair already exists in matches, if not, add
		fk = [f,kd[k]]
		if fk not in matches: matches.append(fk)
		# if [f,k] not in matches: kwd_link.write(f + delim + k + nl)

	def wait(): #for debugging, pauses program until keypress
		print "press any key to continue..."
		m.getch()
		
	delim = ','
	nl = '\n'
	matches = [] #temporary storage for matching terms, will store nested list of kw:filename pairs
		
	###############################################################################################
	#open keyword file
	k = open(rootdir + 'keywords.txt','r').read()
	kl = k.splitlines()
	kd = {} #list of search terms
	
	#load keywords into dictionary
	for ln,l in enumerate(kl):
		r = l.split(delim)
		if ln == 0:	pass #headings, skip
		else: kd[r[0].strip()] = r[1].strip() #load dictionary
	
	###############################################################################################
	# destination file for results
	kwd_link =open('wap_priorities_link.txt','w') # destination file for results
	kwd_link.write('priority'+ delim + 'keyword' + nl) # add header line
	
	###############################################################################################
	#cycle through plans in plandir folder
	# file_slug =  slugify(file[:-4]) #filename of current plan (minus .txt extension)
	f = open(rootdir + 'habitat_to_priorities.txt','r').read()
	fl = f.splitlines()

	#cycle through keywords
	for t in kd.keys():
		#parse through file line by line
		for ln, l in enumerate(fl):
			#check if search term in line
			ld = l.split(delim)
			pri = ''.join(ld[6:]).lower() # join all elements split by comma in text
			if t in pri: save_unique_match(ld[1],t) 
	
	#save matches to file, reset matches array
	for i in matches: kwd_link.write(delim.join(i) + nl)
	matches = []
			
if __name__ == "__main__":
	main()