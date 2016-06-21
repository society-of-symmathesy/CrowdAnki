from uuid import uuid1

from CrowdAnki import utils
from CrowdAnki.common_constants import UUID_FIELD_NAME
from CrowdAnki.utils import merge_dicts


class JsonSerializable(object):
    readable_names = {}
    filter_set = {"mod",  # Modification time
                  "usn"  # Todo clarify
                  }

    def __init__(self):
        pass
        # self._update_fields()

    @staticmethod
    def default_json(wobject):
        if isinstance(wobject, JsonSerializable):
            return wobject.flatten()

        raise TypeError

    @classmethod
    def from_collection(cls, collection, entity_id):
        """
        Initializes object from Anki collection
        :param collection:
        :param entity_id:
        :return:
        """

    def flatten(self):
        return {self.readable_names[key] if key in self.readable_names else key: value
                for key, value in merge_dicts(self.__dict__, self._dict_extension()).iteritems() if
                key not in self.filter_set}

    def _dict_extension(self):
        return {}

    def _update_fields(self):
        """
        Add necessary fields to anki dicts/objects. E.g. uuid
        """

    def get_uuid(self):
        self._update_fields()
        # Todo consider introducing this in another way
        """
        :return: Unique identificator in a string format.
        """


class JsonSerializableAnkiDict(JsonSerializable):
    filter_set = JsonSerializable.filter_set | {"anki_dict"}

    def __init__(self, anki_dict=None):
        super(JsonSerializableAnkiDict, self).__init__()
        self.anki_dict = anki_dict

    def _dict_extension(self):
        return self.anki_dict

    def _update_fields(self):
        self.anki_dict.setdefault(UUID_FIELD_NAME, str(uuid1()))

    def get_uuid(self):
        super(JsonSerializableAnkiDict, self).get_uuid()
        return self.anki_dict[UUID_FIELD_NAME]


class JsonSerializableAnkiObject(JsonSerializable):
    filter_set = JsonSerializable.filter_set | {"anki_object"}

    def __init__(self, anki_object=None):
        super(JsonSerializableAnkiObject, self).__init__()
        self.anki_object = anki_object

    def _dict_extension(self):
        return self.anki_object.__dict__

    def _update_fields(self):
        utils.add_absent_field(self.anki_object, UUID_FIELD_NAME, str(uuid1()))

    def get_uuid(self):
        super(JsonSerializableAnkiObject, self).get_uuid()
        return getattr(self.anki_object, UUID_FIELD_NAME)
