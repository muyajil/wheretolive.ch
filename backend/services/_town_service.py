from ..models import Town


class TownService:
    def get_typeahead_data(self):
        typeahead_dict = {}
        towns = Town.query.with_entities(Town.id, Town.zip_code, Town.name)
        for town in towns:
            typeahead_dict[town[0]] = str(town[1]) + " " + town[2]
        return typeahead_dict
