from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response

from myapp.models import Course, Lesson, Payment, Subscription
from myapp.paginators import CoursePaginator, LessonPaginator
from myapp.permissions import IsOwner, IsModerator
from myapp.serializers import CourseSerializer, LessonSerializer, LessonListSerializer, PaymentSerializer, \
    CourseDetailSerializer, SubscriptionSerializer
from myapp.services.create_payment import create_session
from myapp.tasks import send_message_about_changes
from users.models import UserRoles


# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    default_serializer = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    serializer_classes = {
        "retrieve": CourseDetailSerializer
    }

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.role == UserRoles.MODERATOR:
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()
        return_serializer = CourseSerializer(new_course)
        headers = self.get_success_headers(return_serializer.data)
        return Response(
            return_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        subscribers = Subscription.objects.filter(course=new_lesson.course)
        user_emails = [subscriber.user.email for subscriber in subscribers]
        send_message_about_changes.delay(new_lesson.course.name, user_emails)
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator | IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'owner',)
    ordering_fields = ('name',)
    pagination_class = LessonPaginator

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator | IsAdminUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator | IsAdminUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]



class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.save()




class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'method')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAdminUser]


# Subscription
class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAdminUser | IsOwner]
