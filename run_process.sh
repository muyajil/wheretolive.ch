DOCKER_PREFIX='docker run --name '$1' -d --network container:db -e "LOGLEVEL=INFO" -e "DB_CONN=postgresql://wheretolive:wheretolive@db:5432/wheretolive" -e "MAPS_API_KEY=AIzaSyBzWe16UIfLa_5u1SMiRACTcXOr-K0zCrU" wheretolive'
/bin/bash -c "$DOCKER_PREFIX -m wheretolive.processes.$1"
