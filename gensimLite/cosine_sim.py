# -*- coding: utf-8 -*-
"""
API for computing cosine similarities
"""

from gensim import similarities
import numpy as np


class CosineSimilarity(object):

    def __init__(self, dictionary, corpus, model):

        # the dictionary of tokens to model
        self.dictionary = dictionary

        # the corpus of sdsn documents to query against
        self.corpus = corpus

        # the lda model space for the corpus
        self.model = model

        # similarity matrix of the corpus
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

        # convert document to bag of words vector
        vec_bow = self.dictionary.doc2bow(doc.lower().split())
        # convert bow vector to model vector
        vec_model = self.model[vec_bow]
        return self.index[vec_model]

    def bow2model_vec(self, vec):
        '''converts bow vector to model vector space'''
        return self.model[vec]

    def model_vec2sim(self, model_vec):
        '''converts a dictionary-converted vector to similarity'''
        return self.index[model_vec]

    def calculate_sim(self, doc, n=10):
        '''Takes an average of n doc2sim calls'''
        total = 0
        for i in range(n):
            total += np.array(self.doc2sim(doc))
        return total/n

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

    doc2 = "A prerequisite for advancing equity in society is to improve\
            human well-being and the overall quality of life. While Nepal\
            continues to make progress on most of the MDGs, with particularly\
            notable achievements in the areas of education and health,\
            critical outcome inequities persist. There remains a need to\
            support the GoN in its efforts to address equity of access to\
            basic essential social services with a focus on disadvantaged\
            groups. Hence, this outcome aims to promote equity in policy\
            frameworks, planning processes,resource allocation, systems\
            delivery, monitoring mechanisms and community utilization\
            for a wide range of basic social services-education, health,\
            HIV/AIDS, nutrition, food security, water, sanitation,\
            shelter and child and family welfare—both in rural and\
            urban areas."

    doc3 = "UN agencies will focus on system strengthening that creates a more\
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

    doc4 = "Nepal experiences disasters each year. The Bureau of Crisis\
            Prevention and Recovery at UNDP ranks Nepal as the eleventh\
            most at-risk country for earthquakes and the thirtieth most\
            at-risk for floods. Of 16 countries listed globally as being\
            at ‘extreme risk from climate change over the next 30 years’,\
            Nepal ranks fourth27. Between 1971 and 2007, more than 50,000\
            people were reported injured, 3,000 people missing and more than\
            five million people affected by natural disasters in Nepal28.\
            Outcome 7 focuses on protecting development gains by strengthening\
            national and local government capacity to reduce risk and adapt\
            to climate change as well as by addressing the needs of people\
            vulnerable to climate change and disasters. This will enable government\
            officials to lead and implement policies and systems to effectively\
            manage risks and adapt to climate change; urban populations to\
            prepare for and manage risk and climate change adaptation;\
            vulnerable populations to have increased knowledge about disaster\
            risk management (DRM) and capacity for climate change adaptation\
            and mitigation of risks; and national preparedness and emergency\
            systems to effectively prepare for and respond to hazard-related\
            disasters."


    cosSim = CosineSimilarity(dictionary=dictionary,
                              corpus=corpus,
                              model=lda)
    cosSim.save_index('data/sdsn2.index')
    simScore = cosSim.calculate_sim(doc4, 10)

    # this is a quick hack. plz add into the CosineSimilarity class
    sdsnThemes = [
        "Global Governance",
        "Corporate Social Responsibility",
        "Decarbonization",
        "Childhood Development",
        "Health for All",
        "Poverty Reduction",
        "Sustainable Ecosystems",
        "Sustainable Cities",
        "Social Inclusion",
        "Planetary Boundaries",
        "Natural Resource Management",
        "Sustainable Food Systems"
        ]

    # print("Document:\n %s \n\n" % doc)
    for i in range(len(sdsnThemes)):
        print('%s --- %f' % (sdsnThemes[i], simScore[i]))
