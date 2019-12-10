#!/bin/bash

set_env () {
    url_api="http://localhost:5000/post"
    host_id=1
    hostname="`hostname`"
    users="`who | cut -d' ' -f1 | sort | uniq`"

}

post_to_api () {
    curl -d "{\"host_id\": ${host_id}, \"hostname\": \"${hostname}\",\"users\": \"${users}\"}" \
	    -H "Content-Type: application/json" \
	    ${url_api}
}

main () {
    set_env
    post_to_api
}

main
