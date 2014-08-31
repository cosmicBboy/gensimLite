# -*- coding: utf-8 -*-
"""
API interface for computing cosine similarities
"""

from gensim import similarities


class CosineSimilarity(object):

    def __init__(self, dictionary, corpus, model):
        self.dictionary = dictionary
        self.corpus = corpus
        self.model = model
        self.index = similarities.MatrixSimilarity(
            self.model[self.corpus])

    def save_index(self, fp):
        self.index.save(fp)
        return self

    def load_index(self, fp):
        similarities.MatrixSimilarity.load(fp)
        return self

    def doc2sim(self, doc):
        '''converts text document to similarity array'''
        #convert document to bag of words vector
        vec_bow = self.dictionary.doc2bow(doc.lower().split())
        #convert bow vector to model vector
        vec_model = self.model[vec_bow]
        return self.index[vec_model]

    def bow2model_vec(self, vec):
        '''converts bow vector to model vector space'''
        return self.model[vec]

    def model_vec2sim(self, model_vec):
        '''converts a dictionary-converted vector to similarity'''
        return self.index[model_vec]


if __name__ == "__main__":
    from gensim import corpora, models
    dictionary = corpora.Dictionary.load('data/sdsn2.dict')
    corpus = corpora.MmCorpus('data/sdsn2.mm')
    lda = models.ldamodel.LdaModel.load('data/sdsn2.lda_model')
    doc = "Road transport is the dominant mode of transport in\
           sub-Saharan Africa, carrying close to 90 percent of\
           the region's passenger and freight transport, and\
           providing the only access to rural communities where\
           over 70 percent of Africans live. Despite their importance,\
           most of the region's nearly 2 million km of roads are poorly\
           managed and badly maintained. By 1990, nearly a third of the\
           $150 billion invested in roads had been eroded through lack\
           of maintenance. To restore only those roads that are\
           economically justified and prevent further deteriorations\
           will require annual expenditures of at least $1.5 billion\
           over the next ten years, or more than double the requirements\
           of regular maintenance. To find sustainable solutions to these\
           problems, the United Nations Economic Commission for Africa\
           (UNECA) and the World Bank launched the Road Maintenance\
           Initiative (RMI) as part of the sub-Saharan Africa Transport\
           Policy Program (SSATP). With support from a number of bilateral\
           donors, the Initiative has spent the last six years working with\
           African countries to identify the causes of poor road maintenance\
           policies and to develop an agency for reforming them. The key\
           concept to emerge from the debate on how to strengthen financing\
           and management of roads is commercialiation: bring roads into the\
           marketplace and put them on a fee for service basis. However,\
           since roads are and will largely remain a public monopoly,\
           commercialization requires complementary reforms."
    cosSim = CosineSimilarity(dictionary=dictionary,
                              corpus=corpus,
                              model=lda)
    cosSim.save_index('data/sdsn2.index')
    sim = cosSim.doc2sim(doc)
    print sim
