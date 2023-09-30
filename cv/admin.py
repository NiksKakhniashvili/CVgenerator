from django.contrib import admin

from cv.models import Resume, ProjectExperience, Skill, Percentage, ResumeTemplate

admin.site.register(ResumeTemplate)
admin.site.register(Resume)
admin.site.register(ProjectExperience)
admin.site.register(Skill)
admin.site.register(Percentage)
