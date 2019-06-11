#!/usr/bin/python3
import argparse
import logging
import xml.etree.ElementTree as ET
import json
import os
import sys
from lxml import etree
from bs4 import BeautifulSoup
import codecs
import html


def main():
    logger = logging.getLogger()
    encodings = ['ISO-8859-1','ascii']
    for e in encodings:
        try:
            fh = codecs.open(args.metadatafile,'r',encoding=e)
            fh.seek(0)
        except UnicodeDecodeError:
            logging.debug('got unicode error with %s, trying a different encoding' % e)
        else:
            logging.debug('opening the file with encoding: %s' % e)
            break

    f = codecs.open(args.metadatafile,encoding=e)
    soup = BeautifulSoup(f.read(),'html.parser')
    logger.info("processing XML: "+args.metadatafile)

    metadata_all = []
    publisher_name = html.unescape(soup.find("publisher_name").text)
    publisher_city = html.unescape(soup.find("publisher_city").text)
    publisher_state = html.unescape(soup.find("publisher_state").text)
    publisher_country = html.unescape(soup.find("publisher_country").text)
    publisher_address = ','.join(filter(None,[publisher_city,publisher_state,publisher_country]))

    conference_block = soup.find("conference_rec")
    if conference_block is not None:
        venue_type = 'conference'
        '''
        venue_name is concatenated by proc_desc and proc_title
        e.g., proc_desc = "Proceedings of the 19th international conference"
              proc_title = "World wide web"
        venue_name is proc_desc + " on " + proc_title
        '''
        venue_acronym = soup.find("acronym").text.strip()
        proc_desc = soup.find("proc_desc").text.strip()
        proc_title = soup.find("proc_title").text.strip()
        if proc_title == '':
            venue_name = proc_desc 
        else:
            venue_name = proc_desc + " on " + proc_title
        journal_abbr = None
        venue = [venue_acronym, journal_abbr, venue_name]

        
        # conference location is concatenated by city, state, and country
        venue_loc = ', '.join([html.unescape(soup.find("city").text),
                                    html.unescape(soup.find("state").text),
                                    html.unescape(soup.find("country").text)])

        # conference starting and ending date
        conference_start_date = soup.find("start_date").text
        conference_end_date = soup.find("end_date").text
    
        # chair editors connected by " and "
        chair_editor_block = soup.find("chair_editor")
        editor_names = []
        if chair_editor_block is not None:
            for c in chair_editor_block.find_all("ch_ed"):
                name_components = [html.unescape(c.find("first_name").text.strip()),
                                       html.unescape(c.find("middle_name").text.strip()),
                                       html.unescape(c.find("last_name").text.strip()),
                                       html.unescape(c.find("suffix").text.strip())]
                editor_names.append(" ".join(filter(None,name_components)))

        issn = soup.find("issn").text
        volume = soup.find("proc_volume_no").text
        
        # journal related fields do not apply to proceedings
        number = None
        
    else:
        venue_type = 'journal'
        journal_code = soup.find("journal_code").text
        journal_abbr = soup.find("journal_abbr").text
        journal_name = soup.find("journal_name").text
        venue = [journal_code, journal_abbr, journal_name]
        issn = soup.find("issn").text
        volume = soup.find("volume").text
        number = soup.find("issue").text

        # chair editors
        editor_names = []
        editor_block = soup.find("editor")
        if editor_block is not None:
            for c in editor_block.find_all("ed"):
                name_components = [html.unescape(c.find("first_name").text.strip()),
                                        html.unescape(c.find("middle_name").text.strip()),
                                        html.unescape(c.find("last_name").text.strip()),
                                        html.unescape(c.find("suffix").text.strip())]
                editor_names.append(" ".join(filter(None,name_components)))

        # there is no venue for journals
        venue_loc = None


    '''
    article records
    '''
    for r in soup.find_all("article_rec"):
        metadata = {'venue_type':venue_type, 
                         'venue':venue,
                     'publisher':publisher_name,
             'publisher_address':publisher_address,
                       'editors':editor_names,
                        'volume':volume,
                          'issn':issn,
                        'number':number,
                     'venue_loc':venue_loc}
       
        # article_id
        metadata["article_id"] = r.find("article_id").text
        logger.debug("processing article: "+metadata["article_id"])
        metadata["article_publication_date"] = r.find("article_publication_date").text
        # title
        metadata["title"] = html.unescape(r.find("title").text)
        
        subtitle_block = r.find("subtitle")
        
        if subtitle_block is not None:
            metadata["subtitle"] = html.unescape(subtitle_block.text)
        else:
            metadata["subtitle"] = ""
            logger.debug("subtitle block not found for article: "+metadata["article_id"])

       
        url_block = r.find("url")
        if url_block is not None:
            metadata["url"] = url_block.text
        else:
            metadata["url"] = None

        page_from_block = r.find("page_from")
        if page_from_block is not None:
            metadata["page_from"] = page_from_block.text
        else:
            metadata["page_from"] = None

        page_to_block = r.find("page_to")
        if page_to_block is not None:
            metadata["page_to"] = page_to_block.text
        else:
            metadata["page_to"] = None

        metadata["doi_number"] = r.find("doi_number").text

        abstract_block = r.find("abstract")
        if abstract_block is not None:
            metadata["abstract"] = html.unescape(abstract_block.find("par").text)
        else:
            metadata["abstract"] = ""
            logger.debug("abstract block not found for article: "+metadata["article_id"])

        keywords_block = r.find("keywords")
        if keywords_block is not None:
            metadata["keywords"] = [html.unescape(kw.text) for kw in r.find("keywords").find_all('kw')]
        else:
            metadata["keywords"] = []
            logger.debug("keywords block not found for article: "+metadata["article_id"])
 
        metadata["authors"] = []
        for au in r.find("authors").find_all('au'):
            person_id_block = au.find("person_id")
            if person_id_block is not None: 
                person_id_block_text = person_id_block.text
            else:
                person_id_block_text = None

            orcid_id_block = au.find("orcid_id")
            if orcid_id_block is not None: 
                orcid_id_block_text = orcid_id_block.text
            else:
                orcid_id_block_text = None
            
            affiliation_block = au.find("affiliation")
            if affiliation_block is not None:
                affiliation_block_text = html.unescape(affiliation_block.text.strip())
            else:
                affiliation_block_text = None

            email_address_block = au.find("email_address")
            if email_address_block is not None:
                email_address_block_text = email_address_block.text.strip()
            else:
                email_address_block_text = None

            metadata["authors"].append({"person_id":person_id_block_text,
                                         "orcid_id":orcid_id_block_text,
                                       "first_name":html.unescape(au.find("first_name").text),
                                      "middle_name":html.unescape(au.find("middle_name").text.strip()),
                                        "last_name":html.unescape(au.find("last_name").text),
                                           "suffix":html.unescape(au.find("suffix").text),
                                      "affiliation":affiliation_block_text,
                                    "email_address":email_address_block_text})

        metadata["references"] = []
        references_block = r.find("references")
        if references_block is not None:
            for ref in references_block.find_all('ref'):
                ref_obj_id_text = None
                ref_obj_pid_text = None
                ref_text_text = None

                ref_obj_id_block = ref.find('ref_obj_id')
                ref_obj_pid_block = ref.find('ref_obj_pid')
                ref_text_block = ref.find('ref_text')

                if ref_obj_id_block is not None: ref_obj_id_text = ref_obj_id_block.text
                if ref_obj_pid_block is not None: ref_obj_pid_text = ref_obj_pid_block.text
                if ref_text_block is not None: ref_text_text = ref_text_block.text
                    
                metadata["references"].append({"ref_obj_id":ref_obj_id_text,
                  "ref_obj_pid":ref_obj_pid_text,
                  "ref_text":html.unescape(ref_text_text)})
            
        else:
            logger.debug("references block not found for article: "+metadata["article_id"])

        fulltext_block = r.find("fulltext")
        if fulltext_block is not None:
            metadata["fulltext"] = html.unescape(r.find("fulltext").text)
        else:
            logger.debug("fulltext block not found for article: "+metadata["article_id"])
            metadata["fulltext"] = ''

        metadata_all.append(metadata)
        logger.debug("articles processed in XML file: %d" % len(metadata_all))
        
    # write to a json file
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    xmlfiledir,xmlfiletrunk = os.path.split(args.metadatafile)
    jsonfile = os.path.join(args.outdir,os.path.splitext(xmlfiletrunk)[0]+".json")
    with codecs.open(jsonfile,'w','utf-8-sig') as outfile:
        json.dump(metadata_all,outfile,ensure_ascii=False)

    logger.debug("json file written into: "+jsonfile)


# accept input parameters
parser = argparse.ArgumentParser()
# a positional argument
parser.add_argument("metadatafile",metavar="METADATAFILE",type=str,help="The XML file containing ACM DL paper metadata")
# an optional argument
parser.add_argument("--outdir",help="The directory to save output files. Files are saved to json/ on the same level of src/ by default.",default='../json')
# an optional argument with a shortcut
parser.add_argument("-v","--verbose",help="increase output verbosity",action="store_true",dest="verbose",default=False)
# logdir
parser.add_argument("--logdir",help="The directory to save log files. Logs are saved to logs/ on the same level of src/ by default.",default='../logs')
args = parser.parse_args()
if args.verbose:
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

# logging configurations
if not os.path.exists(args.logdir):
    os.makedirs(args.logdir)
logging.basicConfig(level=logging_level,\
              filename="../logs/acmxml2json.log",\
              format="%(asctime)s %(name)-10s %(levelname)-8s %(message)s",
              filemode="a")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)-10s %(levelname)-8s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)
logging.debug("logging configuration done")

# pass command line configuration to main program
#confc = {"xmlfile":args.metadatafile,"outdir":args.outdir}

if __name__ == "__main__":
    main()
