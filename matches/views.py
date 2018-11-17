from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect
from matches.models import Rate, Object, ClientRate
from django.db.models import Max
import random, inflect
from rest_framework.views import APIView
from rest_framework.response import Response

# Index:
def home(request):
    set_session(request)
    latestRates=Rate.objects.filter(approved=True).order_by('-id',)[:10]
    return render(request,'index.html',{'latestRates':latestRates})
# When 2 objects are searched
def get_data(request):
    data={
        'sales':100,
        'customers':10
    }
    return JsonResponse(data)

def search(request):
    set_session(request)
    match=Rate.objects.none()
    yes_percent=0
    queryA=request.GET.get('qA')
    queryB=request.GET.get('qB')
    if queryA and queryB:
        # remove spaces after (rstrip) and before (lstrip) words:
        queryA = queryA.lstrip()
        queryB = queryB.lstrip()
        queryA=queryA.rstrip()
        queryB=queryB.rstrip()
        # get the desired match
        match=Rate.objects.filter(object1__name=queryA,object2__name=queryB)
        if not match: #check if objects are ordered backwards
            match=Rate.objects.filter(object1__name=queryB,object2__name=queryA)
    for_match_var=for_match(match)
    for_match_var['qA']=queryA.title
    for_match_var['qB']=queryB.title
    # other matches containing same objects:
    otherMatchesA,otherMatchesB=otherMatches(queryA,queryB)
    for_match_var['otherMatchesA']=otherMatchesA
    for_match_var['otherMatchesB'] = otherMatchesB
    return render(request,'match.html',for_match_var)
# finds other matches containing same objects
def otherMatches(queryA,queryB):
    otherMatches1_1 = Rate.objects.filter(object1__name=queryA,approved=True).exclude(object2__name=queryB)
    otherMatches1_2 = Rate.objects.filter(object2__name=queryA,approved=True).exclude(object1__name=queryB)
    otherMatchesA = otherMatches1_1 | otherMatches1_2
    otherMatches2_1 = Rate.objects.filter(object1__name=queryB,approved=True).exclude(object2__name=queryA)
    otherMatches2_2 = Rate.objects.filter(object2__name=queryB,approved=True).exclude(object1__name=queryA)
    otherMatchesB = otherMatches2_1 | otherMatches2_2
    return otherMatchesA[:5], otherMatchesB[:5]
def find(request,queryA,queryB):
    match = Rate.objects.filter(object1__name=queryA, object2__name=queryB)
    if not match:  # check if objects are ordered backwards
        match = Rate.objects.filter(object1__name=queryB, object2__name=queryA)
    for_match_var = for_match(match)
    for_match_var['qA'] = queryA
    for_match_var['qB'] = queryB
    # other matches containing same objects:
    otherMatchesA, otherMatchesB = otherMatches(queryA, queryB)
    for_match_var['otherMatchesA'] = otherMatchesA
    for_match_var['otherMatchesB'] = otherMatchesB
    return render(request, 'match.html', for_match_var)
# Returning context after search
def for_match(match):
    yes_percent = 0
    no_percent=0
    irrelevant_percent=0
    number_of_people=0
    approved=False
    if match:
        ans_yes = match.values_list('ans_yes', flat=True)[0]
        if ans_yes == None: ans_yes = 0
        ans_no = match.values_list('ans_no', flat=True)[0]
        if ans_no == None: ans_no = 0
        ans_irrelevant = match.values_list('ans_irrelevant', flat=True)[0]
        print(ans_irrelevant)
        if ans_irrelevant == None: ans_irrelevant = 0
        number_of_people = ans_yes + ans_no + ans_irrelevant
        if ((ans_yes + ans_no + ans_irrelevant) != 0):
            yes_percent = ((ans_yes) / (number_of_people)) * 100
            no_percent = ((ans_no) / (number_of_people)) * 100
            irrelevant_percent = ((ans_irrelevant) / (number_of_people)) * 100
        yes_percent = round(yes_percent, 2)
        no_percent = round(no_percent, 2)
        irrelevant_percent = round(irrelevant_percent, 2)
        approved=match.values_list('approved', flat=True)[0]
        print(irrelevant_percent)
    response=""
    return {'match':match,'yes_percent':yes_percent,'irrelevant_percent':irrelevant_percent,'no_percent':no_percent,'number_of_people':number_of_people,'response':response,'approved':approved}

# "Add" page:
def add(request):
    set_session(request)
    return render(request,'add.html')
# Adding the actual match to website:
def process(request):
    p=inflect.engine()
    added=False
    objectA = request.POST.get('oA')
    objectB = request.POST.get('oB')
    # strip from spaces:
    objectA=objectA.lstrip()
    objectA=objectA.rstrip()
    objectB=objectB.lstrip()
    objectB=objectB.rstrip()
    # make first letter capital:
    objectA=objectA.title()
    objectB = objectB.title()
    if objectA==objectB:
        response="Can't match the same object"
    else:
    # check if new objects are already in database
        obAExists = Object.objects.filter(name=objectA).exists()
        obBExists = Object.objects.filter(name=objectB).exists()
        if obAExists: rateObA=Object.objects.filter(name=objectA)[0]
        else:
            plural=False
            if p.plural(objectA): plural = True
            rateObA=Object.objects.create(name=objectA,image="#",plural=plural)
        if obBExists: rateObB=Object.objects.filter(name=objectB)[0]
        else:
            if p.plural(objectB): plural = True
            rateObB=Object.objects.create(name=objectB, image="#")

        if Rate.objects.filter(object1=rateObA,object2=rateObB).exists() or Rate.objects.filter(object1=rateObB,object2=rateObA).exists():
            response="Query already exists"
        else:
            rate=Rate.objects.create(object1=rateObA,object2=rateObB)
            response="Query has been added to the website"
            added=True
    return render(request,'add.html',{'response':response,'added':added})
# Returns a random match from database
def process2(request,queryA,queryB):
    added=False
    objectA = queryA
    objectB = queryB
    # strip from spaces:
    objectA=objectA.lstrip()
    objectA=objectA.rstrip()
    objectB=objectB.lstrip()
    objectB=objectB.rstrip()
    # make first letter capital:
    objectA=objectA.title()
    objectB = objectB.title()
    if objectA==objectB:
        response="Can't match the same object"
    else:
    # check if new objects are already in database
        obAExists = Object.objects.filter(name=objectA).exists()
        obBExists = Object.objects.filter(name=objectB).exists()
        if obAExists: rateObA=Object.objects.filter(name=objectA)[0]
        else: rateObA=Object.objects.create(name=objectA,image="#")
        if obBExists: rateObB=Object.objects.filter(name=objectB)[0]
        else: rateObB=Object.objects.create(name=objectB, image="#")

        if Rate.objects.filter(object1=rateObA,object2=rateObB).exists() or Rate.objects.filter(object1=rateObB,object2=rateObA).exists():
            response="Query already exists"
        else:
            rate=Rate.objects.create(object1=rateObA,object2=rateObB)
            response="Query has been added to the website"
            added=True
    return render(request,'add.html',{'response':response,'added':added})
def random_match(request):
    set_session(request)
    match=get_random3()
    queryA=match.values_list('object1__name',flat=True)[0]
    queryB=match.values_list('object2__name',flat=True)[0]
    for_match_var=for_match(match)
    for_match_var['qA'] = queryA
    for_match_var['qB'] = queryB
    # other matches containing same objects:
    otherMatchesA, otherMatchesB = otherMatches(queryA, queryB)
    for_match_var['otherMatchesA'] = otherMatchesA
    for_match_var['otherMatchesB'] = otherMatchesB
    # return render(request,'match.html',for_match_var)
    httpurl='find/'+queryA+'-'+queryB+'/'
    return redirect(httpurl)
def get_random3():
     max_id = Rate.objects.all().aggregate(max_id=Max("id"))['max_id']
     while True:
         pk = random.randint(1,max_id)
         rate = Rate.objects.filter(pk=pk)
         if rate and rate.values_list('approved',flat=True)[0]:
             return rate
def set_session(request):
    # print(request.session.get('id'))
    # del request.session['id']
    # print(request.session.get('id'))

    if request.session.get('id','default')=='default':
        print(1)
        createClient=ClientRate.objects.create()
        client_id=createClient.id
        request.session['id']=client_id
    return
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def vote(request):
    set_session(request)
    rate_id = request.POST.__getitem__('rate_id')
    rate=Rate.objects.filter(id=rate_id)
    ans_yes = rate.values_list('ans_yes', flat=True)[0]
    ans_no = rate.values_list('ans_no',flat=True)[0]
    ans_irrelevant = rate.values_list('ans_irrelevant', flat=True)[0]
    if ans_yes == None: ans_yes = 0
    if ans_no == None: ans_no = 0
    if ans_irrelevant == None: ans_irrelevant = 0
    client_id=request.session.get('id','default')
    if check_voted(request,rate_id):
        response="You already gave your vote for this match"
    else:
        if (request.POST.__getitem__('opinion') == 'yes'):
            Rate.objects.filter(id=rate_id).update(ans_yes=ans_yes+1)

        elif(request.POST.__getitem__('opinion')=='no'):
            Rate.objects.filter(id=rate_id).update(ans_no=ans_no + 1)
        elif (request.POST.__getitem__('opinion') == 'irrelevant'):
            Rate.objects.filter(id=rate_id).update(ans_irrelevant=ans_irrelevant + 1)
        if ClientRate.objects.filter(id=client_id).exists():
            client_rate = ClientRate.objects.get(id=client_id)
            client_rate.rates.add(Rate.objects.get(id=rate_id))
            client_rate.save()
        response="Vote has been added"
    for_match_var=for_match(rate)
    for_match_var['response']=response
    queryA=rate.values_list('object1__name',flat=True)[0]
    queryB=rate.values_list('object2__name',flat=True)[0]
    for_match_var['qA'] = queryA.title
    for_match_var['qB'] = queryB.title
    # other matches containing same objects:
    otherMatchesA, otherMatchesB = otherMatches(queryA, queryB)
    for_match_var['otherMatchesA'] = otherMatchesA
    for_match_var['otherMatchesB'] = otherMatchesB
    return render(request,'match.html',for_match_var)
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ['Nope','Dumb Question','Yup']
        default_items = [30,53,90]
        data = {
            'labels':labels,
            'default':default_items,
        }
        return Response(data)
def check_voted(request,rate_id):
    client_id=request.session.get('id','default')
    if ClientRate.objects.filter(id=client_id, rates__id=rate_id).exists():
        return True
    else: return False