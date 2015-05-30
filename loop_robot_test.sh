#!/usr/bin/env bash
# Check if gameserver is running
count=2
cd ~/
rm -rf result
mkdir result
touch ./result/result.txt

appendResult () {
    cd ~/
    result=`sed -e '$!d' ./run_area/server/data.csv`
    echo $result
    echo "$result\n" >> ./result/result.txt
    cd -
}

for i in 1 2 3 4 5 6
do
    cd ~/game/
    # kill all process about game
    ps t | grep python | cut -c 1-5 | xargs kill -9 >/dev/null 2>&1
    ./RobotTest.sh
    echo "running"
    while true
    do
        if pgrep "gameserver" > /dev/null
        then
            sleep 10
        else
            echo "-----Over-----"
            break
        fi
    done

    echo "generate result to ~/result"
    cd ~/result/
    cp ~/run_area/works/target/my.txt client_$i.txt
    cp ~/run_area/server/log.txt server_$i.txt
    cp ~/run_area/server/replay.txt replay_$i.txt

    appendResult
    echo "waiting for socket port release"
    sleep 60
done

