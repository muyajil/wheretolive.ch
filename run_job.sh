/bin/bash -c "docker run --name $1 -d --network container:db -e 'FLASK_APP=wheretolive.webapp.wsgi' -e 'LOGLEVEL=INFO' -e 'DB_CONN=postgresql://wheretolive:wheretolive@db:5432/wheretolive' wheretolive $1"
