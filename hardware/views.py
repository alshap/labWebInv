from django.shortcuts import render
from django.views import generic

from .models import Hardware, Category, TakenHardware
from .forms import SearchForm
from django.contrib.auth.models import User

from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect

from django.http import HttpResponseRedirect, HttpResponse

from datetime import datetime

class IndexView(generic.ListView):
    """Index view with all categories set specified with card or list view"""
      
    template_name = 'hardware/index.html'
    """Index page template"""  
    
    def get_queryset(self):
        """
        Get all Category objects
        
        :parameter self: self class
        :return: All categories objects
        :rtype: Objects List
        """
        return Category.objects.all()
    
    def get(self, request, *args, **kwargs):
        """
        Get renderred view
        
        View is defined by session variable **obj_view**.
        If variable is 0 then user get renderred page view cardview either listview.
        
        :return: Renderred Index view based on obj_view session value(obj_view = 0 if not defined)
        :rtype: HttpResponse
        """
        if request.session.get('obj_view'):
            return render(request, self.template_name,
                     {'hardware_categories':self.get_queryset(),
                      'obj_view':request.session['obj_view']})
        return render(request, self.template_name,
                     {'hardware_categories':self.get_queryset(),
                      'obj_view':0})

def set_obj_view(request, view_value):
    """
    Set the obj_view session variable by select choice and then redirect to renderred page.
    
    :param view_value: Value got from select choice(should be 0 or 1)
    :type view_value: int
    
    :return: Renderred view with obj_view parameter
    :rtype: HttpResponse
    """
    try:
        request.session['obj_view'] = int(view_value)
        return render(request, IndexView.template_name,
                     {'hardware_categories':IndexView.get_queryset(IndexView),
                      'obj_view':request.session['obj_view']})
    except Exception as e:
        return HttpResponse(e)
        
    
class DevicesView(generic.DetailView):
    """
    Detailed devices view sorted by category
    """
    template_name = 'hardware/category-details.html'
    
    def get(self, request, pk):
        """
        Render template using choosen category
        
        :param pk: category id
        :type pk: int
        
        :return: Renderred view with category id value
        :rtyle: HttpResponse
        """
        if request.session.get('obj_view'):
            return render(request, self.template_name,
                     {'category': Category.objects.get(pk=pk),
                      'obj_view':request.session['obj_view']})
        return render(request, self.template_name,
                     {'category': Category.objects.get(pk=pk),
                      'obj_view':0})

    
class HardwareRequestView(generic.DetailView):
    """
    Hardware request view. User orders hardware.
    """
    model = Hardware
    template_name = 'hardware/hardware-request.html'

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
    
    try:
        return_date = datetime.strptime(request.POST['returndate'], '%Y-%m-%d').date()
        if return_date > datetime.date(datetime.now()):
            pass
        else:
            return render(request, 'hardware/hardware-request.html', {
                'hardware': hw,
                'error_message': 'Date must be greater than today',
                }
                )
    except (KeyError, ValueError) as e:
        return render(request, 'hardware/hardware-request.html', {
            'hardware': hw,
            'error_message': e,
            }
            )
    else:
        desc = request.POST['desc']
        if desc == '':
            new_take = TakenHardware(taker = current_user, hardware = hw, quantity = amount, date_to = return_date)
        else:
            new_take = TakenHardware(taker = current_user, hardware = hw, quantity = amount, description = desc, date_to = return_date)
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
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search_query']
            hardwares = Hardware.objects.filter(name__icontains=query)
            """Filtering query"""
    else:
        form = SearchForm()
    return render(request, 'hardware/search.html',{'hardwares': hardwares})
    
    
    