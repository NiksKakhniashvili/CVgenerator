from django_renderpdf.views import PDFView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cv.models import Resume, ProjectExperience, Skill, Percentage, ResumeTemplate
from cv.serializers import ProjectExperienceSerializer, SkillSerializer, ResumeCreateSerializer, \
    ResumeRetrieveSerializer, ResumeTemplateSerializer
from users.models import CustomUser
from utils.custom_permisions import IsOwnerOrAdmin


class ResumePDFView(PDFView, generics.RetrieveAPIView):
    """
        Generate resume to PDF file.

        Required Permissions:
            - User must be authenticated.
    """
    queryset = Resume.objects.all()
    serializer_class = ResumeRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""

        context = super().get_context_data(**kwargs)
        context["resume"] = Resume.objects.get(id=kwargs["pk"])
        context["user"] = CustomUser.objects.get(resume=kwargs["pk"])
        user = context["user"]
        context["initials"] = user.first_name[0].upper() + "." + user.last_name[0].upper() + "."
        context["project_experiences"] = ProjectExperience.objects.filter(experiences=kwargs["pk"])
        context["skills"] = Percentage.objects.filter(resume=kwargs["pk"])

        # do this for html table purposes
        for skill in context["skills"]:
            skill.percentage *= 5

        self.template_name = f"resumes/{context['resume'].resume_template.name}.html"
        self.download_name = (
            f"{context['resume'].resume_template.name}_{context['resume'].user.first_name}.pdf"
        )

        self.prompt_download = True

        return context


class ResumeTemplateViewset(viewsets.ModelViewSet):
    """
       List all resume templates.

       This view allows to get all the resume templates or the id.

       Returns:
       - 200 OK: List of resumes is successfully retrieved.
       - 401 Unauthorized: User is not authenticated.

    """

    queryset = ResumeTemplate.objects.all()
    serializer_class = ResumeTemplateSerializer
    http_method_names = ["get"]
    permission_classes = (IsAuthenticated,)


class ResumeCreateView(generics.CreateAPIView):
    """
       Create a new resume.

       Required Permissions:
       - User must be authenticated.

       Returns:
       - 201 Created: The new resume is successfully created.
       - 401 Unauthorized: User is not authenticated.
       - 400 Bad Request: Invalid data provided.
    """
    queryset = Resume.objects.all()
    serializer_class = ResumeCreateSerializer
    permission_classes = (IsAuthenticated,)


class ResumeUpdateView(generics.UpdateAPIView):
    """
        Update an existing resume.

        This view allows authenticated users to update their own resumes.

        Required Permissions:
        - User must be authenticated.
        - User must be the owner of the resume or a superuser.

        Returns:
        - 200 OK: The resume is successfully updated.
        - 401 Unauthorized: User is not authenticated.
        - 403 Forbidden: User does not have permission to update this resume.
        - 404 Not Found: Resume with the specified ID does not exist.
        - 400 Bad Request: Invalid data provided.
    """

    serializer_class = ResumeCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        resume_id = self.kwargs.get("pk")
        return Resume.objects.filter(pk=resume_id)


class ResumeListView(generics.ListAPIView):
    """
        List all resumes.

        This view allows to get all the resumes.

        Returns:
        - 200 OK: List of resumes is successfully retrieved.
        - 401 Unauthorized: User is not authenticated.

    """
    queryset = Resume.objects.all()
    serializer_class = ResumeRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                return Resume.objects.filter(user_id=self.request.user)
        except Exception:
            return Resume.objects.none()
        return super().get_queryset()


class ResumeDetailView(generics.RetrieveDestroyAPIView):
    """
        Retrieve or delete a resume.

        This view allows authenticated users to retrieve or delete their own resumes.

        Required Permissions:
        - User must be authenticated.
        - User must be the owner of the resume or a superuser.

        Returns:
        - 200 OK: Resume is successfully retrieved.
        - 204 No Content: Resume is successfully deleted.
        - 401 Unauthorized: User is not authenticated.
        - 403 Forbidden: User does not have permission to access/delete this resume.
        - 404 Not Found: Resume with the specified ID does not exist.
    """
    serializer_class = ResumeRetrieveSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)
    queryset = Resume.objects.all()


class ProjectExperienceViewset(viewsets.ModelViewSet):
    """
        Manage project experiences.

        This viewset allows authenticated users to manage project experiences.

        Required Permissions:
        - User must be authenticated.

        Returns:
        - 200 OK: List of project experiences is successfully retrieved.
        - 201 Created: New project experience is successfully created.
        - 200 OK: Project experience is successfully updated.
        - 204 No Content: Project experience is successfully deleted.
        - 401 Unauthorized: User is not authenticated.

    """
    queryset = ProjectExperience.objects.all()
    serializer_class = ProjectExperienceSerializer
    http_method_names = ["get", "post", "patch"]
    permission_classes = (IsAuthenticated,)


class SkillViewset(viewsets.ModelViewSet):
    """
       Manage skills.

       This viewset allows authenticated users to manage skills.

       Required Permissions:
       - User must be authenticated.

       Returns:
       - 200 OK: List of skills is successfully retrieved.
       - 201 Created: New skill is successfully created.
       - 200 OK: Skill is successfully updated.
       - 204 No Content: Skill is successfully deleted.
       - 401 Unauthorized: User is not authenticated.

    """

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (IsAuthenticated,)
