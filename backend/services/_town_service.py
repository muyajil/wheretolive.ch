from ..models import Town


class TownService:
    def get_typeahead_data(self):
        typeahead_data = []
        towns = Town.query.with_entities(Town.id, Town.zip_code, Town.name)
        for town in towns:
            typeahead_data.append(
                {"id": town[0], "label": str(town[1]) + " " + town[2]}
            )
        typeahead_data = sorted(typeahead_data, key=lambda x: x["label"])
        return typeahead_data

    def get_bfs_nr(self, town_id):
        return Town.query.get(town_id).bfs_nr

    def get_town_identifiers(self, bfs_nrs=[], names=[]):
        towns = Town.query.with_entities(Town.id, Town.name, Town.bfs_nr)
        if bfs_nrs and names:
            towns = towns.filter(Town.bfs_nr.in_(bfs_nrs) or Town.name.in_(names))
        return [{"id": x[0], "name": x[1], "bfs_nr": x[2]} for x in towns]

    def get_shopping_info(self, town_ids=[]):
        towns = Town.query.with_entities(
            Town.id, Town.migros, Town.coop, Town.lidl, Town.aldi
        )
        if town_ids:
            towns = towns.filter(Town.id.in_(town_ids))
        return [
            {"id": x[0], "migros": x[1], "coop": x[2], "lidl": x[3], "aldi": x[4]}
            for x in towns
        ]

    def get_towns_from_zips(self, zip_codes):
        towns = Town.query.with_entities(
            Town.id, Town.zip_code, Town.bfs_nr, Town.name
        ).filter(Town.zip_code.in_(zip_codes))

        return [
            {"id": x.id, "zipCode": x.zip_code, "bfsNr": x.bfs_nr, "name": x.name}
            for x in towns
        ]
