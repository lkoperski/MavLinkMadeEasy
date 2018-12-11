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

def getSemesterByMonth( m ):
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

def getDegree(diploma, type, track):
    '''
    @getDegree searches the Degree table to find the Degree object with corresponding degree and major
    @param d: degree attribute of Degree being searched for
    @param m: major attribute of Degree being searched for
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
    for cc in Complete.objects.get(complete_user=cu).complete_courses.all():
        completedCourses.append(cc)
    return completedCourses

def getCoursesForUser(uID):
    '''
    @getCoursesForUser provides a list of Course (objects) the user must complete for their respective Degree
    @param uID: the primary key corresponding to the active user
    '''
    requiredCourses = []
    degrees = Degree.objects.filter(degree_users=uID)
    reqs = getDegreeReqs(degrees)
    for r in reqs:
        catalog = getReqCourses(r)
        for c in catalog:
            if c not in requiredCourses:
                requiredCourses.append([c.course_subject, c.course_num, c.course_name, c.course_credits, c.pk])
    return requiredCourses

def translateCourseInfoToCourse(reqClasses):
    '''
    @translateCourseInfoToCourse translate the list of course information (from getCoursesForUser) into a list of Course objects
    @param reqClasses: a list of course information pieces
    '''
    courses = []
    for rc in reqClasses:
        courses.append(Course.objects.get(pk=rc[4]))
    return courses

def removeCoursesTaken( requiredClasses, classesTaken ):
    '''
    @removeCoursesTaken provides a list of Course (objects) the user must still take (required, but not completed classes)
    @param requiredClasses: a list of Course (objects) required for the User's Degree
    @param classesTaken: a list of Course (objects) that the User has already completed
    '''
    validCourses = []
    for rc in requiredClasses:
        if rc not in classesTaken:
            validCourses.append(rc)
    return validCourses

def checkPrereqsMet(conditions, classesTaken, currentSemester):
    '''
    @checkPrereqsMet determines if the User has met all Prereqs for a particular Course
    @param coditions: a list of lists of Course (objects) corresponding to Prereqs for a given Course
    @param classesTaken: a list of Course (objects) that the User has already completed
    @parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
    '''
    met = True
    for c in conditions:
        for o in c:
            if o not in classesTaken and o not in currentSemester:
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
    so = course.course_semester #course[4] provided in getCoursesForUser
    if ssf == 'Fall' and (so == 'A' or so =='F' or so == 'Y' or so == 'H'):
        offered = True
    elif ssf == 'Spring' and (so == 'A' or so =='S' or so == 'Y' or so =='P'):
        offered = True
    elif ssf == 'Summer' and (so == 'A' or so == 'M' or so == 'P' or so == 'H' ):
        offered = True
    return offered

def courseValid(course, classesTaken, semesterCourses, ssf):
    '''
    @checkCourseValid determines if a given Course can be taken during a given semester
    @param course: the Course under test
    @param classesTaken: a list of Course (objects) that the User has already completed
    @parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
    @param ssf: the Spring, Summer, Fall, offering attribute of the Course
    '''
    valid = False
    prereqs = getCoursePrereqs(course)
    prereqsMet = checkPrereqsMet(prereqs, classesTaken, semesterCourses)
    offered = checkOfferedSemester(course, ssf)
    if prereqsMet and offered:
        valid = True
    return valid

def getNextSemesterTitle(ssf):
    '''
    @getNextSemseterTitle determines which semester will be the next semester (Spring, Summer, Fall)
    @param ssf: the title of the current semester
    '''
    #TODO - take user prefs into account
    nextSemester = ""
    if ssf == "Spring":
        nextSemester = "Summer"
    elif ssf == "Summer":
        nextSemester = "Fall"
    else:
        nextSemester = "Spring"
    return nextSemester

def generateNewSemester(semester):
    '''
    @generateNewSemester creates a new logical semester
    @param semester: previous semester list
    '''
    ssf = semester[0]
    nextSemester = getNextSemesterTitle(ssf)
    y = semester[1]
    if nextSemester == "Spring":
        y+=1
    semester[0] = nextSemester
    semester[1] = y
    semester[2] = []
    return semester

def setupReqTracker(uID):
    '''
    @setupReqTracker sets up a list of requirements and progress tracking values (i.e., credits needed)
    @param uID: user ID of the user requesting the req tracker; needed to determine requirements needed
    '''
    reqTracker = []
    reqs = getDegreeReqs(Degree.objects.filter(degree_users=uID))
    for r in reqs:
        reqID = r.id
        reqName = r.req_name
        reqCredits = r.req_credits
        reqStart = 0
        reqTracker.append([reqID, reqName, reqCredits, reqStart])
    return reqTracker

def getEnforcedCourses(reqTracker):
    '''
    @getEnforcedCourses gets a list of courses that are enforced by requirements for the user's degree
    @param uID: user ID of the user requesting the enforced courses
    @param reqTracker: a list of requirements the user must complete to receive their degree
    '''
    enCourses = []
    for r in reqTracker:
        req = Requirement.objects.get(pk=r[0])
        courses = req.enforced_for.all()
        for c in courses:
            if c not in enCourses:
                enCourses.append(c)
    return enCourses

def getElectiveCourses(reqTracker):
    '''
    @getEnforcedCourses gets a list of courses that are enforced by requirements for the user's degree
    @param reqTracker: a list of requirements the user must complete to receive their degree
    '''
    elCourses = []
    for r in reqTracker:
        req = Requirement.objects.get(pk=r[0])
        courses = req.counted_toward.all()
        for c in courses:
            if c not in elCourses:
                elCourses.append(c)
    return elCourses

def setupSchedule(uID):
    '''
    @setupSchedule creates a template for generating an schedule
    @param uID: user ID of the user requesting the schedule
    '''
    u = User.objects.get(pk=uID)
    up = UserPreferences.objects.get(pref_user=u)
    currentYear = up.pref_nextYear
    ssfSemester = up.pref_nextSSF
    semester = [ssfSemester, currentYear, []]
    schedule = [semester]
    return schedule

def countCourseTowardReqs(course, reqTracker):
    '''
    @countCourseTowardReqs credits the user for courses fulfilling their necessary requirements
    @param course: the course to be counted for credit
    @param reqTracker: the array of requirements needed for the user's desired degree
    '''
    enforcedFor = course.course_enforced_for.all()
    for en in enforcedFor:
        for r in reqTracker:
            if en.req_name == r[1]:
                r[3] += course.course_credits
    countsToward = course.course_counts_toward.all()
    for ct in countsToward:
        for r in reqTracker:
            if ct.req_name == r[1]:
                r[3] += course.course_credits

def updateReqTrackerForCompletedCourses(coursesCompleted, reqTracker):
    '''
    @updateReqTrackerForCompletedCourses provides credit to a user for completing a number of courses
    @param course: the courses to be counted for credit toward their requirements
    @param reqTracker: the array of requirements needed for the user's desired degree
    '''
    for c in coursesCompleted:
        countCourseTowardReqs(c, reqTracker)

def checkReqsMet(reqTracker):
    '''
    @checkReqsMet returns True if all requirements for the user's desired degree have been met
    @param reqTracker: the list of requirements needed for the user's desired degree
    '''
    reqsMet = True
    for r in reqTracker:
        if r[2] > r[3]:
            reqsMet = False
            break
    return reqsMet

def tallyNumberCreditsTaken(courses):
    '''
    @tallyNumberCreditsTaken returns the total number of credits scheduled for a semester
    @param courses: the list of Course objects scheduled for the semester
    '''
    totalCredits = 0
    for c in courses:
        totalCredits+=c.course_credits
    return totalCredits

def prefNumCreditsMet(uID, ssf, numberCreditsTaken):
    '''
    @prefNumCreditsMet returns True if the number of credits scheduled for a semester is within the user's desired constraints
    @param uID: the id of the user whose schedule is being processed
    @param ssf: denotes the spring, summer, or fall semester
    @numberCreditsTaken: the number of credits taken during the semester
    '''
    u = User.objects.get(pk=uID)
    up = UserPreferences.objects.get(pref_user=u)
    met = False
    if ssf == "Summer":
        prefMax = up.pref_summerMaxCredits
        prefMin = up.pref_summerMinCredits
    else:
        prefMax = up.pref_maxCredits
        prefMin = up.pref_minCredits
    if numberCreditsTaken <= prefMax and numberCreditsTaken >= prefMin:
        met = True
    return met

def combineEnforcedAndElectiveCourses(enforcedCourses, electiveCourses):
    '''
    @combineEnforcedAndElectiveCourses ensures there are no duplicates listed between the enforced and elective courses
    @param enforcedCourses: a list of the course objects that are enforced
    @param electiveCourses: a list of the courses objects that can be taken as electives
    '''
    potential = [enforcedCourses,[]]
    for el in electiveCourses:
        if el not in enforcedCourses:
            potential[1].append(el)
    print("potential courses in combine....", potential)
    return potential

def mandatePrereqsForEnforcedCourses(enfCourses):
    '''
    @mandatePrereqsForEnforcedCourses determine if there are classes needed as Prereqs for beginning enforced courses and if not accounted for, schedules them
    @param enfCourses: a list of Course objects that a user is required to take according to their desired Degree Requirements
    '''
    for en in enfCourses:
        prereqs = getCoursePrereqs(en)
        if prereqs != []:
            for pr in prereqs:
                if pr[0][0] not in enfCourses: #TODO - note that this only tests for the first course in an OR and might not be super time-efficient for the student
                    enfCourses.append(pr[0][0])
    return enfCourses

def createSchedule(uID):
    '''
    @createSchedule generates semester-by-semester schedule for User's needed Courses according to Degree
    @param uID: primary key associated with active user
    '''
    reqTracker = setupReqTracker(uID)  # used to track if Req credit quotas have been met
    enfCourses = getEnforcedCourses(reqTracker)
    electiveCourses = getElectiveCourses(reqTracker)
    enforcedCourses = mandatePrereqsForEnforcedCourses(enfCourses)
    potentialCourses = combineEnforcedAndElectiveCourses(enforcedCourses, electiveCourses)
    completedCourses = getCompletedByUser(uID)
    placeholder = Course.objects.get(course_name="placeholder", course_num="0000")
    completedCourses.append(placeholder)
    schedule = setupSchedule(uID) # get user degree information, semester information etc
    semester = schedule[0]
    ssf = semester[0] #summer spring fall
    semesterSchedule = semester[2]
    semesterCourses = []
    updateReqTrackerForCompletedCourses(completedCourses, reqTracker)
    loopCount = 0
    enforcedNeeded = (potentialCourses[0] != []) #list of enforced classes still needed
    electivesAvailabile = (potentialCourses[1] != []) #list of electives still needed
    while not checkReqsMet(reqTracker) and loopCount < 3:
        while not prefNumCreditsMet(uID, ssf, tallyNumberCreditsTaken(semesterCourses)) and loopCount < 3:
            print("credits not met")
            if enforcedNeeded: # if still need enforced courses
                for en in potentialCourses[0]: #en is a course object out of the list of enforced courses
                    if prefNumCreditsMet(uID, ssf, tallyNumberCreditsTaken(semesterCourses)): #if number of credits in single semester is met
                        break
                    if courseValid(en, completedCourses, semesterCourses, ssf): #if a course can be scheduled
                        print( "appending enforced course!")
                        semesterCourses.append(en) #append course to a semester
                        print("semester Courses:", semesterCourses)
                        semesterSchedule.append([en.course_subject + " " + en.course_num + " " + en.course_name, en.course_credits, 'EN']) #output to screen
                        completedCourses.append(en) # save semester schedule as completed so can continue scheduling
                        potentialCourses[0].remove(en) # remove the scheduled course from the potential course list
                        countCourseTowardReqs(en, reqTracker) # update the reqTracker with the scheduled course
                enforcedNeeded = (potentialCourses[0] != []) #boolean telling if all enforced courses have been scheduled
            #if electivesAvailabile:
                #for el in potentialCourses[1]:
                    #print("checking electives...")
                    #if prefNumCreditsMet(uID, ssf, tallyNumberCreditsTaken(semesterCourses)):
                        #print( "psych!")
                        #break
                    #if courseValid(el, completedCourses, semesterCourses, ssf):
                        #print("appending elective course")
                        #semesterCourses.append(el)
                        #semesterSchedule.append(["***" + el.course_subject + " " + el.course_num + " " + el.course_name, el.course_credits, 'EL'])
                        #completedCourses.append(el)
                        #potentialCourses[1].remove(el)
                        #countCourseTowardReqs(el, reqTracker)
                #electivesAvailabile = (potentialCourses[1] != [])
            # append the semester to the schedule
            print("appending semester to schedule!")
            schedule.append(semester[:])
            print( "schedule:", schedule)
            semester = generateNewSemester(semester)
            semesterCourses = []
            semesterSchedule = semester[2]
            loopCount += 1
        # check to see if all requirements are met to break out of inner while loop and check prereqs.
    return schedule
    # TODO - the first semester is always blank?

def getDegreeReqs(degrees):
    '''
    @getDegreeRegs returns a list of requirements for all degrees a user has selected
    @param degrees: a list of degrees associated with the user
    '''
    requirements = []
    for d in degrees:
        for r in d.requirement_set.all():
            if r not in requirements:
                requirements.append(r)
    return requirements

def sortCoursesBySubNum(courses):
    '''
    @sortCoursesBySubNum takes a list of course information and sorts them course information according to subject and number
    @param courses: list of courses information pieces that need to be stored for the checkbox page
    '''
    numCourses = len(courses)
    for c in range(numCourses):
        for j in range(0,numCourses-c-1):
            oneCourse = courses[j][5] + " " + courses[j][1] + " " + courses[j][2]
            twoCourse = courses[j+1][5] + " " +courses[j+1][1] + " " + courses[j+1][2]
            if oneCourse > twoCourse:
                courses[j], courses[j+1] = courses[j+1], courses[j]

def getReqCourses(reqs):
    '''
    @getReqCourses returns a list of courses (enforced and non-enforced) for a requirements related to a degree a user has selected
    @param reqs: a list of requirements associated with the user's desired degree
    '''
    requiredCourses = []
    for r in reqs:
        courses = []
        enforced = r.enforced_for.all()
        electives = r.counted_toward.all()
        for en in enforced:
            courses.append([en.id, en.course_subject, en.course_num, en.course_name, en.course_credits, 'M'])
        for el in electives:
            courses.append([el.id, el.course_subject, el.course_num, el.course_name, el.course_credits, 'O'])
        sortCoursesBySubNum(courses)
        requiredCourses.append([r.id, r.req_name, r.req_credits, courses])
    return requiredCourses

def getCoursePrereqs(course):
    '''
    @getCoursePrereqs returns a list of prereqs required for a course in the logical form:
        ex: [[courseA, courseB], [courseC, CourseD], [courseE]]
        where subset lists represent logical ORs and the larger list joined by logical ANDs.
        The above list would have prereqs: (courseA OR courseB) AND (courseC OR courseD) AND courseE
    @param course: the Course under test
    '''
    prereqs = []
    for p in course.prereq_set.all():
        options = []
        for pc in p.prereqcourse_set.all():
            options.append(list(pc.prereqcourse_course.all()))
        prereqs.append(options)
    return prereqs

def generateCheckBoxEntities(uID):
    '''
    @generateCheckBoxEntities creates a list of tuples of requirements, course names and numbers for the selectcourses page
    @param uID: primary key corresponding to the active user
    '''
    degrees = Degree.objects.filter(degree_users=uID)
    reqs = getDegreeReqs(degrees)
    checkBoxEntities = getReqCourses(reqs)
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

def generateNumCreditsDD(lo, hi, default):
    '''
    @generateNumCreditsDD generates a dropdown for the number of credits the user can take
    @param lo: the lowest number of credits possible
    @param hi: the highest number of credits possible
    @param default: the value of the number credits dropdown that ahould be selected automatically as a default
    '''
    credits = []
    for credit in range(lo, hi+1):
        if credit is default:
            credits.append(['S', credit])
        else:
            credits.append(['X', credit])
    return credits


def generateYearDD(default):
    '''
    @generateYearDD creates a list of upcoming years for use on the createuser page
    @parm default: the year value to be selected by default
    '''
    years = []
    currentYear = datetime.now().year
    for year in range(currentYear, currentYear+4):
        if year == default:
            years.append(['S', year])
        else:
            years.append(['X', year])
    return years

def generateSemesterDD(default):
    '''
    @generateSemesterDD creates a list of upcoming semester for use on the createuser page
    @parm default: the year value to be selected by default
    '''
    sems = []
    for s in ['Fall', 'Spring', 'Summer']:
        if s is default:
            sems.append(['S', s])
        else:
            sems.append(['X', s])
    return sems

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
    if u in Complete.objects.all(): #TODO - this probably needs to be updated to get the actual user object instead of Complete
        completed = Complete.objects.get(complete_user=u)
    else:
        completed = Complete(complete_user=u)
        completed.save()
    for cc in classesChecked:
        course = cc.split()
        subject = course[0]
        number = course[1]
        c = Course.objects.get(course_subject=subject, course_num=number)
        completed.complete_courses.add(c)

def removeUserCompletedEnteries(uID):
    '''
    @removeUserCompletedEntries updates database to remove courses completed from a particular user
    @param uID: pk of the associated active user
    '''
    u = User.objects.get(pk=uID)
    completedTable = Complete.objects.all()
    for ce in completedTable:
        if ce.complete_user == u:
            ce.delete()

def getDefaultPreferences(uID):
    u = User.objects.get(pk=uID)
    up = UserPreferences.objects.get(pref_user=u)
    summerClass = up.pref_summer
    month = datetime.now().month
    year = datetime.now().year
    semester = getSemesterByMonth(month)
    nextYear = ""
    nextSem = ""
    minCredit = ""
    maxCredit = ""
    if getNextSemesterTitle(semester) == "Summer" and not summerClass:
        nextSem = "Fall"
        nextYear = year
        minCredit = up.pref_minCredits
        maxCredit = up.pref_maxCredits
    elif getNextSemesterTitle(semester) == "Summer":
        nexSem = "Summer"
        nextYear = year
        minCredit = up.pref_summerMinCredits
        maxCredit = up.pref_summerMaxCredits
    elif getNextSemesterTitle(semester) == "Spring":
        nextSem = "Spring"
        nextYear = year + 1
        minCredit = up.pref_minCredits
        maxCredit = up.pref_maxCredits
    else:
        nextSem = getNextSemesterTitle(semester)
        nextYear = year
        minCredit = up.pref_minCredits
        maxCredit = up.pref_maxCredits
    return [nextSem, nextYear, minCredit, maxCredit]


########################################################################################################################
########################################################################################################################

def login(request):
    '''
    @login send a request to render the login.html page
    @param request: generates the response
    '''
    # TODO - the login will fail if the user has not gone through the selectcourese page and clicked submit (regardless of whether or not courses were actually completed)
    if request.method == "POST":
        e = request.POST['email-input']
        #p = request.POST['password-input']
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
                if i==1 and major not in request.POST:
                    return render(request, 'landing/createuser.html',
                                  {'diplomas': generateDiplomaDD(), 'majors': generateMajorDD(),
                                   'minors': generateMinorDD(),
                                   'concentrations': generateConcentrationsDD(), 'errorCode': 1, 'fsMinCredits':generateNumCreditsDD(1,18,12),
                                   'fsMaxCredits':generateNumCreditsDD(1,18,18), 'sumMinCredits':generateNumCreditsDD(1,18,3),
                                   'sumMaxCredits':generateNumCreditsDD(1,18,6)}
                                  )
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
            summerClasses = True
            if prefSummer == 'no':
                summerClasses = False
            if summerClasses: #this part isn't working 100% yet
                sumMin = request.POST['Summin']
                sumMax = request.POST['Summax']
            else:
                sumMin = 0
                sumMax = 0
            up = UserPreferences(
                pref_minCredits = request.POST['FSmin'],
                pref_maxCredits = request.POST['FSmax'],
                pref_summer = summerClasses,
                pref_summerMinCredits = sumMin,
                pref_summerMaxCredits = sumMax,
                pref_user = u
            )
            up.save()
            return HttpResponseRedirect(reverse('landing:selectcourses', args=(userID,)))
        else:
            return render(request, 'landing/createuser.html',
                          {'diplomas': generateDiplomaDD(), 'majors': generateMajorDD(), 'minors': generateMinorDD(),
                           'concentrations': generateConcentrationsDD(), 'errorCode': 2, 'fsMinCredits':generateNumCreditsDD(1,18,12),
                          'fsMaxCredits':generateNumCreditsDD(1,18,18), 'sumMinCredits':generateNumCreditsDD(1,18,3), 'sumMaxCredits':generateNumCreditsDD(1,18,6)}
                          )
    else:
        return render(request, 'landing/createuser.html',
                        {'diplomas':generateDiplomaDD(), 'majors':generateMajorDD(), 'minors':generateMinorDD(),
                          'concentrations':generateConcentrationsDD(), 'errorCode': 0, 'fsMinCredits':generateNumCreditsDD(1,18,12),
                          'fsMaxCredits':generateNumCreditsDD(1,18,18), 'sumMinCredits':generateNumCreditsDD(1,18,3), 'sumMaxCredits':generateNumCreditsDD(1,18,6) }
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
        return HttpResponseRedirect(reverse('landing:nextsemesterpreferences', args=(pk,)))
    else:
        checkBoxes = generateCheckBoxEntities(pk)
        #TODO - might need to write some logic here to determine if boxes have already been checked :)
    return render(request, 'landing/selectcourses.html', {'checkBoxes': generateCheckBoxEntities(pk)})

def nextsemesterpreferences(request, pk):
    '''
    @nextsemesterpreferences send a request to render the nextsemesterpreferences.html page
    @param request: generates the response
    @param pk: primary key corresponding to active user
    '''
    if request.method == "POST":
        cu = User.objects.get(pk=pk)
        ssf = 'id_d-ssf'
        year = 'id_d-year'
        if ssf in request.POST and year in request.POST:
            up = UserPreferences.objects.get(pref_user=cu)
            up.pref_nextSSF = request.POST['id_d-ssf']
            up.pref_nextYear = request.POST['id_d-year']
            up.pref_nextSemMinCredit = request.POST['nextSemMin']
            up.pref_nextSemMaxCredit = request.POST['nextSemMax']
            up.save()
            return HttpResponseRedirect(reverse('landing:schedule', args=(pk,)))
        else:
            return render(request, 'landing/nextsemesterpreferences.html', {'years': generateYearDD(), 'errorCode': 3})
    else:
        prefs = getDefaultPreferences(pk)
        return render(request, 'landing/nextsemesterpreferences.html', {'years': generateYearDD(prefs[1]),
                                                                        'sem':generateSemesterDD(prefs[0]), 'minCred':generateNumCreditsDD(1,18,prefs[2]),
                                                                        'maxCred':generateNumCreditsDD(1,18,prefs[3])})

def schedule(request, pk):
    '''
    @schedule send a request to render the schedule.html page
    @param request: generates the response
    @param pk: primary key corresponding to active user
    '''
    #TODO - if user.is_authenticated
    return render(request, 'landing/schedule.html', {'schedule': createSchedule(pk), 'userID': pk})
