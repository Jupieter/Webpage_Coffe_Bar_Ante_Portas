from django.test import TestCase
from raw_material.models import WareTypes, WareData
from c_app.models import Task

class Test_Task(TestCase):

    def setUp(self) -> None:
        task = Task.objects.create(
        name = "Lilith",
        age = 5000
        )
        task.save()
    
    def test_task_count(self):
        self.assertEqual(Task.objects.count(), 1)

    def test_task_by_id(self):
        task = Task.objects.filter(id=1)[0]
        print("Lilith",task)
        self.assertEqual(task.name, 'Lilith')


class Test_WareTypes(TestCase):

    def setUp(self) -> None:
        self.ware_types_1 = WareTypes.objects.create(
        ware_types = "Coffee",
        ware_wght = 7
        )
        self.ware_types_1.save()
    
    def test_ware_types_count(self):
        self.assertEqual(WareTypes.objects.count(), 1)

    def test_ware_types_by_id(self):
        coffee = WareTypes.objects.filter(id=1)[0]
        self.assertEqual(coffee.ware_types, "Coffee")



class Test_WareData(TestCase):

    def setUp(self) -> None:
        # WareTypes load with Data
        types = ["Coffee", "Milk", "Sugar", "Flavour"]
        weigth = [7,50, 50, 50]
        for i in range(4):
            ware_types= WareTypes.objects.create(
            ware_types = types[i],
            ware_wght = weigth[i]
            )
            ware_types.save()
       

        # WareData load with Data
        w_datas = [[1, "Brand_Coffee", "Brand_Name_Coffee", 1000, 400],  
        [2, "Brand_Milk", "Brand_Name_Milk", 1000, 300], 
        [3, "Brand_Sugar", "Brand_Name_Sugar", 999, 200],
        [4, "Brand_Flavour", "Brand_Name_Flavour", 1000, 100]
        ]
        for w_data in w_datas:
            ware_data = WareData(
                ware_type = WareTypes.objects.filter(id=w_data[0])[0],
                ware_brand = w_data[1],
                ware_brand_name = w_data[2],
                ware_weight = w_data[3],
                ware_price = w_data[4],
            )
            ware_data.save()


    def test_ware_data_count(self):
        # print("2   WareTypes", WareTypes.objects.all())
        # print(self.ware_data2)
        # print(WareData.objects.all())
        self.assertEqual(WareData.objects.count(), 4)
    
    def test_ware_types_by_id(self):
        coffee_ware = WareData.objects.filter(id=1)[0]
        milk_ware = WareData.objects.filter(id=2)[0]
        sugar_ware = WareData.objects.filter(id=3)[0]
        flavour_ware = WareData.objects.filter(id=4)[0]
        self.assertEqual(coffee_ware.ware_brand_name, "Brand_Name_Coffee")
        self.assertEqual(milk_ware.ware_brand, "Brand_Milk")
        self.assertEqual(sugar_ware.ware_weight, 999)
        self.assertEqual(flavour_ware.ware_price, 100)