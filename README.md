# Footprint.ai

### Project Presentation: https://youtu.be/TZeC62czbkk

## Introduction

A service for a wide range of newsrooms that leverages **natural language processing (NLP)** to provide insight on how an article’s language impacts public perception & discourse. Newsrooms can monitor public discourse and key words in their content impacting public perception, increasing their awareness on internal biases. 

## Technologies

**Word2Vec**

A  process of creating numeric vectors to represent words, such that a word vector is a mathematical representation of how a word is used in a corpus.
Words with similar usage patterns have similar vectors, so they will have smaller angular or distance metrics between them than dissimilar words will have. 
This is also a simpler version of an LLM that is more targeted for our specific use case.

**Co-Occurrences**

The process involves checking the co-occurrences of two keywords in a single corpus, indicating whether the two words are present in a single context window.

## The Case Study

We grounded the testing of our two quantitative methods in a Northwestern sports publication, **Inside NU**, and its coverage of three sports scandals that happened at Northwestern within the same time period. Our goal was to test if computational methods and the resulting data could prove our hypothesis – in this case, our hypothesis was that the football scandal, which received outsized coverage by InsideNU, would have also had disproportionate impact on public discourse and opinion around Northwestern and Northwestern football. 
