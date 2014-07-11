from django.db import models
from django.conf import settings

from django_hstore import hstore

# determine if geodjango is in use
GEODJANGO = settings.DATABASES['default']['ENGINE'] == 'django.contrib.gis.db.backends.postgis'


__all__ = [
    'Ref',
    'DataBag',
    'ModeledDataBag',
    'NullableDataBag',
    'RefsBag',
    'NullableRefsBag',
    'DefaultsModel',
    'BadDefaultsModel',
    'DefaultsInline',
    'NumberedDataBag',
    'GEODJANGO'
]


class Ref(models.Model):
    name = models.CharField(max_length=32)


class HStoreModel(models.Model):
    objects = hstore.HStoreManager()

    class Meta:
        abstract = True


class DataBag(HStoreModel):
    name = models.CharField(max_length=32)
    data = hstore.DictionaryField()

from django_hstore.virtual import VirtualField

class ModeledDataBag(HStoreModel):
    name = models.CharField(max_length=32)
    data = hstore.ModeledDictionaryField(schema={
        'number': {
            'type': int,
            'default': 0
        }
    })
    # the ModeledDictionaryField should create the virtual fields automatically
    # each created virtualfield should be initialized with an on the fly created (metaprogramming)
    # virtual field which should be the result of for example IntegerField and VirtualFieldMixin
    # validation should be handled by the VirtualField only, no HStoreModelValidation shit
    
    number = VirtualField(hstore_field_name='data')


class NullableDataBag(HStoreModel):
    name = models.CharField(max_length=32)
    data = hstore.DictionaryField(null=True)


class RefsBag(HStoreModel):
    name = models.CharField(max_length=32)
    refs = hstore.ReferencesField()


class NullableRefsBag(HStoreModel):
    name = models.CharField(max_length=32)
    refs = hstore.ReferencesField(null=True, blank=True)


class DefaultsModel(models.Model):
    a = hstore.DictionaryField(default={})
    b = hstore.DictionaryField(default=None, null=True)
    c = hstore.DictionaryField(default={'x': '1'})


class BadDefaultsModel(models.Model):
    a = hstore.DictionaryField(default=None)


class DefaultsInline(models.Model):
    parent = models.ForeignKey(DefaultsModel)
    d = hstore.DictionaryField(default={ 'default': 'yes' })


class NumberedDataBag(HStoreModel):
    name = models.CharField(max_length=32)
    data = hstore.DictionaryField()
    number = models.IntegerField()


# if geodjango is in use define Location model, which contains GIS data
if GEODJANGO:
    from django.contrib.gis.db import models as geo_models
    class Location(geo_models.Model):
        name = geo_models.CharField(max_length=32)
        data = hstore.DictionaryField()
        point = geo_models.GeometryField()
    
        objects = hstore.HStoreGeoManager()
    
    __all__.append('Location')