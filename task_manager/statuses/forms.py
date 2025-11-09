from django import forms

from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': 'Имя',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Имя',
            'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        status = Status.objects.filter(name=name)
        if status.exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Cтатус с таким именем уже существует."
                )
        return name

    def save(self, commit=True):
        status = super().save(commit=False)
        if commit:
            status.save()
        return status
