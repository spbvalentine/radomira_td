from django.contrib import admin

# Register your models here.
from .models import (
    DurationCategory,
    Gender,
    AgeGroup,
    MaritalStatus,
    SocialStatus,
    ProblemGroup,
    Problem,
    EmotionalState,
    ProblemDuration,
    EmotionDynamics,
    HelpProvided,
    CallFrequency
)

@admin.register(DurationCategory)
class DurationCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('description',)


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')


@admin.register(MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')


@admin.register(SocialStatus)
class SocialStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('description',)


@admin.register(ProblemGroup)
class ProblemGroupAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('code', 'group', 'description')
    list_filter = ('group',)
    search_fields = ('description', 'code')


@admin.register(EmotionalState)
class EmotionalStateAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('description',)


@admin.register(ProblemDuration)
class ProblemDurationAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')


@admin.register(EmotionDynamics)
class EmotionDynamicsAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')


@admin.register(HelpProvided)
class HelpProvidedAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')


@admin.register(CallFrequency)
class CallFrequencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')