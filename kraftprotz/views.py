import datetime

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum
from django.forms.models import model_to_dict
from django.forms.util import ErrorList
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView
from django.views.generic import TemplateView, ListView, DetailView

from kraftprotz.forms import RunningForm, CyclingForm, SwimmingForm
from kraftprotz.forms import WorkoutForm, WorkoutDataFormSet
from kraftprotz.models import Running, Cycling, Swimming
from kraftprotz.models import Workout, WorkoutUnit, WorkoutExercise
from kraftprotz.utils import AthleteFormMixin
from kraftprotz.utils import LoginRequiredMixin, AthleteFilterMixin


class WorkoutList(LoginRequiredMixin, AthleteFilterMixin, ListView):
	model = Workout
	paginate_by = 7


class WorkoutDetail(LoginRequiredMixin, AthleteFilterMixin, DetailView):
	model = Workout


class WorkoutCreate(LoginRequiredMixin, AthleteFormMixin, CreateView):
	model = Workout
	form_class = WorkoutForm

	def get_context_data(self, **kwargs):
		context = super(WorkoutCreate, self).get_context_data(**kwargs)
		context['formset'] = WorkoutDataFormSet(self.request.POST or None)
		return context

	def get_success_url(self):
		return self.request.GET.get('next',
				reverse_lazy('kraftprotz_workout_list'))

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['formset']
		if formset.is_valid():
			w = form.save()
			for form in formset:
				for index in range(form.cleaned_data['sets_total']):
					u, c = WorkoutUnit.objects.get_or_create(number=index + 1,
						workout=w)
					data = {
						'unit': u,
						'exercise': form.cleaned_data['exercise'],
						'repeats': form.cleaned_data['repeats_set_%d' % index],
						'workout': w
					}
					e = WorkoutExercise(**data)
					e.save()
			return redirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))


class WorkoutDelete(LoginRequiredMixin, AthleteFilterMixin, DeleteView):
	model = Workout

	def get_success_url(self):
		return self.request.GET.get('next',
				reverse_lazy('kraftprotz_workout_list'))


class RunningList(LoginRequiredMixin, AthleteFilterMixin, ListView):
	model = Running
	paginate_by = 7


class RunningDetail(LoginRequiredMixin, AthleteFilterMixin, DetailView):
	model = Running


class RunningCreate(LoginRequiredMixin, AthleteFormMixin, CreateView):
	model = Running
	form_class = RunningForm

	def get_success_url(self):
		return self.request.GET.get('next',
				reverse_lazy('kraftprotz_running_list'))


class RunningDelete(LoginRequiredMixin, AthleteFilterMixin, DeleteView):
	model = Running

	def get_success_url(self):
		return self.request.GET.get('next',
				reverse_lazy('kraftprotz_running_list'))


class CyclingList(LoginRequiredMixin, AthleteFilterMixin, ListView):
	model = Cycling
	paginate_by = 7


class CyclingDetail(LoginRequiredMixin, AthleteFilterMixin, DetailView):
	model = Cycling


class CyclingCreate(LoginRequiredMixin, AthleteFormMixin, CreateView):
	model = Cycling
	form_class = CyclingForm

	def get_success_url(self):
		return self.request.GET.get('next',
				reverse_lazy('kraftprotz_cycling_list'))


class CyclingDelete(LoginRequiredMixin, AthleteFilterMixin, DeleteView):
	model = Cycling

	def get_success_url(self):
		return self.request.GET.get('next',
				reverse_lazy('kraftprotz_cycling_list'))


class SwimmingList(LoginRequiredMixin, AthleteFilterMixin, ListView):
	model = Swimming
	paginate_by = 7


class SwimmingDetail(LoginRequiredMixin, AthleteFilterMixin, DetailView):
	model = Swimming


class SwimmingCreate(LoginRequiredMixin, AthleteFormMixin, CreateView):
	model = Swimming
	form_class = SwimmingForm

	def get_success_url(self):
		return self.request.GET.get('next',
				reverse_lazy('kraftprotz_swimming_list'))


class SwimmingDelete(LoginRequiredMixin, AthleteFilterMixin, DeleteView):
	model = Swimming

	def get_success_url(self):
		return self.request.GET.get('next',
				reverse_lazy('kraftprotz_swimming_list'))
