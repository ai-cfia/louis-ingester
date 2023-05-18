# louis-ingester: opendata for the louis virtual assistant 

## introduction

As part of the work on our CFIA virtual assistant Louis, we're testing adding a conversational interface (using ChatGPT) and a semantic search to the [Consolidated federal Acts and regulations in XML - Open Government Portal (canada.ca)](https://open.canada.ca/data/en/dataset/eb0dee21-9123-4d0d-b11d-0763fa1fb403). 

A copy of the 947 laws XML file [has been archived](https://drive.google.com/file/d/11u5tfCzbr6vfWpF5OCh8hZbLOph-lAd8/view?usp=share_link) and should be placed inside data/acts/

Being part of a regulatory agency,we need to interpret laws and regulations. Having a conversational agent able to search, understand and explain legalese would be helpful. 

The dataset is challenging as most models are not trained on corpus of laws.

Eventually, we hope to add case precedents to add more "meat" into the interpretation of Canadian laws. 

## overview

the pipeline is divided as follow:

* fetcher.py: download XML law (use the [archive instead](https://drive.google.com/file/d/11u5tfCzbr6vfWpF5OCh8hZbLOph-lAd8/view?usp=share_link))
* chunker.py: split on sections, cleaning some of the nodes we don't use
* indexer.py: create embedding from text and upsert them into a vector store

Also:

* query.py: example queries
* summarizer.py: summarization feature

## development

a devcontainer is defined for a Jupyter environment to prototype further. 