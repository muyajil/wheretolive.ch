export LOGLEVEL="INFO"
export DB_CONN="postgresql://wheretolive:wheretolive@localhost:5432/wheretolive"
python -m wheretolive.processes.init_db
python -m wheretolive.processes.towns_to_db
python -m wheretolive.processes.route_distances_to_db
python -m wheretolive.processes.tax_rates_to_db
python -m wheretolive.processes.health_insurance_to_db

