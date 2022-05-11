from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone
from .models import WareTypes, WareData, ProductIngredient, ProductAcquisition
from .forms import WareDataForm, AquisitionForm
from django.shortcuts import redirect

def ware_choice(request):
    ware_type_list = WareTypes.objects.all().order_by('ware_types')
    wares = WareData.objects.all().order_by('ware_type').order_by('ware_brand')
    return render (request, 'raw_material/ware_choice.html', {'wares': wares, 'ware_type_list':ware_type_list})

def ware_list(request, pk):
    ware_type_list = get_object_or_404(WareTypes, pk=pk)
    sub_site_logo = "src=static/image/coffe_bean_draw.jfif"
    wares = WareData.objects.filter(ware_type=ware_type_list)
    return render (request, 'raw_material/ware_list.html', {'wares': wares, 'ware_type_list':ware_type_list, 'sub_site_logo':sub_site_logo})


def ware_new(request):      
    if request.method == "POST":
        form = WareDataForm(request.POST)
        if form.is_valid():
            ware = form.save(commit=False)
            ware.pub_date = timezone.now()
            ware.save()
            return redirect('raw_material:ware_list')
    else:
        form = WareDataForm()
    return render(request, 'raw_material/ware_edit.html', {'form': form})


def ware_remove(request, pk):
    ware = get_object_or_404(WareData, pk=pk)
    ware.delete()
    return redirect('raw_material:ware_list')


def ware_edit(request, pk):
    ware = get_object_or_404(WareData, pk=pk)
    if request.method == "POST":
        form = WareDataForm(request.POST, instance=ware)
        if form.is_valid():
            ware = form.save(commit=False)
            ware.pub_date = timezone.now()
            ware.save()
            return redirect('raw_material:ware_list')
    else:
        form = WareDataForm(instance=ware)
    return render(request, 'raw_material/ware_edit.html', {'form': form})


def acquisition_new(request):
    user = request.user
    
    form = AquisitionForm(request.POST)
    
    return render(request, 'raw_material/acquisition_new.html', {'form': form})
