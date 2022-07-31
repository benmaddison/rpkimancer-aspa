#
# $Id: Makefile,v 1.1.1.1 2002-11-11 05:11:48 randy Exp $
#
MOD=RPKI-ASPA-2022

.PHONY: all
all: asn1

.PHONY: asn1
asn1: rpkimancer_aspa/asn1/$(MOD).asn

rpkimancer_aspa/asn1/$(MOD).asn: $(MOD).asn $(MOD).patch
	patch $(MOD).asn $(MOD).patch -o $@

clean:
	rm -f rpkimancer_aspa/asn1/$(MOD).asn
