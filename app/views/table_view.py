from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import serializers, viewsets
from app.utils import *
from django.db import models, connection
from django.apps import apps
from app.serializer.table_serializer import DynamicModelSerializer
from app.models import Table
from django.db import transaction
from django.db.utils import DataError


class DynamicModelView(viewsets.ViewSet):
    """
    The view for creating a dynamic model.
    """

    def create(self, request, *args, **kwargs):
        serializer = DynamicModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model_name = serializer.validated_data["model_name"]
        fields = serializer.validated_data["fields"]
        app_label = __package__.split(".")[0]
        factory = DRFFactory(model_name, fields, app_label)
        model = factory.create_model()
        sid = transaction.savepoint()
        try:
            with transaction.atomic():
                create_model_database(model)
                Table.objects.create(name=model_name, fields=fields)
        except:
            transaction.savepoint_rollback(sid)
            return Response(
                {"message": f"Model '{model_name}' already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": f"Model '{model_name}' has been created."},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk):
        serializer = DynamicModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model_name = serializer.validated_data["model_name"]
        fields = serializer.validated_data["fields"]
        app_label = __package__.split(".")[0]  # get app_label
        try:
            table = Table.objects.get(id=pk)
        except Table.DoesNotExist:
            raise serializers.ValidationError("model already exists")
        factory = DRFFactory(model_name, table.fields, app_label)
        model = factory.create_model()
        exist_fields, new_fields, deleted_fields, alter_fields = get_fields(
            fields, table.fields, model
        )
        if alter_fields:
            raise serializers.ValidationError("alter fields type not supported yet")
        apply_migrations(model, deleted_fields, new_fields)
        table.fields = fields
        table.save()
        return Response(
            {"message": f"Model '{model_name}' has been updated."},
            status=status.HTTP_201_CREATED,
        )


class DataViewset(viewsets.ViewSet):
    """
    The view for creating a dynamic model.
    """

    def list(self, request, pk):
        app_label = __package__.split(".")[0]
        try:
            table = Table.objects.get(id=pk)
        except Table.DoesNotExist:
            return Response(
                {"message": "custom model cannot be found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        factory = DRFFactory(table.name, table.fields, app_label)
        model = factory.create_model()
        queryset = model.objects.all()
        serializer_obj = factory.create_dynamic_serializer()
        serializer = serializer_obj(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pk):
        app_label = __package__.split(".")[0]
        table = Table.objects.get(id=pk)
        factory = DRFFactory(table.name, table.fields, app_label)
        model = factory.create_model()
        serializer_obj = factory.create_dynamic_serializer()
        serializer = serializer_obj(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
