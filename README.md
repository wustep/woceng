# woceng
Various scripts for The Ohio State University College of Engineering Research Group

**Why We Persist: An Intersectional Study to Characterize and Examine the Experiences of Women Tenure-Track Faculty in Engineering** (NSF Grant #1535456)
PI: Dr. Monica Cox

The goal of these scripts was to supplement this study, by **identifying viable survey candidates**: women of color in tenure-track faculty positions. Pictures and titles of faculty from across the nation were scraped separately, and these tools were used to help identify the proper contacts from those.

(These scripts all use Python 3.6!)

## links-test
`link-test-v1.py` and `v2` batch process links in a text file and reports their http status (Y if fine or HTTPError/URLError/InvalidURL/etc.). 

`link-analyzer.py` does that, and runs the links through the [Face++ API](https://www.faceplusplus.com/), which returns gender and ethnicity analysis.

## faculty-classifier

`faculty-classifier.py` classifies faculty as (1) tenure-track faculty, (2) non-tenure-track faculty, (3) support staff, (4) none (blanks) using Naive Bayes. 

## TemplateScripts

These scripts, written by @jalacardio helped clean up the original Excel files, using IPEDs files 
