import json, urllib2, re, nltk
from collections import defaultdict

_names = dict()
_fp = open("/Users/michael/Documents/Classes/Advanced Bioinformatics/git/Clusterizer/test_output.json")
_json = json.load(_fp)

foo0 = "http://www.rcsb.org/pdb/explore/explore.do?structureId="
foo1 = "http://www.rcsb.org/pdb/explore/remediatedSequence.do?structureId="
foo2 = "http://www.rcsb.org/pdb/explore/biologyAndChemistry.do?structureId="
foo3 = "http://www.cathdb.info/version/latest/superfamily/"


classes = defaultdict(int)
orgs = defaultdict(int)
names = defaultdict(int)
types = defaultdict(int)
families = defaultdict(int)

def walk(data) :
	if isinstance(data, list) :
		for thing in data :
			walk(thing)
	elif isinstance(data, dict) :
		newData = dict(data)
		for key, val in data.iteritems() :
			#correct the cathid
			if str(key) == 'cathid' :
				cath = str(val)
				if str(val) != 'None' :
					print val
					cath =  val[0].replace(',','.')
					newData.update({'cathid' : cath.encode('utf-8')})
					newData.update({'cath_url':(foo3 + cath).encode('utf-8')})
					family = scrape_cath(cath)
					newData.update({'cath_superfamily': family.encode('utf-8')})
				
					if family in families :
						families[family] += 1
					else :
						families[family] = 1
				else :
					family = "N/A"
					newData.update({'cath_url': foo3.encode('utf-8')})
					newData.update({'cath_superfamily': family.encode('utf-8')})
					if family in families :
						families[family] += 1
					else :
						families[family] = 1
				print cath
				print "\t" + str(families[family]) + " : " + family 	
				

			if str(key) == "name" :
				match = re.search(r'%', str(val))
				if not match :
					name, length, type, cname, keyword, weight = scrape_pdb(str(val))
					newData.update({'pdb_url':(foo0 + name).encode('utf-8')})
					newData.update({'residues':length.encode('utf-8')})
					newData.update({'type':type.encode('utf-8')})
					newData.update({'organism':cname.encode('utf-8')})
					newData.update({'pdb_class':keyword.encode('utf-8')})
					newData.update({'weight':weight.encode('utf-8')})
					
					if keyword in classes :
						classes[keyword] += 1
					else :
						classes[keyword] = 1
					
					if cname in orgs :
						orgs[cname] += 1
					else :
						orgs[cname] = 1
						
					if name in names :
						names[name] += 1
					else :
						names[name] = 1

					if type in types :
						types[type] += 1
					else :
						types[type] = 1
			walk(val)
		data.update(newData)


def scrape_cath(cathid) :
	success = 0
	page = ""
	while success == 0 :
		try:
			page = urllib2.urlopen(foo3 + cathid).read()
			success = 1
		except urllib2.URLError as e:
			success = 0
			print str(e)
	
	#print page
	superfamily_pattern = re.compile('^\s*<h1>CATH Superfamily [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+<\/h1>\s*^\s*<h2>(.+)<small>', re.M)
	superfamily = superfamily_pattern.search(page)
	if superfamily :
		superfamily = superfamily.group().split('<h2>')
		superfamily = superfamily[1].split('<small')
		if(superfamily[0].strip()) :
			superfamily = superfamily[0].strip()
		else :
			superfamily = "N/A"		
	return superfamily
	
def scrape_pdb(name) :
	name = name[:-1]
	success0 = 0
	success1 = 0
	success2 = 0
	
	while success0 == 0:
		try:
			page0 = urllib2.urlopen(foo0 + name).read()
			success0 = 1
		except urllib2.URLError as e:
			success0 = 0
			print str(e)
	while success1 == 0:
		try:
			page1 = urllib2.urlopen(foo1 + name).read()
			success1 = 1
		except urllib2.URLError as e:
			success1 = 0
			print str(e)
	while success2 == 0:
		try:
			page2 = urllib2.urlopen(foo2 + name).read()
			success2 = 1
		except urllib2.URLError as e:
			success2 = 0
			print str(e)

	page0 = nltk.clean_html(page0)
	page1 = nltk.clean_html(page1)
	page2 = nltk.clean_html(page2)

	length_pattern = re.compile(r'.*Length:.*')
	type_pattern = re.compile(r'.*Chain Type:.*')
	keyword_pattern = re.compile(r'^\s*Keywords.*\n.*\n.*\n', re.M)
	cname_pattern = re.compile(r'^.*Common Name.*\n.*\n.*\n', re.M)
	cname2_pattern = re.compile(r'^.*Scientific Name.*\n.*\n.*\n', re.M)
	weight_pattern = re.compile('^.*Structure Weight:.*\n.*\n.*\n.*\n.*\n.*\n.*\n', re.M)
	
	weight = weight_pattern.search(page0)
	length = length_pattern.search(page1)
	type = type_pattern.search(page1)
	cname = cname_pattern.search(page2)
	cname2 = cname2_pattern.search(page2)
	keyword = keyword_pattern.search(page2)

	if weight :
		weight = weight.group().strip().split()[2]
		#print weight
	if length :
		length = length.group().strip().split()[1]
		#print "length " + length
	if type :
		type = type.group().strip().split()
		_type = ""
		for i in range(2, len(type)) :
			_type += " " + type[i]
		type = _type.strip()
	#	print "type " + type
	if cname :
		cname = cname.group().split()
		_cname = ""
		for i in range(2, len(cname)) :
			_cname += " " + cname[i]
		cname = _cname.strip()
		#print "cname " + cname
	elif cname2 :
		cname2 = cname2.group().split()
		_cname = ""
		for i in range(2, len(cname2)) :
			_cname += " " + cname2[i]
		cname = _cname.strip()
		#print "cname " + cname
	else :
		cname = "N/A"
		#print "cname " + cname
	if keyword :
		keyword = keyword.group().replace("\n", "")
		keyword = re.sub("Keywords\s*", "", keyword).strip()
		#print "keyword " + keyword
	#s = '",\n "len" : "' + length + '",\n "type" : "' + type + '",\n "animal" : "' + cname +'",\n "keyword" : "' + keyword + '",'
	#print 
	return name, length, type, cname, keyword, weight
	
walk(_json)

with open('useful.json', 'w') as outfile :
     json.dump(_json, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

with open('organisms.json', 'w') as outfile :
	json.dump(orgs, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

with open('classes.json', 'w') as outfile :
	json.dump(classes, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

with open('types.json', 'w') as outfile :
	json.dump(types, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

with open('names.json', 'w') as outfile :
	json.dump(names, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

with open('families.json', 'w') as outfile :
	json.dump(families, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
