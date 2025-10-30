from django.db import models


class PlanItem(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Plan(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=50)
    plan_items = models.ManyToManyField(PlanItem)
    is_active = models.BooleanField(default=True)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class FrequentlyQuestionAndAnswer(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question
