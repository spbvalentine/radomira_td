from django.db import models

# Create your models here.

class DurationCategory(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=50, verbose_name="Продолжительность контакта")

    class Meta:
        verbose_name = "Категория продолжительности"
        verbose_name_plural = "Категории продолжительности"

    def __str__(self):
        return f"{self.code} — {self.description}"

class Gender(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=20, verbose_name="Пол абонента")

    class Meta:
        verbose_name = "Пол абонента"
        verbose_name_plural = "Пол абонента"

    def __str__(self):
        return f"{self.code} — {self.description}"

class AgeGroup(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=50, verbose_name="Возрастная группа")

    class Meta:
        verbose_name = "Возрастная группа"
        verbose_name_plural = "Возрастные группы"

    def __str__(self):
        return f"{self.code} — {self.description}"

class MaritalStatus(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=50, verbose_name="Семейное положение")

    class Meta:
        verbose_name = "Семейное положение"
        verbose_name_plural = "Семейное положение"

    def __str__(self):
        return f"{self.code} — {self.description}"

class SocialStatus(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=100, verbose_name="Социальное положение")

    class Meta:
        verbose_name = "Социальное положение"
        verbose_name_plural = "Социальное положение"

    def __str__(self):
        return f"{self.code} — {self.description}"

class EmotionalState(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=100, verbose_name="Эмоциональное состояние")

    class Meta:
        verbose_name = "Эмоциональное состояние"
        verbose_name_plural = "Эмоциональные состояния"

    def __str__(self):
        return f"{self.code} — {self.description}"

class ProblemGroup(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Номер группы")
    name = models.CharField(max_length=100, verbose_name="Тип обращения")

    class Meta:
        verbose_name = "Группа проблем"
        verbose_name_plural = "Группы проблем"

    def __str__(self):
        return f"{self.number} — {self.name}"


class Problem(models.Model):
    code = models.PositiveIntegerField(primary_key=True, verbose_name="Код проблемы")
    group = models.ForeignKey(ProblemGroup, on_delete=models.CASCADE, verbose_name="Группа")
    description = models.CharField(max_length=200, verbose_name="Тип обращения")

    class Meta:
        verbose_name = "Проблема"
        verbose_name_plural = "Проблемы"

    def __str__(self):
        return f"{self.code} — {self.description}"

class ProblemDuration(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=50, verbose_name="Длительность существования проблемы")

    class Meta:
        verbose_name = "Длительность проблемы"
        verbose_name_plural = "Длительности проблем"

    def __str__(self):
        return f"{self.code} — {self.description}"

class EmotionDynamics(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=100, verbose_name="Динамика переживаний")

    class Meta:
        verbose_name = "Динамика переживаний"
        verbose_name_plural = "Динамики переживаний"

    def __str__(self):
        return f"{self.code} — {self.description}"

class HelpProvided(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=200, verbose_name="Предоставленная помощь")

    class Meta:
        verbose_name = "Предоставленная помощь"
        verbose_name_plural = "Предоставленные виды помощи"

    def __str__(self):
        return f"{self.code} — {self.description}"

class CallFrequency(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True, verbose_name="Код")
    description = models.CharField(max_length=50, verbose_name="Периодичность обращений")

    class Meta:
        verbose_name = "Периодичность обращения"
        verbose_name_plural = "Периодичности обращений"

    def __str__(self):
        return f"{self.code} — {self.description}"

class CallRecord(models.Model):
    # I. Дата обращения
    call_date = models.DateField(verbose_name="Дата обращения")

    # II. Время обращения
    call_time = models.TimeField(verbose_name="Время обращения")

    # III. Продолжительность контакта (код)
    duration = models.ForeignKey(DurationCategory, on_delete=models.PROTECT, verbose_name="Продолжительность контакта")

    # IV. Пол абонента (код)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, verbose_name="Пол абонента")

    # V. Возраст абонента (группа)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.PROTECT, verbose_name="Возрастная группа")

    # VI*. Семейное положение
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.PROTECT, null=True, blank=True,
                                       verbose_name="Семейное положение")

    # VII. Социальное положение
    social_status = models.ForeignKey(SocialStatus, on_delete=models.PROTECT, verbose_name="Социальное положение")

    # VIII. Проблема
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT, verbose_name="Проблема")

    # IX. Эмоциональное состояние
    emotional_state = models.ForeignKey(EmotionalState, on_delete=models.PROTECT, verbose_name="Эмоциональное состояние")

    # X. Кризисность — определяется через problem.group (например, 10 или 11)
    # Не отдельное поле, логика в методе

    # XI*. Длительность существования проблемы
    problem_duration = models.ForeignKey(ProblemDuration, on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name="Длительность существования проблемы")

    # XII*. Динамика переживаний
    emotion_dynamics = models.ForeignKey(EmotionDynamics, on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name="Динамика переживаний")

    # XIII. Предоставленная помощь
    help_provided = models.ForeignKey(HelpProvided, on_delete=models.PROTECT, verbose_name="Предоставленная помощь")

    # XIV. Периодичность обращений
    frequency = models.ForeignKey(CallFrequency, on_delete=models.PROTECT, verbose_name="Периодичность обращений")

    # XV. Личный номер консультанта
    consultant = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Консультант"
    )

    # Время создания записи
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Звонок"
        verbose_name_plural = "Звонки"
        ordering = ['-call_date', '-call_time']

    def __str__(self):
        return f"Звонок {self.call_date} {self.call_time} — {self.problem}"

    def is_crisis(self):
        """Проверка, является ли звонок кризисным (по группе проблемы)"""
        crisis_groups = [10, 11]  # Кризис и Суицид
        return self.problem.group.number in crisis_groups

    def is_suicidal(self):
        """Является ли звонок суицидальным?"""
        return self.problem.group.number == 11
