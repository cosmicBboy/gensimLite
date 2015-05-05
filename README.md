GensimLite
===========

A lightweight api that wraps around Gensim for semi-supervised topic modelling.
Specify metatopic documents that will represent a probability distribution of topics.

The supervised training set is used to construct an initial LDA model. This set is
composed of structured text, which may or may not be grounded in a formal domain taxomony.

The unsupervised test set is a corpus of documents that are to be labelled with the metatopics.

This is approximated by creating a cosine similarity matrix between each document in the supervised test set and the unsupervised training set. 

[Project Road Map here](https://trello.com/b/JifUtYzW/gensimlite-roadmap)