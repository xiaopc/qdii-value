import demjson3

_data = {
    "_id": None,
    "version": None,
    "fund_name": None,
    "fund_source": None,
    "last_update": None,
    "reference": None,
    "forex": None,
    "equities": None,
    "equities_percent": "100"
}
_equity = {
    "source": None,     # String,
    "source_id": None,  # String/Integer
    "name": None,       # String,
    "code": None,       # String,
    "capital": None,    # Optional String,
    "volume": None,     # Optional String,
    "weight": None      # String+%
}


class Config:
    def __init__(self, obj=None, _id=None):
        self.data = _data.copy()
        # import
        if obj:
            if isinstance(obj, str):
                obj = demjson3.decode(obj)
            # update
            if isinstance(obj, list) or "version" not in obj.keys():
                raise Exception("配置文件版本过低，请删除后重试.")
            self.data.update(obj)
        # create
        elif _id:
            self.data["_id"] = _id
            self.data["version"] = 3

    def save(self, path):
        with open(path, 'w') as f:
            f.write(demjson3.encode(self.data))
        return path
