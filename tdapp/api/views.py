# tdapp/api/views.py

from rest_framework import viewsets, filters
from django_filters import rest_framework as django_filters
from tdapp import models
from . import serializers
from .pagination import DataTablesPagination

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from tdapp.models import CallRecord

# Фильтры
class CallRecordFilter(django_filters.FilterSet):
    call_date = django_filters.DateFromToRangeFilter()  # ?call_date_after=2025-01-01&call_date_before=2025-04-01

    class Meta:
        model = models.CallRecord
        fields = ['gender', 'age_group', 'social_status', 'emotional_state', 'help_provided', 'frequency', 'consultant', 'crisis_situation']

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

class EmotionalStateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EmotionalState.objects.all()
    serializer_class = serializers.EmotionalStateSerializer

class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Problem.objects.all()
    serializer_class = serializers.ProblemSerializer

class ProblemDurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ProblemDuration.objects.all()
    serializer_class = serializers.ProblemDurationSerializer

class EmotionDynamicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EmotionDynamic.objects.all()
    serializer_class = serializers.EmotionDynamicSerializer

class HelpProvidedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.HelpProvided.objects.all()
    serializer_class = serializers.HelpProvidedSerializer

class CallFrequencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.CallFrequency.objects.all()
    serializer_class = serializers.CallFrequencySerializer

class CrisisSituationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.CrisisSituation.objects.all()
    serializer_class = serializers.CrisisSituationSerializer

class CallRecordViewSet(viewsets.ModelViewSet):
    queryset = models.CallRecord.objects.select_related(
        'duration', 'gender', 'age_group', 'marital_status', 'social_status',
        'emotional_state', 'problem_duration',
        'emotion_dynamic', 'help_provided', 'frequency', 'consultant', 'crisis_situation'
    ).order_by('-id')  # ← Изменено здесь!

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.CallRecordReadSerializer
        return serializers.CallRecordWriteSerializer

    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CallRecordFilter
    search_fields = ['problem__description', 'consultant__username']
    ordering_fields = ['call_date', 'call_time', 'id']  # ← Добавили 'id' для возможности переопределения через API

    pagination_class = DataTablesPagination

@api_view(['GET'])
def stats_summary(request):
    """
    Возвращает сводную статистику по обращениям.
    """
    # Общее количество звонков
    total_calls = CallRecord.objects.count()

    return Response({
        "total_calls": total_calls,
        # Можно добавить другие поля позже:
        # "crisis_calls": ...,
        # "avg_duration": ...,
        # "help_rate": ...,
    })