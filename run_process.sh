DOCKER_PREFIX='docker run -d --rm --network container:db -e "LOGLEVEL=INFO" -e "DB_CONN=postgresql://wheretolive:wheretolive@db:5432/wheretolive" wheretolive'
/bin/bash -c "$DOCKER_PREFIX -m wheretolive.processes.$1"
