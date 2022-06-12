#!/bin/bash

$1 -vf -s $2 -T s
$1 -vf -s $2 -T S 
$1 -vf -s $2 -T r 
$1 -vf -s $2 -T P 
$1 -vf -s $2 -T p 
$1 -vf -s $2 -T O 
$1 -vf -s $2 -T o 
$1 -vf -s $2 -T n 
$1 -vf -s $2 -T L 
$1 -vf -s $2 -T l 
$1 -vf -s $2 -T c

mkdir ./db_data

cp *.tbl ./db_data

python clean_data.py ./db_data/customer.tbl
python clean_data.py ./db_data/lineitem.tbl
python clean_data.py ./db_data/nation.tbl
python clean_data.py ./db_data/orders.tbl
python clean_data.py ./db_data/part.tbl
python clean_data.py ./db_data/partsupp.tbl
python clean_data.py ./db_data/region.tbl
python clean_data.py ./db_data/supplier.tbl