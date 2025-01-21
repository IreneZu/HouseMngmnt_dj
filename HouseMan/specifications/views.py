from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .models import Building, ExpenseItem, Expenses
from .forms import BuildExpFormSet


def platform(request):
    title = 'Main'
    header = 'Управляющая организация ООО "Ромашка"'
    cont = 'По всем вопросам просьба обращаться по адресу г. Москва, 3-я ул.Строителей, д.1'
    #    page_number = request.GET.get('page')
    context = {
        'title': title,
        'header': header,
        'cont': cont
    }
    return render(request, 'main.html', context)


#class building_view(TemplateView):
class building_view(ListView):

    template_name = 'buildings.html'
    model = Building
    title = 'Buildings'
    header = 'Многоквартирные дома в управлении ООО "Ромашка"'
    paginate_by = 9

    buildings = Building.objects.values()
    for item in buildings:
        item['adr_for_map'] = item['title'].replace(' ', '+') + ',+Moscow'

    context_object_name = 'buildings'
    extra_context = {
        'title': title,
        'header': header,
#        'buildings': buildings,
    }


def building_spec(request, building_id):
    building = Building.objects.get(id=building_id)
    header = f"Характеристики МКД :  {building.title}"

    context = {
        'title': 'specification',
        'header': header,
        'building': building,
    }
    return render(request, 'building_spec.html', context)


def items_list(build_id):
    items = ExpenseItem.objects.order_by('sort_num').values()

    initial = []

    for item in items:
        building_exp = Expenses.objects.filter(building_id=build_id, item_id=item['id']).values()
        if building_exp.count() == 1:
            init_values = dict(building_exp[0])
            init_values['item'] = item['title']
            initial.append(init_values)
        else:
            initial.append({'building_id': build_id, 'item': item['title']})

    return initial


def building_exp_view(request, building_id):
    context = {}
    list_init = items_list(building_id)
    formset = BuildExpFormSet(request.POST or None, initial=list_init)  #Expenses.objects.all().values() )

    summa = 0
    if Expenses.objects.filter(building_id=building_id).count() > 0:
        summa = float(list(Expenses.objects.filter(building_id=building_id).aggregate(Sum('summ')).values())[0])
    context['expenses'] = list_init
    context['building_id'] = building_id

    context['header'] = "Плановые расходы на 2025 г.:  " + Building.objects.get(id=building_id).title
    context['summa'] = f'Всего расходов по дому:  {summa} руб.'

    return render(request, 'exps_view.html', context)


def building_exp_edit(request, building_id):
    context = {}
    list_init = items_list(building_id)
    formset = BuildExpFormSet(request.POST or None, initial=list_init)  #Expenses.objects.all().values() )

    if request.method == 'POST':

        if formset.is_valid():
            for f in formset:

                cd = f.cleaned_data
                building = building_id
                item = cd.get('item')
                type = cd.get('type')
                summ = cd.get('summ')

                building_exp = Expenses.objects.filter(building_id=building_id, item=item)
                if building_exp.count() == 0:
                    building_exp = Expenses(building_id=building, item=item, type=type, summ=summ)

                else:
                    try:
                        building_exp = Expenses.objects.get(building_id=building_id, item=item)
                    except ObjectDoesNotExist:
                        print("Объект не существует")
                    except MultipleObjectsReturned:
                        print(f"Найдено более одного объекта: building_id={building_id}, item={str(item)}")
                        building_exp = list(Expenses.objects.filter(building_id=building_id, item=item))[0]

                    building_exp.type = type
                    building_exp.summ = summ

                building_exp.save()

    #           return HttpResponseRedirect(reverse('buildings'))
    summa = 0
    if Expenses.objects.filter(building_id=building_id).count() > 0:
        summa = float(list(Expenses.objects.filter(building_id=building_id).aggregate(Sum('summ')).values())[0])
    context['formset'] = formset

    context['header'] = "Плановые расходы на 2025 г.:  " + Building.objects.get(id=building_id).title
    context['summa'] = f'Всего расходов по дому:  {summa} руб.'

    return render(request, 'exps.html', context)


class items_view(ListView):
    template_name = 'items.html'
    paginate_by = 5
    model = ExpenseItem
    context_object_name = 'items'
    extra_context = {
        'header': 'Статьи затрат на содержание и текущий ремонт МКД',
    }

import datetime

def test():
   t1 = datetime.datetime.now()
   q = Expenses.objects.all()
   tsum = 0
   for i in range(1, 501):
       u = q.get(id = i + 1)
       tsum += u.summ
   t2 = datetime.datetime.now()
   print(f'tsum = {tsum}')
   print("get object by key: django req/seq:",500/(t2-t1).total_seconds(),'req time (ms):',(t2-t1).total_seconds()*1000/500)

test()
# get object by key: django req/seq: 2402.887309390964 req time (ms): 0.416166
#                                   2358.30145695864 req time (ms): 0.424034
