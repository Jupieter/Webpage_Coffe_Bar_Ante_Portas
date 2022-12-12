from django.test import TestCase
from raw_material.models import WareTypes, WareData

class Test_WareTypes(TestCase):

    def setUp(self) -> None:
        self.ware_types_1 = WareTypes.objects.create(
        ware_types = "Coffee",
        ware_wght = 7
        )
        self.ware_types_1.save()

        self.ware_types_2 = WareTypes.objects.create(
        ware_types = "Milk",
        ware_wght = 50
        )
        self.ware_types_2.save()

        self.ware_types_3 = WareTypes.objects.create(
        ware_types = "Sugar",
        ware_wght = 50
        )
        self.ware_types_3.save()

        self.ware_types_4 = WareTypes.objects.create(
        ware_types = "Flavour",
        ware_wght = 50
        )
        self.ware_types_4.save()
    
    def test_ware_types_count(self):
        self.assertEqual(WareTypes.objects.count(), 4)

    def test_ware_types_by_id(self):
        coffee = WareTypes.objects.filter(id=1)[0]
        milk = WareTypes.objects.filter(id=2)[0]
        sugar = WareTypes.objects.filter(id=3)[0]
        flavour = WareTypes.objects.filter(id=4)[0]
        self.assertEqual(coffee.ware_types, "Coffee")
        self.assertEqual(milk.ware_types, "Milk")
        self.assertEqual(sugar.ware_types, "Sugar")
        self.assertEqual(flavour.ware_types, "Flavour")


class Test_WareData(TestCase):

    def setUp(self) -> None:
        # WareTypes load with Data
        
        self.ware_types_1 = WareTypes.objects.create(
        ware_types = "Coffee",
        ware_wght = 7
        )
        self.ware_types_1.save()

        self.ware_types_2 = WareTypes.objects.create(
        ware_types = "Milk",
        ware_wght = 50
        )
        self.ware_types_2.save()

        self.ware_types_3 = WareTypes.objects.create(
        ware_types = "Sugar",
        ware_wght = 50
        )
        self.ware_types_3.save()

        self.ware_types_4 = WareTypes.objects.create(
        ware_types = "Flavour",
        ware_wght = 50
        )
        self.ware_types_4.save()

        # WareData load with Data
        self.ware_data1 = WareData(
            ware_type = self.ware_types_1,
            ware_brand = "Brand_1",
            ware_brand_name = "Brand_Name_1_coffee",
            ware_weight = 1000,
            ware_price = 100
        )
        self.ware_data1.save()

        self.ware_data2 = WareData(
            ware_type = self.ware_types_2,
            ware_brand = "Brand_2",
            ware_brand_name = "Brand_Name_2_milk",
            ware_weight = 1000,
            ware_price = 100
        )
        self.ware_data2.save()

        self.ware_data3 = WareData(
            ware_type = self.ware_types_3,
            ware_brand = "Brand_3",
            ware_brand_name = "Brand_Name_3_sugar",
            ware_weight = 1000,
            ware_price = 100
        )
        self.ware_data3.save()

        self.ware_data4 = WareData(
            ware_type = self.ware_types_4,
            ware_brand = "Brand_4",
            ware_brand_name = "Brand_Name_4_flavour",
            ware_weight = 1000,
            ware_price = 100
        )
        self.ware_data4.save()

    def test_ware_data_count(self):
        # print(self.ware_data2)
        # print(WareData.objects.all())
        self.assertEqual(WareData.objects.count(), 4)
    
    def test_ware_types_by_id(self):
        coffee_ware = WareData.objects.filter(id=1)[0]
        milk_ware = WareData.objects.filter(id=2)[0]
        sugar_ware = WareData.objects.filter(id=3)[0]
        flavour_ware = WareData.objects.filter(id=4)[0]
        self.assertEqual(coffee_ware.ware_brand_name, "Brand_Name_1_coffee")
        self.assertEqual(milk_ware.ware_brand_name, "Brand_Name_2_milk")
        self.assertEqual(sugar_ware.ware_brand_name, "Brand_Name_3_sugar")
        self.assertEqual(flavour_ware.ware_brand_name, "Brand_Name_4_flavour")