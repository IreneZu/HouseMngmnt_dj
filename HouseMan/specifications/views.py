from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .models import Address, Building, ExpenseItem, Expenses
from .forms import BuildExpFormSet


def platform(request):
    title = 'Main'
    header = 'Управляющая организация ООО "Ромашка"'
    cont  = 'По всем вопросам просьба обращаться по адресу г. Москва, 3-я ул.Строителей, д.1'
#    page_number = request.GET.get('page')
    context = {
        'title': title,
        'header': header,
        'cont': cont
    }
    return render(request, 'main.html', context)

class building_view(TemplateView):
    template_name = 'buildings.html'
    title = 'Buildings'
    header = 'Многоквартирные дома в управлении ООО "Ромашка"'

    buildings = Building.objects.values()
    for item in buildings:
        item['adr_for_map'] = item['title'].replace(' ', '+')+ ',+Moscow'

    extra_context = {
        'title': title,
        'header': header,
        'buildings': buildings,
    }

def building_spec(request, building_id):
    building = Building.objects.get(id=building_id)
    header = "Характеристики МКД:   " + building.title

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
        building_exp = Expenses.objects.filter(building_id=build_id, item_id = item['id']).values()
        if building_exp.count() == 1:
            init_values = dict(building_exp[0])
            init_values['item'] = item['title']
            initial.append(init_values)
#            print(building_exp[0])
        else:
#            initial.append({'building_id':build_id,'item_id' : item['id']})
            initial.append({'building_id':build_id,'item' : item['title']})

    return initial


def building_exp_view(request, building_id):
    context = {}
    list_init = items_list(building_id)
    formset = BuildExpFormSet(request.POST or None, initial= list_init)#Expenses.objects.all().values() )

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
    context['formset']= formset
    context['header']= "Плановые расходы на 2025 г.:  "+Building.objects.get(id=building_id).title
    context['summa']= f'Всего расходов по дому:  {summa} руб.'

    return render(request, 'exps.html', context)


class items_view(ListView):
    template_name = 'items.html'
    paginate_by = 5
    model = ExpenseItem
    context_object_name = 'items'
    extra_context = {
        'header': 'Статьи затрат на содержание и текущий ремонт МКД',
    }


