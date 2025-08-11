# tdapp/api/serializers.py

from rest_framework import serializers
from tdapp import models
from django.contrib.auth.models import User

# Базовый сериализатор для справочников (code + description)
class CodeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # будет переопределено
        fields = ('code', 'description')

# Сериализаторы для справочников
class DurationCategorySerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.DurationCategory

class GenderSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.Gender

class AgeGroupSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.AgeGroup

class MaritalStatusSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.MaritalStatus

class SocialStatusSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.SocialStatus

class ProblemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProblemGroup
        fields = ('number', 'name')

class ProblemSerializer(serializers.ModelSerializer):
    group = ProblemGroupSerializer(read_only=True)
    class Meta:
        model = models.Problem
        fields = ('code', 'group', 'description')

class EmotionalStateSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.EmotionalState

class ProblemDurationSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.ProblemDuration

class EmotionDynamicsSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.EmotionDynamics

class HelpProvidedSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.HelpProvided

class CallFrequencySerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.CallFrequency

# Сериализатор для консультанта
class ConsultantSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'full_name')
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

# Основной сериализатор — Звонок
class CallRecordReadSerializer(serializers.ModelSerializer):
    duration = DurationCategorySerializer(read_only=True)
    gender = GenderSerializer(read_only=True)
    age_group = AgeGroupSerializer(read_only=True)
    marital_status = MaritalStatusSerializer(read_only=True)
    social_status = SocialStatusSerializer(read_only=True)
    problem = ProblemSerializer(read_only=True)
    emotional_state = EmotionalStateSerializer(read_only=True)
    problem_duration = ProblemDurationSerializer(read_only=True)
    emotion_dynamics = EmotionDynamicsSerializer(read_only=True)
    help_provided = HelpProvidedSerializer(read_only=True)
    frequency = CallFrequencySerializer(read_only=True)
    consultant = ConsultantSerializer(read_only=True)

    # Дополнительные поля
    crisis_level = serializers.SerializerMethodField()
    is_suicidal = serializers.SerializerMethodField()

    class Meta:
        model = models.CallRecord
        fields = '__all__'

    def get_crisis_level(self, obj):
        group = obj.problem.group.number
        if group == 10:
            return "Кризис"
        elif group == 11:
            return "Суицид"
        return "Некризис"

    def get_is_suicidal(self, obj):
        return obj.problem.group.number == 11

class CallRecordWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CallRecord
        fields = '__all__'