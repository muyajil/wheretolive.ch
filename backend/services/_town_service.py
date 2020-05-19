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

    def get_towns(self, bfs_nrs=[], names=[]):
        towns = Town.query.with_entities(Town.id, Town.name, Town.bfs_nr)
        if bfs_nrs and names:
            towns = towns.filter(Town.bfs_nr.in_(bfs_nrs) or Town.name.in_(names))
        return towns.all()
