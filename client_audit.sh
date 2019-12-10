#!/bin/bash

set_env () {
    url_api="http://localhost:5000/post"
    host_id=5
    #cpu_serial=`cpuid | grep "processor serial number:" | uniq | grep -oe "[0-9-].*"`
    id_mb=`dmidecode | grep UUID | cut -d" " -f2`
    ipv4=`ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'`
    mac_address="`ifconfig enp9s0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'`"
    timestamp=`date +"%H:%M:%S %d.%m.%Y"`
    hostname=a-trushchenkova-pc.adminforum.online #"`hostname`"
    users=a.trushchenkova #"`who | cut -d' ' -f1 | sort | uniq`"
}

post_to_api () {
    response=`curl -d "{\"id_mb\": \"${id_mb}\", \"timestamp\": \"${timestamp}\", \"hostname\": \"${hostname}\", \"ipv4\": \"${ipv4}\",\"users\": \"${users}\"}" \
	    -H "Content-Type: application/json" \
	    ${url_api}`
    echo "This is response --- ${response}"
}

main () {
    set_env
    post_to_api
}

main

