#!/bin/bash

# Lint the text files by removing blank lines and putting
# items in alphabetical order.

# For human organizational purposes only; program does not care.

lists=(premium.txt premiummod.txt free.txt freemod.txt responses.txt)

for list in "${lists[@]}"
do
    sed -i '/^[[:space:]]*$/d' $list
    sort $list -o $list
done
    
