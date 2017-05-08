PYTHON=python

ALEXA_SCRIPT=get_alexa_1m.py
CISCO_SCRIPT=get_cisco_1m.py
MAJESTIC_SCRIPT=get_majestic_1m.py

INTERSECT=./lines_in_common.sh

OUTDIR=tmp_results
LOG="$(OUTDIR)/log.txt"

ALEXA_LIST=alexa.txt
CISCO_LIST=cisco.txt
MAJESTIC_LIST=majestic.txt

ALEXA_CISCO_LIST=intersect_alexa_cisco.txt
ALEXA_MAJESTIC_LIST=intersect_alexa_majestic.txt
CISCO_MAJESTIC_LIST=intersect_cisco_majestic.txt
ALEXA_CISCO_MAJESTIC_LIST=intersect_all.txt

.PHONY: all force clean intersections int_full int_alexa_majestic int_cisco_majestic alexa cisco majestic

intersections: int_alexa_cisco int_alexa_majestic int_cisco_majestic int_full
	@echo "Intersection between Alexa and Cisco:     $(shell wc -l $(OUTDIR)/$(ALEXA_CISCO_LIST)) lines"
	@echo "Intersection between Alexa and Majestic:  $(shell wc -l $(OUTDIR)/$(ALEXA_MAJESTIC_LIST)) lines"
	@echo "Intersection between Cisco and Majestic:  $(shell wc -l $(OUTDIR)/$(CISCO_MAJESTIC_LIST)) lines"
	@echo "Intersection between all three:           $(shell wc -l $(OUTDIR)/$(ALEXA_CISCO_MAJESTIC_LIST))"

all: alexa cisco majestic

force:
	make -B

int_full: $(OUTDIR)/$(ALEXA_CISCO_MAJESTIC_LIST)

$(OUTDIR)/$(ALEXA_CISCO_MAJESTIC_LIST): $(OUTDIR)/$(ALEXA_CISCO_LIST) $(OUTDIR)/$(MAJESTIC_LIST)
	$(INTERSECT) -p "$(OUTDIR)/$(ALEXA_CISCO_LIST)" "$(OUTDIR)/$(MAJESTIC_LIST)" \
		>"$(OUTDIR)/$(ALEXA_CISCO_MAJESTIC_LIST)"

int_alexa_cisco: $(OUTDIR)/$(ALEXA_CISCO_LIST)
int_alexa_majestic: $(OUTDIR)/$(ALEXA_MAJESTIC_LIST)
int_cisco_majestic: $(OUTDIR)/$(CISCO_MAJESTIC_LIST)

$(OUTDIR)/$(ALEXA_CISCO_LIST): $(OUTDIR)/$(ALEXA_LIST) $(OUTDIR)/$(CISCO_LIST)
	$(INTERSECT) -p "$(OUTDIR)/$(ALEXA_LIST)" "$(OUTDIR)/$(CISCO_LIST)" \
		>"$(OUTDIR)/$(ALEXA_CISCO_LIST)"

$(OUTDIR)/$(ALEXA_MAJESTIC_LIST): $(OUTDIR)/$(ALEXA_LIST) $(OUTDIR)/$(MAJESTIC_LIST)
	$(INTERSECT) -p "$(OUTDIR)/$(ALEXA_LIST)" "$(OUTDIR)/$(MAJESTIC_LIST)" \
		>"$(OUTDIR)/$(ALEXA_MAJESTIC_LIST)"

$(OUTDIR)/$(CISCO_MAJESTIC_LIST): $(OUTDIR)/$(CISCO_LIST) $(OUTDIR)/$(MAJESTIC_LIST)
	$(INTERSECT) -p "$(OUTDIR)/$(CISCO_LIST)" "$(OUTDIR)/$(MAJESTIC_LIST)" \
		>"$(OUTDIR)/$(CISCO_MAJESTIC_LIST)"

alexa: $(OUTDIR)/$(ALEXA_LIST)
cisco: $(OUTDIR)/$(CISCO_LIST)
majestic: $(OUTDIR)/$(MAJESTIC_LIST)

$(OUTDIR)/$(ALEXA_LIST):
	@mkdir -p "$(OUTDIR)"
	$(PYTHON) $(ALEXA_SCRIPT) >"$(OUTDIR)/$(ALEXA_LIST)"
	@echo "Downloaded Alexa 1m:    " $(shell date "+%Y-%m-%d %H:%M:%S") >>$(LOG)

$(OUTDIR)/$(CISCO_LIST):
	@mkdir -p "$(OUTDIR)"
	$(PYTHON) $(CISCO_SCRIPT) >"$(OUTDIR)/$(CISCO_LIST)"
	@echo "Downloaded Cisco 1m:    " $(shell date "+%Y-%m-%d %H:%M:%S") >>$(LOG)

$(OUTDIR)/$(MAJESTIC_LIST):
	@mkdir -p "$(OUTDIR)"
	$(PYTHON) $(MAJESTIC_SCRIPT) >"$(OUTDIR)/$(MAJESTIC_LIST)"
	@echo "Downloaded Majestic 1m: " $(shell date "+%Y-%m-%d %H:%M:%S") >>$(LOG)

clean:
	rm -rf $(OUTDIR)
