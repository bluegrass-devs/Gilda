#!/bin/bash
for i in 1 2 3 4 5
do
   echo "Welcome test $i times"
   curl -X "POST" http://localhost:8080/t/gilda/events -d '{"type":"url_verification","token":"09876","challenge":"54321","event":{"type":"member_joined_channel","channel":"C013R9EK6QM","user":"ULPT5Q78T"}}' &
done
