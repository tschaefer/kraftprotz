from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse


class Workout(models.Model):
	athlete = models.ForeignKey(User,unique_for_date="date")
	date = models.DateField(auto_now=False)

	class Meta:
		get_latest_by = "date"
		ordering = ["-date"]

	def get_absolute_url(self):
		return reverse('kraftprotz_workout_detail', args=[str(self.id)])

	def get_repeats_sum(self):
		q = WorkoutExercise.objects.filter(workout=self.id)
		d = {}
		for e in list(set(q.values_list('exercise'))):
			d.update({
				e[0]: sum([r.repeats for r in q.filter(exercise=e[0])])
			})
		return d


class WorkoutUnit(models.Model):
	number = models.PositiveSmallIntegerField()
	workout = models.ForeignKey(Workout)

	class Meta:
		ordering = ['workout', 'number']


EXERCISES = (
	(u"Crunches", u"Crunches"),
	(u"Pull Ups", u"Pull Ups"),
	(u"Push Ups", u"Push Ups"),
	(u"Squats", u"Squats"),
)

class WorkoutExercise(models.Model):
	exercise = models.CharField(max_length=128,choices=EXERCISES)
	repeats = models.PositiveSmallIntegerField()
	unit = models.ForeignKey(WorkoutUnit)
	workout = models.ForeignKey(Workout)

	class Meta:
		ordering = ['workout', 'unit']


GARMIN_BASE_URL = "http://connect.garmin.com/modern/activity/"

class Running(models.Model):
	athlete = models.ForeignKey(User,unique_for_date="date")
	date = models.DateField(auto_now=False)
	time = models.FloatField()
	distance = models.DecimalField(max_digits=4,decimal_places=2)
	garmin_id = models.PositiveIntegerField(blank=True,null=True,
		verbose_name="Garmin")

	class Meta:
		get_latest_by = "date"
		ordering = ["-date"]

	@property
	def duration(self):
		return timedelta(seconds=self.time)

	@property
	def time_in_minutes(self):
		return self.time / 60

	@property
	def garmin_url(self):
		return GARMIN_BASE_URL + str(self.garmin_id)

	@property
	def average_pace(self):
		sk = self.time / float(self.distance)
		return timedelta(seconds=round(sk, 0))

	@property
	def average_speed(self):
		m = float(self.distance * 1000)
		ms = m / self.time
		kh = ms * 3.6
		return round(kh, 1)

	def get_absolute_url(self):
		return reverse('kraftprotz_running_detail', args=[str(self.id)])

class Cycling(models.Model):
	athlete = models.ForeignKey(User,unique_for_date="date")
	date = models.DateField(auto_now=False)
	time = models.FloatField()
	distance = models.DecimalField(max_digits=4,decimal_places=2)
	garmin_id = models.PositiveIntegerField(blank=True,null=True,
		verbose_name="Garmin")

	class Meta:
		get_latest_by = "date"
		ordering = ["-date"]

	@property
	def duration(self):
		return timedelta(seconds=self.time)

	@property
	def time_in_minutes(self):
		return self.time / 60

	@property
	def garmin_url(self):
		return GARMIN_BASE_URL + str(self.garmin_id)

	@property
	def average_pace(self):
		sk = self.time / float(self.distance)
		return timedelta(seconds=round(sk, 0))

	@property
	def average_speed(self):
		m = float(self.distance * 1000)
		ms = m / self.time
		kh = ms * 3.6
		return round(kh, 1)

	def get_absolute_url(self):
		return reverse('kraftprotz_cycling_detail', args=[str(self.id)])


class Swimming(models.Model):
	athlete = models.ForeignKey(User,unique_for_date="date")
	date = models.DateField(auto_now=False)
	time = models.FloatField()
	distance = models.DecimalField(max_digits=4,decimal_places=2)
	garmin_id = models.PositiveIntegerField(blank=True,null=True,
		verbose_name="Garmin")

	class Meta:
		get_latest_by = "date"
		ordering = ["-date"]

	@property
	def duration(self):
		return timedelta(seconds=self.time)

	@property
	def time_in_minutes(self):
		return self.time / 60

	@property
	def garmin_url(self):
		return GARMIN_BASE_URL + str(self.garmin_id)

	@property
	def average_pace(self):
		sk = self.time / float(self.distance)
		return timedelta(seconds=round(sk, 0))

	@property
	def average_speed(self):
		m = float(self.distance * 1000)
		ms = m / self.time
		kh = ms * 3.6
		return round(kh, 1)

	def get_absolute_url(self):
		return reverse('kraftprotz_swimming_detail', args=[str(self.id)])
