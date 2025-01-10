from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import types, Dialect
from typing import Any
import json


class JSONField(types.TypeDecorator):
    impl = LONGTEXT

    cache_ok = True

    def process_bind_param(self, value, dialect: Dialect) -> Any:
        return json.dumps(value)

    def process_result_value(self, value, dialect: Dialect) -> Any:
        if value is not None:
            return json.loads(value)

    def copy(self, **kw) -> 'JSONField':
        return JSONField()

    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)
