#!/bin/bash

if [ ! -f ./CITY_TO_STATE.py ] || [ ! -f ./craiglist_scrapper.py ] || [ ! -f ./email_real_estate.py ]
then 
    echo "Hello"
fi

read -p "Email will be sent from: " VAR1
read -sp "Password: " PASS
read -p "Email will be sent to: " VAR2

if [[ "$1" != "daily" ]] && [[ "$1" != "all" ]];
then
    echo The third argument can either be "daily" or "all"
fi

i=1
sp="/-\|"
echo -n ' '
while true
do
    printf "\b${sp:i++%${#sp}:1}"
done
python3 ./scripts/email_real_estate.py $VAR1 $VAR2 $1 $PASS
