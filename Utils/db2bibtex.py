#!/usr/bin/python3
# The program reads ACM DL bibliographic data from a MysQL database and 
# generate bibtex files, putting them in directories corresponding to 
# conferences and journal articles, respectively. 
# Version history:
# 2019-01: Bradley Desh
#          * basic functions are implemented, including reading from the database and
#            writing output files. 
# 2019-04: Jian Wu
#          * changed the output format, using {} instead of "" for fields
#          * pass input parameters
# 2019-04: Jian Wu
#          * segment the addresses then add spaces between tokens, e.g., 
#            New York,NY,USA is converted to New York, NY, USA
# 2019-06: Jian Wu
#          * add more comments
#          * separate journals and conferences output to different directories
# 
#paperE author, title, journal, year, volume, number, pages, doi
#inproceedings: author, title, booktitle, year, editor, volume, number, pages, address, publisher
#author: The name(s) of the author(s) (in the case of more than one author, separated by and)
#title: title of the work
#journal: the journal or magazine where the paper was published
#booktitle: name of conference

import mysql.connector
import codecs
import argparse
import logging
import os
import string
from multiprocessing_mapreduce import SimpleMapReduce
from config import workdir,acmdldb

# the task to write a bibtex file using metadata retrieved from the database
def dbrec_to_bibtex(dbrec):
    logger = logging.getLogger("dbrec_to_bibtex")
    num,article_id,title,year,issn,number,volume,venue_name,page_from,page_to,editor,publisher,address,doi,venue_type = dbrec[0:15]
    cnx = mysql.connector.connect(**acmdldb)
    cursor = cnx.cursor(buffered = True)
    cursor.execute("SELECT first_name, middle_name, last_name, suffix FROM AUTHOR WHERE article_id = " + str(article_id))
    author_info = cursor.fetchall()
    cursor.close()
    cnx.close()

    auth = ""
    for person in author_info:
        first_name, middle_name,last_name,suffix = person[0:4]
        first_name = first_name.strip()
        middle_name = middle_name.strip()
        last_name = last_name.strip()
        suffix = suffix.strip()

        # last_name, suffix, first_name middle_name, e.g., Ororbia,II, Alexander G.
        auth += "{" + last_name + "}, {" + first_name + "} "
        if middle_name != "":
            auth += "{" + middle_name + "} "
        if suffix != "":
            auth += ", {" + suffix + "} "
        auth += "and "
    author = auth[:len(auth) - 5]

    # generate bibtex string based on record type
    text = ""
    if venue_type == 'conference':
        text += "@inproceedings{ " + str(article_id) + ",\n"
        text += "\tauthor     = {" + author   + "},\n"
        text += "\ttitle      = {" + title    + "},\n"
        text += "\tbooktitle  = {" + venue_name  + "},\n"
        text += "\tyear       = {" + str(year)   + "},\n"
        if volume != None:
            text += "\tvolume   = {" + str(volume) + "},\n"
        if number != None:
            text += "\tnumber   = {" + str(number) + "},\n"
        if editor != "" and editor != None:
            text += "\teditor   = {" + editor      +  "},\n"
        if publisher != "" and publisher != None:
            text += "\tpublisher  = {" + publisher +  "},\n"
        if address != "" and address != None:
            # segment the address using "," and reconcatenate them by a space
            address = ", ".join(address.split(","))
            text += "\taddress    = {" + address   +  "},\n"
        if page_from != None and page_to != None:
            text += "\tpages      = {" + str(page_from) + "--" + str(page_to) +  "},\n"
        elif page_from != None:
            text += "\tpages      = {" + str(page_from) + "},\n"

        text = text[:len(text)-2] + "\n}"
        subdir = str(int(article_id / 1000))
        bibtexdir = os.path.join(conf_dir,subdir)
    elif venue_type == 'journal':
        text += "@article { " + str(article_id) + ",\n"
        text += "\tauthor  = {" + author  + "},\n"
        text += "\ttitle   = {" + title   + "},\n"
        text += "\tjournal = {" + venue_name + "},\n"
        text += "\tyear    = {" + str(year)  + "},\n"
        if volume != None:
            text += "\tvolume= {" + str(volume)+ "},\n"
        if number != None:
            text += "\tnumber= {" + str(number) +"},\n"
        if page_from != None and page_to != None:
            text += "\tpages = {" + str(page_from) + "--" + str(page_to) +  "},\n"
        elif page_from != None:
            text += "\tpages = {" + str(page_from)  + "},\n"
        if doi != "" and doi != None:
            text += "\tdoi     = {" + doi +  "},\n"

        text = text[:len(text)-2] + "\n}"
        subdir = str(int(article_id / 1000))
        bibtexdir = os.path.join(jour_dir,subdir)

    # subdirectory name
    if not os.path.exists(bibtexdir):
        os.makedirs(bibtexdir,exist_ok=True)
    outputfile = os.path.join(bibtexdir,str(article_id) + ".bib")
    f = codecs.open(outputfile, "w",encoding='utf-8-sig')
    f.write(text)
    print("BibTeX Created: {}".format(article_id))
    f.close()

    return [(venue_type,1)]

# reduce 
def count_type(item):
    venue_type, occurances = item
    return (venue_type,sum(occurances))

# accept input parameters
parser = argparse.ArgumentParser()
# a positional argument
#parser.add_argument("metadatafile",metavar="METADATAFILE",type=str,help="The XML file containing ACM DL paper metadata")
# an optional argument
parser.add_argument("--outdir",help="The directory to save output files. The default is $workdir/BibTexGenerator-v4-output.",default=os.path.join(workdir,"BibTexGenerator-v4-output"))
# an optional argument with a shortcut
parser.add_argument("-v","--verbose",help="increase output verbosity",action="store_true",dest="verbose",default=False)
# logdir
parser.add_argument("--logdir",help="The directory to save log files. The default is $workdir/logs.",default=os.path.join(workdir,"logs"))
args = parser.parse_args()
if args.verbose:
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

# logging configurations
if not os.path.exists(args.logdir):
    os.makedirs(args.logdir)
if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)
# create conference and journal directories inside the output directory
conf_dir = os.path.join(args.outdir,"conference")
jour_dir = os.path.join(args.outdir,"journal")
if not os.path.exists(conf_dir):
    os.makedirs(conf_dir)
if not os.path.exists(jour_dir):
    os.makedirs(jour_dir)

logging.basicConfig(level=logging_level,\
              filename=os.path.join(args.logdir,"db2bibtex.log"),\
              format="%(asctime)s %(name)-10s %(levelname)-8s %(message)s",
              filemode="a")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)-10s %(levelname)-8s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)
logging.debug("logging configuration done")


if __name__ == '__main__':

    cnx = mysql.connector.connect(**acmdldb)
    cursor = cnx.cursor(buffered = True)
    cursor.execute("SELECT iid, article_id, title, year, issn, number, volume, venue_name, page_from, page_to, editors, publisher_name, publisher_address, doi_number, venue_type FROM PAPER LIMIT 1000") 

    dbrecs = cursor.fetchall()
    cursor.close()
    cnx.close()

    mapper = SimpleMapReduce(dbrec_to_bibtex,count_type,num_workers=50)
    bibtex_types = mapper(dbrecs)

    for typename, count in bibtex_types:
        print('{}: {}'.format(typename,count))
