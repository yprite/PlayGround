from django import forms
from bootstrap_modal_forms.forms import BSModalForm

from . import models

class AddReplaceForm(BSModalForm):

    replace = forms.CharField(error_messages={'invalid' : 'Not Null'})

    class Meta:
        model = models.company
        fields = ['replace']
        widgets = {
                'replace': forms.TextInput(attrs={'size': '40', 'placeholder': '대체상품 - 제품들을 콤마(,)로 구분해주세요.'}),
                }

