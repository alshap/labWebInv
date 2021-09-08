from django import forms

class SearchForm(forms.Form):
    """Search form to control search query correctness."""
    search_query = forms.CharField(label='Search',max_length=100)
    room_choice = forms.CharField(max_length=100)