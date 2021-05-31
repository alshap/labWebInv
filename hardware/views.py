from django.shortcuts import render
from django.views import generic

from .models import Hardware, Category, TakenHardware
from django.contrib.auth.models import User

from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect

from django.http import HttpResponseRedirect, HttpResponse

class IndexView(generic.ListView):
    template_name = 'hardware/index.html'
    context_object_name = 'hardware_categories'
    
    def get_queryset(self):
        return Category.objects.all()
    
class DevicesView(generic.DetailView):
    model = Category
    template_name = 'hardware/category-details.html'
    
class HardwareRequestView(generic.DetailView):
    model = Hardware
    template_name = 'hardware/hardware-request.html'

def take(request, hardware_id):
    hw = get_object_or_404(Hardware, pk=hardware_id)
    try:
        taker_value = request.POST['username']
        current_user = User.objects.get(username = taker_value)
    except (KeyError, User.DoesNotExist):
        return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': 'Taker field is empty or user does not exist',
            }
            )
    try:
        amount = request.POST['quantity']
        if int(amount) < 1:
            return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': 'Quantity should be positive number',
            }
            )
        elif int(amount) > int(hw.hardwareamount.quantity):
            return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': 'Typed quantity is more than available',
            }
            )
            
    except (KeyError, ValueError):
        return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': 'You did not choose quantity',
            }
            )
    else:
        
        desc = request.POST['desc']
        if desc == '':
            new_take = TakenHardware(taker = current_user, hardware = hw, quantity = amount)
        else:
            new_take = TakenHardware(taker = current_user, hardware = hw, quantity = amount, description = desc)
        new_take.save()
        return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'modal_available': 'Yes',
            'taken_amount': int(amount),
            }
            )


#       