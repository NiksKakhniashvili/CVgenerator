from django_renderpdf.views import PDFView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from cv.models import Resume, ProjectExperience, Skill
from cv.serializers import ProjectExperienceSerializer, SkillSerializer, ResumeCreateSerializer, \
    ResumeRetrieveSerializer
from utils.custom_permisions import IsOwnerOrAdmin


class ResumeFilling(PDFView, RetrieveAPIView):
    """
        An endpoint for the User to retrieve a Resume/CV.
    """
    queryset = Resume.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ResumeRetrieveSerializer

    # def get_context_data(self, **kwargs):
    #     """Pass some extra context to the template."""
    #     context = super().get_context_data(**kwargs)
    #     resume = Resume.objects.get(id=kwargs["pk"])


# @extend_schema(
#         request=ResumeSerializer,
#         responses={status.HTTP_201_CREATED: ResumeSerializer},
#         examples=[
#             OpenApiExample(
#                 'Example',
#                 value={
#                     'user': 0,
#                     'position': "position",
#                     "description": "description",
#                     "skill": [
#                         {'text': 'Blue', 'is_correct': True},
#                         {'text': 'Red', 'is_correct': False},
#                     ]
#                 },
#
#             ),
#         ],
#     )
class ResumeCreateView(generics.CreateAPIView):
    """
    """
    queryset = Resume.objects.all()
    serializer_class = ResumeCreateSerializer
    permission_classes = (IsAuthenticated, )

    # def get_permissions(self):
    #     if self.request.method != "POST":
    #         return [IsOwnerOrAdmin()]
    #     return super().get_permissions()


class ResumeUpdateView(generics.UpdateAPIView):
    serializer_class = ResumeCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        resume_id = self.kwargs.get("pk")
        return Resume.objects.filter(pk=resume_id)


class ResumeListView(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeRetrieveSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class ResumeDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ResumeRetrieveSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        resume_id = self.kwargs.get("pk")
        return Resume.objects.filter(pk=resume_id)


class ProjectExperienceViewset(viewsets.ModelViewSet):
    """
    """
    queryset = ProjectExperience.objects.all()
    serializer_class = ProjectExperienceSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (IsAuthenticated, )


class SkillViewset(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

