

# Lint the text files by removing blank lines and putting
# items in alphabetical order.

# For human organizational purposes only; program does not care.

lists=(premium.txt premiummod.txt free.txt freemod.txt)

for list in "${lists[@]}"
do
    sort $list -o $list
done
    
