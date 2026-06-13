from collections import deque
from django.shortcuts import render, get_object_or_404
from .models import Store

def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    stores = Store.objects.all()

    if query:
        stores = stores.filter(name__icontains=query)

    if category:
        stores = stores.filter(category=category)

    floors = {}

    for store in stores:
        if store.floor not in floors:
            floors[store.floor] = []

        floors[store.floor].append(store)

    categories = Store.objects.values_list(
        'category',
        flat=True
    ).distinct()

    return render(
        request,
        'navigation/home.html',
        {
            'floors': floors,
            'query': query,
            'categories': categories,
            'selected_category': category
        }
    )


def store_detail(request, id):
    store = get_object_or_404(Store, id=id)

    return render(
        request,
        'navigation/store_detail.html',
        {'store': store}
    )


def mall_map(request):
    floors = {
        1: ["Zudio", "Reliance Trends"],
        2: ["Starbucks", "Dominos"],
        3: ["Reliance Digital"]
    }

    return render(
        request,
        "navigation/mall_map.html",
        {"floors": floors}
    )
mall_graph = {
    "Entrance": {
        "Escalator": "Go straight"
    },

    "Escalator": {
        "Floor 1": "Take escalator to Floor 1",
        "Floor 2": "Take escalator to Floor 2",
        "Floor 3": "Take escalator to Floor 3"
    },

    "Floor 1": {
        "Zudio": "Turn left"
    },

    "Floor 2": {
        "Starbucks": "Turn left",
        "Dominos": "Turn right"
    },

    "Floor 3": {
        "Reliance Digital": "Go straight"
    }
}
def find_path(graph, start, end):
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            return path

        if node not in visited:
            visited.add(node)

            for neighbour in graph.get(node, {}):
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

    return None


def navigation(request):

    path_result = None
    directions = []

    locations = [
        "Entrance",
        "Zudio",
        "Reliance Trends",
        "Starbucks",
        "Dominos",
        "Reliance Digital"
    ]

    if request.method == "POST":

        start = request.POST.get("start")
        destination = request.POST.get("destination")

        path_result = find_path(
            mall_graph,
            start,
            destination
        )

        if path_result:

            for i in range(len(path_result) - 1):

                current = path_result[i]
                nxt = path_result[i + 1]

                if current in mall_graph and nxt in mall_graph[current]:

                    directions.append(
                        mall_graph[current][nxt] + " → " + nxt
                    )

    return render(
        request,
        "navigation/navigation.html",
        {
            "locations": locations,
            "path_result": path_result,
            "directions": directions
        }
    )