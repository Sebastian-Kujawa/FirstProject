from calendar import month_name
from typing import Union

from django.http import HttpResponse
from django.shortcuts import render


def hello_world(request):
    return render(request, "blog/base.html")


def flatten_list(request):
    """
    Mamy dodać nowy adres url `flatten_list/` po wejściu na który ma się wyświetlić lista bez zagnieżdżeń, oczywiście
    mamy wymyślić program który będzie wypłaszczał nam każdą listę którą podamy, a nie tylko przykład
    """
    list_to_be_flattened = [1, 2, [3, 4, [5], [6, [7]]], 8, [9]]
    flattened_list = _flatten_list(list_to_be_flattened)

    return HttpResponse(f"Spłaszczona lista:  {flattened_list}")


def flatten_list_with_html(request):
    """
    Mamy dodać nowy adres url `flatten_list/` po wejściu na który ma się wyświetlić lista bez zagnieżdżeń, oczywiście
    mamy wymyślić program który będzie wypłaszczał nam każdą listę którą podamy, a nie tylko przykład
    """
    list_to_be_flattened = [1, 2, [3, 4, [5], [6, [7]]], 8, [9]]
    flattened_list = _flatten_list(list_to_be_flattened)

    return HttpResponse(f"<html><body><h1>{flattened_list}</h1><body></html>")


def _flatten_list(list_to_be_flattened: list[Union[list, int]]) -> list[int]:
    flattened_list = []
    for element in list_to_be_flattened:
        if not isinstance(element, list):
            flattened_list.append(element)
        else:
            flattened_list.extend(_flatten_list(element))

    return flattened_list


def my_next_view_with_context(request):
    my_context = {
        "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "enabled": True,
    }

    return render(request, "first_app/template_with_context.html", context=my_context)


def iterate_over_months(request):
    """
    Co chcemy zmienić w tym widoku? Chcielibyśmy, aby wyświetlały się tylko miesiące parzyste, czyli luty, kwiecień itd.
    Jak to zrobić? Musimy dodać dodatkowy kontekst który pozwoli nam w templatce użyć ifa który będzie powodował, że wyświetli
    się nazwa miesiąca, albo `---`
    """
    months = list(month_name)
    months_with_enabler = [
        {"enabled": idx % 2 == 0, "month": month}
        for idx, month in enumerate(months)
        if month
    ]
    ctx = {"months": months_with_enabler}

    return render(request, "first_app/months.html", context=ctx)
