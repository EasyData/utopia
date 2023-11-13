#!/bin/bash

CITIES=(
  beijing
  shanghai
  shenzhen
)

for city in ${CITIES[@]}; do
  mkdir -p archives/$city
  output="archives/$city/$(date +%F).jsonl"
  scrapy runspider spiders/$city.py -o $output:jsonlines
  if [[ -s $output ]]; then
    gzip -f $output
    echo "OK: $city"
  else
    rm -f $output
    echo "ERROR: $city"
  fi
done
