# FIXED VERSION

As I was reviewing my alternate version (rolling window), I've noticed an error on my part because of partial misinterpretation from the instructions. I've decided to correct this as to how it should've been correctly implemented and written to the final output file (repeat_donors.txt). The fix was simple ( for-loop ) in the `__init__.py` and importing `collections` library.

The original output from the original `itcont.txt` remains the same:

```
C00384516|02895|2018|333|333|1
C00384516|02895|2018|333|717|2
```

However, as new data comes in for instance, `DEEHAN, WILLIAM N`, decides to donate to `C00177436` in `2018`, (this new entry line will be placed at the end of `itcont.txt`) - `01312018` at `384` @ `trans_amt`

```
C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|384||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337
```

The new output file should now read the following as the third entry line will display `DEEHAN, WILLIAM N` contribution to `C00177436` with a new running `percentile` and running count of the total amount of contributions.

```
C00384516|02895|2018|333|333|1
C00384516|02895|2018|333|717|2
C00177436|30004|2018|333|1101|3
```




#


#  Practice Challenge
 
Author: Hoa Quach

Table of Contents
===================

* [Challenge Summary](README.md#challenge-summary)
* [Dependencies](README.md#dependencies)
* [Execution](README.md#execution)
* [Source Files](README.md#source-files)
* [Input File Considerations](README.md#input-files-considerations)
* [Required Input Files](README.md#required-input-files)
	* [Percentile Value Constraints](README.md#percentile-value-constraints)
* [Output File](README.md#output-file)
* [Algorithm](README.md#algorithm)
* [Tests](README.md#tests)
* [Performance](README.md#performance)
* [Questions?](README.md#questions)

# Challenge Summary
For this challenge, we were asked to take a file listing of individual campaign contributions for multiple years, determine which ones came from repeat donors, calculate a few values and distill the results into a single output file, ```repeat_donors.txt```

For each recipient, zip code and calendar year, calculate these three values for contributions coming from repeat donors:

- total dollars received
- total number of contributions received
- donation amount in a given percentile

The political consultants, who are primarily interested in donors who have contributed in multiple years, are concerned about possible outliers in the data. So they have asked us that our program allows for a variable percentile. That way the program could calculate the
nearest-rank.


# Dependencies

- Python 2.7.6

- ```import sys```

- ```import os```

- ```from decimal import getcontext, Decimal```

- ```from collections import OrderedDict```


# Execution

To execute the code use the `run.sh` bash script from the root directory.

```
./run.sh
```


# Source Files

This challenge contains the following source files located in the `\src` directory:

- `__init__.py` - main file
- `file_parser.py` - functions to parse `itcont.file` and `percentile.txt file`
- `process_log.py`


# Input Files Considerations

Directory: `/input`



#### Required Input Files

- `itcont.txt`
- `percentile.txt` 

# 

`itcont.txt` - Below are the fields that we will need to complete this challenge:

- `CMTE`: identifies the flier, which for our purposes is the recipient of this contribution
- `NAME`: name of the donor
- `ZIP_CODE`: zip code of the contributor (we only want the first five digits/characters)
- `TRANS_DT`: date of the transaction [`YEAR`]
- `TRANS_AMT`: amount of the transaction
- `OTHER_ID`: a field that denotes whether contribution came from a person or an entity

**For the purposes of this challenge, we can **assume** the input file follows the data dictionary noted by the FEC for the 2015-current election years.

#

`percentile.txt` - The first line of `percentile.txt` contains the percentile we should compute for these given input pair. For the percentile computation use the nearest-rank method as described by [Wikipedia](https://en.wikipedia.org/wiki/Percentile).


### Percentile Value Constraints

**IMPORTANT NOTES:** 

The program will exit due to the following input values from `percentile.txt`:

  - contains either a `blank file` or `0`
  - contains a value of **more than** `100.00`
  - contains a **negative integer**
  - contains an invalid **character**
  
**These warning messages have been enabled.**

Additionally, if `percentile.txt` contains **blank line(s)** beginning of the file, but contains an integer on the second line, this program will accept the first integer from the next non-empty line.


# Output File

Directory: `/output`

For the output file, `repeat_donors.txt`, the fields on each line should be separated by a `|`

The output should contain the same number of lines or records as the input data file, `itcont.txt`, minus any records that were ignored as a result of the 'Input file considerations' and any records you determine did not originate from a repeat donor.

Each line of this file should contain these fields:

- recipient of the contribution (or `CMTE` from the input file)
- 5-digit zip code of the contributor (or the first five characters of the `ZIP_CODE` field from the input file)
- 4-digit year of the contribution
- running percentile of contributions received from repeat donors to a recipient streamed in so far for this zip code and calendar year. Percentile calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar)
- total amount of contributions received by recipient from the contributor's zip code streamed in so far in this calendar year from repeat donors
- total number of transactions received by recipient from the contributor's zip code streamed in so far this calendar year from repeat donors
 

According to the instructions, I have skipped an entire record due to the following situation:

- `trans_dt` (aka `YEAR`) must either 2017 or 2018
- if `other_id` is non-empty
- if `cmte` is empty
- if `zip_code` is empty
- if `name` is empty
- `trans_amt` is empty
- `zip_code` is fewer 5 characters
- `zip_code` must start with a numeric

Processing all of the input lines in `itcont.txt`, the entire contents of `repeat_donors.txt` would be:


```
C00384516|02895|2018|333|333|1
C00384516|02895|2018|333|717|2
```


# Algorithm

### Hash table (dictionary) approach

Searching is the most common operation applied to collections of data. It's not only used to determine if an item is in the collection, but can also be used in adding new items to the collection and removing existing items. Given the importance of searching, we need to be able to accomplish this operation fast and efficiently.

Hash table is a technique other than comparing the target key against other keys in the collection. Hashing is the process of mapping a search key to a limited range of array indices with the goal of providing direct access to the keys. The keys are stored in an array called a hash table and a hash function is associated with the table. The function converts or maps the search keys to specific entries in the table.

Python's hash dictionary implementation reduces the average complexity of dictionary lookups to O(1) by requiring that key objects provide a "hash" function. The idea is to create a hash table in which all items of the `l1` list is a key with a value. The important point is that each item existing in the `l1` list is also a key of the hash table. Once the hash table has been initialized, you simply iterate over the items of the `l2` list and check if it exists as a key in the hash table.

# Tests

```
test1 - Insight default
test2 - removed `cmte` from 6th entry
test3 - percentile = 90
test4 - percentile = 0
test5 - removed `SABOURIN, JAMES` name 7th record name
test6 - added float `transact_amt` for 6th and 7th records
test7 - added a letter in front of `zip_code` in the 7th record
```


# Performance

### (1st pass) - non-dictionary key/value pairs; traditional lists

```
7 records @ Elapsed Time:  0.0846440792084 seconds
14 records @ Elapsed Time:  0.162224054337 seconds
21 records @ Elapsed Time:  0.159292936325 seconds
119 records @ Elapsed Time:  0.492459058762 seconds
504 records @ Elapsed Time:  3.92950201035 seconds
6652 records @ Elapsed Time:  440.244781017 seconds (7.37 mins)
```

### (2nd pass) - with hash table dictionary key/value pairs

```
7 records @ Elapsed Time:  0.0693910121918
14 records @ Elapsed Time:  0.0351810455322
21 records @ Elapsed Time:  0.0459311008453
119 records @ Elapsed Time:  0.131927967072
504 records @ Elapsed Time:  0.43389582634
6652 records @ Elapsed Time:  4.91110396385
13304 records @ Elapsed Time:  10.1381549835
26608 records @ Elapsed Time:  20.7352311611
53216 records @ Elapsed Time:  41.668836832
106432 records @ Elapsed Time:  96.2671291828 (1.60 mins)

```

# Questions? 