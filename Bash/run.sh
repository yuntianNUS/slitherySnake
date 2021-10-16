echo dhruvasexy

# pip3 install -r requirements.txt

if [ ! -d dockerDump ]
then 
    mkdir ./dockerDump
fi

getDataCatToFile() {
    secs=86400
    endTime=$(( $(date +%s) + secs))
    while [ $(date +%s) -lt $endTime ]; do
        names=$(python3 ftx.py "$1")
        SAVEIFS=$IFS   # Save current IFS
        IFS=$'\n'      # Change IFS to new line
        names=($names) # split to array $names
        IFS=$SAVEIFS   # Restore IFS
        filename=dockerDump/$(basename ${names[1]})
        jsout=${names[0]}
        
        if [ ! -f filename ]
        then  
            touch $filename
            echo "$jsout" >> $filename 
        else 
            echo "$jsout" >> $filename
        fi
    done
}

topTen=($(python3 CMP.py))

for coin in ${topTen[@]}; do 
    getDataCatToFile ${coin^^} &
done
