from django.urls import path
from .views import CertificateListView, GenerateCertificateView

urlpatterns = [
    path('certificates/', CertificateListView.as_view(), name='certificate-list'),
    path('certificates/generate/<int:course_id>/', GenerateCertificateView.as_view(), name='generate-certificate'),
]
