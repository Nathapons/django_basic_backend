from rest_framework import serializers
from django.db.models import Avg
from .models import Personnel, SchoolStructure, Schools, StudentSubjectsScore, Subjects


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    school = serializers.CharField(source='school_class.school.title')

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = Personnel
        fields = ('id', 'full_name', 'school', )


class SubjectDetailSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subjects.title')
    credit = serializers.SerializerMethodField()
    score = serializers.FloatField()
    grade = serializers.SerializerMethodField()

    def get_credit(self, obj):
        credit = obj.credit
        if credit:
            return Subjects.objects.get(id=credit).title
        return ''

    def get_grade(self, obj):
        return obj.grade

    class Meta:
        model = StudentSubjectsScore
        fields = ('subject', 'credit', 'score', 'grade')


class StudentSubjectsScoreDetailsSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    subject_detail = serializers.SerializerMethodField()
    grade_point_average = serializers.SerializerMethodField()

    def get_student(self, obj):
        serializer = StudentSerializer(obj)
        return serializer.data

    def get_subject_detail(self, obj):
        student_subject_scores = obj.student_score.all()
        serializer = SubjectDetailSerializer(student_subject_scores, many=True)
        return serializer.data

    def get_grade_point_average(self, obj):
        student_subject_scores = obj.student_score.all()
        return student_subject_scores.aggregate(grade_avg=Avg('score'))['grade_avg']

    class Meta:
        model = Personnel
        fields = ('student', 'subject_detail', 'grade_point_average')


class SchoolHierarchySerializer(serializers.ModelSerializer):
    school = serializers.CharField(source='title')
    class1 = serializers.SerializerMethodField()
    class2 = serializers.SerializerMethodField()
    class3 = serializers.SerializerMethodField()
    class4 = serializers.SerializerMethodField()
    class5 = serializers.SerializerMethodField()

    def get_class1(self, obj):
        return 'class1'

    def get_class2(self, obj):
        return 'class1'

    def get_class3(self, obj):
        return 'class1'

    def get_class4(self, obj):
        return 'class1'

    def get_class5(self, obj):
        return 'class1'

    class Meta:
        model = Schools
        fields = ('school', )


class SubSchoolStructureSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    sub = serializers.SerializerMethodField()

    def get_sub(self, obj):
        return obj.self.all().values('title')

    class Meta:
        model = SchoolStructure
        fields = ('title', 'sub', )


class SchoolStructureSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    sub = serializers.SerializerMethodField()

    def get_sub(self, obj):
        sub_school_structures = obj.self.all()
        serializer = SubSchoolStructureSerializer(sub_school_structures, many=True)
        return serializer.data

    class Meta:
        model = SchoolStructure
        fields = ('title', 'sub', )
