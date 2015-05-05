# -*- coding: utf-8 -*-
"""
Script for cosine similarity for UNDAFs
"""

from cosine_sim import CosineSimilarity
from process_json import Preprocessor


"""
Preprocessing the undaf documents
"""

# preprocess('../core-engine/data/undaf.json', 'data/undaf.json')

if __name__ == "__main__":
    from gensim import corpora, models

    # loading dictionary, corpus, lda_model
    dictionary = corpora.Dictionary.load('data/sdg.dict')
    corpus = corpora.MmCorpus('data/sdg.mm')
    lda = models.ldamodel.LdaModel.load('data/sdg.lda_model')

    #loading json file
    sdg_p = Preprocessor('data/sdg.json')
    sdg_p.loadjson()

    p = Preprocessor('data/undaf.json')
    p.loadjson()

    # TODO redo the data structuring, because it didn't save
    for key in p.json[0].keys():
        cosSim = CosineSimilarity(dictionary=dictionary,
                                  corpus=corpus,
                                  model=lda)

        cosSim.save_index('data/sdg.index')
        simScore = cosSim.calculate_sim(doc4, 10)

