from django.db import models


class SchoolStructure(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='self')


class Schools(models.Model):
    title = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.title


class Classes(models.Model):
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, null=False, blank=False, related_name='classes')
    class_order = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"Class {self.class_order} of {self.school}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['school', 'class_order'], name='unique_school_order')
        ]


class Personnel(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    school_class = models.ForeignKey(Classes, on_delete=models.CASCADE, null=False, blank=False, related_query_name='personnel')
    personnel_type = models.IntegerField(default=2, null=False, blank=False,
                                         choices=((0, "teacher"),  (1, "head_of_the_room"), (2, "student")))

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Subjects(models.Model):
    title = models.CharField(max_length=50, unique=True, null=False, blank=False)


class StudentSubjectsScore(models.Model):
    student = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=False, blank=False, related_name='student_score')
    subjects = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=False, blank=False)
    credit = models.IntegerField(null=False, blank=False)
    score = models.FloatField(null=False, blank=False, default=0)

    @property
    def grade(self):
        grade = ''
        score = self.score

        if score >= 80:
            grade = 'A'
        elif score >= 75:
            grade = 'B+'
        elif score >= 70:
            grade = 'B'
        elif score >= 65:
            grade = 'C+'
        elif score >= 60:
            grade = 'C'
        elif score >= 55:
            grade = 'D+'
        elif score >= 50:
            grade = 'D'
        else:
            grade = 'F'
        
        return grade

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'subjects'], name='unique_subject_score')
        ]
