#!/usr/bin/env python3

import sys


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
	for header, seq in D.items():
		if len(header) < 3:
			continue
		name = header.split('_')[0]
		sys.stdout.write('{},{}\n'.format(header, name))
		sys.stderr.write('>{}\n{}\n'.format(header, seq.upper()))

