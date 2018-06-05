import pandas as pd
import numpy as np
from collections import OrderedDict
from iobio import cluster_ordered_agglomerative
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors
from scipy.stats import triang
import uuid, random
class Baffle:
    def __init__(self,data,k_min=4,clusters=5):
        self._data = data

        #save the names
        snames = pd.DataFrame({'samples':data.columns})
        snames['id'] = [str(uuid.uuid4()) for x in range(0,snames.shape[0])]
        self.snames = snames

        #get the clusters
        cd = data.corr()
        acd = cluster_ordered_agglomerative(cd,clusters)
        # add the k nearest neighbors from the tsne every point to its cluster point
        tcd = TSNE(2).fit_transform(cd)
        tcd = pd.DataFrame(tcd)
        tcd.columns = ['x','y']
        tcd.index = cd.columns
        nns = pd.DataFrame(NearestNeighbors(n_neighbors=k_min+1).fit(tcd).kneighbors_graph(tcd).toarray())
        nns.columns = cd.columns.copy()
        nns.columns.name = 'sample_2'
        nns.index = cd.columns.copy()
        nns.index.name = 'sample_1'
        nns = nns.unstack().reset_index().rename(columns={0:'match'})
        nns = nns[nns['match']!=0]
        nns = nns[nns['sample_1']!=nns['sample_2']]

        ## For each cluster samples add in nn samples
        clusters = {}
        for cluster_id in acd['cluster_id'].unique():
            #print(cluster_id)
            clusters[cluster_id] = set(acd[acd['cluster_id']==cluster_id].index)
            for member in list(clusters[cluster_id]):
                #print(member)
                ## add each points nearest neighbors
                ns = list(nns.loc[nns['sample_1']==member,'sample_2'])
                clusters[cluster_id] |= set(ns)
        self.clusters = clusters
        models = {}
        for cluster_id in self.clusters:
            models[cluster_id] = data[list(clusters[cluster_id])].\
                 apply(lambda x: pd.Series(OrderedDict(zip(
                     ['min','max','mean','std','values'],
                     [np.min(x),np.max(x),np.mean(x),np.std(x)]+[list(x)]
            ))),1)
        self.models = models

    def permute(self):
        ids = []
        for cluster_id in self.clusters:
            ids += [cluster_id]*len(self.clusters[cluster_id])
        myid = ids[random.randint(0,len(ids)-1)]
        model = self.models[myid]
        myname = str(uuid.uuid4())
        fake = model.apply(lambda x:
            pd.Series(OrderedDict(zip(
                [myname],
                [np.mean([x['values'][random.randint(0,len(x['values'])-1)],
                          random.triangular(x['min'],x['max'],x['mean'])])]
            )))
            ,1)
        return fake

    def fakes(self,n=1):
        return pd.concat([self.permute() for x in range(0,n)],1)
