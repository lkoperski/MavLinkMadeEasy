from django.db import models
from django.contrib.auth.models import User

#class User(models.Model):
    #userPK = models.IntegerField()
    #username = models.CharField(max_length=75)
    #password = models.CharField(max_length=75)

class Degree(models.Model):
    BS = 'Bachelor of Science'
    MS = 'Master of Science'
    PhDS = 'Doctor of Science'
    DIPLOMA_CHOICE = (
        (BS, 'Bachelor of Science'),
        (MS, 'Master of Science'),
        (PhDS, 'Doctor of Science'),
    )
    degree_diploma = models.CharField( max_length=50, choices=DIPLOMA_CHOICE, default=BS)
    MAJ = 'Major'
    MIN = 'Minor'
    CON = 'Concentration'
    TYPE_CHOICE = (
        (MAJ, 'Major'),
        (MIN, 'Minor'),
        (CON, 'Concentration'),
    )
    degree_type = models.CharField( max_length=50, choices=TYPE_CHOICE, default=MAJ )
    CSCI = 'Computer Science'
    MIS = 'Management Information Systems'
    BIOI = 'Bioinformatics'
    ITIN = 'IT Innovation'
    CYBR = 'Cybersecurity'
    TRACK_CHOICE = (
        (CSCI, 'Computer Science'),
        (MIS, 'Management Information Systems'),
        (BIOI, 'Bioinformatics'),
        (ITIN, 'IT Innovation'),
        (CYBR, 'Cybersecurity'),
    )
    degree_track = models.CharField( max_length=50, choices=TRACK_CHOICE, default=CSCI )
    degree_users = models.ManyToManyField(User)

class Requirement(models.Model):
    #req_pk = models.IntegerField()
    req_name = models.CharField(max_length=50)
    req_credits = models.IntegerField()
    req_degrees = models.ManyToManyField(Degree)

class Course(models.Model):
    #course_pk = models.IntegerField()
    course_name = models.CharField(max_length=75)
    course_num = models.CharField(max_length=15)
    A = "All"
    S = "Spring"
    F = "Fall"
    M = "Summer"
    SEM_CHOICE = (
        (A, "All"),
        (S, "Spring"),
        (F, "Fall"),
        (M, "Summer"),
    )
    course_semester = models.CharField(max_length=10, choices=SEM_CHOICE, default=A)
    course_credits = models.IntegerField()
    N = "No"
    Y = "Lab"
    W = "Waiver"
    SPECIAL_TYPE_CHOICE = (
        (N, "No"),
        (Y, "Lab"),
        (W, "Waiver"),
    )
    course_special = models.CharField(max_length=15, choices=SPECIAL_TYPE_CHOICE, default=N)
    course_comment = models.CharField(max_length=200, blank=True)
    course_requirements = models.ForeignKey(Requirement, on_delete=models.CASCADE)

class Prereq(models.Model):
    #prereq_pk = models.IntegerField
    C = "Corequisite"
    P = "Prerequisite"
    REQ_CHOICE = (
        (C, "Corequisite"),
        (P, "Prerequisite"),
    )
    prereq_type = models.CharField(max_length=20, choices=REQ_CHOICE, null=True)
    prereq_courses = models.ManyToManyField(Course)

class Complete(models.Model):
    complete_user = models.ForeignKey(User, on_delete=models.CASCADE)
    complete_courses = models.ManyToManyField(Course)

class UserPreferences(models.Model):
    pref_minCredits = models.IntegerField()
    pref_maxCredits = models.IntegerField()
    pref_summer = models.BooleanField()
    pref_summerMinCredits = models.IntegerField()
    pref_summerMaxCredits = models.IntegerField()
    pref_user = models.ForeignKey(User, on_delete=models.CASCADE)

#class UserDegree(models.Model):
    #user_pk = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    #degree_pk = models.ForeignKey(Degree, on_delete=models.CASCADE)

#class DegreeReq(models.Model):
    #degree_pk = models.ForeignKey(Degree, primary_key=True,on_delete=models.CASCADE)
    #requirement_pk = models.ForeignKey(Requirement, primary_key=True, on_delete=models.CASCADE)

#class RequirementCourse(models.Model):
    #requirement_pk=models.ForeignKey(Requirement, primary_key=True, on_delete=models.CASCADE)
    #course_pk=models.ForeignKey(Course, primary_key=True, on_delete=models.CASCADE)

#class CoursePreqreq(models.Model):
    #course_pk=models.ForeignKey(Course, primary_key=True, on_delete=models.CASCADE)
    #prereq_pk=models.ForeignKey(Prereq, primary_key=True, on_delete=models.CASCADE)

#class PrereqCourse(models.Model):
    #prereq_pk = models.ForeignKey(Prereq, primary_key=True, on_delete=models.CASCADE)
    #course_pk = models.ForeignKEey(Course, preimary_key=True, on_delete=models.CASCADE)