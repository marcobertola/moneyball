#!/usr/bin/env python
# coding: utf8
"""Example of a spaCy v2.0 pipeline component that sets entity annotations
based on list of single or multiple-word company names. Companies are
labelled as ORG and their spans are merged into one token. Additionally,
._.has_tech_org and ._.is_tech_org is set on the Doc/Span and Token
respectively.

* Custom pipeline components: https://spacy.io//usage/processing-pipelines#custom-components

Compatible with: spaCy v2.0.0+
Last tested with: v2.1.0
"""
from __future__ import unicode_literals, print_function

import plac
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span, Token
from nlp_matcher import * 


def main():
    # For simplicity, we start off with only the blank English Language class
    # and no model or pre-defined pipeline loaded.
    nlp = English()
    text = str(input("Write something (min 2 words):\n"))

    players = ["Lukaku", "Modric", "Messi", "Ronaldo"]  # etc.
    players = FootballPlayerRecognizer(nlp, players)  # initialise component
    nlp.add_pipe(players, last=True)  # add last to the pipeline


    buy_verbs = ["buy", "get", "purchase"]  # etc.
    component = VerbBuyRecognizer(nlp, buy_verbs)  # initialise component
    nlp.add_pipe(component, last=True)  # add last to the pipeline


    seach_verbs = ["search", "find", "look for"]  # etc.
    component = VerbSearchRecognizer(nlp, seach_verbs)  # initialise component
    nlp.add_pipe(component, last=True)  # add last to the pipeline


    doc = nlp(text)
    print("Pipeline", nlp.pipe_names)  # pipeline contains component name
    print("Tokens", [t.text for t in doc])  # company names from the list are merged
    print("Doc has_player", doc._.has_player)  # Doc contains tech orgs
    print("Doc buy_player", doc._.buy_player)  # Doc contains tech orgs
    for token in doc :
        print("Token has_player", token._.has_player)  

    for token in doc :
        print(token.lemma_)  

    
    print("Token 1 has_player", doc[1]._.has_player)  
    print("Entities", [(e.text, e.label_) for e in doc.ents])  # all orgs are entities



if __name__ == "__main__":
    main()

    