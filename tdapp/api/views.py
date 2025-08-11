# tdapp/api/views.py

from rest_framework import viewsets, filters
from django_filters import rest_framework as django_filters
from tdapp import models
from . import serializers

# Фильтры
class CallRecordFilter(django_filters.FilterSet):
    call_date = django_filters.DateFromToRangeFilter()  # ?call_date_after=2025-01-01&call_date_before=2025-04-01
    problem_group = django_filters.NumberFilter(field_name='problem__group__number')
    crisis = django_filters.BooleanFilter(method='filter_crisis')
    suicidal = django_filters.BooleanFilter(method='filter_suicidal')

    class Meta:
        model = models.CallRecord
        fields = ['gender', 'age_group', 'social_status', 'emotional_state', 'help_provided', 'frequency', 'consultant']

    def filter_crisis(self, queryset, name, value):
        crisis_groups = [10, 11]
        if value:
            return queryset.filter(problem__group__number__in=crisis_groups)
        return queryset.exclude(problem__group__number__in=crisis_groups)

    def filter_suicidal(self, queryset, name, value):
        if value:
            return queryset.filter(problem__group__number=11)
        return queryset.exclude(problem__group__number=11)

# ViewSets
class DurationCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.DurationCategory.objects.all()
    serializer_class = serializers.DurationCategorySerializer

class GenderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Gender.objects.all()
    serializer_class = serializers.GenderSerializer

class AgeGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.AgeGroup.objects.all()
    serializer_class = serializers.AgeGroupSerializer

class MaritalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer

class SocialStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.SocialStatus.objects.all()
    serializer_class = serializers.SocialStatusSerializer

class ProblemGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ProblemGroup.objects.all()
    serializer_class = serializers.ProblemGroupSerializer

class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Problem.objects.all()
    serializer_class = serializers.ProblemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['description']

class EmotionalStateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EmotionalState.objects.all()
    serializer_class = serializers.EmotionalStateSerializer

class ProblemDurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ProblemDuration.objects.all()
    serializer_class = serializers.ProblemDurationSerializer

class EmotionDynamicsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EmotionDynamics.objects.all()
    serializer_class = serializers.EmotionDynamicsSerializer

class HelpProvidedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.HelpProvided.objects.all()
    serializer_class = serializers.HelpProvidedSerializer

class CallFrequencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.CallFrequency.objects.all()
    serializer_class = serializers.CallFrequencySerializer

class CallRecordViewSet(viewsets.ModelViewSet):
    queryset = models.CallRecord.objects.select_related(
        'duration', 'gender', 'age_group', 'marital_status', 'social_status',
        'problem__group', 'emotional_state', 'problem_duration',
        'emotion_dynamics', 'help_provided', 'frequency', 'consultant'
    ).order_by('-call_date', '-call_time')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.CallRecordReadSerializer
        return serializers.CallRecordWriteSerializer

    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CallRecordFilter
    search_fields = ['problem__description', 'consultant__username']
    ordering_fields = ['call_date', 'call_time']