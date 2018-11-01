from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import _datetime

from .forms import *
from .models import *
from django.contrib.auth.models import User

from datetime import datetime

def getUserByEmail(e):
    '''
    @getUserByEmail searches the User table to find the User object with a corresponding email
    @param e: the email being searched for
    '''
    userTable = User.objects.all()
    for cu in userTable:
        if cu.username == e:
            return cu

def getDegree(diploma, type, track):
    '''
    @getDegree searches the Degree table to find the Degree object with corresponding degree and major
    @param diploma: degree attribute of Degree being searched for (bachelors, masters, doctorate)
    @param type: degree attribute of Degree being searched for (science, art)
    @param track: major attribute of Degree being searched for (computer science, MIS, etc)
    '''
    degreeTable = Degree.objects.all()
    for deg in degreeTable:
        if deg.degree_diploma == diploma and deg.degree_type == type and deg.degree_track == track:
            return deg

def getCompletedByUser(uID):
    '''
    @getCompletedByUser provides a list of Course (objects) the user has taken
    @param uID: the primary key corresponding to the active user
    '''
    cu = User.objects.get(pk=uID)
    completedCourses = []
    for cc in Complete.objects.get(user=cu).complete.all():
        completedCourses.append(cc)
    return completedCourses

def getCoursesForUser(uID):
    '''
    @getCoursesForUser provides a list of Course (objects) the user must complete for their respective Degree
    @param uID: the primary key corresponding to the active user
    '''
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

def removeCoursesTaken( requiredClasses, classesTaken ):
    '''
    @removeCoursesTaken provides a list of Course (objects) the user must still take (required, but not completed classes)
    @param requiredClasses: a list of Course (objects) required for the User's Degree
    @param classesTaken: a list of Course (objects) that the User has already completed
    '''
    validCourses = []
    for rc in requiredClasses:
        if rc not in classesTaken :
            validCourses.append(rc)
    return validCourses

def checkPrereqsMet(preqreqs, classesTaken, currentSemester):
    '''
    @checkPrereqsMet determines if the User has met all Prereqs for a particular Course
    @param prereqs: a list of Course (objects) corresponding to Prereqs for a given Course
    @param classesTaken: a list of Course (objects) that the User has already completed
    @parm currentSemester: a list of Course (objects) the scheduling algorithm has accounted for already
    '''
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

def checkOfferedSemester(course, ssf):
    '''
    @checkOfferedSemester determines if a given Course if offered during the current semester
    @param course: the Course under test
    @param ssf: the Spring, Summer, Fall, offering attribute of the Course
    '''
    offered = False
    if course.semester == ssf or course.semester == 'All':
        offered = True
    return offered

def checkCourseValid(course, classesTaken, semesterCourses, ssf): #checkCourseValid( nc, classesTaken, semesterCourses, ssfSemester )
    '''
    @checkCourseValid determines if a given Course can be taken during a given semester
    @param course: the Course under test
    @param classesTaken: a list of Course (objects) that the User has already completed
    @parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
    @param ssf: the Spring, Summer, Fall, offering attribute of the Course
    '''
    valid = False
    prereqs = course.prereqs.all()
    prereqsMet = checkPrereqsMet(prereqs, classesTaken, semesterCourses)
    offered = checkOfferedSemester(course, ssf)
    if prereqsMet and offered:
        valid = True
    return valid

def getSemesterByMonthYear( m ):
    '''
    @getSemesterByMonthYear determines semester (Spring, Summer, Fall) according to current month
    @param m: current month
    '''
    if  m < 5 :
        title = "Spring"
    elif  m < 8 :
        title = "Summer"
    else:
        title = "Fall"
    return title

def generateNewSemester(semester):
    '''
    @generateNewSemester creates a new logical semester
    @param semester: previous semester list
    '''
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

def isFull(courseList):
    '''
    @isFull determines if a semester has hit the maximum number of credits allowable
    @param courseList: list of Course (objects) the user is scheduled to take during current semester
    '''
    full = False
    totalCredits = 0
    for c in courseList:
        totalCredits+= c.credits
    if totalCredits >= 12 and totalCredits <= 16:
        full = True
    return full

def createSchedule(uID):
    '''
    @createSchedule generates semester-by-semester schedule for User's needed Courses according to Degree
    @param uID: primary key associated with active user
    '''
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

def getDegreeReqs(degrees):
    '''
    @getDegreeRegs returns a list of requirements for all degrees a user has selected
    @param degrees: a list of degrees associated with the user
    '''
    requirements = []
    for d in degrees:
        requirement = d.req.all()
        if requirement not in requirements:
            requirements.append(requirement)
    return requirements

def generateCheckBoxEntities(uID):
    '''
    @generateCheckBoxEntities creates a list of tuples of requirements, course names and numbers for the selectcourses page
    @param uID: primary key corresponding to the active user
    '''
    degrees = Degree.objects.get(degree_users=uID).all()
    reqs = getDegreeReqs(degrees)
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

def generateMajorDD():
    '''
    @generateMajorDD creates a list of possible majors for use on the createuser page
    '''
    allDegrees = Degree.objects.all()
    majors = []
    for d in allDegrees:
        if d.degree_type == "MAJ" and d.degree_track not in majors:
            majors.append(d.degree_track)
    return majors

def generateMinorDD():
    '''
    @generateMinorDD creates a list of possible minors for use on the createuser page
    '''
    allDegrees = Degree.objects.all()
    minors = []
    for d in allDegrees:
        if d.degree_type == "MIN" and d.degree_track not in minors:
            minors.append(d.degree_track)
    return minors

def generateConcentrationsDD():
    '''
    @generateConcentrationsDD creates a list of possible concentrations for use on the createuser page
    '''
    allDegrees = Degree.objects.all()
    concentrations = []
    for d in allDegrees:
        if d.degree_type == "CON" and d.degree_track not in concentrations:
            concentrations.append(d.degree_track)
    return concentrations

def generateDiplomaDD():
    '''
    @generateDiplomaDD creates a list of possible diplomas for use on the createuser page
    '''
    allDegrees = Degree.objects.all()
    diplomas = []
    for d in allDegrees:
        if d.degree_diploma not in diplomas:
            diplomas.append(d.degree_diploma)
    return diplomas

def generateYearDD():
    '''
    @generateYearDD creates a list of upcoming years for use on the createuser page
    '''
    years = []
    date = datetime.now()
    currentYear = date.year
    years.append(currentYear)
    years.append(currentYear+1)
    years.append(currentYear+2)
    years.append(currentYear+3)
    return years

def emailFound(email):
    '''
    @emailFound provides feedback if the email is already in the User database table
    @param email: email under test
    '''
    found = False
    userTable = User.objects.all()
    for cu in userTable:
        if cu.username == email:
            found = True
    return found

def saveClassesToUser(classesChecked, uID):
    '''
    @saveClassesToUser updates database with a list of the user has taken
    @param classesChecked: list of courses the user specified as having taken
    @param uID: pk of the associated active user
    '''
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

def removeUserCompletedEnteries(uID):
    '''
    @removeUserCompletedEntries updates database to remove courses completed from a particular user
    @param uID: pk of the associated active user
    '''
    u = User.objects.get(pk=uID)
    completedTable = Complete.objects.all()
    for ce in completedTable:
        if ce.user == u:
            ce.delete()


########################################################################################################################
########################################################################################################################

def login(request):
    '''
    @login send a request to render the login.html page
    @param request: generates the response
    '''
    if request.method == "POST":
        e = request.POST['email-input']
        if emailFound(e):
            u = getUserByEmail(e)
            userID = u.id
            return HttpResponseRedirect(reverse('landing:schedule', args=(userID,)))
        else:
            message = "Email not found" # TODO - this is not working properly... it somehow does a check first?
            return render(request, 'landing/login.html', {'message':message})
    else:
        return render(request, 'landing/login.html' )

def createuser(request):
    '''
    @createuser send a request to render the createuser.html page
    @param request: generates the response
    '''
    if request.method == "POST": #TODO - need to confirm that at least one major was submitted!
        e = request.POST['email-input']
        if not emailFound(e) :
            p = request.POST['password-input']
            u = User(username=e, password=p)
            u.save()
            userID = u.id
            i = 1
            while True:
                diploma = 'id_d-diploma-' + str(i)
                major = 'id_d-major-' + str(i)
                if major in request.POST:
                    dip = request.POST[diploma]
                    maj = request.POST[major]
                    desiredDegree = getDegree(dip,"MAJ",maj)
                    desiredDegree.degree_users.add(u)
                    i+=1
                else:
                    break
            i = 1
            while True:
                diploma = 'id_d-diploma-1'
                minor = 'id_d-minor-' + str(i)
                if minor in request.POST:
                    dip = request.POST[diploma]
                    min = request.POST[minor]
                    desiredDegree = getDegree(dip, "MIN", min)
                    desiredDegree.degree_users.add(u)
                    i+=1
                else:
                    break
            i = 1
            while True:
                diploma = 'id_d-diploma-1'
                concentration = 'id_d-concentration-' + str(i)
                if concentration in request.POST:
                    dip = request.POST[diploma]
                    con = request.POST[concentration]
                    desiredDegree = getDegree(dip, "CON", con)
                    desiredDegree.degree_users.add(u)
                    i+=1
                else:
                    break
            prefSummer = request.POST['summer-course']
            sumMin = 0
            sumMax = 0
            if prefSummer: #this part isn't working 100% yet
                sumMin = request.POST['Summin']
                sumMax = request.POST['Summax']
            up = UserPreferences(
                pref_minCredits = request.POST['FSmin'],
                pref_maxCredits = request.POST['FSmax'],
                pref_summer = prefSummer,
                pref_summerMinCredits = sumMin,
                pref_summerMaxCredits = sumMax,
                pref_user = u
            )
            up.save()
            return HttpResponseRedirect(reverse('landing:selectcourses', args=(userID,)))
        else:
            message = "Email already taken"
            return render(request, 'landing/createuser.html',
                          {'diplomas': generateDiplomaDD(), 'majors': generateMajorDD(), 'minors': generateMinorDD(),
                           'concentrations': generateConcentrationsDD(), 'message':message}
                          )
    else:
        return render(request, 'landing/createuser.html',
                      {'diplomas':generateDiplomaDD(), 'majors':generateMajorDD(), 'minors':generateMinorDD(), 'concentrations':generateConcentrationsDD() }
                      )

def selectcourses(request, pk):
    '''
    @selectcourses send a request to render the selectcourses.html page
    @param request: generates the response
    @param pk: primary key corresponding to active user
    '''
    if request.method == "POST":
        removeUserCompletedEnteries(pk)
        classesChecked = request.POST.getlist('chexmix')
        saveClassesToUser(classesChecked, pk)
        return HttpResponseRedirect(reverse('landing:nextsemesterschedule', args=(pk,)))
    else:
        checkBoxes = generateCheckBoxEntities(pk)
        # might need to write some logic here to determine if boxes have already been checked :)
    return render(request, 'landing/selectcourses.html', {'checkBoxes': generateCheckBoxEntities(pk)})

def nextsemesterpreferences(request, pk):
    '''
    @nextsemesterpreferences send a request to render the nextsemesterpreferences.html page
    @param request: generates the response
    @param pk: primary key corresponding to active user
    '''
    if request.method == "POST":
        cu = User.objects.get(pk=pk)
        up = UserPreferences.objects.get(pref_user=cu)
        up.pref_nextSSF = request.POST['id_d-ssf']
        up.pref_nextYear = request.POST['id_d-year']
        up.pref_nextSemMinCredit = request.POST['nextSemMin']
        up.pref_nextSemMaxCredit = request.POST['nextSemMax']
        up.save()
        return HttpResponseRedirect(reverse('landing:schedule', args=(pk,)))
    else:
        return render(request, 'landing/nextsemesterpreferences.html', {'years': generateYearDD()})

def schedule(request, pk):
    '''
    @schedule send a request to render the schedule.html page
    @param request: generates the response
    @param pk: primary key corresponding to active user
    '''
    return render(request, 'landing/schedule.html', {'schedule': createSchedule(pk), 'userID': pk})