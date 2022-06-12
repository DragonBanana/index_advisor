#!/bin/bash

export PGPASSWORD='adv'

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
docker cp ./db_data postgres_index_advisor:/    

python clean_data.py ./db_data/customer.tbl
python clean_data.py ./db_data/lineitem.tbl
python clean_data.py ./db_data/nation.tbl
python clean_data.py ./db_data/orders.tbl
python clean_data.py ./db_data/part.tbl
python clean_data.py ./db_data/partsupp.tbl
python clean_data.py ./db_data/region.tbl
python clean_data.py ./db_data/supplier.tbl



psql -U adv -h 127.0.0.1 -c "TRUNCATE customer;"
psql -U adv -h 127.0.0.1 -c "TRUNCATE lineitem;"
psql -U adv -h 127.0.0.1 -c "TRUNCATE nation;"
psql -U adv -h 127.0.0.1 -c "TRUNCATE orders;"
psql -U adv -h 127.0.0.1 -c "TRUNCATE part;"
psql -U adv -h 127.0.0.1 -c "TRUNCATE partsupp;"
psql -U adv -h 127.0.0.1 -c "TRUNCATE region;"
psql -U adv -h 127.0.0.1 -c "TRUNCATE supplier;"


psql -U adv -h 127.0.0.1 -c "COPY lineitem FROM '/db_data/lineitem.tbl' DELIMITERS '|' CSV;"
psql -U adv -h 127.0.0.1 -c "COPY customer FROM '/db_data/customer.tbl' DELIMITERS '|' CSV;"
psql -U adv -h 127.0.0.1 -c "COPY nation FROM '/db_data/nation.tbl' DELIMITERS '|' CSV;"
psql -U adv -h 127.0.0.1 -c "COPY orders FROM '/db_data/orders.tbl' DELIMITERS '|' CSV;"
psql -U adv -h 127.0.0.1 -c "COPY part FROM '/db_data/part.tbl' DELIMITERS '|' CSV;"
psql -U adv -h 127.0.0.1 -c "COPY partsupp FROM '/db_data/partsupp.tbl' DELIMITERS '|' CSV;"
psql -U adv -h 127.0.0.1 -c "COPY region FROM '/db_data/region.tbl' DELIMITERS '|' CSV;"
psql -U adv -h 127.0.0.1 -c "COPY supplier FROM '/db_data/supplier.tbl' DELIMITERS '|' CSV;"

rm -rf ./db_data