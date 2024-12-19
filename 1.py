# import osmnx as ox
# import networkx as nx
# import folium

# # Настройка OSMnx (по необходимости)
# ox.settings.log_console = False
# ox.settings.use_cache = True

# # Зададим небольшую область в Москве
# center_point = (55.753930, 37.620795)
# dist = 1500
# G = ox.graph_from_point(center_point, dist=dist, network_type='walk')

# Координаты
# start_coords = (55.7558, 37.6173)  # Красная площадь
# poi_coords = [
#     (55.7580, 37.6155, "Исторический музей"),
#     (55.7597, 37.6184, "ГУМ")
# ]
# end_coords = (55.7614, 37.6200)  # Большой театр

# # Ближайшие узлы
# orig_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
# poi_nodes = [ox.distance.nearest_nodes(G, lon, lat) for (lat, lon, name) in poi_coords]
# dest_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])

# # Формируем маршрут
# route_nodes = [orig_node] + poi_nodes + [dest_node]
# full_route = []
# for i in range(len(route_nodes)-1):
#     segment = nx.shortest_path(G, route_nodes[i], route_nodes[i+1], weight='length')
#     if i == 0:
#         full_route.extend(segment)
#     else:
#         full_route.extend(segment[1:])

# # Получаем координаты всех узлов на маршруте для отрисовки
# route_latlng = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in full_route]

# # Создаём интерактивную карту Folium
# # Можно использовать разные tiles, например:
# # tiles="Stamen Terrain", "Stamen Toner", "OpenStreetMap"
# # Для спутника (без ключа Mapbox) можно попробовать: tiles="Stamen Terrain" (не спутник, но другой стиль)
# # По-настоящему спутниковый слой обычно требует ключ (например, tiles="http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr='Esri', name='Esri Satellite', overlay=False, control=True)

# m = folium.Map(
#     location=start_coords,
#     zoom_start=15,
#     tiles='http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#     attr='Esri',
#     name='Esri Satellite',
#     overlay=False,
#     control=True
# )

# # Добавляем на карту маршрут
# folium.PolyLine(route_latlng, color="blue", weight=5).add_to(m)

# # Добавляем маркеры
# folium.Marker(location=start_coords, popup="Старт", icon=folium.Icon(color='green')).add_to(m)
# for (lat, lon, name) in poi_coords:
#     folium.Marker(location=(lat, lon), popup=name, icon=folium.Icon(color='orange', icon='info-sign')).add_to(m)
# folium.Marker(location=end_coords, popup="Финиш", icon=folium.Icon(color='red')).add_to(m)

# # Сохраняем и открываем карту в браузере
# m.save("interactive_route.html")
# print("Карта сохранена в interactive_route.html. Откройте этот файл в браузере.")
