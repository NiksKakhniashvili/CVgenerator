from django.core.validators import MaxValueValidator
from django.db import models

from users.models import CustomUser, Profile


class Percentage(models.Model):
    percentage = models.IntegerField(validators=[MaxValueValidator(100)], default=0)
    skill = models.ForeignKey("Skill", on_delete=models.CASCADE)
    resume = models.ForeignKey("Resume", on_delete=models.CASCADE)


class Skill(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Resume(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=150)
    description = models.TextField()
    skill = models.ManyToManyField("Skill", related_name="skills_list")
    project_experiences = models.ManyToManyField("ProjectExperience", related_name="experiences")


class ProjectExperience(models.Model):
    title = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    technology = models.CharField(max_length=150)
    project_description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

