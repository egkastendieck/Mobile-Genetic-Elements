#!/usr/bin/env python3

import requests
import re
import sys
from bs4 import BeautifulSoup
from contextlib import closing

TR_URL = 'http://transposon.lstmed.ac.uk/tn-registry'
TR_OPT = '?page='
ACC_SPLIT = re.compile(r'[A-Za-z]+[0-9]+\.?[0-9]?')


def check_eq(lst):
    return not lst or [lst[0]]*len(lst) == lst


def get_html(url):
    """
    Attempts to retrieve HTML content from the provided url, otherwise return None.
    :param url: URL at which to retrieve HTML source code
    :return: HTML source code if valid URL else None
    """
    with closing(requests.get(url, stream=True)) as r:
        if r.status_code == 200 and r.headers['Content-Type'].lower() is not None:
            return r.content
        else:
            return None


def parse_html(html_content):
    """
    Given a page of HTML content, find the accession numbers for each entry.
    :param html_content: HTML content as returned by the requests package
    :return: Dictionary of accessions and information for each database entry
    """
    return_dict = {'titles': [],
                   'descriptions': [],
                   'references': [],
                   'accessions': []}

    soup = BeautifulSoup(html_content, 'html.parser')
    return_dict['titles'] = [x.get_text() for x in soup.find_all(class_='tn-title')]
    details = soup.find_all(class_='record-expand')
    for record in details:
        char = record.find(class_='tn-char tn-expand-field')
        ref = record.find(class_='tn-ref tn-expand-field')
        acc = record.find(class_='tn-acc-num tn-expand-field')
        if acc:
            separate_acc = tuple(x for x in ACC_SPLIT.findall(acc.get_text()))
        else:
            separate_acc = None
        if char:
            return_dict['descriptions'].append(char.get_text().strip().replace('\n', ' ').replace('\t', ' ').replace('\r', ' '))
        else:
            return_dict['descriptions'].append('NA')
        if ref:
            return_dict['references'].append(ref.get_text().strip().replace('\n', ' ').replace('\t', ' ').replace('\r', ' '))
        else:
            return_dict['references'].append('NA')
        if separate_acc:
            return_dict['accessions'].append(separate_acc)
        else:
            return_dict['accessions'].append(('NA',))
    return return_dict


if __name__ == '__main__':
    values = parse_html(get_html(TR_URL))
    for i in range(1, 42):
        html = get_html(TR_URL + TR_OPT + str(i))
        if not html:
            break
        for k, v in parse_html(html).items():
            values[k] += v
    out_values = zip(values['titles'],
                     values['accessions'],
                     values['descriptions'],
                     values['references'])
    sys.stdout.write('Name\tAccessions\tDescription\tReferences\n')
    for x in out_values:
        sys.stdout.write('{}\t{}\t{}\t{}\n'.format(
            x[0],
            '|'.join([str(y) for y in x[1]]),
            x[2],
            x[3]
        ))
