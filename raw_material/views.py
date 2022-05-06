from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone
from .models import WareData, ProductIngredient
from .forms import WareDataForm
from django.shortcuts import redirect

def ware_list(request):
    ware_type_list = WareData.ware_type_choices
    i = 0
    wares_type_list = []
    wares_name_list = []
    while i < len(ware_type_list):
        p = ware_type_list[i]
        pkey= p[0]
        pname= p[1]
        wares_type_list.append(pkey)
        wares_name_list.append(pname)
        i = i + 1
    
    
    wares = WareData.objects.all().order_by('ware_type')
    return render(request, 'raw_material/ware_list.html', {'wares': wares, 'wares_type_list':wares_type_list,'wares_name_list':wares_name_list})
    # milks = WareData.objects.filter(ware_type='milks').order_by('ware_brand')
    # coffees = WareData.objects.filter(ware_type='coffe').order_by('ware_brand')
    # return render(request, 'raw_material/ware_list.html', {'milks': milks, 'coffees':coffees})

def ware_new(request):      
    if request.method == "POST":
        form = WareDataForm(request.POST)
        if form.is_valid():
            ware = form.save(commit=False)
            ware.pub_date = timezone.now()
            ware.save()
            return redirect('ware_list')
    else:
        form = WareDataForm()
    return render(request, 'raw_material/ware_edit.html', {'form': form})

def ware_remove(request, pk):
    ware = get_object_or_404(WareData, pk=pk)
    ware.delete()
    return redirect('ware_list')

def ware_edit(request, pk):
    ware = get_object_or_404(WareData, pk=pk)
    if request.method == "POST":
        form = WareDataForm(request.POST, instance=ware)
        if form.is_valid():
            ware = form.save(commit=False)
            ware.pub_date = timezone.now()
            ware.save()
            return redirect('ware_list')
    else:
        form = WareDataForm(instance=ware)
    return render(request, 'raw_material/ware_edit.html', {'form': form})