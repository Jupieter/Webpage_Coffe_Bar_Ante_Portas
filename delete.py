
from raw_material.models import ProductAcquisition


def store_date_null():
    wares = ProductAcquisition.objects.all().order_by('ware_type')
    for ware in wares:
        ware.store_date = None
        ware.save()
    