from django.test import TestCase
from raw_material.models import WareTypes, WareData, ProductAcquisition
from accounts.models import User
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



class DB_Creator():

    def user_creator(self, mail  = "test@admin.com", pswd= "ABC123", u_name = "Tester", fn = "John", ln ="Doe"):
        user_c = User.objects.create_user(
        email = mail,
        username = u_name,
        password = pswd,
        first_name = fn, 
        last_name = ln
        )
        return user_c

    def ware_type_creator(ware_typ = "ware_types", ware_wg = 1):
        ware_t = WareTypes.objects.create(
        ware_types = ware_typ,
        ware_wght = ware_wg
        )
        return ware_t

    def ware_data_creator(
        ware_typ,
        ware_bd = "Brand_1",
        ware_br_name = "Brand_Name_1",
        ware_wght = 99,
        ware_pr = 9,
        ):
        ware_d = WareData.objects.create(
            ware_type = ware_typ,
            ware_brand = ware_bd,
            ware_brand_name = ware_br_name,
            ware_weight = ware_wght,
            ware_price = ware_pr,
        )
        return ware_d

    def ware_product_creator(self, ware_typ, acq_price = 111, acq_user=None):
        ware_d = ProductAcquisition.objects.create(
            ware_type = ware_typ,
            acquisition_price = acq_price,
            acquisiton_user = acq_user,
        )
        return ware_d


class Test_0_Account_User(TestCase):

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



class Test_2_WareData(TestCase):

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
