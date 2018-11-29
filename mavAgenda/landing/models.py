from django.db import models
from django.contrib.auth.models import User


class Degree(models.Model):
    """
    @Degree holds the degree a user would have, this includes the
            diploma (i.e Bachelor of Science), type (i.e. major),
            and track (i.e. computer science).
    """
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
    """
    @Requirement holds the required classes for a specific degree, this includes the
            name (i.e Java 1), credits (i.e. 3),
            and degrees (i.e. Bachelor of Science, Major, Computer Science).
    """
    req_name = models.CharField(max_length=50)
    req_credits = models.IntegerField()
    req_degrees = models.ManyToManyField(Degree)


class Course(models.Model):
    """
    @Course holds the systems classes, this includes the
            name (i.e Java 1), subject (i.e. IS&T), semester it is offered in (i.e. Spring and Fall),
            special flag if it has an extra requirement (i.e. lab), comment for any other special
            characteristics (i.e. capstone must be taken in the last semester),
            credits (i.e. 3), and num (1400).
    """
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
    """
    @Campus holds where classes are held, this includes the
            campus name (i.e north campus). This allows for insights on
            the amount of time a student has to get to class.
    """
    N = "North Campus"
    S = "Scott (South) Campus"
    B = "Center Street Campus"
    R = "Remote"
    SPECIAL_TYPE_CHOICE = (
        (N, "North Campus"),
        (S, "Scott (South) Campus"),
        (B, "Center Street Campus"),
        (R, "Remote"),
    )
    campus_name = models.CharField(max_length=30, choices=SPECIAL_TYPE_CHOICE, default=None)


class Building(models.Model):
    """
    @Campus holds where classes are held, this includes the
            building name (i.e PKI), room number(i.e. 156), and campus(i.e. Scott (South) Campus.
            This allows for insights on the amount of time a student has to get to class.
    """
    building_name = models.CharField(max_length=45)
    building_roomNumber = models.CharField(max_length=8)
    building_campus = models.ManyToManyField(Campus)


class Instructor(models.Model):
    """
    @Instructor holds what teachers teach a class, this includes the
            instructors first and last name (i.e Harvey Siy),
            This allows for insights on the teachers available for a student to take.
    """
    instructor_firstName = models.CharField(max_length=20)
    instructor_lastName = models.CharField(max_length=30)


class Weekday(models.Model):
    """
    @Weekday holds what days classes are held, this includes the
            day of the week (i.e Monday, Wednesday). This helps students understand their schedule.
    """
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
    """
    @Offering holds the specific class scheduling information labeled above.
            This is not implemented due to time limits given in the Capstone class,
            however, it is coded to show that the application is extensible.
    """
    offering_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    offering_time = models.CharField(max_length=20)
    offering_location = models.ForeignKey(Building, on_delete=models.CASCADE)
    offering_days = models.ManyToManyField(Weekday)
    offering_sectionNum = models.IntegerField()
    offering_instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)


class Prereq(models.Model):
    """
    @Prereq  holds conditions that are prerequisites to other classes,
            this includes the type (i.e Corequisite or Prerequisite) and a foreign key reference
            back to the Course table.
    """
    C = "Corequisite"
    P = "Prerequisite"
    REQ_CHOICE = (
        (C, "Corequisite"),
        (P, "Prerequisite"),
    )
    prereq_type = models.CharField(max_length=20, choices=REQ_CHOICE, null=True)
    prereq_course = models.ManyToManyField(Course)


class PrereqCourse(models.Model):
    """
    @PrereqCourse  holds classes that are viable condition fulfilling options (prereq classes),
            referring to the Course object itself
    """
    prereqcourse_prereqs = models.ManyToManyField(Prereq)
    prereqcourse_course = models.ManyToManyField(Course)


class Complete(models.Model):
    """
    @Complete  holds classes that a specific user has completed,
            this includes the user and course tables to combine this information.
    """
    complete_user = models.ForeignKey(User, on_delete=models.CASCADE)
    complete_courses = models.ManyToManyField(Course)


class UserPreferences(models.Model):
    """
    @UserPreferences  holds extra information that relates to how a
            user schedules his or her time, this includes
            min and max number of credits a user is willing to take,
            if the user plans on taking summer credits (and how many),
            and the user's more specific preferences for their very next
            semester, as they will have a very good idea of what their schedule
            will look like, they can choose to change their default values for
            number of credits (i.e. 15), when they are available to take a class (i.e. summer, spring, and/or fall),
            what year they will be taking their next semester, and a reference back to the user table.               .
    """
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
