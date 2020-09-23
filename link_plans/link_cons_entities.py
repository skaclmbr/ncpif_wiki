### finds matches from keyword list in text files in given folder
### INPUT:
###		keywords.txt: csv file containing search_term, id values
###		plandir: folder path to location of text files to be searched
### OUTPUT:
###		keyword_link.txt: csv file containing keyword key and slugified text file title

import os
import sys
import datetime
import msvcrt as m



def main():

	now = datetime.datetime.utcnow()
	tm = str(now.strftime('%Y-%m-%d'))+'T'+ str(now.strftime('%X'))+'Z' #run date - to be used in file name
	print (tm)

	rootdir= os.path.dirname(os.path.abspath(__file__)) #retrieves the current file location as the base folder
	plandir= rootdir + '\\plans_txt\\' #search through text files in this folder
	

	def slugify(t,d='-'):
		#pass text and delimiter
		#insert delimiter into spaces in text
		t.replace(' ', d)
		t.replace('_', d)
		return t

	def wikify(t,d=' '):
		#pass text and delimiter
		#insert delimiter into spaces in text
		r = t.replace('_',' ').title().replace("'S","'s") #remove underscores, use proper case, lowercase possessives (caused by .title())
		return r
		
	def save_unique_match(f,i):
		#pass:
		#	k = keyword id
		#	f = filename slug
		#check to see if pair already exists in matches, if not, add
		fk = [f]+i
		if fk not in matches: matches.append(fk)
		# if [f,k] not in matches: kwd_link.write(f + delim + k + nl)

	def wait(): #for debugging, pauses program until keypress
		print ("press any key to continue...")
		m.getch()
		
	delim = ','
	nl = '\n'
	matches = [] #temporary storage for matching terms, will store nested list of kw:filename pairs
		
	###############################################################################################
	#open keyword file
	k = open(rootdir + '\\20200413_keywords.txt','r', encoding='utf-8').read()
	kl = k.splitlines()
	kd = {} #list of search terms
	
	#load keywords into dictionary
	for ln,l in enumerate(kl):
		r = l.split(delim)
		if ln == 0:	pass #headings, skip
		else: kd[r[0].strip()] = [r[1].strip(),r[2].strip()] #load dictionary
	
	# print (kd)
	
	
	###############################################################################################
	# destination file for results
	kwd_link =open(str(tm[:10])+'_keyword_link.txt','w', encoding='utf-8') # destination file for results
	kwd_link.write(delim.join(['plan_wiki','link_wiki','type']) + nl) # add header line
	
	###############################################################################################
	#cycle through plans in plandir folder
	for dp, dn, fs in os.walk(plandir):
		for file in fs:
			file_slug = slugify(file[:-4]) #filename of current plan (minus .txt extension)
			file_wiki = wikify(file[:-4]) #filename of current plan (minus .txt extension)
			print (dp)
			print (file)
			f = open(dp + file,'r', encoding='utf-8').read()
			fl = f.splitlines()
			
			print ('--------------------------------------' + nl + file_wiki + nl)
			
			for ln, l in enumerate(fl):
				#parse through file line by line

				for key,item in kd.items():
				#cycle through keywords
					#check if search term in line
					# print(t)
					if key in l: save_unique_match(file_wiki,item) 
			
			#save matches to file, reset matches array
			for i in matches: kwd_link.write(delim.join(i) + nl)
			matches = []
	# print (kd)
			
if __name__ == "__main__":
	main()