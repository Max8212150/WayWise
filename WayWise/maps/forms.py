from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(
        label='Поиск мест',
        max_length=100
    )


class RouteForm(forms.Form):
    start_coords = forms.CharField(
        label='Начальные координаты (широта, долгота)',
        widget=forms.TextInput(attrs={'placeholder': '55.7558,37.6173'}),
        required=True
    )
    poi_coords = forms.CharField(
        label='Координаты промежуточных точек (каждая с новой строки)',
        widget=forms.Textarea(attrs={'placeholder': '55.7580,37.6155\n55.7597,37.6184'}),
        required=False
    )
    end_coords = forms.CharField(
        label='Конечные координаты (широта, долгота)',
        widget=forms.TextInput(attrs={'placeholder': '55.7614,37.6200'}),
        required=True
    )
