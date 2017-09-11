
lists=(premium.txt premiummod.txt free.txt freemod.txt)


for list in "${lists[@]}"
do
    sort $list -o $list
done
    
