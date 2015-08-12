# -*- coding: utf-8 -*-
"""
Script for cosine similarity for UNDAFs
"""

from similarity.cosine_sim import CosineSimilarity
from preprocess.process_json import Preprocessor


"""
Preprocessing the undaf documents
"""

if __name__ == "__main__":

    from gensim import corpora, models

    clean_data_fp = '../data/sdg_v2.json'
    dict_fp = '../data/sdg_v2.dict'
    corpus_fp = '../data/sdg_v2.mm'
    model_fp = '../data/sdg_v2.lda_model'

    # loading dictionary, corpus, lda_model
    dictionary = corpora.Dictionary.load(dict_fp)
    corpus = corpora.MmCorpus(corpus_fp)
    lda = models.ldamodel.LdaModel.load(model_fp)

    cosSim = CosineSimilarity(dictionary=dictionary,
                              corpus=corpus,
                              model=lda)

    cosSim.save_index('../data/sdg_v2.index')

    # loading undaf data
    undaf_fp = '../data/undaf_v2.json'
    p = Preprocessor(undaf_fp)
    p.loadjson()
    undaf_docs = p.json

    # loading metatopic data
    sdg = Preprocessor(clean_data_fp)
    sdg.loadjson()
    sdg_metatopics = sdg.json[0].keys()

    for topic in sdg_metatopics:
        print topic

    for k,v in p.json[0].items():
        simScore = cosSim.calculate_sim(v, 10)
        print '\n', k
        {'y': 0.089070708, 'x': 0, 'doc': 2},
        for i in range(len(simScore)):
            print "{\'y\': %f, \'x\': %d}" % (simScore[i], i)

    doc1 = "UN agencies will focus on system strengthening that creates a more\
            inclusive democracy through the creation and/or protection of\
            ‘invited spaces’ in which all citizens can interact and engage\
            with government, from the level of Ward Citizens’ Forums to that\
            of the national assembly. Inclusive democracy, based on participation\
            and representation for all citizens, promotes accountable, effective\
            and efficient government. It enables the provision of public services\
            and public funds that improve livelihoods, and supports development for\
            all groups, the vulnerable in particular. The UN’s contributions\
            will ensure these groups are prioritized in plans and budgets as\
            well as meaningfully represented in government bodies at all levels,\
            be they administrative, legislative, judicial or quasi-autonomous\
            constitutional bodies. Devolution has been a priority of the GoN\
            since the mid-1990s. Its vision was captured in the 1999 Local\
            Self-Governance Act and its subsequent rules and regulations, the\
            gender-responsive budget guidelines and the 2001 Decentralization\
            Implementation Plan. More recently, it has been embodied in the\
            Local Governance and Community Development Programme (LGCDP),\
            fully owned by the government through its implementing agency,\
            the Ministry of Federal Affairs and Local Development (MFALD).\
            With its focus on strengthening access to public services and\
            the provision of local development funds for bottom-up allocations\
            through local bodies, the LGCDP demonstrates a strong government\
            commitment to devolution. Electoral reform, including the\
            registration of voters and the holding of regular free and fair\
            elections"

    # simScore = cosSim.calculate_sim(doc1, 10)
    # for i in range(len(simScore)):
    #     print "%s --- %f" % (sdg_metatopics[i], simScore[i])