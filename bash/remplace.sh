#!/bin/bash
for file in *.txt
do
  echo "Traitement de $file ..."
  sed -n '$=' "$file"
  sed -i -e "s/;/,/g" "$file"
done
