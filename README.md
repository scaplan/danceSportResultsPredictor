# danceSportResultsPredictor

This simple script takes as input a ranking (I pulled from dancesportinfo.net) as well as a heatlist and prints the 'predicted result' to stdout.

Any entry without a ranking is by default listed at 999 (and thus held at the end of the 'predicted results')

Example Usage:

python ballroom-results-predictor.py rawDanceSportInfo-scrape-mar25-2017.txt nationalsPrechamp2017List.txt
