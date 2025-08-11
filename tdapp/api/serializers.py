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

class EmotionalStateSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.EmotionalState

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = ('code', 'group', 'description')

class ProblemDurationSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.ProblemDuration

class EmotionDynamicSerializer(CodeNameSerializer):
    class Meta(CodeNameSerializer.Meta):
        model = models.EmotionDynamic

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

class CrisisSituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CrisisSituation
        fields = ['code', 'description']

# Основной сериализатор — Звонок
class CallRecordReadSerializer(serializers.ModelSerializer):
    duration = DurationCategorySerializer(read_only=True)
    gender = GenderSerializer(read_only=True)
    age_group = AgeGroupSerializer(read_only=True)
    marital_status = MaritalStatusSerializer(read_only=True)
    social_status = SocialStatusSerializer(read_only=True)
    emotional_state = EmotionalStateSerializer(read_only=True)
    problem = ProblemSerializer(read_only=True)
    problem_duration = ProblemDurationSerializer(read_only=True)
    emotion_dynamic = EmotionDynamicSerializer(read_only=True)
    help_provided = HelpProvidedSerializer(read_only=True)
    frequency = CallFrequencySerializer(read_only=True)
    consultant = ConsultantSerializer(read_only=True)
    crisis_situation = CrisisSituationSerializer(read_only=True)
    # call_date = serializers.DateField(format="%d.%m.%Y")

    class Meta:
        model = models.CallRecord
        fields = '__all__'

class CallRecordWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CallRecord
        exclude = ['created_at', 'updated_at']  # или fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['consultant'] = request.user
        return super().create(validated_data)