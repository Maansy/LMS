from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.base import ContentFile
from .models import Certificate
from .serializers import CertificateSerializer
from courses.models import Enrollment, LessonProgress, Course
from django.utils import timezone
import io
from reportlab.pdfgen import canvas

class CertificateListView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user)

class GenerateCertificateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            if not LessonProgress.objects.filter(enrollment=enrollment, completed=False).exists():
                certificate, created = Certificate.objects.get_or_create(student=request.user, course=course)
                if created:
                    buffer = io.BytesIO()
                    p = canvas.Canvas(buffer)
                    p.drawString(100, 750, f"Certificate of Completion")
                    p.drawString(100, 725, f"Course: {course.name}")
                    p.drawString(100, 700, f"Student: {request.user.username}")
                    p.drawString(100, 675, f"Date: {timezone.now().strftime('%Y-%m-%d')}")
                    p.showPage()
                    p.save()
                    buffer.seek(0)
                    certificate.certificate_file.save(f'certificate_{course_id}_{request.user.id}.pdf', ContentFile(buffer.read()), save=True)
                serializer = CertificateSerializer(certificate)
                return Response(serializer.data)
            else:
                return Response({"detail": "Not all lessons are completed"}, status=400)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)
        except Enrollment.DoesNotExist:
            return Response({"detail": "Enrollment not found"}, status=404)
