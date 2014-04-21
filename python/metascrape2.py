import json, urllib2, re, nltk
from collections import defaultdict

_names = dict()
_fp = open("../html/test_output.json")
_json = json.load(_fp)

foo0 = "http://www.rcsb.org/pdb/explore/explore.do?structureId="
foo1 = "http://www.rcsb.org/pdb/explore/remediatedSequence.do?structureId="
foo2 = "http://www.rcsb.org/pdb/explore/biologyAndChemistry.do?structureId="
foo3 = "http://www.cathdb.info/version/latest/superfamily/"


classes = defaultdict(int)
orgs = defaultdict(int)
names = defaultdict(int)
types = defaultdict(int)

def walk(data) :
	if isinstance(data, list) :
		for thing in data :
			walk(thing)
	elif isinstance(data, dict) :
		newData = dict(data)
		for key, val in data.iteritems() :
			#correct the cathid
			if str(key) == 'cathid' :
				cath =  val[0].replace(',','.')
				newData.update({'cathid' : cath.encode('utf-8')})
				newData.update({'cath_url':(foo3 + cath).encode('utf-8')})
			if str(key) == "name" :
				match = re.search(r'%', str(val))
				if not match :
					name, length, type, cname, keyword, weight = scrape(str(val))
					newData.update({'pdb_url':(foo0 + name).encode('utf-8')})
					newData.update({'residues':length.encode('utf-8')})
					newData.update({'type':type.encode('utf-8')})
					newData.update({'organism':cname.encode('utf-8')})
					newData.update({'class':keyword.encode('utf-8')})
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
		print newData
		data.update(newData)


def scrape(name) :
	name = name[:-1]
	#print name
	page0 = nltk.clean_html(urllib2.urlopen(foo0 + name).read())
	page1 = nltk.clean_html(urllib2.urlopen(foo1 + name).read())
	page2 = nltk.clean_html(urllib2.urlopen(foo2 + name).read())

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
		#print "type " + type
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

print "++++++++++++++++++++++++++++++++++++++++++++\n"
print "++++++++++++++++++++++++++++++++++++++++++++\n"
print "++++++++++++++++++++++++++++++++++++++++++++\n"
print "++++++++++++++++++++++++++++++++++++++++++++\n"
print "++++++++++++++++++++++++++++++++++++++++++++\n"
print "++++++++++++++++++++++++++++++++++++++++++++\n"
print "++++++++++++++++++++++++++++++++++++++++++++\n"
print(_json)

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