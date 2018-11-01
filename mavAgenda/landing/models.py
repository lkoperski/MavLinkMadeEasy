from django.db import models
from django.contrib.auth.models import User

class Degree(models.Model):
    BS = 'Bachelor of Science'
    MS = 'Master of Science'
    PhDS = 'Doctor of Science'
    DIPLOMA_CHOICE = (
        (BS, 'Bachelor of Science'),
        (MS, 'Master of Science'),
        (PhDS, 'Doctor of Science'),
    )
    degree_diploma = models.CharField(max_length=50, choices=DIPLOMA_CHOICE, default=BS)
    MAJ = 'Major'
    MIN = 'Minor'
    CON = 'Concentration'
    TYPE_CHOICE = (
        (MAJ, 'Major'),
        (MIN, 'Minor'),
        (CON, 'Concentration'),
    )
    degree_type = models.CharField(max_length=50, choices=TYPE_CHOICE, default=MAJ)
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
    degree_track = models.CharField(max_length=50, choices=TRACK_CHOICE, default=CSCI)
    degree_users = models.ManyToManyField(User)

class Requirement(models.Model):
    req_name = models.CharField(max_length=50)
    req_credits = models.IntegerField()
    req_degrees = models.ManyToManyField(Degree)

class Course(models.Model):
    course_name = models.CharField(max_length=75)
    course_subject = models.CharField(max_length=15)
    course_num = models.CharField(max_length=15)
    A = "All"
    S = "Spring"
    F = "Fall"
    M = "Summer"
    Y = "Year-Only"
    P = "Spring/Summer"
    H = "Fall/Summer"
    SEM_CHOICE = (
        (A, "All"),
        (S, "Spring"),
        (F, "Fall"),
        (M, "Summer"),
        (Y, "Year-Only"),
        (P, "Spring/Summer"),
        (H, "Fall/Summer"),
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
    course_special = models.CharField(max_length=15, choices=SPECIAL_TYPE_CHOICE, default=None)
    course_comment = models.CharField(max_length=200, blank=True)
    course_requirements = models.ManyToManyField(Requirement)

class Campus(models.Model):
    N = "North Campus"
    S = "Scott (South) Campus"
    B = "Center Street Campus"
    SPECIAL_TYPE_CHOICE = (
        (N, "North Campus"),
        (S, "Scott (South) Campus"),
        (B, "Center Street Campus"),
    )
    campus_name = models.CharField(max_length=30, choices=SPECIAL_TYPE_CHOICE, default=None)

class Building(models.Model):
    building_name = models.CharField(max_length=45)
    building_roomNumber = models.CharField(max_length=8)
    building_campus = models.ManyToManyField(Campus)

class Instructor(models.Model):
    instructor_firstName = models.CharField(max_length=20)
    instructor_lastName = models.CharField(max_length=30)

class Weekday(models.Model):
    M = "Monday"
    T = "Tuesday"
    W = "Wednesday"
    R = "Thursday"
    F = "Friday"
    S = "Saturday"
    U = "Sunday"
    DAY_CHOICE = (
        (M, "Monday"),
        (T, "Tuesday"),
        (W, "Wednesday"),
        (R, "Thursday"),
        (F, "Friday"),
        (S, "Saturday"),
        (U, "Sunday"),
    )
    weekday_name = models.CharField(max_length=10, choices=DAY_CHOICE, default=None)


class Offering(models.Model):
    offering_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    offering_time = models.CharField(max_length=20)
    offering_location = models.ForeignKey(Building, on_delete=models.CASCADE)
    offering_days = models.ManyToManyField(Weekday)
    offering_sectionNum = models.IntegerField()
    offering_instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

class Prereq(models.Model):
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
    pref_nextSSF = models.CharField(max_length=10, null=True)
    pref_nextYear = models.IntegerField(null=True)
    pref_nextSemMinCredit = models.IntegerField(null=True)
    pref_nextSemMaxCredit = models.IntegerField(null=True)
    pref_user = models.ForeignKey(User, on_delete=models.CASCADE)