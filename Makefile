#
# Ph20: Makefile for Lab 3.
#

PC     = chmod
PFLAGS = +x
PY     = python

default:
	$(PC) $(PFLAGS) Lab3.py
	$(PY) Lab3.py
