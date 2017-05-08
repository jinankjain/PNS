MAIN_SCRIPT=retrieve_ttls.py

TLD_LIST_SCRIPT=get_tld_list.py
TLD_FILE=tlds-alpha-by-domain.txt
TLD_OUTDIR=results_tld
TLD_RESULT_FILES=\
	$(TLD_OUTDIR)/a_output.txt \
	$(TLD_OUTDIR)/ns_output.txt \
	$(TLD_OUTDIR)/ds_output.txt \
	$(TLD_OUTDIR)/rrsig_output.txt \
	$(TLD_OUTDIR)/dnskey_output.txt

ALEXA_1M_LIST_SCRIPT=get_alexa_1m.py
ALEXA_1M_FILE=alexa-top-1m.txt
ALEXA_OUTDIR=results_alexa
ALEXA_RESULT_FILES=\
	$(ALEXA_OUTDIR)/a_output.txt \
	$(ALEXA_OUTDIR)/ns_output.txt \
	$(ALEXA_OUTDIR)/ds_output.txt \
	$(ALEXA_OUTDIR)/rrsig_output.txt \
	$(ALEXA_OUTDIR)/dnskey_output.txt
ALEXA_LIMIT=1000000

.PHONY: all clean tld alexa tld_res alexa_res

tld_res: $(TLD_RESULT_FILES)
alexa_res: $(ALEXA_RESULT_FILES)
tld: $(TLD_FILE)
alexa: $(ALEXA_1M_FILE)

all: tld_res alexa_res

$(TLD_RESULT_FILES): $(TLD_FILE)
	mkdir -p "$(TLD_OUTDIR)"
	cd "$(TLD_OUTDIR)" && python ../"$(MAIN_SCRIPT)" ../"$(TLD_FILE)"

$(TLD_FILE):
	python "$(TLD_LIST_SCRIPT)" > $(TLD_FILE)

$(ALEXA_RESULT_FILES): $(ALEXA_1M_FILE)
	mkdir -p "$(ALEXA_OUTDIR)"
	cd "$(ALEXA_OUTDIR)" && head -$(ALEXA_LIMIT) ../$(ALEXA_1M_FILE) | python ../"$(MAIN_SCRIPT)"

$(ALEXA_1M_FILE):
	python "$(ALEXA_1M_LIST_SCRIPT)" > $(ALEXA_1M_FILE)

clean:
	rm -rf $(TLD_OUTDIR) $(ALEXA_OUTDIR)
	rm -f $(TLD_FILE) $(ALEXA_1M_FILE)

