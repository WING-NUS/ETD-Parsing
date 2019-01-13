#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os, glob


cwd = os.getcwd()


def blind_test_mapping():
    mapping_dict = {
'doi':'DOI',
'authors':'author',
'marker':'citation-number',
'booktitle':'collection-title',
'journal':'collection-title',
'publisher':'container-title',
'editor':'editor',
'issue':'issue',
'others':'others',
'pages':'page',
'page':'page',
'publisher':'publisher',
'title':'title',
'volume':'volume',
'year':'year',
'month':'year',
'address':'container-title',
'note': 'other',
'url': 'other',
'number': 'volume',
'institution': 'other',
'school': 'other',
'type': 'other',
'reportnumber': 'other',
'edition': 'volume',
    }


    path = '/convert-ann-eval-output'
    out_f = open('blind_test', 'w')

    for filename in glob.glob(os.path.join(cwd + path, '*.tll')):
        with open (filename, 'r') as f:
            for lines in f.readlines():
                a = lines.strip().split()
                if a:
                    if a[1] in mapping_dict.keys():
                        label = mapping_dict[a[1]]
                    else:
                        label_top_level = a[1].split('_')

                        if len(label_top_level) == 2:
                            if label_top_level[0] in mapping_dict.keys() and label_top_level[1] == 'extra':
                                label = mapping_dict[label_top_level[0]]
                            else:
                                print (label_top_level[0])
                        else:
                            print (label_top_level)

                    out_f.write(a[0]+'\t'+label+'\n')
            out_f.write('\n')


def cora_mapping():
    mapping_dict = {
        'author': 'author',
        'booktitle': 'collection-title',
        'journal': 'collection-title',
        'editor': 'editor',
        'pages': 'page',
        'publisher': 'publisher',
        'title': 'title',
        'volume': 'volume',
        'date': 'year',
        'location': 'other',
        'note': 'other',
        'tech': 'other',
        'institution': 'other',
    }

    path = 'cora.train'
    out_f = open('cora_test', 'w')
    seta = []

    with open(path, 'r') as f:
            for lines in f.readlines():
                a = lines.strip().split()
                if a:
                    a = [a[0], a[-1]]
                    seta.append(a[1])
                    if a[1] in mapping_dict.keys():
                        label = mapping_dict[a[1]]
                    # else:
                    #     label_top_level = a[1].split('_')
                    #
                    #     if len(label_top_level) == 2:
                    #         if label_top_level[0] in mapping_dict.keys() and label_top_level[1] == 'extra':
                    #             label = mapping_dict[label_top_level[0]]
                    #         else:
                    #             print(label_top_level[0])
                    #     else:
                    #         print(label_top_level)

                    out_f.write(a[0] + '\t' + label + '\n')
                else:
                    out_f.write('\n')
    print (set(seta))

#Note both cora and blind_test need to be updated for mapping once conf and ETD bibs are also added

if __name__ ==  "__main__":
    #blind_test_mapping()
    cora_mapping()
