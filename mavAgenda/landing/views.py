from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import *
from .models import *
from django.contrib.auth.models import User

from datetime import datetime

'''
@getUserByEmail searches the User table to find the User object with a corresponding email
@param e: the email being searched for
'''
def getUserByEmail(e):
    userTable = User.objects.all()
    for cu in userTable:
        if cu.username == e:
            return cu

'''
@getDegree searches the Degree table to find the Degree object with corresponding degree and major
@param d: degree attribute of Degree being searched for
@param m: major attribute of Degree being searched for
'''
def getDegree(d, m):
    degreeTable = Degree.objects.all()
    for deg in degreeTable:
        if deg.major == m and deg.degree == d:
            return deg

'''
@getCompletedByUser provides a list of Course (objects) the user has taken
@param uID: the primary key corresponding to the active user
'''
def getCompletedByUser(uID):
    cu = User.objects.get(pk=uID)
    completedCourses = []
    for cc in Complete.objects.get(user=cu).complete.all():
        completedCourses.append(cc)
    return completedCourses

'''
@getCoursesForUser provides a list of Course (objects) the user must complete for their respective Degree
@param uID: the primary key corresponding to the active user
'''
def getCoursesForUser(uID):
    requiredCourses = []
    reqs = Degree.objects.get(user=uID).req.all()
    for r in reqs:
        catalog = r.course.all()
        for g in catalog:
            requiredCourses.append(g)
            prereqs = Course.objects.get(id=g.id).prereqs.all()
            for pr in prereqs:
                additionalCourse = Course.objects.get(id=pr.prereq.id)
                if additionalCourse not in requiredCourses:
                    requiredCourses.append(additionalCourse)
    return requiredCourses

'''
@removeCoursesTaken provides a list of Course (objects) the user must still take (required, but not completed classes)
@param requiredClasses: a list of Course (objects) required for the User's Degree
@param classesTaken: a list of Course (objects) that the User has already completed
'''
def removeCoursesTaken( requiredClasses, classesTaken ):
    validCourses = []
    for rc in requiredClasses:
        if rc not in classesTaken :
            validCourses.append(rc)
    return validCourses

'''
@checkPrereqsMet determines if the User has met all Prereqs for a particular Course
@param prereqs: a list of Course (objects) corresponding to Prereqs for a given Course
@param classesTaken: a list of Course (objects) that the User has already completed
@parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
'''
def checkPrereqsMet(preqreqs, classesTaken, currentSemester):
    met = True
    for pr in preqreqs:
        notInClassesTaken = pr.prereq not in classesTaken and pr.this_or not in classesTaken
        inCurrentSemester = pr.prereq in currentSemester or pr.this_or in currentSemester
        if notInClassesTaken:
            met = False
            break
        elif inCurrentSemester:
            met = False
            break
    return met

'''
@checkOfferedSemester determines if a given Course if offered during the current semester
@param course: the Course under test
@param ssf: the Spring, Summer, Fall, offering attribute of the Course
'''
def checkOfferedSemester(course, ssf):
    offered = False
    if course.semester == ssf or course.semester == 'All':
        offered = True
    return offered

'''
@checkCourseValid determines if a given Course can be taken during a given semester
@param course: the Course under test
@param classesTaken: a list of Course (objects) that the User has already completed
@parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
@param ssf: the Spring, Summer, Fall, offering attribute of the Course
'''
def checkCourseValid(course, classesTaken, semesterCourses, ssf): #checkCourseValid( nc, classesTaken, semesterCourses, ssfSemester )
    valid = False
    prereqs = course.prereqs.all()
    prereqsMet = checkPrereqsMet(prereqs, classesTaken, semesterCourses)
    offered = checkOfferedSemester(course, ssf)
    if prereqsMet and offered:
        valid = True
    return valid

'''
@getSemesterByMonthYear determines semester (Spring, Summer, Fall) according to current month
@param m: current month
'''
def getSemesterByMonthYear( m ):
    if  m < 5 :
        title = "Spring"
    elif  m < 8 :
        title = "Summer"
    else:
        title = "Fall"
    return title

'''
@generateNewSemester creates a new logical semester
@param semester: previous semester list
'''
def generateNewSemester(semester):
    ssf = semester[0]
    nextSemester = ""
    y = semester[1]
    if ssf == "Spring" :
        nextSemester = "Summer"
    elif ssf == "Summer" :
        nextSemester = "Fall"
    else:
        nextSemester ="Spring"
        y += 1
    semester[0] = nextSemester
    semester[1] = y
    semester[2] = []
    return semester

'''
@isFull determines if a semester has hit the maximum number of credits allowable
@param courseList: list of Course (objects) the user is scheduled to take during current semester
'''
def isFull(courseList):
    full = False
    totalCredits = 0
    for c in courseList:
        totalCredits+= c.credits
    if totalCredits >= 12 and totalCredits <= 16:
        full = True
    return full

'''
@createSchedule generates semester-by-semester schedule for User's needed Courses according to Degree
@param uID: primary key associated with active user
'''
def createSchedule(uID):
    loopCount = 0
    maxLoopCount = 35
    reqTracker = [] #used to track if Req credit quotas have been met
    requiredClasses = getCoursesForUser(uID)
    reqs = Degree.objects.get(user=uID).req.all()
    for r in reqs:
        req_id = r.id
        req_name = r.name
        req_type = r.req_type
        req_creds = r.credits
        req_start = 0
        reqTracker.append([req_id, req_name, req_type, req_creds, req_start])
    classesTaken = getCompletedByUser(uID)
    neededClasses = removeCoursesTaken( requiredClasses, classesTaken )
    schedule = []
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    ssfSemester = getSemesterByMonthYear(currentMonth)
    semester = [ssfSemester, currentYear, []]
    currentSemester = generateNewSemester(semester)
    scheduleComplete = True
    for c in classesTaken:
        for r in reqTracker:  # determine which Req this course falls under
            if c in Req.objects.get(id=r[0]).course.all():
                r[4] += c.credits  # increment the completed running total for that Req
    while neededClasses != [] and loopCount < maxLoopCount:
        loopCount+=1
        for nc in neededClasses:
            if ( checkCourseValid( nc, classesTaken, currentSemester[2], ssfSemester ) ):
                currentSemester[2].append(nc)
                classesTaken.append(nc)
                neededClasses.remove(nc)
                for r in reqTracker: # determine which Req this course falls under
                    if nc in Req.objects.get(id=r[0]).course.all():
                        r[4]+=nc.credits # increment the completed running total for that Req
            if ( neededClasses != [] and isFull(semester[2])):
                schedule.append(semester[:])
                semester = generateNewSemester(semester)
                break
            scheduleComplete = True
            for r in reqTracker:
                if r[3] > r[4]:
                    scheduleComplete = False
        if scheduleComplete:
            print( "BREAKING FREEEEEEE!!!!")
            break
    return schedule

'''
@generateCheckBoxEntities creates a list of tuples of requirements, course names and numbers for the selectcourses page
@param uID: primary key corresponding to the active user
'''
def generateCheckBoxEntities(uID):
    reqs = Degree.objects.get(user=uID).req.all()
    checkBoxEntities = []
    for r in reqs:
        req_id = r.id
        req_name = r.name
        req_type = r.req_type
        req_creds = r.credits
        catalog = r.course.all()
        courseList = []
        for g in catalog:
            number = g.num
            name = g.name
            creds = g.credits
            courseList.append([number,name,creds])
        checkBoxEntities.append([req_id, req_name, req_type, req_creds, courseList])
    return checkBoxEntities

'''
@generateMajorDD creates a list of possible majors for use on the createuser page
'''
def generateMajorDD():
    allDegrees = Degree.objects.all()
    majors = []
    for d in allDegrees:
        if d.degree_type == "MAJ" and d.degree_track not in majors:
            majors.append(d.degree_track)
    return majors

def generateMinorDD():
    allDegrees = Degree.objects.all()
    minors = []
    for d in allDegrees:
        if d.degree_type == "MIN" and d.degree_track not in minors:
            minors.append(d.degree_track)
    return minors

def generateConcentrationsDD():
    allDegrees = Degree.objects.all()
    concentrations = []
    for d in allDegrees:
        if d.degree_type == "CON" and d.degree_track not in concentrations:
            concentrations.append(d.degree_track)
    return concentrations

def generateDiplomaDD():
    allDegrees = Degree.objects.all()
    diplomas = []
    for d in allDegrees:
        if d.degree_diploma not in diplomas:
            diplomas.append(d.degree_diploma)
    return diplomas

'''
@emailFound provides feedback if the email is already in the User database table
@param email: email under test
'''
def emailFound(email):
    found = False
    userTable = User.objects.all()
    for cu in userTable:
        if cu.email == email:
            found = True
    return found

'''
@saveClassesToUser updates database with a list of the user has taken
@param classesChecked: list of courses the user specified as having taken
@param uID: pk of the associated active user
'''
def saveClassesToUser(classesChecked, uID):
    u = User.objects.get(pk=uID)
    if u in Complete.objects.all():
        completed = Complete.objects.get(user_id=u)
    else:
        completed = Complete(user=u)
        completed.save()
    for cc in classesChecked:
        c = Course.objects.get(num=cc)
        completed.complete.add(c)
        completed.save()

'''
@removeUserCompletedEntries updates database to remove courses completed from a particular user
@param uID: pk of the associated active user
'''
def removeUserCompletedEnteries(uID):
    u = User.objects.get(pk=uID)
    completedTable = Complete.objects.all()
    for ce in completedTable:
        if ce.user == u:
            ce.delete()


########################################################################################################################
########################################################################################################################

'''
@login send a request to render the login.html page
@param request: generates the response
'''
def login(request):
    if request.method == "POST":
        e = request.POST['email-input']
        if emailFound(e):
            u = getUserByEmail(e)
            userID = u.id
            return HttpResponseRedirect(reverse('landing:schedule', args=(userID,)))
        else:
            message = "Email not found"
            return render(request, 'landing/login.html', {'message':message})
    else:
        return render(request, 'landing/login.html' )

'''
@selectcourses send a request to render the selectcourses.html page
@param request: generates the response
@param pk: primary key corresponding to active user
'''
def selectcourses(request, pk):
    if request.method == "POST":
        removeUserCompletedEnteries(pk)
        classesChecked = request.POST.getlist('chexmix')
        saveClassesToUser(classesChecked, pk)
        return HttpResponseRedirect(reverse('landing:schedule', args=(pk,)))
    else:
        checkBoxes = generateCheckBoxEntities(pk)
        # might need to write some logic here to determine if boxes have already been checked :)
    return render(request, 'landing/selectcourses.html', {'checkBoxes': generateCheckBoxEntities(pk)})

'''
@schedule send a request to render the schedule.html page
@param request: generates the response
@param pk: primary key corresponding to active user
'''
def schedule(request, pk):
    return render(request, 'landing/schedule.html', {'schedule': createSchedule(pk), 'userID': pk})

'''
@createuser send a request to render the createuser.html page
@param request: generates the response
'''
def createuser(request):
    if request.method == "POST":
        e = request.POST['email-input']
        p = request.POST['password-input']
        u = User(username=e, password=p)
        u.save()
        userID = u.id
        i = 1
        while True:
            diploma = 'id_d-diploma' + str(i)
            major = 'id_d-major-' + str(i)
            if major in request.POST:
                    print(diploma)
                    print(major) #this is where we will actually update the db
                    i+=1
            else:
                break
        i = 1
        while True:
            minor = 'id_d-minor' + str(i)
            if minor in request.POST:
                    print(minor) #this is where we will actually update the db
                    i+=1
            else:
                break
        i = 1
        while True:
            concentration = 'id_d-concentration' + str(i)
            if concentration in request.POST:
                print(concentration)  # this is where we will actually update the db
                i += 1
            else:
                break
        return HttpResponseRedirect(reverse('landing:selectcourses', args=(userID,)))
    else:
        return render(request, 'landing/createuser.html',
                      {'diplomas':generateDiplomaDD(), 'majors':generateMajorDD(), 'minors':generateMinorDD(), 'concentrations':generateConcentrationsDD() }
                      )
