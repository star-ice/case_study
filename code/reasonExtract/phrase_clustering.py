# -*- coding: utf-8 -*-
'''
Use skipgram and negative sampling(as implemented in the Fasttext toolkit)
'''
import fasttext
import os
import numpy as np
from nltk.cluster import KMeansClusterer, euclidean_distance, cosine_distance
from sklearn import cluster
from sklearn import metrics
import nltk
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


base_url = "/Users/starice/OwnFiles/cityu/RA/"
output_base_url = "/Users/starice/OwnFiles/cityu/RA/case_study/phrase_embedding/clustering/"
pre_dir = ['type1', 'type2', 'type3', 'type4']
dir_name = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
dir_sname = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
def import_dataset(pre_dir, dir_name, dir_sname):
    i = "-".join(pre_dir)
    j = "-".join(dir_name)
    k = "-".join(dir_sname)
    phrase_vector_list = {}
    phrase_vector_file_path = "/Users/starice/Desktop/noun_phrases/" + str(i) + \
                              "_" + str(j) + "_" + str(k) + "_" + "nps.txt"
    if not os.path.exists(phrase_vector_file_path):
        print("路径不存在！", phrase_vector_file_path)
        return
    with open(phrase_vector_file_path, 'r') as f:
        next(f)
        for line in f:
            phrase_vector = eval(str(line))
            if phrase_vector[0] not in list(phrase_vector_list.keys()):
                phrase_vector_list[phrase_vector[0]] = np.frombuffer(phrase_vector[1], dtype=np.float32)
    return phrase_vector_list

def build_phrase_cluster(num_cluster):
    np.seterr(divide='ignore', invalid='ignore')
    phrase_vector_list = import_dataset(pre_dir[:1], dir_name[:1], dir_sname[:])
    print("The number of phrases are: ", len(list(phrase_vector_list.keys())))
    vocab = list(phrase_vector_list.keys())

    X = np.stack(phrase_vector_list[t] for t in vocab)
    print("X (the document matrix) has shape: {}".format(X.shape))

    kcluster = KMeansClusterer(num_cluster, distance=nltk.cluster.util.cosine_distance)
    assigned_clusters = kcluster.cluster(X, True)
    # print("Clustered:", X)
    # print("As:", assigned_clusters)
    # print("Means:", assigned_clusters.means())
    # print()
    return assigned_clusters, vocab

if __name__ == "__main__":
    assigned_clusters, vocab = build_phrase_cluster(10)
    words = list(vocab)
    cluster_dict = {10:"", 1:"", 2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 0:""}
    for i, word in enumerate(words):
        cluster_dict[assigned_clusters[i]] += str(word + ", ")
        # print(word + ":" + str(assigned_clusters[i]))
    with open("/Users/Starice/Desktop/cluster_dict.txt", "w+", encoding="utf-8") as f:
        for k, v in cluster_dict.items():
            f.write(str((k, v)) + "\n\n")