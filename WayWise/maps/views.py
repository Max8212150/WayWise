import folium
import osmnx as ox
import networkx as nx

from django.http import HttpResponseRedirect
from django.shortcuts import render


from .forms import RouteForm, SearchForm  # Форма для динамического маршрута


def map_view(request):
    # Обработка формы
    form = RouteForm(request.POST or None)
    map_html = None  # Изначально карта пустая

    if request.method == "POST" and form.is_valid():
        # Получение координат из формы
        start_coords = tuple(map(float, form.cleaned_data['start_coords'].split(',')))
        poi_coords = [
            tuple(map(float, coord.split(',')))
            for coord in form.cleaned_data['poi_coords'].splitlines()
        ]
        end_coords = tuple(map(float, form.cleaned_data['end_coords'].split(',')))

        # Создание дорожного графа
        center_coords = start_coords
        dist = 1500  # Радиус загрузки дорожной сети
        G = ox.graph_from_point(center_coords, dist=dist, network_type='walk')

        # Находим ближайшие узлы для начальной, промежуточных и конечной точек
        orig_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
        poi_nodes = [ox.distance.nearest_nodes(G, lon, lat) for lat, lon in poi_coords]
        dest_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])

        # Построение маршрута через точки
        route_nodes = [orig_node] + poi_nodes + [dest_node]
        full_route = []
        for i in range(len(route_nodes) - 1):
            segment = nx.shortest_path(G, route_nodes[i], route_nodes[i + 1], weight='length')
            if i == 0:
                full_route.extend(segment)
            else:
                full_route.extend(segment[1:])

        # Получение координат узлов маршрута
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in full_route]

        # Создаём карту Folium
        m = folium.Map(location=start_coords, zoom_start=15)

        # Добавляем маршрут
        folium.PolyLine(route_coords, color="blue", weight=5, popup="Маршрут").add_to(m)

        # Добавляем метки
        folium.Marker(location=start_coords, popup="Старт", icon=folium.Icon(color='green')).add_to(m)
        for (lat, lon) in poi_coords:
            folium.Marker(location=(lat, lon), popup="Точка посещения", icon=folium.Icon(color='orange', icon='info-sign')).add_to(m)
        folium.Marker(location=end_coords, popup="Финиш", icon=folium.Icon(color='red')).add_to(m)

        # Добавляем базовые слои
        folium.TileLayer(name='Схема').add_to(m)
        folium.TileLayer(
            tiles='http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Спутник'
        ).add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)

        # Генерируем HTML карты
        map_html = m._repr_html_()
    else:
        # Если форма ещё не отправлена, показываем пустую карту
        m = folium.Map(location=[55.7558, 37.6173], zoom_start=15)  # Москва
        map_html = m._repr_html_()

    # Передаём карту и форму в шаблон
    return render(request, 'maps/map.html', {'map_html': map_html, 'form': form})


def search_places(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['search_query']
            # Логика поиска мест с использованием OSMnx
            # Здесь следует добавить код, который будет выполнять поиск
            # Например, поиск через OSMnx или внешние API
            # Для примера будем просто перенаправлять на карту
    return HttpResponseRedirect('/')
