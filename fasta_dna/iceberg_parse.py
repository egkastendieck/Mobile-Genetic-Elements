#!/usr/bin/env python3

import sys
import re

LOCATION_REGEX = re.compile(r'([0-9]+\.\.[0-9]+\s)')


def fastaParse(infile):
    with open(infile, 'r') as fastaFile:
        # Skip whitespace
        while True:
            line = fastaFile.readline()
            if line is "":
                return  # Empty file or premature end of file?
            if line[0] is ">":
                break
        while True:
            if line[0] is not ">":
                raise ValueError("Records in FASTA should begin with '>'")
            header = line[1:].rstrip()
            allLines = []
            line = fastaFile.readline()
            while True:
                if not line:
                    break
                if line[0] is ">":
                    break
                allLines.append(line.rstrip())
                line = fastaFile.readline()
            yield header, "".join(allLines).replace(" ", "").replace("\r", "")
            if not line:
                return  # Stop Iteration
        assert False, "Should not reach this line"


if __name__ == '__main__':
	D = {k: v for k, v in fastaParse(sys.argv[1])}
	with open(r'/Users/egkastendieck/Desktop/MGE/fasta_dna/iceberg_detailed_annotations.tsv', 'w') as out:
		out.write('Header\tAccession\tName\tStart\tStop\n')
		for header, seq in D.items():
			new_header = header.replace(' ', '_').replace('..', '|').replace('.', '_').replace(',', '_').replace('__', '_')
			info = header.split('|')
			name = info[2]
			acc = info[4]
			description = info[5]
			location = [x for x in LOCATION_REGEX.findall(description)][0]
			start, stop = location.split('..')
			out.write('\t'.join([header, acc, name, start, stop]) + '\n')
			sys.stdout.write('{},{}\n'.format(new_header, name))
			sys.stderr.write('>{}\n{}\n'.format(new_header, seq.upper()))

