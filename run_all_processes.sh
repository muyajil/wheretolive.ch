DOCKER_PREFIX='docker run -d --rm --network container:db -e "LOGLEVEL=INFO" -e "DB_CONN=postgresql://wheretolive:wheretolive@db:5432/wheretolive" wheretolive'
/bin/bash -c "$DOCKER_PREFIX -m wheretolive.processes.towns_to_db"
/bin/bash -c "$DOCKER_PREFIX -m wheretolive.processes.route_distances_to_db"
/bin/bash -c "$DOCKER_PREFIX -m wheretolive.processes.tax_rates_to_db"
/bin/bash -c "$DOCKER_PREFIX -m wheretolive.processes.health_insurance_to_db"
