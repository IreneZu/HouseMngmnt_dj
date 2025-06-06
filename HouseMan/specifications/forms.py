from django import forms
from django.forms import formset_factory
from .models import Expenses, ExpenseItem

class BuildExpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BuildExpForm, self).__init__(*args, **kwargs)
        self.fields['item'].widget.attrs['readonly'] = True

    item = forms.ModelChoiceField(queryset=ExpenseItem.objects.all(),
                                  to_field_name='title',
                                  label = '',
                                  empty_label="Статья затрат",
                                  )

    class Meta:
        model = Expenses
        fields = ['item', 'summ', 'type']
#        exclude = ["building"]
#        summ = forms.DecimalField()
        labels = {'summ': '  ', 'type': ' руб. в '}

        TYPE_CHOICES = (
            ('', 'Период (год/месяц)'),
            ('месяц', 'месяц'),  # First one is the value of select option and second is the displayed value in option
            ('год', 'год'),
        )
        widgets = {
            'type': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'})
        }

BuildExpFormSet = formset_factory(BuildExpForm, extra=0)


