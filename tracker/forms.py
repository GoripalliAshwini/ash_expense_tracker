# forms.py
from django import forms
from tracker.models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'Date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
    Type = forms.ChoiceField(
            choices=(("Income", "Income"), ("Expense", "Expense")),
            widget=forms.RadioSelect
        )