from django.urls import path
from rest_framework.routers import DefaultRouter

from myapp.apps import MyappConfig
from myapp.views import CourseViewSet, PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView, \
    PaymentUpdateAPIView, PaymentDestroyAPIView
from myapp.views import LessonCreateAPIView, LessonListAPIView, LessonUpdateAPIView, LessonRetrieveAPIView, \
    LessonDestroyAPIView

app_name = MyappConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
                  path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
                  path('lessons/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('lessons/delete/<int:pk', LessonDestroyAPIView.as_view(), name='lesson_delete'),

                  path('payments/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
                  path('payments/', PaymentListAPIView.as_view(), name='payment_list'),
                  path('payments/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_get'),
                  path('payments/update/<int:pk>', PaymentUpdateAPIView.as_view(), name='payment_update'),
                  path('payments/delete/<int:pk', PaymentDestroyAPIView.as_view(), name='payment_delete')
              ] + router.urls
