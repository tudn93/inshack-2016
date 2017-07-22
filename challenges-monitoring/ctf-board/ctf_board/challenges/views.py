from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_protect

from challenges.forms import ChallengeForm, SubmitionForm
from challenges.models import Challenge, TeamFlagChall, CTFSettings
from ctf_board.decorators.custom_decorators import delete_messages, delete_messages_before, ctf_running, is_active
from user_manager.models import TeamProfile

FORBIDDEN_SLUGS = ['score_board', 'add_challenge']


@login_required
@is_active
@delete_messages
def challenges_list(request):
    ctf_settings = CTFSettings.objects.first()

    if request.user.is_staff:
        challenges = Challenge.all_objects.all().order_by('-nb_points', 'category')
    elif ctf_settings.is_running:
        challenges = Challenge.objects.all().order_by('-nb_points', 'category')

    if request.user.is_staff or ctf_settings.is_running:
        challenges_list = []
        for chall in challenges:
            if request.user.is_staff:
                flaggers = TeamProfile.objects.filter(teamflagchall__chall=chall)
            else:
                flaggers = TeamProfile.objects.filter(teamflagchall__chall=chall, team__is_staff=False)
            challenges_list.append({
                'chall': chall,
                'flaggers': flaggers
            })

        chall_validated = []
        for index, chall in enumerate(challenges):
            team_flag = TeamFlagChall.objects.filter(flagger=request.user.teamprofile, chall=chall)
            if team_flag.count() > 0:
                chall_validated.append(index)
    return render(request, 'challenges/list.html', locals())


@login_required
@is_active
@delete_messages
def score_board(request):
    ctf_settings = CTFSettings.objects.first()

    if ctf_settings.is_running or request.user.is_staff:
        teams_ranking = []
        if request.user.is_staff:
            users_to_show = User.objects.filter(is_active=True)
        else:
            users_to_show = User.objects.filter(is_active=True, is_staff=False)
        for t in users_to_show:
            # if hasattr(t, 'teamprofile'):
            reward_count = 0
            for index, chall_val in enumerate(t.teamprofile.validated_challenges.all()):
                team_flag = TeamFlagChall.objects.get(flagger=t.teamprofile, chall=chall_val)

                if request.user.is_staff:
                    rank = TeamFlagChall.objects.filter(chall=chall_val,
                                                        date_flagged__lte=team_flag.date_flagged
                                                        ).count()
                else:
                    rank = TeamFlagChall.objects.filter(chall=chall_val,
                                                        date_flagged__lte=team_flag.date_flagged,
                                                        flagger__team__is_staff=False
                                                        ).count()
                if rank is 1:
                    reward_count += 3
                elif rank is 2:
                    reward_count += 2
                elif rank is 3:
                    reward_count += 1

            if request.user.is_staff:
                rank = TeamProfile.objects.filter(score__gt=t.teamprofile.score).count() + 1
            else:
                rank = TeamProfile.objects.filter(score__gt=t.teamprofile.score,
                                                  team__is_staff=False
                                                  ).count() + 1

            team_ranking = {
                'team': t,
                'reward_range': range(reward_count),
                'rank': rank
            }
            teams_ranking.append(team_ranking)
        teams_ranking.sort(key=lambda k: k['rank'])

    return render(request, 'challenges/score_board.html', locals())


def create_or_update_challenge(request, chall_form, creating):
    if chall_form.is_valid():
        chall = chall_form.save(commit=False)
        if creating:
            chall_slug = slugify(chall.name)
            nb_same_slug = Challenge.objects.filter(slug=chall_slug).count()
            if nb_same_slug != 0:
                chall_slug += '-' + str(nb_same_slug)
            if chall_slug in FORBIDDEN_SLUGS:
                chall_slug += '-' + slugify(str(datetime.now()))
            chall.slug = chall_slug
            message = "Challenge created. Thanks for your contribution."
        else:
            message = "Challenge updated. Thanks for your contribution."
        chall.save()
        request.session["messages"] = [message]
        return redirect(reverse('challenges:display', args=(chall.slug,)))
    return None


@staff_member_required
@csrf_protect
def add_challenge(request):
    if request.method == 'POST':
        challenge_form = ChallengeForm(request.POST, request.FILES)
        response = create_or_update_challenge(request, challenge_form, True)
        if response is not None:
            return response
    else:
        challenge_form = ChallengeForm()
    return delete_messages_before(render(request, 'challenges/add.html', locals()), request)


@staff_member_required
@csrf_protect
def update_challenge(request, slug):
    challenge = get_object_or_404(Challenge.all_objects, slug=slug)
    if request.method == 'POST':
        challenge_form = ChallengeForm(request.POST, request.FILES, instance=challenge)
        response = create_or_update_challenge(request, challenge_form, False)
        if response is not None:
            return response
        else:
            request.method = "GET"
            return challenge_display(request, slug, challenge_form)
    return delete_messages_before(redirect(reverse('challenges:display', args=(challenge.slug,))), request)


@login_required
@is_active
@ctf_running
@delete_messages
@csrf_protect
def challenge_display(request, slug, challenge_form=None):
    team = request.user
    if not hasattr(team, 'teamprofile'):
        request.session['messages'] = ['We tried really hard to find it but this team does not exists.']
        return redirect(reverse('challenges:list'))
    team_profile = team.teamprofile
    if team.is_staff:
        challenge = get_object_or_404(Challenge.all_objects, slug=slug)
        if challenge_form is None:
            challenge_form = ChallengeForm(instance=challenge)
    else:
        challenge = get_object_or_404(Challenge.objects, slug=slug)
    if request.method == "POST":
        submition_form = SubmitionForm(request.POST)
        if submition_form.is_valid():
            flag = submition_form.cleaned_data["flag"]
            if flag == challenge.flag:
                if TeamFlagChall.objects.filter(flagger=team_profile, chall=challenge).count() > 0:
                    request.session["messages"] = ["Congratulations ! This is indeed the correct flag."
                                                   " But your team already flagged this challenge."]
                else:
                    new_team_flagger = TeamFlagChall(flagger=team_profile, chall=challenge)
                    new_team_flagger.save()  # fail if not unique together
                    request.session["messages"] = ["Congratulations ! You won " + str(challenge.nb_points) + "pts !"]
                    points_to_add = challenge.nb_points
                    # if request.user.is_staff:
                    #     rank = challenge.flaggers.count()
                    # else:
                    if request.user.is_staff:
                        rank = TeamFlagChall.objects.filter(chall=challenge).count()
                    else:
                        rank = TeamFlagChall.objects.filter(chall=challenge,
                                                            flagger__team__is_staff=False).count()
                    if rank == 1:
                        request.session["messages"].append("Excellent ! You are the first team to flag this challenge."
                                                           "You won an extra " + str(challenge.nb_points_first_blood) +
                                                           "pts for this exploit !")
                        points_to_add += challenge.nb_points_first_blood
                    elif rank == 2:
                        request.session["messages"].append("Excellent ! You are the second team to flag this challenge."
                                                           "You won an extra " + str(challenge.nb_points_second_blood) +
                                                           "pts for this exploit !")
                        points_to_add += challenge.nb_points_second_blood
                    elif rank == 3:
                        request.session["messages"].append("Excellent ! You are the third team to flag this challenge."
                                                           "You won an extra " + str(challenge.nb_points_third_blood) +
                                                           "pts for this exploit !")
                        points_to_add += challenge.nb_points_third_blood
                    team_profile.score += points_to_add
                    team_profile.save()
            else:
                request.session["messages"] = ["Sorry it's not the correct flag. Keep searching"
                                               " and don't hesitate to call a staff member if needed."]
    else:
        submition_form = SubmitionForm()

    # Les données nécessaires à l'affichage
    team_flag = TeamFlagChall.objects.filter(flagger=team_profile, chall=challenge)
    challenge_valide = team_flag.count() > 0
    if challenge_valide:
        if request.user.is_staff:
            rank = TeamFlagChall.objects.filter(chall=challenge,
                                                date_flagged__lte=team_flag[0].date_flagged,
                                                ).count()
        else:
            rank = TeamFlagChall.objects.filter(chall=challenge,
                                                date_flagged__lte=team_flag[0].date_flagged,
                                                flagger__team__is_staff=False
                                                ).count()

    return render(request, 'challenges/display.html', locals())


@staff_member_required
@csrf_protect
def delete_challenge(request, slug):
    if request.method == "POST":
        challenge = get_object_or_404(Challenge.all_objects, slug=slug)
        all_teams_flaggers = challenge.flaggers.all()
        for rank, team_profile in enumerate(all_teams_flaggers):
            team_profile.score -= challenge.nb_points
            if rank == 0:
                team_profile.score -= challenge.nb_points_first_blood
            elif rank == 1:
                team_profile.score -= challenge.nb_points_second_blood
            elif rank == 2:
                team_profile.score -= challenge.nb_points_third_blood
            get_object_or_404(TeamFlagChall, flagger=team_profile, chall=challenge).delete()
            team_profile.save()
        challenge.delete()
        request.session["messages"] = ["The challenge has been deleted."]
    return delete_messages_before(redirect(reverse('challenges:list')), request)
