from django.shortcuts import render
from django.views import generic

from .models import Hardware, Category, TakenHardware, Room, HardwareAmount
from .forms import SearchForm
from django.contrib.auth.models import User


from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect

from django.http import HttpResponseRedirect, HttpResponse

from datetime import datetime

class IndexView(generic.ListView):    
    template_name = 'hardware/index.html'
 
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        categories = Category.objects.all()
        scope_room = 'All'
        hardware_categories_amounts = []
        if 'scope' in request.GET:
            if request.GET['scope'] == 'All':
                pass
            else:
                scope_room = request.GET['scope']
                categories = [cat for cat in categories if cat.bool_hardwares_inroom(room = Room.objects.get(name = scope_room))]
        else:
            pass
        if scope_room != 'All':
            for cat in categories:
                hardware_categories_amounts.append({'category':cat,
                                                    'hardwares_amount': cat.hardwares_amount_inroom(room = Room.objects.get(name = scope_room)),
                                                    'hardwares_available_amount': cat.hardwares_available_amount_inroom(room = Room.objects.get(name = scope_room)),
                                                    'hardwares_empty_amount': cat.hardwares_empty_amount_inroom(room = Room.objects.get(name = scope_room))})
        else:
            for cat in categories:
                hardware_categories_amounts.append({'category':cat,
                                                    'hardwares_amount': cat.hardwares_totalamount_values(),
                                                    'hardwares_available_amount': cat.hardwares_amount_values(),
                                                    'hardwares_empty_amount': cat.hardwares_totalamount_values() - cat.hardwares_amount_values()})

        

        if not request.session.get('obj_view'):
            request.session['obj_view'] = 0
        return render(request, self.template_name,
                    {'hardware_categories':hardware_categories_amounts,
                    'obj_view':request.session['obj_view'],
                    'rooms':rooms,
                    'scope_room':scope_room})


def set_obj_view(request, view_value, *args):
    try:
        request.session['obj_view'] = int(view_value)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    except Exception as e:
        return HttpResponse(e)
        
    
class DevicesView(generic.DetailView):
    template_name = 'hardware/category-details.html'
    
    def get(self, request, pk):
        rooms = Room.objects.all()
        scope_room = 'All'
        category = Category.objects.get(pk=pk)
        hardwares_n_amounts = []
        if 'scope' in request.GET:
            if request.GET['scope'] == 'All':
                pass
            else:
                #with scope
                scope_room = request.GET['scope']
        
        if scope_room == 'All':
            for hw in category.hardware_set.all():
                hardwares_n_amounts.append({'hardware': hw,
                                            'amount_available':hw.get_amount_values(),
                                            'totalquantity':hw.get_totalamount_values(),
                                            'amount_empty': hw.get_totalamount_values() - hw.get_amount_values()})
        else:
            for hw in category.hardware_set.all():
                available = hw.get_amount_inroom(room = Room.objects.get(name = scope_room))
                total = hw.get_totalamount_inroom(room = Room.objects.get(name = scope_room))
                empty = total - available
                if total > 0:
                    hardwares_n_amounts.append({'hardware': hw,
                                                'amount_available':available,
                                                'totalquantity':total,
                                                'amount_empty': empty})
        

        if not request.session.get('obj_view'):
            request.session['obj_view'] = 0
        return render(request, self.template_name,
                     {'category_hardwares': hardwares_n_amounts,
                     'category': category,
                      'obj_view':request.session['obj_view'],
                      'rooms':rooms,
                      'scope_room':scope_room})


class HardwareRequestView(generic.DetailView):
    """
    Hardware request view. User orders hardware.
    """
    model = Hardware
    template_name = 'hardware/hardware-request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['rooms'] = Room.objects.all()
        return context

def take(request, hardware_id):
    """
    Hardware POST request.
    On success creates new object **TakenHardware**.
    To success the function all form fields should be filled correctly.
    On error appears **error_message** with redirecting to the same page.
    
    :param hardware_id: choosen hardware id
    :type hardware_id: int
    
    :return: On success creates new TakenHardware object and redirects to the same page with modal window
    :rtype: HttpResponse
    """
    hw = get_object_or_404(Hardware, pk=hardware_id)
    try:
        current_user = request.user
    except (KeyError, User.DoesNotExist):
        return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': 'Taker field is empty or user does not exist',
            'rooms': Room.objects.all()
            }
            )
    try:
        room = request.POST['room']
        if room:
            pass
        else:
            return render(request, 'hardware/hardware-request.html', {
                'hardware': hw,
                'error_message': 'Choose a valid room',
                'rooms': Room.objects.all()
                }
                )
    except (KeyError, ValueError) as e:
        return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': 'Provide valid room',
            'rooms': Room.objects.all()
            }
            )
    try:
        amount = request.POST['quantity']
        hw_amount = hw.hardwareamount_set.get(room = Room.objects.get(designation = room))
        if int(amount) < 1:
            return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': 'Quantity should be positive number',
            'rooms': Room.objects.all()
            }
            )
        elif int(amount) > int(hw_amount.quantity):
            return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': 'Typed quantity is more than available in selected room',
            'rooms': Room.objects.all()
            }
            )
            
    except (KeyError, ValueError, HardwareAmount.DoesNotExist):
        return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': 'You did not choose quantity or hardware is not presented in the selected room',
            'rooms': Room.objects.all()
            }
            )
    
    try:
        return_date = datetime.strptime(request.POST['returndate'], '%Y-%m-%d').date()
        if return_date > datetime.date(datetime.now()):
            pass
        else:
            return render(request, 'hardware/hardware-request.html', {
                'hardware': hw,
                'error_message': 'Date must be greater than today',
                'rooms': Room.objects.all()
                }
                )
    except (KeyError, ValueError) as e:
        return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': e,
            'rooms': Room.objects.all()
            }
            )
    else:
        desc = request.POST['desc']
        if desc == '':
            new_take = TakenHardware(taker = current_user, hardware = hw, quantity = amount, date_to = return_date, room = Room.objects.get(designation = room))
        else:
            new_take = TakenHardware(taker = current_user, hardware = hw, quantity = amount, description = desc, date_to = return_date, room = Room.objects.get(designation = room))
        new_take.save()
        return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'modal_available': 'Yes',
            'taken_amount': int(amount),
            }
            )

def hardware_search(request):
    """
        Hardware GET search request.
        On form valid redirects to the search template with success found hardware
        
        :param request: GET parameter holder
        
        :return: rendered search template
        :rtype: HttpResponse
    """
    hardwares = []
    msg = ''
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search_query']
            room = form.cleaned_data['room_choice']
            if room == 'All':
                hardwares = Hardware.objects.filter(name__icontains=query)
            else:
                amounts = HardwareAmount.objects.filter(room = Room.objects.get(designation = room))
                hardwares = [x.hardware for x in amounts if x not in hardwares and query in x.hardware.name]
            if len(hardwares) == 0:
                msg = 'Nothing found'
            else:
                msg = "Found %s items" % (len(hardwares))
            """Filtering query"""
    else:
        msg = 'Search provides with error!'
        form = SearchForm()
    return render(request, 'hardware/search.html',{'hardwares': hardwares, 
                                                    'msg': msg, 
                                                    'rooms': Room.objects.all()})
    
    
    