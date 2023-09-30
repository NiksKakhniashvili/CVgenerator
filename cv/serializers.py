from django.db import transaction
from rest_framework import serializers

from cv.models import ProjectExperience, Resume, Skill, Percentage, ResumeTemplate


class ResumeTemplateSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize Template model.
    """

    class Meta:
        model = ResumeTemplate
        fields = ("id", "name",)


class PercentageSerializer(serializers.ModelSerializer):
    """
       Serializer class to serialize Percentage model.
    """

    class Meta:
        model = Percentage
        fields = ("id", "percentage", "skill")


class SkillSerializer(serializers.ModelSerializer):
    """
       Serializer class to serialize ProjectExperience model.
    """

    class Meta:
        model = Skill
        fields = ("id", "name")


class ProjectExperienceSerializer(serializers.ModelSerializer):
    """
       Serializer class to serialize ProjectExperience model.
    """

    class Meta:
        model = ProjectExperience
        fields = ("id", "user", "title", "role", "technology", "project_description")


class ResumeCreateSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize Resume model for creation.
    """
    skill_percentages = PercentageSerializer(many=True, write_only=True)
    project_experience_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Resume
        fields = (
            "id",
            "user",
            "position",
            "description",
            "project_experience_ids",
            "skill_percentages",
            "resume_template"
        )

    def create(self, validated_data):
        skill_percentage = validated_data.pop("skill_percentages")
        project_experience_ids = validated_data.pop("project_experience_ids")

        with transaction.atomic():
            resume = Resume.objects.create(**validated_data)
            resume.project_experiences.set(project_experience_ids)

            percentage_objects = []

            for skill_percentage in skill_percentage:
                skill_id = skill_percentage["skill"]
                percentage_value = skill_percentage["percentage"]
                percentage = Percentage(resume=resume, skill=skill_id, percentage=percentage_value)

                percentage_objects.append(percentage)

            Percentage.objects.bulk_create(percentage_objects)

        return resume

    def update(self, instance, validated_data):
        validated_data.pop("user", None)

        # Update the Resume instance with the validated data
        instance.position = validated_data.get("position", instance.position)
        instance.description = validated_data.get("description", instance.description)

        project_experience_ids = validated_data.get("project_experience_ids", [])

        project_experiences_to_remove = instance.project_experiences.exclude(pk__in=project_experience_ids)

        for project_experience in project_experiences_to_remove:
            instance.project_experiences.remove(project_experience)

        # Add new project experiences
        for pr_exp_id in project_experience_ids:
            project_experience = ProjectExperience.objects.filter(pk=pr_exp_id).first()
            if project_experience:
                instance.project_experiences.add(project_experience)

        # Update skill percentages
        skill_percentages_data = validated_data.get("skill_percentages", [])

        for skill_percentage_data in skill_percentages_data:
            skill_id = skill_percentage_data["skill"].id
            percentage_value = skill_percentage_data["percentage"]

            # Check if the skill already exists for this resume
            existing_percentage = Percentage.objects.filter(resume=instance, skill_id=skill_id).first()

            if existing_percentage:
                # Update the existing percentage value
                existing_percentage.percentage = percentage_value
                existing_percentage.save()
            else:
                # Create a new skill percentage
                Percentage.objects.create(resume=instance, skill_id=skill_id, percentage=percentage_value)

        instance.save()
        return instance


class ResumeRetrieveSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize Resume model for retrieval.
    """
    skill_percentages = serializers.SerializerMethodField()
    project_experiences = ProjectExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = ("id", "user", "position", "description", "project_experiences", "skill_percentages")

    def get_skill_percentages(self, instance):
        percentages = Percentage.objects.filter(resume=instance)
        serialized_percentages = PercentageSerializer(percentages, many=True, read_only=True)

        return serialized_percentages.data
