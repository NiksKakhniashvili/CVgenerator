from django.contrib import admin

from cv.models import Resume, ProjectExperience, Skill, Percentage

admin.site.register(Resume)
admin.site.register(ProjectExperience)
admin.site.register(Skill)
admin.site.register(Percentage)

