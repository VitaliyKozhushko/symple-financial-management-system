"""
Модуль с роутами для транзакций и формирования отчетов
"""
from django.urls import path
from .views import (GenerateReportView,
                    ReportDownloadView)

urlpatterns = [
    path('report/', GenerateReportView.as_view(), name='generate_report'),
    path('report/<str:task_id>/', ReportDownloadView.as_view(),
         name='report_download'),
]
