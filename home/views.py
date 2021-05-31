from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.conf import settings

class IndexView(generic.ListView):
    template_name = 'home/index.html'
    context_object_name = 'hardware_categories'
    
    def get_queryset(self):
        return None
    
def change_language(request):
    response = HttpResponseRedirect('')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = '/'+language
            elif language == settings.LANGUAGE_CODE:
                redirect_path = ''
            else:
                return response
            from django.utils import translation
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response


