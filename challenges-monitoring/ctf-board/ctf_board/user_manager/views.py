import string

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils import timezone

from challenges.models import Challenge, TeamFlagChall, CTFSettings
from ctf_board import settings
from ctf_board.decorators.custom_decorators import delete_messages_before, is_active
from user_manager.forms import TeamProfileForm, UserForm, LoginForm
from user_manager.models import TeamProfile, CV

FORBIDDEN_USERNAMES = ['register', 'login', 'logout', 'email_verification', 'resend_mail', 'get_all_mails']


def key_generator(size=35, chars=string.ascii_letters + string.digits):
    import random
    return ''.join(random.choice(chars) for _ in range(size))


def send_verification_mail(team):
    message = "Hello {team},\n\nWe are proud to have you among the InSecurity's CTF's participants.\nIt will take place here : http://bit.ly/1OXo649 from 06:30PM to 12:00AM (GMT+2)\nOf course you can also play online ! But if you come on site you'll be able to enjoy free food&drinks, exclusive challenges AND gifts !\n\nIn any case please confirm your email by clicking the following link : {url}\nFor any question please contact : contact@insecurity-insa.fr\n\nHave a nice day,\nThe InSecurity team."
    message = message.format(team=team.username,
                             url='https://ctf.insecurity-insa.fr/team/email_verification/' +
                                 team.username + '/' +
                                 team.teamprofile.activation_key)
    from django.core.mail import send_mail
    send_mail("Registration to InSecurity's CTF", message, "contact@insecurity-insa.fr", [team.email])


def create_or_update_team(request, team_form, team_profile_form, creating):
    if team_form.is_valid() and team_profile_form.is_valid():
        username = team_form.cleaned_data['username']
        if username not in FORBIDDEN_USERNAMES:
            email_changed = False
            messages = []
            try:
                with transaction.atomic():
                    if creating:
                        team = User.objects.create_user(username=team_form.cleaned_data['username'],
                                                        email=team_form.cleaned_data['email'],
                                                        password=team_form.cleaned_data['password'],
                                                        is_active=False)
                        email_changed = True
                    else:
                        team = team_form.instance
                        team.username = team_form.cleaned_data['username']
                        if 'password' in team_form.initial and team_form.initial['password'] != team.password:
                            team.set_password(team_form.cleaned_data['password'])
                        if 'email' in team_form.initial and team_form.initial['email'] != team.email:
                            email_changed = True
                            team.is_active = False
                        team.email = team_form.cleaned_data['email']
                        team.save()
                    team_profile = team_profile_form.save(commit=False)
                    team_profile.team = team
                    if team_profile_form.cleaned_data.get('delete_avatar'):
                        team_profile.delete_avatar()
                    if email_changed:
                        team_profile.activation_key = key_generator()
                        team_profile.key_expires = timezone.now() + timezone.timedelta(days=2)
                    team_profile.save()
                    for f in team_profile_form.cleaned_data['cvs']:
                        if CV.folder_size_is_too_big():
                            from django.core.mail import send_mail
                            send_mail("Warning ! May be under DOS attack.", "CV folder too big !",
                                      "contact@insecurity-insa.fr", ["contact@insecurity-insa.fr"])
                            messages += ["Error, no more free space to upload your CV, an admin will solve it soon :"]
                            break
                        else:
                            CV.objects.create(team_profile=team_profile, cv=f)
                CV.check_folders_size_to_avoid_dos()
                if email_changed:
                    send_verification_mail(team)
                    messages += [
                        'An email has been sent to validate your account and address. Please check it out !']
                if creating:
                    messages += ['Congratulations ! Your team is created.']
                else:
                    messages += ['Your profile is up to date.']
                t = authenticate(username=team.username, password=team_form.cleaned_data['password'])
                if t is not None:
                    login(request, t)
                request.session['messages'] = messages
                return redirect(reverse('team:profile_other_user', args=(username,)))
            except:  # ZeroDivisionError: # to test
                request.session['messages'] = ['Sorry, an error occurred, please alert an admin.']
        else:
            request.session['messages'] = ["We can't accept this username, sorry."]
    else:
        request.session['messages'] += team_form.non_field_errors()
    return None


@login_required
@csrf_protect
def validate_email(request, username, verification_key):
    team = get_object_or_404(User, username=username)
    if team == request.user or request.user.is_staff:
        if not team.is_active and team.teamprofile.activation_key == verification_key \
                and team.teamprofile.key_expires > timezone.now():
            team.is_active = True
            team.save()
            request.session['messages'] = [
                "Your email is now verified. "
                "You can now use the entire website and you'll receive updates at the same email address."]
        else:
            request.session['messages'] = [
                "Sorry, your verification key is either wrong or too old. Please re-generate one."]
    return redirect(reverse('team:profile'))


@login_required
@csrf_protect
def regenerate_verification_key(request, username):
    if request.method == "POST":
        team = get_object_or_404(User, username=username)
        if (team == request.user or request.user.is_staff) and not team.is_active:
            team.teamprofile.activation_key = key_generator()
            team.teamprofile.key_expires = timezone.now() + timezone.timedelta(days=2)
            team.teamprofile.save()
            send_verification_mail(team)
            request.session['messages'] = [
                'An email has been sent to validate your account and address. Please check it out !']
        else:
            request.session['messages'] = ["Your account is already enabled."]
    return redirect(reverse('team:profile'))


@login_required
@csrf_protect
def profile(request, user_to_show):
    team = get_object_or_404(User, username=user_to_show)
    if not hasattr(team, 'teamprofile'):
        request.session['messages'] = ['We tried really hard to find it but this team does not exists.']
        return redirect(reverse('challenges:list'))
    team_profile = team.teamprofile

    ctf_settings = CTFSettings.objects.first()
    if ctf_settings.is_running or request.user.is_staff:
        if request.user.is_staff:
            number_of_contenders = User.objects.filter(is_active=True).count()
            rank = TeamProfile.objects.filter(score__gt=team_profile.score).count() + 1
            nb_challs = Challenge.all_objects.all().count()
        else:
            number_of_contenders = User.objects.filter(is_active=True, is_staff=False).count()
            rank = TeamProfile.objects.filter(score__gt=team_profile.score, team__is_staff=False).count() + 1
            nb_challs = Challenge.objects.count()
        percentage_valitated_challs = 0
        if nb_challs != 0:
            percentage_valitated_challs = int(100 * (team_profile.validated_challenges.count() / nb_challs))

    rank_by_challenge_val = {}
    for index, chall_val in enumerate(team_profile.validated_challenges.all()):
        if request.user.is_staff:
            team_flag = TeamFlagChall.objects.filter(flagger=team_profile, chall=chall_val)
            rank = TeamFlagChall.objects.filter(chall=chall_val,
                                                date_flagged__lte=team_flag[0].date_flagged).count()
        else:
            team_flag = TeamFlagChall.objects.filter(flagger=team_profile, chall=chall_val,
                                                     flagger__team__is_staff=False)
            rank = TeamFlagChall.objects.filter(chall=chall_val,
                                                date_flagged__lte=team_flag[0].date_flagged,
                                                flagger__team__is_staff=False).count()
        rank_by_challenge_val[index] = rank

    # form to update personnal infos
    if user_to_show == request.user.username or request.user.is_staff:
        personnal_space = True
        if request.method == "POST":
            team_form = UserForm(request.POST, instance=team)
            team_profile_form = TeamProfileForm(request.POST, request.FILES, instance=team_profile)
            response = create_or_update_team(request, team_form, team_profile_form, False)
            if response is not None:
                return response
        else:
            team_form = UserForm(instance=team)
            team_profile_form = TeamProfileForm(instance=team_profile)
    if user_to_show == request.user.username:
        name = 'You'
        pronoum = 'Your'
    else:
        name = user_to_show
        pronoum = user_to_show

    return delete_messages_before(render(request, 'user_manager/profile.html', locals()), request)


@login_required
def profile_redirect(request):
    return redirect(reverse('team:profile_other_user', args=(request.user.username,)))


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        request.session['messages'] = ["You've been logged out. Have a nice day."]
    else:
        request.session['messages'] = ["Mmmh.. You have to be logged in to do this."]
    return redirect(reverse('team:login'))


@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request):
    if settings.REGISTER_ENABLED:
        if request.method == "POST":
            team_profile_form = TeamProfileForm(request.POST, request.FILES)
            team_form = UserForm(request.POST)
            response = create_or_update_team(request, team_form, team_profile_form, True)
            if response is not None:
                return response
        else:
            team_profile_form = TeamProfileForm()
            team_form = UserForm()
    else:
        request.session["messages"] = ["You cannot register anymore, please contact an admin."]
    return delete_messages_before(render(request, 'user_manager/register.html', locals()), request)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            team_name_or_email = login_form.cleaned_data['username_or_email']
            password = login_form.cleaned_data['password']
            team = authenticate(username=team_name_or_email, password=password)
            if team is None:
                user_by_mail = User.objects.filter(email=team_name_or_email)
                if user_by_mail and user_by_mail[0]:
                    username = user_by_mail[0].username
                    team = authenticate(username=username, password=password)
            if team is None:
                request.session['messages'] = ['Wrong team name or password. Please try again.']
            else:
                login(request, team)
                request.session['messages'] = ["You've been successfully logged in."]
                return redirect(request.GET.get('next', reverse('team:profile')))
    else:
        login_form = LoginForm()
    return delete_messages_before(render(request, 'user_manager/login.html', locals()), request)


@login_required
@csrf_protect
def delete(request, user_to_delete):
    if request.method == "POST":
        team = get_object_or_404(User, username=user_to_delete)
        if team == request.user or request.user.is_staff:
            if hasattr(team, 'teamprofile'):
                for team_flagged in team.teamprofile.teamflagchall_set.all():
                    team_flagged.delete()
                team.teamprofile.delete()
            team.delete()
            request.session["messages"] = ["{team} has been deleted successfully.".format(team=user_to_delete)]
    return redirect(reverse('challenges:score_board'))


@staff_member_required
def mails(request):
    users = User.objects.all()
    return render(request, 'user_manager/mails.html', locals())
