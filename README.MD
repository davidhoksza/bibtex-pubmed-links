# BibTeX PubMed Links Enricher

This script enriches a BibTeX file with PubMed, PubMed Central, and DOI links. Such links are required, for example, for submissions to the [NAR Web Server Issue](https://academic.oup.com/nar/pages/submission_webserver). 

NAR provides a Perl script by Gary Benson, but it stopped working for me in 2025. That’s why I created this small Python script as an alternative

The output should look similar to [this](data/NAR_urls_in_reference_list_for_LaTeX.pdf).

Usage:

```
python extend.py data/main.bib output.bib
```