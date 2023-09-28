from django.urls import path
from rest_framework.routers import DefaultRouter

from cv.views import ResumeCreateView, ResumeListView, ProjectExperienceViewset, SkillViewset, ResumeFilling, \
      ResumeDetailView, ResumeUpdateView

app_name = "cv"

router = DefaultRouter()

router.register("project-experiences", ProjectExperienceViewset, basename="experiences")
router.register("skills", SkillViewset, basename="skill")

urlpatterns = [
      path("download/<int:pk>/", ResumeFilling.as_view()),
      path("resume/create", ResumeCreateView.as_view()),
      path("resumes/", ResumeListView.as_view()),
      path("resume/update/<int:pk>/", ResumeUpdateView.as_view()),
      path("resume/<int:pk>/", ResumeDetailView.as_view()),
] + router.urls
