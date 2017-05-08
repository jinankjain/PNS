The main python script is retrieve_ttls.py, which queries for NS records and
outputs the TTLs for each name. The script outputs these results to different
files according to the RR type, keeping track, besides the NS type, also of DS,
RRSIG, and A records (found in the additional section).

Use the makefile to run the script.

The results for the TTLs of TLDs are as follows:
The average TTL for NS records and for A records (glue records in the additional
section) is 172800 s (48 hours), while the average TTL for DS and RRSIG records
is 86400 s (24 hours).

