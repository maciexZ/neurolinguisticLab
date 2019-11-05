#!/bin/bash

#pliki wav w obserwowanych folderach
#~/data/FOKUS/ENG
#rusza docker wykonujący skrypt. Samozagłada dockera na koniec
printf "finded files\n"
sleep 300
printf "go on\n"
docker run --name t1 --rm -i -v /home/myserver/data:/root/data fokus:1.2
rm -rf /home/myserver/data/FOKUS/ENG/*
#zmina własności potrzebna nexcloud
chown www-data:www-data $(find /home/myserver/rezultaty -name "*.*")
echo "done $(date)" >> /home/myserver/rezultaty/dataWykonania.txt
printf 'seems to be ok\n'

exit 0
