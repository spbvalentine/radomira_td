# tdapp/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'calls', views.CallRecordViewSet, basename='call')
router.register(r'durations', views.DurationCategoryViewSet, basename='duration')
router.register(r'genders', views.GenderViewSet, basename='gender')
router.register(r'age-groups', views.AgeGroupViewSet, basename='agegroup')
router.register(r'marital-statuses', views.MaritalStatusViewSet, basename='maritalstatus')
router.register(r'social-statuses', views.SocialStatusViewSet, basename='socialstatus')
router.register(r'emotional-states', views.EmotionalStateViewSet, basename='emotionalstate')
router.register(r'problems', views.ProblemViewSet, basename='problem')
router.register(r'problem-durations', views.ProblemDurationViewSet, basename='problemduration')
router.register(r'emotion-dynamics', views.EmotionDynamicViewSet, basename='emotiondynamic')
router.register(r'help-provided', views.HelpProvidedViewSet, basename='helpprovided')
router.register(r'frequencies', views.CallFrequencyViewSet, basename='frequency')
router.register(r'crisis-situations', views.CrisisSituationViewSet, basename='crisissituation')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/summary/', views.stats_summary, name='stats_summary'),
]