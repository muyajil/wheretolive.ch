/bin/bash -c "docker run --name $1 -d --network container:db -e 'LOGLEVEL=INFO' -e 'DB_CONN=postgresql://wheretolive:wheretolive@db:5432/wheretolive' wheretolive -m wheretolive.jobs.$1"
