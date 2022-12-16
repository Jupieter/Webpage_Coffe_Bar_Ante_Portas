from django.test import TestCase
from datetime import timezone, datetime
from raw_material.models import WareTypes, WareData, ProductAcquisition
from accounts.models import User


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

    def test_ware_types_by_id(self):
        wt = WareTypes.objects.get(id=1)
        self.assertEqual(wt.ware_types, "Something")
        self.assertEqual(wt.ware_wght, 77)     


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
    
    def test_ware_data_by_id(self):
        self.assertEqual(WareData.objects.get(id=1).ware_brand, "Brand_1")
        self.assertEqual(WareData.objects.get(id=1).ware_brand_name, "Brand_Name_1")
        self.assertEqual(WareData.objects.get(id=1).ware_weight, 99)
        self.assertEqual(WareData.objects.get(id=1).ware_price, 9)

class Test_3_ProductAcquisition(TestCase):

    def setUp(self) -> None:

        # User create
        # u_ser = User.objects.create_user(self, "test@admin.com", "ABC123", "Tester", "John", "Doe")
        # u_ser.save()

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
        
        pa = DB_Creator.ware_product_creator(self, WareData.objects.get(id=1), 699)
        pa.save()

        
    def test_product_aquisition_count(self):
        # print(ProductAcquisition.objects.all())
        self.assertEqual(ProductAcquisition.objects.count(), 1)


#   
#       def test_ware_data_count(self):
#           # print(self.ware_data2)
#           # print(WareData.objects.all())
#           self.assertEqual(WareData.objects.count(), 4)
#       
#       def test_ware_data_by_id(self):
#           coffee_ware = WareData.objects.filter(id=1)[0]
#           milk_ware = WareData.objects.filter(id=2)[0]
#           sugar_ware = WareData.objects.filter(id=3)[0]
#           flavour_ware = WareData.objects.filter(id=4)[0]
#           self.assertEqual(coffee_ware.ware_brand_name, "Brand_Name_1_coffee")
#           self.assertEqual(milk_ware.ware_brand_name, "Brand_Name_2_milk")
#           self.assertEqual(sugar_ware.ware_brand_name, "Brand_Name_3_sugar")
#           self.assertEqual(flavour_ware.ware_brand_name, "Brand_Name_4_flavour")
#   