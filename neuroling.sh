#!/bin/bash

#chcecks whether there are wav files in project directories 
count=$(find /home/myserver/data/ENG -name '*.[wW][aA][vV]' | wc -l)
count2=$(find /home/myserver/data/PL -name '*.[wW][aA][vV]' | wc -l)

#if so, runs docker with the script
if ([ $count != 0 ] || [ $count2 != 0 ]); 
then
	echo "Finded!"
    sleep 300
	docker run --name t1 --rm -i -v /home/myserver/data:/root/data neuroling:1.2
	rm -rf /home/myserver/data/ENG*
    rm -rf /home/myserver/data/PL*
	#for nextcloud
	chown www-data:www-data $(find /home/myserver/data/results -name "*.*")
	echo 'end of task'

else
	echo 'directory empty'
	sleep 10
fi
