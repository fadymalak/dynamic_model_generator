from abc import ABC, abstractmethod
from rest_framework import serializers
from django.apps import apps
from django.db import models, connection


def create_model_database(model):
    try:
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)
    except:
        raise serializers.ValidationError("model already exists")
    return True


def generate_model(app_label, model_name, fields):
    meta_attrs = {"app_label": app_label, "verbose_name_plural": model_name}
    attrs = {"__module__": app_label, "Meta": type("Meta", (object,), meta_attrs)}
    for field in fields:
        attrs[field["name"]] = getattr(models, field["type"])()
    model = type(model_name, (models.Model,), attrs)
    print(model._meta.get_fields())
    return model


def create_model_fields(model, new_fields):
    for field in new_fields:
        model.add_to_class(field["name"], getattr(models, field["type"])(null=True))
        with connection.schema_editor() as schema_editor:
            schema_editor.add_field(model, model._meta.get_field(field["name"]))
    return True


def delete_model_fields(model, deleted_fields):
    for field in deleted_fields:
        model.add_to_class(field["name"], getattr(models, field["type"])(null=True))
        with connection.schema_editor() as schema_editor:
            schema_editor.remove_field(model, model._meta.get_field(field["name"]))
    return True


def alter_model_fields(model, alter_fields):
    for field in alter_fields:
        try:
            field = getattr(models, field["type"])(null=True)
            field.column = field["name"]
            old_field = model._meta.get(field["name"])
            with connection.schema_editor() as schema_editor:
                schema_editor.alter_field(model, old_field, field)
        except DataError:
            print(
                f"cannot cast from {model._meta.get(field['name']).get_internal_type()}  to  {field['type']}"
            )
    return True


def get_exist_fields(field_keys, fields):
    return list(filter(lambda field: field["name"] in field_keys, fields))


def get_new_fields(field_keys, fields):
    return list(filter(lambda field: field["name"] not in field_keys, fields))


def get_deleted_fields(deleted_keys, fields):
    return list(filter(lambda field: field["name"] not in deleted_keys, fields))


def get_altered_fields(exist_fields, model):
    alter_fields = []
    for item in exist_fields:
        condition = lambda field: getattr(models, field["type"]) == type(
            model._meta.get_field(field["name"])
        )
        if not condition(item):
            alter_fields.append(item)
    return alter_fields


def apply_migrations(model, deleted_fields, new_fields):
    try:
        delete_model_fields(model, deleted_fields)
        create_model_fields(model, new_fields)
    except:
        serializers.ValidationError("error happen during migration")
    return True


def get_fields(fields, table_fields, model):
    field_keys = [field["name"] for field in table_fields]
    deleted_keys = [field["name"] for field in fields]
    exist_fields = get_exist_fields(field_keys, fields)
    new_fields = get_new_fields(field_keys, fields)
    deleted_fields = get_deleted_fields(deleted_keys, table_fields)
    alter_fields = get_altered_fields(exist_fields, model)
    return exist_fields, new_fields, deleted_fields, alter_fields


class AbstractFactory(ABC):
    """
    The abstract factory for creating dynamic models and serializers.
    """

    @abstractmethod
    def create_dynamic_serializer(self, model_name, fields):
        pass

    @abstractmethod
    def create_model(self, app_label, model_name, fields):
        pass


class DRFFactory(AbstractFactory):
    """
    The concrete factory for creating dynamic models and serializers using DRF.
    """

    def __init__(self, model_name, fields, app_label):
        self.model_name = model_name
        self.fields = fields
        self.app_label = app_label
        self.model = None

    def create_dynamic_serializer(self):
        if self.model is None:
            self.model = self.create_model()
        attrs = {
            "Meta": type("Meta", (object,), {"model": self.model, "fields": "__all__"})
        }
        for field in self.fields:
            if field["name"] != "id":
                attrs[field["name"]] = serializers.CharField(max_length=255)
        serializer = type(
            f"{self.model_name}Serializer", (serializers.ModelSerializer,), attrs
        )
        return serializer

    def create_model(self):
        meta_attrs = {
            "app_label": self.app_label,
            "verbose_name_plural": self.model_name,
        }
        attrs = {
            "__module__": self.app_label,
            "Meta": type("Meta", (object,), meta_attrs),
        }
        for field in self.fields:
            attrs[field["name"]] = getattr(models, field["type"])()
        model = type(self.model_name, (models.Model,), attrs)
        return model
