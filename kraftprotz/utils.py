import datetime

from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class AthleteFilterMixin(object):

	def get_queryset(self):
		return super(AthleteFilterMixin, self).get_queryset(). \
				filter(athlete=self.request.user)


class AthleteFormMixin(object):

	def get_form(self, form_class):
		form = super(AthleteFormMixin, self).get_form(form_class)
		form.fields['athlete'].initial = self.request.user
		return form


class DurationField(forms.TimeField):

	def to_python(self, value):
		time = super(DurationField, self).to_python(value)

		return datetime.timedelta(
				hours=time.hour,
				minutes=time.minute,
				seconds=time.second).total_seconds()
