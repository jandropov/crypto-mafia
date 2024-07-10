from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from tgbot.models import User
from .models import Quest, QuestDone, RurWithdraw
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def ProfileAuth(request, session_token):
    if request.headers['User-Agent']=='TelegramBot (like TwitterBot)':
        return None
    userp = User.objects.get(session_token=session_token)
    user = userp.django_user
    login(request,user)
    userp.session_token = ''
    userp.save()
    return redirect('/me/')

@login_required
def QuestDetail(request, slug):
    user = request.user
    profile = User.objects.get(django_user = user)
    quest = get_object_or_404(Quest, slug = slug)
    if profile.score_num < quest.score_need:
        return redirect('/me/')
    else:
        return render(request, 'dashboard/quest_detail.html',{
            'user':user,
            'profile':profile,
            'quest':quest,
        })

@login_required
def QuestDoneView(request):
    user = request.user
    profile = User.objects.get(django_user = user)
    questsdone = QuestDone.objects.filter(user = profile)
    return render(request, 'dashboard/quests_done.html',{
        'user':user,
        'profile':profile,
        'questsdone':questsdone,
    })

@login_required(login_url = '/non-auth/')
def ProfileView(request):
    user = request.user
    profile = User.objects.get(django_user = user)

    questsdone = QuestDone.objects.filter(user = profile)
    qlist = []
    for quest in questsdone:
        qlist.append(quest.quest.pk)

    quests = Quest.objects.filter(is_hide=False).exclude(id__in=qlist).order_by('score_need')

    return render(request, 'dashboard/me_template.html',{
        'user':user,
        'profile':profile,
        'quests':quests,
    })

@login_required
def WithdrawView(request):
    user = request.user
    profile = User.objects.get(django_user = user)

    rurwithdraws = RurWithdraw.objects.filter(user = profile)

    return render(request, 'dashboard/withdraw.html',{
        'user':user,
        'profile':profile,
        'rurwithdraws':rurwithdraws,
    })
