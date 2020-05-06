create materialized view agg_closest_train_commute as
(select 
	source_town.zip_code as source_zip_code,
	target_town.zip_code as target_zip_code,
	train_commute.time,
	train_commute.changes
from 
	commute 
	join train_commute on train_commute.commute_id = commute.id
	join town as source_town on source_town.id = commute.source_town_id
	join town as target_town on target_town.id = commute.target_town_id
	join sbb_station as source_sbb_station on source_sbb_station.id = source_town.closest_train_station_id
	join sbb_station as target_sbb_station on target_sbb_station.id = target_town.closest_train_station_id
where
	train_commute.commute_type = 'closest_train');

create index closest_train_target_zip_idx on agg_closest_train_commute (target_zip_code, time);