from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from myapp.models import Course, Lesson, Payment


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

    def get_course_lessons(self, instance):
        return [lesson.name for lesson in Lesson.objects.filter(course=instance)]

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonListSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'course',)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'method',)
