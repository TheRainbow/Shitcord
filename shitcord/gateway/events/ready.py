from shitcord.models.core import Model


class Ready(Model):
    def __init__(self, data, http):
        data.update({'id': 0})
        super().__init__(data['id'], http)
        self._json = data

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json
