from raw_material.models import ProductAcquisition

def coffee_order_data():
    wares = ProductAcquisition.objects.filter(store_status=3)
    sugar = []; milk = []; flavour = []
    for ware in wares:
        if ware.ware_type.ware_type.id == 2:
            dt1 = ware.id
            dt2 = ware
            dt = (dt1,dt2)
            sugar.append(dt)
        elif ware.ware_type.ware_type.id == 3: 
            dt1 = ware.id
            dt2 = ware
            dt = (dt1,dt2)
            milk.append(dt)
        elif ware.ware_type.ware_type.id == 4: 
            dt1 = ware.id
            dt2 = ware
            dt = (dt1,dt2)
            flavour.append(dt)
    return sugar, milk, flavour

if __name__ == '__main__':
    print('START MAIN')
    coffee_order_data()