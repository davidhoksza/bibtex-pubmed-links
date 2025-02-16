import requests
import xml.etree.ElementTree as ET
import bibtexparser
import sys
from colorama import init, Fore, Style
import re

init(autoreset=True)

def search_article(title):
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    title_cleaned = re.sub("[{}*]", "", title)
    print(title_cleaned)
    params = {
        'db': 'pubmed',
        'term': f'"{title_cleaned}"',
        'retmode': 'json'
    }
    response = requests.get(search_url, params=params)
    search_results = response.json()
    return search_results['esearchresult']['idlist']

#def fetch_article_details(pmids):
def fetch_article_details(pmid):
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        #'id': ','.join(pmids),
        'id': pmid,
        'retmode': 'xml'
    }
    response = requests.get(fetch_url, params=params)
    return response.text

def extract_ids(xml_data):
    root = ET.fromstring(xml_data)
    doi = None
    pmc = None
    for article_id in root.findall(".//ArticleId"):
        t = article_id.get('IdType')
        if article_id.get('IdType') == 'doi':
            doi = article_id.text
        elif article_id.get('IdType') == 'pmc':
            pmc = article_id.text
    return doi, pmc

def enrich_bibtex_with_ids(bibtex_file, output_file):
    with open(bibtex_file) as bib_file:
        bib_database = bibtexparser.load(bib_file)

    for entry in bib_database.entries:
        title = entry.get('title')
        print(Fore.GREEN + Style.BRIGHT + f"Processing {title}")
        if title:
            pmids = search_article(title)
            pmid = pmids[0] if len(pmids) > 0 else None
            if pmids:
                print(Fore.GREEN + Style.BRIGHT + f"\t PubMed record found")
                article_xml = fetch_article_details(pmid)
                doi, pmcid = extract_ids(article_xml)
                # entry['note'] = f"DOI: {doi}, PMID: {', '.join(pmids)}"
                template_pubmed = "[PubMed:\href{http://www.ncbi.nlm.nih.gov/pubmed/_ID_}{_ID_}]"
                template_pubmed_central = "[PubMed Central:\href{http://www.ncbi.nlm.nih.gov/pmc/articles/_ID_}{_ID_}]"
                template_doi = "[doi:\href{http://dx.doi.org/_ID_}{_ID_}]"

                note = ""
                if pmid:
                    note += template_pubmed.replace('_ID_', pmid)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\t\t No PMID found")
                if pmcid:
                    note += template_pubmed_central.replace('_ID_', pmcid)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\t\t No PMCID found")
                if doi:
                    note += template_doi.replace('_ID_', doi)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\t\t No DOI found")

                if note:                
                    entry['note'] = note
            else:
                print(Fore.RED + Style.BRIGHT + f"\t No PubMed record found")
            

    with open(output_file, 'w') as output:
        bibtexparser.dump(bib_database, output)
    print(Fore.GREEN + Style.BRIGHT + f"Enriched BibTeX saved to {output_file}")

# enrich_bibtex_with_ids('main.bib', 'main1.bib')

def main():
    
    if len(sys.argv) < 2:
        print(Fore.YELLOW + "Usage: python enrich.py <input bib file> <output bib file>")        
        sys.exit(1)

    f_input = sys.argv[1]
    f_output = sys.argv[2]

    enrich_bibtex_with_ids(f_input, f_output)
    

if __name__ == "__main__":
    main()

# Example usage:
# enrich_bibtex_with_ids('input.bib', 'output.bib')