from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from matches.models import Rate,Object,AddressRate
from django.db.models import Max
import random
from matches.models import matches
# Index:
def home(request):
    return render(request,'index.html')
# When 2 objects are searched
def search(request):
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
    for_match_var['qA']=queryA
    for_match_var['qB']=queryB

    return render(request,'match.html',for_match_var)

# Returning context after search
def for_match(match):
    yes_percent = 0
    number_of_people=0
    if match:
        ans_yes = match.values_list('ans_yes', flat=True)[0]
        if ans_yes == None: ans_yes = 0
        ans_no = match.values_list('ans_no', flat=True)[0]
        if ans_no == None: ans_no = 0
        number_of_people = ans_yes + ans_no
        if ((ans_yes + ans_no) != 0):
            yes_percent = ((ans_yes) / (ans_no + ans_yes)) * 100
            yes_percent = round(yes_percent, 2)
    response=""
    return {'match':match,'yes_percent':yes_percent,'number_of_people':number_of_people,'response':response}

# "Add" page:
def add(request):
    return render(request,'add.html')
# Adding the actual match to website:
def process(request):
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
        else: rateObA=Object.objects.create(name=objectA,image="#")
        if obBExists: rateObB=Object.objects.filter(name=objectB)[0]
        else: rateObB=Object.objects.create(name=objectB, image="#")

        if Rate.objects.filter(object1=rateObA,object2=rateObB).exists() or Rate.objects.filter(object1=rateObB,object2=rateObA).exists():
            response="Query already exists"
        else:
            rate=Rate.objects.create(object1=rateObA,object2=rateObB)
            if not (AddressRate.objects.filter(ipAddress=get_client_ip(request)).exists()):
                address_rate=AddressRate.objects.create(ipAddress=get_client_ip(request))
                address_rate.save()
            response="Query has been added to the website"
            added=True
    return render(request,'add.html',{'response':response,'added':added})
# Returns a random match from database
def random_match(request):
    match=get_random3()
    for_match_var=for_match(match)
    return render(request,'match.html',for_match_var)
def get_random3():
     max_id = Rate.objects.all().aggregate(max_id=Max("id"))['max_id']
     while True:
         pk = random.randint(1,max_id)
         rate = Rate.objects.filter(pk=pk)
         if rate:
             return rate
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def vote(request):
    rate_id = request.POST.__getitem__('rate_id')
    rate=Rate.objects.filter(id=rate_id)
    ans_yes = rate.values_list('ans_yes', flat=True)[0]
    ans_no = rate.values_list('ans_no',flat=True)[0]
    if ans_yes == None: ans_yes = 0
    if ans_no == None: ans_no = 0
    ipAddress=get_client_ip(request)
    if AddressRate.objects.filter(ipAddress=ipAddress,rates__id=rate_id).exists():
        response="You already gave your vote for this match"
    else:
        if (request.POST.__getitem__('opinion') == 'yes'):
            Rate.objects.filter(id=rate_id).update(ans_yes=ans_yes+1)
            # rate = Rate.objects.filter(id=rate_id)

        elif(request.POST.__getitem__('opinion')=='no'):
            Rate.objects.filter(id=rate_id).update(ans_no=ans_no + 1)
            # rate = Rate.objects.filter(id=rate_id)
            # address_rate = AddressRate.objects.create(ipAddress=get_client_ip(request))
            # address_rate.rates.add(rate_id)
            # address_rate.save()
        if AddressRate.objects.filter(ipAddress=ipAddress).exists():
            address_rate = AddressRate.objects.get(ipAddress=ipAddress)
            address_rate.rates.add(Rate.objects.get(id=rate_id))

        else:
            address_rate = AddressRate.objects.create(ipAddress=get_client_ip(request))
            address_rate.rates.add(Rate.objects.get(id=rate_id))
        address_rate.save()
        response="Vote has been added"
    for_match_var=for_match(rate)
    for_match_var['response']=response
    return render(request,'match.html',for_match_var)
# def home(request):
#     yes_percent = 0
#     number_of_people=0
#     matches_var = matches.objects.filter(ans_yes=-1)
#     query1 = request.GET.get("q1")
#     query2 = request.GET.get("q2")
#
#     if query1 and query2:
#     # remove spaces after (rstrip) and before (lstrip) words
#         query1 = query1.lstrip()
#         query2 = query2.lstrip()
#         query1=query1.rstrip()
#         query2=query2.rstrip()
#         matches_var=matches.objects.filter(object1=query1,object2=query2)
#         if not matches_var:
#             matches_var = matches.objects.filter(object1=query2, object2=query1)
#         if matches_var:
#             ans_yes=matches_var.values_list('ans_yes', flat=True)[0]
#             ans_no = matches_var.values_list('ans_no',flat=True)[0]
#             number_of_people=ans_yes+ans_no
#             if(ans_yes!=0):
#                 yes_percent=((ans_yes)/(ans_no+ans_yes))*100
#                 yes_percent=round(yes_percent,2)
#     # # if user submitted an opinion:
#     if request.method=="POST":
#         # get the id of the match that the choice was submitted to
#         match_id=request.POST.__getitem__('match_id')
#         # get ans_yes and ans_no from the match
#         ans_yes = matches_var.values_list('ans_yes', flat=True)[0]
#         ans_no = matches_var.values_list('ans_no', flat=True)[0]
#         if(request.POST.__getitem__('opinion')=='yes'):
#             matches.objects.filter(id=match_id).update(ans_yes=ans_yes+1)
#             matches_var = matches.objects.filter(id=match_id)
#         elif(request.POST.__getitem__('opinion')=='no'):
#             matches.objects.filter(id=match_id).update(ans_no=ans_no + 1)
#             matches_var = matches.objects.filter(id=match_id)
#         ans_yes = matches_var.values_list('ans_yes', flat=True)[0]
#         ans_no = matches_var.values_list('ans_no', flat=True)[0]
#         number_of_people = ans_yes + ans_no
#         yes_percent = ((ans_yes) / (ans_no + ans_yes)) * 100
#         yes_percent = round(yes_percent, 2)
#
#     # this will return everything. theres also a method filter where you pass in arguments like "WHERE".
#     return render(request,'index.html', {'matches':matches_var,'yes_percent':yes_percent,'num_people':number_of_people})
#
# def process(request):
#     print(request.POST)
#     return render(request,'index.html')