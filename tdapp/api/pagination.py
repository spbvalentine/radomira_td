# pagination.py
from rest_framework.pagination import BasePagination
from rest_framework.response import Response
from django.db import models
from django.db.models import CharField
from django.db.models.functions import Concat, Coalesce
from tdapp import models as app_models  # ← чтобы не конфликтовало с django.db.models

class DataTablesPagination(BasePagination):
    page_size_query_param = 'length'
    max_page_size = 100

    COLUMNS_MAP = [
        'id',
        'call_date',
        'call_time',
        'duration__description',
        'gender__description',
        'age_group__description',
        'marital_status__description',
        'social_status__description',
        'problem__description',
        'problem_duration__description',
        'emotional_state__description',
        'crisis_situation__description',
        'help_provided__description',
        'frequency__description',
        'consultant_full_name',  # ← аннотированное поле
    ]

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request

        # Пагинация
        try:
            start = int(request.query_params.get('start', 0))
        except (ValueError, TypeError):
            start = 0

        try:
            length = int(request.query_params.get(self.page_size_query_param, 10))
        except (ValueError, TypeError):
            length = 10

        length = max(1, min(length, self.max_page_size))

        # Поиск
        search_value = request.query_params.get('search[value]', '').strip()
        if search_value:
            queryset = queryset.filter(
                models.Q(call_date__icontains=search_value) |
                models.Q(duration__description__icontains=search_value) |
                models.Q(gender__description__icontains=search_value) |
                models.Q(age_group__description__icontains=search_value) |
                models.Q(marital_status__description__icontains=search_value) |
                models.Q(social_status__description__icontains=search_value) |
                models.Q(emotional_state__description__icontains=search_value) |
                models.Q(problem__description__icontains=search_value) |
                models.Q(problem_duration__description__icontains=search_value) |
                models.Q(emotion_dynamic__description__icontains=search_value) |
                models.Q(help_provided__description__icontains=search_value) |
                models.Q(frequency__description__icontains=search_value) |
                models.Q(crisis_situation__description__icontains=search_value) |
                models.Q(consultant__username__icontains=search_value) |
                models.Q(consultant__first_name__icontains=search_value) |
                models.Q(consultant__last_name__icontains=search_value)
            )

        # 🧩 Аннотация для сортировки по full_name
        queryset = queryset.annotate(
            consultant_full_name=Coalesce(
                Concat('consultant__first_name', models.Value(' '), 'consultant__last_name'),
                'consultant__username',
                output_field=CharField()
            )
        )

        # 🔁 Сортировка
        order_col = request.query_params.get('order[0][column]')
        order_dir = request.query_params.get('order[0][dir]', 'asc')

        if order_col is not None and order_col.isdigit():
            col_index = int(order_col)
            if 0 <= col_index < len(self.COLUMNS_MAP):
                order_field = self.COLUMNS_MAP[col_index]
                if order_dir == 'desc':
                    order_field = '-' + order_field
                queryset = queryset.order_by(order_field)

        # Подсчёт
        self.recordsTotal = queryset.model.objects.count()
        self.recordsFiltered = queryset.count()

        # Срез
        self.page = queryset[start:start + length]

        return list(self.page)

    def get_paginated_response(self, data):
        draw = self.request.query_params.get('draw', 1)
        return Response({
            'draw': int(draw),
            'recordsTotal': self.recordsTotal,
            'recordsFiltered': self.recordsFiltered,
            'data': data,
            'count': self.recordsFiltered,
            'results': data
        })