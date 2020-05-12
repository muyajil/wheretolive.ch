from ..models import Town


class TownService:
    def get_typeahead_data(self):
        typeahead_data = []
        towns = Town.query.with_entities(Town.id, Town.zip_code, Town.name)
        for town in towns:
            typeahead_data.append(
                {"id": town[0], "label": str(town[1]) + " " + town[2]}
            )
        return typeahead_data
