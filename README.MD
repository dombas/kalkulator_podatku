# Kalkulator podatku - simple 2020 linear tax calculator
A simple tax calculator for polish linear tax as of 2020
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Functions](#functions)
* [Setup](#setup)

## General info
This project will help to calculate estimation tax prepayments, mainly for single person businesses. 
When you are your own boss it's good to know how much tax you will have to pay at the beginning of month/quarter.

You will be able to easily answer questions such as:
* "How much tax will I pay if I earn X more?"
* "If I buy this expensive piece of equipment how much will I save on tax?"

Calculating tax is based on:
* revenue (the sum of all sales values)
* expenses (the costs of running your business)
* tax reduction (mainly national health insurance)
* income reduction (mainly national retirement fund, donations, losses from previous years)
* calculation of tax free amount (which can be annoying to do by hand)
* tax prepayment (paid so far)

### Bibliography?
Websites with info on tax calculation
* https://www.ksiega-podatkowa.pl/kalkulator-podatkowy-2020
* https://kalkulatory.gofin.pl/Kalkulator-zaliczki-PIT-od-dochodow-z-dzialalnosci-gospodarczej-skala-podatkowa-2020,12.html
* https://www.pit.pl/kwota-zmniejszajaca-podatek/

## Functions
### Functions implemented
Calculation of:
* tax basis
* tax free amount
* tax
* tax owed
### Functions planned
* graphical user interface
* ability to calculate how much expenses would be needed to lower the tax owed by a given amount/to 0/below the tax threshold
* remembering the entered data (saving)
* ability to change various constants (mainly tax thresholds)
	
## Technologies
Project is created with:
* Python version: 3.8
	
## Setup
To run this project, run the kalkulator_GUI.py file:

```
$ cd ../kalkulator_podatku
$ python kalkulator_GUI.py
```

To run tests:

```
$ cd ../kalkulator_podatku
$ python skala_podatkowa_tests.py
```