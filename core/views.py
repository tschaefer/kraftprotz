from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, TemplateView

from kraftprotz.models import Cycling, Running
from kraftprotz.models import Workout, WorkoutUnit, WorkoutExercise
from kraftprotz.utils import LoginRequiredMixin


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
		redirect_field_name=REDIRECT_FIELD_NAME,
		authentication_form=AuthenticationForm,
		current_app=None, extra_context=None):
	"""
	Displays the login form and handles the login action.
	"""
	redirect_to = request.REQUEST.get(redirect_field_name, '')

	if request.method == "POST":
		form = authentication_form(request, data=request.POST)
		if form.is_valid():

			# Ensure the user-originating redirection url is safe.
			if not is_safe_url(url=redirect_to, host=request.get_host()):
				redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

			# Okay, security check complete. Log the user in.
			auth_login(request, form.get_user())

			return HttpResponseRedirect(redirect_to)
	else:
		if request.user.is_authenticated():
			return redirect('core_dashboard')
		else:
			form = authentication_form(request)

	current_site = get_current_site(request)

	context = {
		'form': form,
		redirect_field_name: redirect_to,
		'site': current_site,
		'site_name': current_site.name,
	}
	if extra_context is not None:
		context.update(extra_context)
	return TemplateResponse(request, template_name, context,
							current_app=current_app)


class CoreDashboard(LoginRequiredMixin, TemplateView):
	template_name = 'dashboard.html'

	def get_context_data(self, **kwargs):
		context = super(CoreDashboard, self).get_context_data(**kwargs)
		today = date.today()
		back_7_days = today - timedelta(days=7)

		obj = Cycling.objects.filter(athlete=self.request.user)
		try:
			latest = obj.latest()
		except Cycling.DoesNotExist:
			latest = None
		context['cycling'] = {
			'latest': latest,
			'activities': {
				'last_7_days': obj.filter(date__range=(back_7_days, today)),
				'month': obj.filter(date__month=today.month),
			},
		}

		obj = Running.objects.filter(athlete=self.request.user)
		try:
			latest = obj.latest()
		except Running.DoesNotExist:
			latest = None
		context['running'] = {
			'latest': latest,
			'activities': {
				'last_7_days': obj.filter(date__range=(back_7_days, today)),
				'month': obj.filter(date__month=today.month),
			},
		}

		obj = Workout.objects.filter(athlete=self.request.user)
		try:
			latest = obj.latest()
		except Workout.DoesNotExist:
			latest = None
		context['workout'] = {
			'latest': latest,
			'activities': {
				'last_7_days': obj.filter(date__range=(back_7_days, today)),
				'month': obj.filter(date__month=today.month),
			},
		}

		return context
