from django.test import TestCase
from datetime import timezone, datetime
from raw_material.models import WareTypes, WareData, ProductAcquisition
from accounts.models import User
from shop.models import CoffeeMake, CoffeeOrder
from c_app.models import Task


class DB_Creator():
    def user_creator(self, mail  = "test@admin.com", u_name = "Tester", pswd= "ABC123", fn = "John", ln ="Doe"):
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

    def ware_product_creator(ware_typ, acq_price = 111, acq_user=None):
        ware_d = ProductAcquisition.objects.create(
            ware_type = ware_typ,
            acquisition_price = acq_price,
            acquisiton_user = acq_user,
        )
        return ware_d


class Test_0_Account_User(TestCase):

    def setUp(self) -> None:
        usr = DB_Creator.user_creator(self)
        usr.save()

    def test_user_count(self):
        #   print("USER:    ", User.objects.all())
        self.assertEqual(User.objects.count(), 1)
    
    def test_user_detail(self):
        us_er = User.objects.get(id=1)
        self.assertEqual(us_er.email, "test@admin.com")
        self.assertEqual(us_er.username, "Tester")
        # self.assertEqual(us_er.password, "ABC123")
        self.assertEqual(us_er.first_name, "John")
        self.assertEqual(us_er.last_name, "Doe")
        self.assertEqual(us_er.__str__(), "Tester" )
        self.assertEqual(us_er.get_short_name(), "John" )
        self.assertEqual(us_er.get_full_name(), "John Doe" )
        self.assertEqual( us_er.is_active, True ) 
        self.assertEqual( us_er.is_staff, False )
        self.assertEqual(us_er.is_superuser, False )
        with self.assertRaises(ValueError) as error:
            User.objects.create_user(self, "test@admin.com", "", "Tester", "John", "Doe")
        self.assertEqual(str(error.exception), 'Users must have a password')
        u_ser = User.objects.create_user(email = "test@mail.com", username = "u_name", password = "pswd")
        self.assertEqual(u_ser.get_short_name(), "test@mail.com" )
        self.assertEqual(u_ser.get_full_name(), "test@mail.com" )
    
    def test_staffuser(self):
        user_saff = User.objects.create_staff_user(
        email = "staff@admin.com",
        username = "STAFF",
        password = "XYZ999",
        first_name = "Stefi", 
        last_name = "Stafi"
        )
        user_saff.save()
        # (User.objects.all())
        self.assertEqual(User.objects.count(), 2)

    def test_superuser(self):
        user_super = User.objects.create_superuser(
        email = "superuser@admin.com",
        username = "SUPER",
        password = "QW12ER",
        first_name = "Super", 
        last_name = "User"
        )
        user_super.save()
        # print(User.objects.all())
        self.assertEqual(User.objects.count(), 2)


class Test_1_WareTypes(TestCase):

    def setUp(self) -> None:
        wt = DB_Creator.ware_type_creator("Something", 77)
        wt.save()
    
    def test_ware_types_count(self):
        self.assertEqual(WareTypes.objects.count(), 1)

    def test_ware_types_by_detail(self):
        wt_1 = WareTypes.objects.get(id=1)
        self.assertEqual(wt_1.ware_types, "Something")
        self.assertEqual(wt_1.ware_wght, 77) 
        self.assertEqual(wt_1.__str__(), 'Something')


class Test_2_WareData(TestCase):

    def setUp(self) -> None:
        # WareTypes load with Data
        ware_type_list = [ ["Coffee", 7], ["Milk", 50], ["Sugar", 50], ["Flavour", 50] ]
        for ware_type_data in ware_type_list: 
            wt_types = ware_type_data[0]
            wt_wght = ware_type_data[1]
            wt = DB_Creator.ware_type_creator(wt_types, wt_wght)
            wt.save()
        wt1 = WareTypes.objects.get(id=1)
        wd = DB_Creator.ware_data_creator(wt1)
        wd.save()

    def test_ware_data_count(self):
        self.assertEqual(WareTypes.objects.count(), 4)
    
    def test_ware_data_by_detail(self):
        wd_1 = WareData.objects.get(id=1)
        self.assertEqual(wd_1.ware_brand, "Brand_1")
        self.assertEqual(wd_1.ware_brand_name, "Brand_Name_1")
        self.assertEqual(wd_1.ware_weight, 99)
        self.assertEqual(wd_1.ware_price, 9)
        self.assertEqual(wd_1.__str__(), 'Brand_1, Brand_Name_1, Coffee')


class Test_3_ProductAcquisition(TestCase):
    
    def setUp(self) -> None:
        # User create
        user_list = [
        ["test@acquisition.com", "Acquisitor", "ABC001", "Ac", "Qu"],
        ["test@store.com", "Storer", "ABC002", "St0", "Re"],
        ["test@open.com", "Opener", "ABC003", "Op", "En"],
        ["test@empty.com", "Emptyr", "ABC004", "Em", "Pty"],
        ]
        for i in range(4): 
            u_ser = DB_Creator.user_creator(self, user_list[i][0], user_list[i][1], user_list[i][2], user_list[i][3])
            u_ser.save()
        # WareTypes load with Data
        ware_type_list = [ ["Coffee", 7], ["Milk", 50], ["Sugar", 50], ["Flavour", 50] ]
        for ware_type_data in ware_type_list: 
            wt_types = ware_type_data[0]
            wt_wght = ware_type_data[1]
            wt = DB_Creator.ware_type_creator(wt_types, wt_wght)
            wt.save()
        # WareData load with Data
        ware_data_list = [
            ["Brand_Coffee", "Brand_Name_Coffee", 250, 900,],
            ["Brand_Milk", "Brand_Name_Milk", 500, 800,],
            ["Brand_Sugar", "Brand_Name_Sugar", 100, 700,],
            ["Brand_Flavour", "Brand_Name_Flavour", 450, 600,]
            ]
        for i in range(4): 
            wt = WareTypes.objects.get(id=i+1)
            wd = DB_Creator.ware_data_creator(wt, ware_data_list[i][0], ware_data_list[i][1], ware_data_list[i][2], ware_data_list[i][3])
            wd.save()
        
        ware_pa = WareData.objects.get(id=1)
        u_ser = User.objects.get(id=1)
        pa = DB_Creator.ware_product_creator(ware_pa, 699, u_ser)
        pa.save()
    
    def test_product_acquisition_count(self):
        self.assertEqual(ProductAcquisition.objects.count(), 1)

    def test_product_acquisition_by_detail(self):
        pa_1 = ProductAcquisition.objects.get(id=1)
        self.assertEqual(pa_1.ware_type.ware_brand, "Brand_Coffee")
        self.assertEqual(pa_1.store_status, 0)
        self.assertEqual(pa_1.acquisition_price, 699)
        self.assertEqual(pa_1.acquisiton_user.username, "Acquisitor")
        self.assertEqual(pa_1.__str__(), "Brand_Coffee, Brand_Name_Coffee, Coffee, 1")
        self.assertEqual(pa_1.store_user, None)
        pa_1.store_user = User.objects.get(id=2)
        self.assertEqual(pa_1.store_user.username, "Storer")
        self.assertEqual(pa_1.open_user, None)
        pa_1.open_user = User.objects.get(id=3)
        self.assertEqual(pa_1.open_user.username, "Opener")
        self.assertEqual(pa_1.empty_user, None)
        pa_1.empty_user = User.objects.get(id=4)
        self.assertEqual(pa_1.empty_user.username, "Emptyr")


class Test_4_CoffeeMake(TestCase):

    def setUp(self) -> None:
        # User create
        user_list = [
        ["test@acquisition.com", "Acquisitor", "ABC001", "Ac", "Qu"],
        ["test@store.com", "Storer", "ABC002", "St0", "Re"],
        ["test@open.com", "Opener", "ABC003", "Op", "En"],
        ["test@make.com", "Maker", "ABC004", "Ma", "Ker"],
        ]
        for i in range(4): 
            u_ser = DB_Creator.user_creator(self, user_list[i][0], user_list[i][1], user_list[i][2], user_list[i][3])
            u_ser.save()
        # WareTypes load with Data
        ware_type_list = [ ["Coffee", 7], ["Milk", 50], ["Sugar", 50], ["Flavour", 50] ]
        for ware_type_data in ware_type_list: 
            wt_types = ware_type_data[0]
            wt_wght = ware_type_data[1]
            wt = DB_Creator.ware_type_creator(wt_types, wt_wght)
            wt.save()
        # WareData load with Data
        ware_data_list = [
            ["Brand_Coffee", "Brand_Name_Coffee", 250, 900,],
            ["Brand_Milk", "Brand_Name_Milk", 500, 800,],
            ["Brand_Sugar", "Brand_Name_Sugar", 100, 700,],
            ["Brand_Flavour", "Brand_Name_Flavour", 450, 600,]
            ]
        for i in range(4): 
            wt = WareTypes.objects.get(id=i+1)
            wd = DB_Creator.ware_data_creator(wt, ware_data_list[i][0], ware_data_list[i][1], ware_data_list[i][2], ware_data_list[i][3])
            wd.save()
        # ProductAcquisition load with Data
        price_list = [699, 399, 299, 599]
        for i in range(4): 
            ware_pa = WareData.objects.get(id=i+1)
            u_ser = User.objects.get(id=1)
            pa = DB_Creator.ware_product_creator(ware_pa, price_list[i], u_ser)
            pa.store_user = User.objects.get(id=2)
            pa.open_user = User.objects.get(id=3)
            pa.save()
        
        cm = CoffeeMake.objects.create(
            c_make_ware = ProductAcquisition.objects.get(id=1),
            c_make_dose = 4,
            c_make_user = User.objects.get(id=4),
            c_make_date = datetime(2022, 2, 22, 6, 6, 6, 0)
        )
        cm.save()
    
    def test_coffee_make_count(self):
        self.assertEqual(CoffeeMake.objects.count(), 1)
    
    def test_coffee_make_by_detail(self):
        cm_1 = CoffeeMake.objects.get(id=1)
        self.assertEqual(cm_1.c_make_ware.ware_type.ware_brand, "Brand_Coffee")
        self.assertEqual(cm_1.c_make_dose, 4.0)
        self.assertEqual(cm_1.c_make_user.username, "Maker")
        self.assertEqual(cm_1.c_make_date.__str__(), "2022-02-22 06:06:06")
        self.assertEqual(cm_1.__str__(), "Brand_Coffee, Brand_Name_Coffee, Coffee, 1 / 1")

class Test_5_CoffeeOrder(TestCase):

    def setUp(self) -> None:
        # User create
        user_list = [
        ["test@acquisition.com", "Acquisitor", "ABC001", "Ac", "Qu"],
        ["test@store.com", "Storer", "ABC002", "St0", "Re"],
        ["test@open.com", "Opener", "ABC003", "Op", "En"],
        ["test@make.com", "Maker", "ABC004", "Ma", "Ker"],
        ["test@drink.com", "Drinker", "ABC005", "Dr", "Ink"],
        ]

        for i in range(5): 
            u_ser = DB_Creator.user_creator(self, user_list[i][0], user_list[i][1], user_list[i][2], user_list[i][3])
            u_ser.save()
        # WareTypes load with Data
        ware_type_list = [ ["Coffee", 7], ["Milk", 50], ["Sugar", 50], ["Flavour", 50] ]
        for ware_type_data in ware_type_list: 
            wt_types = ware_type_data[0]
            wt_wght = ware_type_data[1]
            wt = DB_Creator.ware_type_creator(wt_types, wt_wght)
            wt.save()
        # WareData load with Data
        ware_data_list = [
            ["Brand_Coffee", "Brand_Name_Coffee", 250, 900,],
            ["Brand_Sugar", "Brand_Name_Sugar", 100, 700,],
            ["Brand_Milk", "Brand_Name_Milk", 500, 800,],
            ["Brand_Flavour", "Brand_Name_Flavour", 450, 600,]
            ]
        for i in range(4): 
            wt = WareTypes.objects.get(id=i+1)
            wd = DB_Creator.ware_data_creator(wt, ware_data_list[i][0], ware_data_list[i][1], ware_data_list[i][2], ware_data_list[i][3])
            wd.save()
        # ProductAcquisition load with Data
        price_list = [699, 399, 299, 599]
        for i in range(4): 
            ware_pa = WareData.objects.get(id=i+1)
            u_ser = User.objects.get(id=1)
            pa = DB_Creator.ware_product_creator(ware_pa, price_list[i], u_ser)
            pa.store_user = User.objects.get(id=2)
            pa.open_user = User.objects.get(id=3)
            pa.save()
        
        cm = CoffeeMake.objects.create(
            c_make_ware = ProductAcquisition.objects.get(id=1),
            c_make_dose = 4,
            c_make_user = User.objects.get(id=4),
            c_make_date = datetime(2022, 2, 22, 6, 6, 6, 0)
        )
        cm.save()

        co = CoffeeOrder.objects.create(
            coffee_selected = cm,
            coffee_dose = 0.5,
            sugar_choice = ProductAcquisition.objects.get(id=2),
            sugar_dose = 1.0,
            milk_choice = ProductAcquisition.objects.get(id=3),
            milk_dose = 2.0,
            flavour_choice = ProductAcquisition.objects.get(id=4),
            flavour_dose = 1.5,
            coffe_user = User.objects.get(id=5),
        )
        co.save()
               
    def test_coffee_make_count(self):
        self.assertEqual(CoffeeOrder.objects.count(), 1)
    
    def test_coffee_make_by_detail(self):
        co_1 = CoffeeOrder.objects.get(id=1)
        self.assertEqual(co_1.coffee_selected.c_make_ware.ware_type.ware_brand, "Brand_Coffee")
        self.assertEqual(co_1.coffee_dose, 0.5)
        self.assertEqual(co_1.sugar_choice.ware_type.ware_brand, "Brand_Sugar")
        self.assertEqual(co_1.sugar_dose, 1.0)
        self.assertEqual(co_1.milk_choice.ware_type.ware_brand, "Brand_Milk")
        self.assertEqual(co_1.milk_dose, 2.0)
        self.assertEqual(co_1.flavour_choice.ware_type.ware_brand, "Brand_Flavour")
        self.assertEqual(co_1.flavour_dose, 1.5)
        self.assertEqual(co_1.coffe_user.username, "Drinker")
        self.assertLess("2022-02-22 06:06:06", co_1.coffee_reg.__str__())
        self.assertEqual(co_1.__str__(), "1:Brand_Coffee, Brand_Name_Coffee, Coffee, 1 / 1:Drinker")
        self.assertEqual(co_1.c_user().email, "test@drink.com")

class Test_6_Task(TestCase):

    def setUp(self) -> None:
        task = Task.objects.create(
            name = "Carmen",
            age = 28
        )
        task.save()

    def test_user_count(self):
        self.assertEqual(Task.objects.count(), 1)
    
    def test_ware_types_by_detail(self):
        task_1 = Task.objects.get(id=1)
        self.assertEqual(task_1.name, "Carmen")
        self.assertEqual(task_1.age, 28) 
        self.assertEqual(task_1.__str__(), 'Carmen')