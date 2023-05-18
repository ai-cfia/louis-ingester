# louis-ingester: intaking data for the louis virtual assistant 

## introduction

As part of the work on our CFIA virtual assistant Louis, we're testing adding a conversational interface (using ChatGPT) and a semantic search to the Consolidated federal Acts and regulations in XML - Open Government Portal (canada.ca). 

Being part of a regulatory agency,we need to interpret laws and regulations. Having a conversational agent able to search, understand and explain legalese would be helpful. 

The dataset is challenging as most models are not trained on corpus of laws.

Eventually, we hope to add case precedents to add more "meat" into the interpretation of Canadian laws. 

## overview

the pipeline is divided as follow:

* fetcher.py: download XML law
* chunker.py: split on sections, cleaning some of the nodes we don't use
* indexer.py: create embedding from text and upsert them into a vector store

Also:

* query.py: example queries
* summarizer.py: summarization feature

## development

a devcontainer is defined for a Jupyter environment to prototype further. 