from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from tgbot.models import User
from quests.models import QuestDone
from django.db.models import Count, Sum, F


def NAuthView(request):
    return render(request, 'landing/non-auth.html')

def LandingView(request):
    return render(request, 'landing/index.html')

def RatingView(request):
    users = User.objects.filter(is_admin=False).order_by('-score_num')
    quests = QuestDone.objects.all()
    quests_count = quests.count()
    generalrursum = quests.aggregate(Sum('rub'))
    generalscore = quests.aggregate(Sum('score'))

    rusers = []
    for user in users:
        uquests =  QuestDone.objects.filter(user = user)
        rursum = uquests.aggregate(Sum('rub'))
        data = {
            'user': user,
            'rursum': rursum,

        }
        rusers.append(data)

    return render(request, 'landing/rating.html',{
        'rusers':rusers,
        'quests_count':quests_count,
        'generalrursum':generalrursum,
        'generalscore':generalscore,
    })
