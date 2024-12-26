import folium
import osmnx as ox
import networkx as nx

from django.shortcuts import render, redirect


def map_view(request):
    # Получаем данные маршрута из сессии, если они есть
    route_data = request.session.get('route_data', None)
    m = folium.Map(location=[55.7558, 37.6173], zoom_start=15)  # Москва по умолчанию

    if route_data:
        start_coords = route_data['start_point']
        end_coords = route_data['end_point']

        # Создаём дорожный граф
        center_coords = start_coords
        dist = 1500  # Радиус загрузки дорожной сети
        G = ox.graph_from_point(center_coords, dist=dist, network_type='walk')

        # Находим ближайшие узлы для начальной и конечной точек
        orig_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
        dest_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])

        # Построение маршрута
        route_nodes = nx.shortest_path(G, orig_node, dest_node, weight='length')
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route_nodes]

        # Добавляем маршрут на карту
        folium.PolyLine(route_coords, color="blue", weight=5, popup="Маршрут").add_to(m)

        # Добавляем метки начальной и конечной точек
        folium.Marker(location=start_coords, popup="Старт", icon=folium.Icon(color='green')).add_to(m)
        folium.Marker(location=end_coords, popup="Финиш", icon=folium.Icon(color='red')).add_to(m)

    # Генерируем HTML карты
    map_html = m._repr_html_()

    # Рендерим шаблон "home.html" (ранее был map.html)
    return render(request, 'maps/home.html', {'map_html': map_html})


def create_route(request):
    if request.method == 'POST':
        # Получаем начальную и конечную точки маршрута из формы
        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')

        if start_point and end_point:
            # Преобразуем их в кортежи координат (если необходимо)
            try:
                start_coords = tuple(map(float, start_point.split(',')))
                end_coords = tuple(map(float, end_point.split(',')))

                # Сохраняем данные маршрута в сессии
                request.session['route_data'] = {
                    'start_point': start_coords,
                    'end_point': end_coords,
                }

                # Перенаправление на домашнюю страницу или другую страницу
                return redirect('home')
            except ValueError:
                # Если введены некорректные координаты
                return render(request, 'maps/create_route.html', {
                    'error': 'Введите координаты в формате "широта,долгота".'
                })

    # Рендерим шаблон карты с полями ввода
    return render(request, 'maps/create_route.html')


def generate_route(request):
    if request.method == 'POST':
        preferences = request.POST.get('preferences')
        # Логика для обработки предпочтений (можно добавить)
        request.session['preferences'] = preferences
        return redirect('home')  # возвращаемся на главную или куда нужно
    return render(request, 'maps/generate_route.html')


def about(request):
    return render(request, 'maps/about.html')