# BibTeX PubMed Links Enricher

This script enriches a BibTeX file with PubMed, PubMed Central, and DOI links. Such links are required, for example, for submissions to the [NAR Web Server Issue](https://academic.oup.com/nar/pages/submission_webserver). 

NAR provides a Perl script by Gary Benson, but it stopped working for me in 2025. That’s why I created this small Python script as an alternative

The output should look similar to [this](data/NAR_urls_in_reference_list_for_LaTeX.pdf).

Usage:

```
python extend.py data/main.bib output.bib
```

## Possible issues

- If the document contains any non-standard BibTeX  entry types (such as `electronic` or `online`), they will not be recognized by [bibtexparser](https://pypi.org/project/bibtexparser/) and, consequently, will not appear in the output file. These record will need to be added into the resulting bib file manually.

- A PubMed query could theoretically return multiple results. In such cases, only the first result is used, which may not be the one you are interested in. If this occurs, the command-line output will display information about those queries.