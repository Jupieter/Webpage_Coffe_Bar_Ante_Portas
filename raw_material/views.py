# from asyncio.windows_events import NULL
from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone
from .models import WareTypes, WareData, ProductAcquisition
from .forms import WareDataForm, AquisitionForm, AquisitionStockedForm, WareListChoice


def ware_choice(request):
    ware_type_list = WareTypes.objects.all().order_by('ware_types')    
    return render (request, 'raw_material/ware_choice.html', {'ware_type_list':ware_type_list})

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
            return redirect('raw_material:ware_choice')
    else:
        form = WareDataForm()
    return render(request, 'raw_material/ware_edit.html', {'form': form})


def ware_remove(request, pk, pkey):
    ware = get_object_or_404(WareData, pk=pkey)
    ware.delete()
    return redirect('raw_material:ware_list', pk=pk)


def ware_edit(request, pk, pkey):
    ware = get_object_or_404(WareData, pk=pkey)
    if request.method == "POST":
        form = WareDataForm(request.POST, instance=ware)
        if form.is_valid():
            ware = form.save(commit=False)
            ware.pub_date = timezone.now()
            ware.save()
            return redirect('raw_material:ware_list', pk=pk)
    else:
        form = WareDataForm(instance=ware)
    return render(request, 'raw_material/ware_edit.html', {'form': form})


def acquisition_new(request, pk, pkey):
    ware = get_object_or_404(WareData, pk=pkey) 
    acquisiton_user = request.user
    now = timezone.now()
    if request.method == "POST":
        form = AquisitionForm(request.POST)
        # form.ware_type= ware.ware_brand_name 
        # form.acquisition_price= ware.ware_price
        if form.is_valid():
            acquisition_new = form.save(commit=False)
            acquisition_new.ware_type = ware
            acquisition_new.acquisition_date = timezone.now()
            acquisition_new.stock = ware.ware_weight
            acquisition_new.store_status = 1
            acquisition_new.save()
            return redirect('raw_material:ware_list', pk=pk)
    else:
        form = AquisitionForm(initial=
            {'acquisition_price':ware.ware_price,
            'acquisiton_user':acquisiton_user,
            'acquisition_date':now,
            }) 
  
    return render(request, 'raw_material/acquisition_new.html', {'form': form, 'ware':ware, 'now':now})


def acquisition_list(request):
    ware_type_list = WareTypes.objects.all().order_by('ware_types')
    wares = ProductAcquisition.objects.all().order_by('store_status').order_by('ware_type').order_by('acquisition_date')
    if request.method == "POST":
        form = WareListChoice(request.POST)
        if form.is_valid():
            acq = request.POST.get('store_status', 0)
            if acq == "0":
                wares = ProductAcquisition.objects.all()
            else:
                wares = ProductAcquisition.objects.filter(store_status=acq)
        wares.order_by('store_status').order_by('ware_type').order_by('acquisition_date')
        return render (request, 'raw_material/acquisition_list.html', 
            {'form': form, 'acq':acq, 'wares':wares, 'ware_type_list':ware_type_list,})
    else:
        form = WareListChoice()

    return render (request, 'raw_material/acquisition_list.html', {'form': form,'wares': wares, 'ware_type_list':ware_type_list})


def acquisition_remove(request, pkey):
    ware = get_object_or_404(ProductAcquisition, pk=pkey)
    ware.delete()
    return redirect('raw_material:acquisition_list')

def acquisition_edit(request, pkey):
    ware = get_object_or_404(ProductAcquisition, pk=pkey)
    if request.method == "POST":
        form = AquisitionForm(request.POST, instance=ware)
        if form.is_valid():
            acquisition_edit = form.save(commit=False)
            acquisition_edit.acquisition_date = timezone.now()
            acquisition_edit.save()
            return redirect('raw_material:acquisition_list')
    else:
        form = AquisitionForm(instance=ware) 
  
    return render(request, 'raw_material/acquisition_new.html', {'form': form, 'ware':ware})

def acquisition_storing(request, pkey):
    ware = get_object_or_404(ProductAcquisition, pk=pkey)
    user = request.user
    if ware.store_status == 1:
        ware.store_date = timezone.now()
        ware.store_user = user
        ware.store_status = 2
        ware.save()
    return redirect('raw_material:acquisition_list')
  

def box_open(request, pkey):
    ware = get_object_or_404(ProductAcquisition, pk=pkey)
    user = request.user
    if ware.store_status == 2:
        ware.open_date = timezone.now()
        ware.open_user = user
        ware.store_status = 3
        ware.save()
    return redirect('raw_material:acquisition_list')

def box_empty(request, pkey):
    ware = get_object_or_404(ProductAcquisition, pk=pkey)
    user = request.user
    if ware.store_status == 3:
        ware.empty_date = timezone.now()
        ware.empty_user = user
        ware.store_status = 4
        ware.save()
    return redirect('raw_material:acquisition_list')
