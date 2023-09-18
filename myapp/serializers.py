from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from myapp.models import Course, Lesson, Payment, Subscription
from myapp.services.create_payment import create_session
from myapp.validators import VideoValidator


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, instance):
        if instance.lesson_set.all():
            return instance.lesson_set.all().count()
        else:
            return 0

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    course_lessons = SerializerMethodField()
    subscription = SerializerMethodField()

    def get_course_lessons(self, instance):
        return [lesson.name for lesson in Lesson.objects.filter(course=instance)]

    def get_subscription(self, instance):
        return Subscription.objects.filter(course=instance).exists()

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoValidator(field='video')]


class LessonListSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'course',)


class PaymentSerializer(serializers.ModelSerializer):
    payment_url = SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'method', 'payment_url')

    def get_payment_url(self, payment):
        return create_session(payment)



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'course', 'is_active')
