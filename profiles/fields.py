import json

from django.db.models import TextField
from django.core.serializers.json import DjangoJSONEncoder


class JSONField(TextField):
    def to_python(self, value):
        if value == '':
            return None
        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        val = None
        if value == '':
            return None
        if isinstance(value, dict):
            val = json.dumps(str(value), cls=DjangoJSONEncoder)
        return val
