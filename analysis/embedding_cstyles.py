
from sklearn.feature_extraction.text import TfidfVectorizer
import random
from gensim.similarities import MatrixSimilarity
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS, TSNE
from matplotlib.markers import MarkerStyle
from matplotlib.lines import Line2D
from sklearn import cluster
from sklearn.decomposition import PCA, TruncatedSVD
import os
import xml.etree.ElementTree as ET

def _preprocess(text):
    return text.strip().split()


with open('../DataParser/data/0/0000/0.b2s', 'r') as styles:
    all = styles.readlines()
    style_string = []
    lstyle_string = []
    all2 = []
    for item in all:
        a = item.strip()
        if a is not '':
            all2.append(a)

    style_string = [all2[i] for i in xrange(len(all2)) if i%2 == 0]
    lstyle_string = [all2[i] for i in xrange(len(all2)) if i%2 != 0]

    print lstyle_string

    assert(len(style_string) == len(lstyle_string))





tfidf_vectorizer = TfidfVectorizer( max_features=5000, lowercase=False,
                                    stop_words=None,
                                   use_idf=False, tokenizer=_preprocess, ngram_range=(1, 4))
tfidf_matrix = tfidf_vectorizer.fit_transform([' '.join(item).decode('utf-8', errors='replace') for item in style_string])

feats_names = tfidf_vectorizer.get_feature_names()


def parse_label_file(labels_strings):
    out_labels = []
    out_name = []
    for items in labels_strings:
        s = items.strip().split(' ')
        if len(s) > 1:
            out_name.append(s[0])
            names = ET.fromstring("<fake>" + ' '.join(s[1:]) +"</fake>")
            for items in names.findall("category"):
                a=items.attrib['field']
            out_labels.append(a)
        else:
            out_name.append(s[0])
            out_labels.append('NA')
    return out_labels, out_name


labels, names = parse_label_file(lstyle_string)




def plotter(labels=labels, tfidf_matrix=tfidf_matrix):

    dist = 1 - cosine_similarity(tfidf_matrix) #precomputed is not there in TSNE
    mds = TSNE(random_state=1)
    pos = mds.fit_transform(tfidf_matrix.todense())  # shape (n_samples, n_components) either tfidf_matrix.todense() for raw or dist for processed

    xs, ys = pos[:, 0], pos[:, 1]

    get_color = lambda: random.randint(0, 255)


    # def static_list():
    #     a=[]
    #     counter = 0
    #     while counter < 30:
    #         a.append('#%02X%02X%02X' % (get_color(), get_color(), get_color()))
    #         counter+=1
    #     print a
    # static_list()

    static_color_list = ['#e6194b', '#3cb44b',  '#4063d8', '#f58231', '#911eb4', '#f032e6', '#bcf60c', '#9a6324', '#000000', '#fabebe',  '#cffac8', '#800000', '#8f8000', '#ffd8b1', '#000075', '#DF87A6', '#A63C72', '#7D3997', '#91C1E5', '#196BE0', '#6C1F99', '#A4A6B9', '#6DBC1F', '#E2CF4A', '#0D356D', '#DC6D0D', '#BCACE2', '#6A128D', '#B93AB9', '#9C16AF', '#6E7A1C', '#EF508F', '#A34DA5', '#34A6B7', '#292349', '#9074D1', '#3D435E', '#D3E734', '#3FFF48', '#CD5A09', '#A88348', '#27F05C', '#D20076', '#E4B25C', '#871483']

    unique_color_list = {}

    unique_labels = sorted(list(set(labels + ['astronomy'])))

    for i, plot_cluster in enumerate(unique_labels):
        unique_color_list[plot_cluster] = static_color_list[i] #'#%02X%02X%02X' % (get_color(), get_color(), get_color())


    # set up plot
    fig, ax = plt.subplots(figsize=(10, 10))  # set size
    fig, bx = plt.subplots(figsize=(3, 10))
    ax.margins(0.0)  # Optional, just adds 5% padding to the autoscaling


    # iterate through groups to layer the plot
    # note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    for group, name, x, y in zip(labels, names, xs, ys):
        if group == 'generic-base':
            ax.plot(x, y, marker='*', linestyle='', ms=12,
                    label=names, color=unique_color_list[group],
                    markersize=2,
                    mec='none')
            #ax.text(x, y, name, size=12)

        ax.plot(x, y, marker='.', linestyle='', ms=12,
                label=names, color=unique_color_list[group],
                markersize=2,
                mec='none')
        ax.set_aspect('auto')
        ax.tick_params( \
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom='off',  # ticks along the bottom edge are off
            top='off',  # ticks along the top edge are off
            labelbottom='off')
        ax.tick_params( \
            axis='y',  # changes apply to the y-axis
            which='both',  # both major and minor ticks are affected
            left='off',  # ticks along the bottom edge are off
            top='off',  # ticks along the top edge are off
            labelleft='off')


        name_map = {'acm-sigchi-proceedings-extended-abstract-format':'ACM', 'chicago-author-date':'Chicago-AD',
                    'apa':'APA', 'modern-language-association':'MLA',
                    'turabian-fullnote-bibliography':'Turabian', 'ieee':'IEEE', 'chicago-fullnote-bibliography':'Chicago-NB',
                    'nature':'Nature', 'vancouver':'Vancouver', 'elsevier-harvard':'Elsevier-Harvard',
                    'harvard-cranfield-university':'Harvard-Cranfield',
                    'taylor-and-francis-national-library-of-medicine':'Taylor-Francis-Medicine', 'iso690-author-date-fr':'ISO690-FR',
                    'international-labour-organization':'ILO',
                    'harvard-institut-fur-praxisforschung-de': 'Harvard-DE',
                    'harvard-deakin-university': 'Harvard-Deakin',
                    'harvard-kings-college-london': 'Harvard-KCL',
                    'springer-vancouver-author-date': 'Springer-Vancouver-AD',
                    'springer-vancouver' : 'Springer-Vancouver'
                    }

        if name in name_map.keys():
           ax.text(x, y, name_map[name], size=12)



    custom_leg = [Line2D([], [], marker='o', linestyle='None',
                         color=unique_color_list[item], label=item,
                     markersize=6) for item in unique_labels]
    bx.legend(custom_leg, unique_labels, loc='right', frameon=False,
               numpoints=1, fontsize='small', mode='expand', ncol=1)

    plt.show()  # show the plot


plotter()
exit()
