#!/usr/bin/env bash
# Check if gameserver is running
count=10
for i in 1 2 3 .. count
do
    cd
    cd game/
    # kill all process about game
    ps t | grep 127.0.0.1 | cut -c 1-5 | xargs kill -9
    sleep 2
    ./RobotTest.sh > /dev/null
    while true
    do
        if pgrep "gameserver" > /dev/null
        then
            echo "still running"
            sleep 30
        else
            echo "game over"
            break
        fi
    done

    cd ../run_area/server
    result=`sed -e '$!d' data.csv`
    cd ../..
    echo "$result\n" >> result.txt
done
