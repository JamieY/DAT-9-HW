# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 20:07:11 2015

@author: jamieyachera
"""

# Part 1 - Reading in tsv file
import csv
with open("chipotle.tsv") as tsvfile:
    data = []
    for line in csv.reader(tsvfile, delimiter = "\t"):
        data.append(line)
        print(line)
        
# Part 2 - Separate header and data into two different lists
headerlist = data[0]
print headerlist
datalist = data[1:]
print datalist

# Part 3 - Calculate the average price of an order
total = 0
num_order=[]
for row in data[1:]:
    rowprice = float(row[4][1:])
    total += rowprice
    num_order.append(row[0]) 
max_num_order = len(set(num_order))
avgprice = round(total/max_num_order,2)
print avgprice

# Part 4 - Create a list (or set) of all unique sodas and soft drinks that they sell.
# Note: Just look for 'Canned Soda' and 'Canned Soft Drink', and ignore other drinks like 'Izze'.

soda = set([row[3] for row in data[1:] if 'Canned' in row[2]])
print soda

# Part 5 - Calculate the average number of toppings per burrito.
toppings=[row[3] for row in data[1:] if 'Burrito' in row[2]]
num_burritos = len(toppings)

total_toppings = 0
for row in toppings:
    total_toppings += (row.count(',')+1)

avgtoppings = round(total_toppings/float(num_burritos),2)
print avgtoppings

# Part 6 - Create a dictionary in which the keys represent chip orders and the values 
# represent the total number of orders. Expected output: {'Chips and Roasted Chili-Corn Salsa': 18, ... }
# Note: Please take the 'quantity' column into account

chip_dict = {}
chip_orders = [row[1:3] for row in data[1:] if 'Chips' in row[2]]
print chip_orders[:5]
for row in chip_orders:
    if row[1] in chip_dict:
        chip_dict[row[1]]+=int(row[0])
    else:
        chip_dict[row[1]]=int(row[0])
print chip_dict