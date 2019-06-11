import sys
from pybtex.database.input import bibtex
from pybtex.database import Person

parser = bibtex.Parser()
bib_data = parser.parse_file(sys.argv[1]) #'data/0/0000/7237.bib'

fine_grained = False


field_keys= [u'title', u'journal', u'year', u'month', u'day', u'volume', u'number', u'pages', u'note', u'issn', u'url']
person_keys = [u'author', u'editor']
name_splits = {u'first':'', u'middle':'', u'prelast':'', u'last':'', u'lineage':''}

for f in field_keys:
    try:
        # if f == u'year':
        #     a = unicode(bib_data.entries[bib_data.entries.keys()[0]].fields[f]).split()
        #     bib_data.entries[bib_data.entries.keys()[0]].fields[f] = a #' '.join([ tokens for tokens in a])
        # else:
            a = unicode(bib_data.entries[bib_data.entries.keys()[0]].fields[f]).split()
            bib_data.entries[bib_data.entries.keys()[0]].fields[f] = ' '.join([f + '-' + tokens for tokens in a])
    except:
        pass


for p in person_keys:
    try:
        person_list = []
        for person in bib_data.entries[bib_data.entries.keys()[0]].persons[p]:
            name_splits = {u'first': '', u'middle': '', u'prelast': '', u'last': '', u'lineage': ''}
            for name_types in name_splits:
                if person.get_part(name_types) != []:
                    if fine_grained:
                        name_splits[name_types] = p + '-' + name_types + '-' + person.get_part(name_types)[0]
                    else:
                        name_splits[name_types] = p  + '-' + person.get_part(name_types)[0]

            new_p = Person(first=name_splits[u'first'], middle=name_splits[u'middle'],
                           prelast=name_splits[u'prelast'], last=name_splits[u'last'],
                           lineage=name_splits[u'lineage'])
            person_list.append(new_p)

        bib_data.entries[bib_data.entries.keys()[0]].persons[p] = person_list
    except Exception, e:
        pass


print(bib_data.to_string('bibtex'))
