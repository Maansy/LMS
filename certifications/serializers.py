# certifications/serializers.py

from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'student', 'course', 'issued_at', 'certificate_file']
        read_only_fields = ['student', 'course', 'issued_at', 'certificate_file']
