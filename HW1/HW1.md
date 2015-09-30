# HW1

### Problem 1. 
Using chipotle.tsv in the data subdirectory:  Look at the head and the tail, and think for a minute about how the data is structured. What do you think each column means? What do you think each row means? Tell me! (If you're unsure, look at more of the file contents.)

a. The data is structured as a list of lists.  In reviewing the data returned through the 'head chipotle.tsv' code, the "ID" field is not unique.  A dictionary will require unique values for each of the primary keys.  Each row represents an item purchased and its corresponding price.  The columns show the values of the transaction including the order number, the quantity of item 'x' purchased, the item 'x' that was purchased, a string listing the description of the item purchased (where applicable), and the corresponding price.

	$ head chipotle.tsv


b. How many orders do there appear to be?
Using the 'tail chipotle.tsv' command, we see that the bottom row shows 1834 orders.  

	$ tail chipotle.tsv

c. How many lines are in the file?
There are 4623 lines in the file

	$ wc - l chipotle.tsv

d. Which burrito is more popular, steak or chicken?
Chicken burrito is more popular as more orders contained at least one chicken burrito (553) vs. steak burrito (368)

	$ grep -c 'Steak Burrito' chipotle.tsv --> returned 368
	$ grep -c 'Chicken Burrito' chipotle.tsv --> returned 553

e. Do chicken burritos more often have black beans or pinto beans?
Chicken burritos more often have black beans than pinto beans.  In the instances of chicken burritos ordered, 282 had black beans and 105 had pinto beans.  

	$ grep -w 'Chicken Burrito' chipotle.tsv | grep -c 'Pinto Beans'
	$ grep -w 'Chicken Burrito' chipotle.tsv | grep -c 'Black Beans'

### Problem 2. 
Count the number of occurrences of the word 'dictionary' (regardless of case) across all files in the DAT9 repo.
There were 39 ocurrences

	$ grep -ir 'dictionary' DAT9/DAT-DC-9/ | wc -l

### Problem 3 (OPTIONAL) 
Use the command line to find out something interesting about the chipotle data.
Out of 4623 lines, there are 4579 unique orders not including the order id/quantity

	$ cut -f3,4,5,6 chipotle.tsv > hw1partc.txt
	$ uniq hw1partc.txt | wc -l
