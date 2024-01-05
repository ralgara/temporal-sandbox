#!/usr/bin/env bash
cd ~/code/temporal-sandbox/cache/pageviews/; 
for f in $(ls); 
do jq -r '.items[] | 
    .year + .month + .day as $date | 
    .articles[] | 
    ( "\($date)|\(.views)|\(.rank)|\(.article)" )' $f | head -500; done > ../../table.txt

cd ~/code/temporal-sandbox
sqlite3 pageviews.db
create table pageviews (date NUMBER, views NUMBER, rank NUMBER, article TEXT);
.separator "|"
.import table.txt pageviews

