SHELL:=/bin/bash
UNAME:=$(shell uname)

# ~~~~~ Setup Conda ~~~~~ #
PATH:=$(CURDIR)/conda/bin:$(PATH)
unexport PYTHONPATH
unexport PYTHONHOME

# install versions of conda for Mac or Linux
ifeq ($(UNAME), Darwin)
CONDASH:=Miniconda3-4.5.4-MacOSX-x86_64.sh
endif

ifeq ($(UNAME), Linux)
CONDASH:=Miniconda3-4.5.4-Linux-x86_64.sh
endif

CONDAURL:=https://repo.continuum.io/miniconda/$(CONDASH)
conda:
	@echo ">>> Setting up conda..."
	@wget "$(CONDAURL)" && \
	bash "$(CONDASH)" -b -p conda && \
	rm -f "$(CONDASH)"

conda-install: conda
	conda install -y django=2.1.2 pandas=0.23.4 'xlrd>=0.9.0'

# ~~~~~ SETUP DJANGO APP ~~~~~ #
# create the app for development
# start:
# 	django-admin startproject webapp .
# 	python manage.py startapp interpreter

init:
	python manage.py makemigrations
	python manage.py migrate
	# python manage.py migrate lims --database=lims_db # need to do this for each database
	python manage.py createsuperuser

# # re-initialize just the databases
reinit:
	python manage.py makemigrations
	python manage.py migrate
# 	python manage.py migrate lims --database=lims_db

# # destroy app database
nuke:
	rm -rf interpreter/migrations/__pycache__
	rm -f interpreter/migrations/0*.py
	# rm -f lims.sqlite3
	rm -f db.sqlite3

# import data from PMKB .xlsx into database
import:
	python import-pmkb.py

# ~~~~~ RUN ~~~~~ #
# runs the web server
runserver:
	python manage.py runserver
