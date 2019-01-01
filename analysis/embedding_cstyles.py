
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


#'../DataParser/data/0/0000/1.b2s'
#'../DataParser/data/0/0000/2.b2s'
with open('../DataParser/data/0/0000/10.b2s', 'r') as styles, open('../DataParser/data/0/0000/10.sl', 'r') as lstyles:
    style_string = styles.readlines()
    lstyle_string = lstyles.readlines()


tfidf_vectorizer = TfidfVectorizer(max_df=0.99, max_features=5000,
                                   min_df=0.01, stop_words=None,
                                   use_idf=False, tokenizer=_preprocess, ngram_range=(1, 3))
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
    dist = 1 - cosine_similarity(tfidf_matrix)
    #mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    mds = TSNE()


    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

    xs, ys = pos[:, 0], pos[:, 1]



    get_color = lambda: random.randint(0, 255)

    unique_color_list = {}

    unique_labels = list(set(labels))
    for plot_cluster in unique_labels:
        unique_color_list[plot_cluster] = '#%02X%02X%02X' % (get_color(), get_color(), get_color())



    # set up plot
    fig, ax = plt.subplots(figsize=(10, 10))  # set size
    ax.margins(0.0)  # Optional, just adds 5% padding to the autoscaling


    # iterate through groups to layer the plot
    # note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    for group, name, x, y in zip(labels, names, xs, ys):
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

        #TODO: name important ones
        if name in ['acm-sigchi-proceedings-extended-abstract-format', 'chicago-author-date',
                    'apa', 'modern-language-association',
                    'turabian-fullnote-bibliography', 'ieee']:
           ax.text(x, y, name, size=10)



    custom_leg = [Line2D([], [], marker='o', linestyle='None',
                         color=unique_color_list[item], label=item,
                     markersize=6) for item in unique_labels]
    ax.legend(custom_leg, unique_labels, loc='upper center', frameon=False,
              numpoints=1, fontsize='small', mode='expand', ncol=4)

    # ax.legend(numpoints=0.5)
    plt.show()  # show the plot
    plt.savefig('cstyles1.png', dpi=200)

plotter()
exit()

