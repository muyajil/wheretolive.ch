# export LOGLEVEL="INFO"
# export DB_CONN="postgresql://wheretolive:wheretolive@localhost:5432/wheretolive"
DOCKER_PREFIX='docker run -d --rm -e "LOGLEVEL=INFO" -e "DB_CONN=postgresql://wheretolive:wheretolive@localhost:5432/wheretolive" wheretolive'
$DOCKER_PREFIX python -m wheretolive.processes.init_db
$DOCKER_PREFIX python -m wheretolive.processes.towns_to_db
$DOCKER_PREFIX python -m wheretolive.processes.route_distances_to_db
$DOCKER_PREFIX python -m wheretolive.processes.tax_rates_to_db
$DOCKER_PREFIX python -m wheretolive.processes.health_insurance_to_db

