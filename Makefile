#
# Ph20: Makefile for Lab 3.
#

PC     = chmod
PFLAGS = +x
PY     = python
PLX    = pdflatex

default:
	$(PC) $(PFLAGS) Lab3.py
	$(PY) Lab3.py
	$(PLX) Lab3.tex
