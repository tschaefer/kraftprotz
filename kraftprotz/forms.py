import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet, formset_factory

from kraftprotz.models import Running, Cycling, Swimming, Workout, EXERCISES
from kraftprotz.utils import DurationField


class WorkoutForm(forms.ModelForm):

	class Meta:
		model = Workout
		fields = ['date', 'athlete']
		widgets = {
			'athlete': forms.HiddenInput(),
		}


class WorkoutDataForm(forms.Form):
	exercise = forms.ChoiceField(choices=EXERCISES)
	sets_total = forms.IntegerField(widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		sets_total = kwargs.pop('sets', 2)
		super(WorkoutDataForm, self).__init__(*args, **kwargs)
		self.fields['sets_total'].initial = sets_total

		for index in range(int(sets_total)):
			self.fields['repeats_set_%d' % (index)] = \
				forms.IntegerField(min_value=0,
						widget=forms.NumberInput(attrs={'placeholder':
							'Repeats', 'required': 'required'}))


class WorkoutDataBaseFormSet(BaseFormSet):

	def clean(self):
		l = []
		for i in range(0, self.total_form_count()):
			form = self.forms[i]
			l.append(form.cleaned_data['exercise'])

		try:
			if any(l.count(x) > 1 for x in l):
				raise ValidationError('Duplicated exercises found.')
		except ValidationError as e:
			self._non_form_errors = self.error_class(e.messages)


WorkoutDataFormSet = formset_factory(WorkoutDataForm,
		formset=WorkoutDataBaseFormSet, extra=3)


class RunningForm(forms.ModelForm):
	time = DurationField()

	class Meta:
		model = Running
		fields = '__all__'
		widgets = {
			'athlete': forms.HiddenInput(),
		}


class CyclingForm(forms.ModelForm):
	time = DurationField()

	class Meta:
		model = Cycling
		fields = '__all__'
		widgets = {
			'athlete': forms.HiddenInput(),
		}

class SwimmingForm(forms.ModelForm):
	time = DurationField()

	class Meta:
		model = Swimming
		fields = '__all__'
		widgets = {
			'athlete': forms.HiddenInput(),
		}
