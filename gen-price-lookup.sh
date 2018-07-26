#!/bin/bash

for i in `seq 1 100`;
do
    for j in `seq 1 10`;
    do
      echo "{\"statement\":\"select store_prices[0] from pricing2 USE KEYS 'store::$i::product::$j';\"}"
    done
done
