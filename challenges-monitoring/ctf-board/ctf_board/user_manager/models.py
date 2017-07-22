import datetime

from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.text import slugify

from ctf_board.settings import UPLOAD_ROOT


def content_file_name(instance, filename):
    return os.path.join('avatars', str(instance.team.id))


def pdf_file_name(instance, filename):
    name = os.path.join(slugify(instance.team_profile.team.id),
                        slugify('cv_' +
                                instance.team_profile.team.username + '_' +
                                filename + "_" +
                                str(datetime.datetime.now()))
                        )
    return os.path.join(CV.FOLDER, name)


class TeamProfile(models.Model):
    BEGINNER = 'BEG'
    EXPERIMENTED = 'EXP'
    LEVEL_CHOICES = (
        (BEGINNER, 'Beginner (never played a CTF)'),
        (EXPERIMENTED, 'Experimented (at least 1 CTF)'),
    )
    # utilisateur associé
    team = models.OneToOneField(User)
    # image représentant la team
    avatar = models.ImageField(upload_to=content_file_name, blank=True, null=True)
    # nombre de participants dans la team (environ)
    nb_players = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    # niveau de la team
    level = models.CharField(max_length=3,
                             choices=LEVEL_CHOICES,
                             default=EXPERIMENTED)

    # challenges validés par la team : validated_challenges

    # score total de la team
    score = models.PositiveIntegerField(default=0)
    # key to activate account and verify email
    activation_key = models.CharField(max_length=40)
    # key expiration
    key_expires = models.DateTimeField()
    # is the team playing on site ?
    on_site = models.BooleanField(default=False)

    # quelques CVs de l'équipe
    # ->CV_set

    def __str__(self):
        return str(self.team)

    def delete_avatar(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            storage, path = self.avatar.storage, self.avatar.url
            self.avatar.delete()
            if os.path.isfile(path):
                storage.delete(path)


class CV(models.Model):
    FOLDER = 'cvtheque'

    upload_outside_django = FileSystemStorage(location=UPLOAD_ROOT)
    # le CV au format pdf (on l'espère du moins..)
    cv = models.FileField(storage=upload_outside_django, upload_to=pdf_file_name, max_length=4 * 1024 * 1024,
                          blank=True, null=True)
    # le team_profile correspondant
    team_profile = models.ForeignKey(TeamProfile)

    @staticmethod
    def folder_size_is_too_big():
        import os

        def get_size(start_path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            return total_size

        cvs_folder = os.path.join(UPLOAD_ROOT, CV.FOLDER)
        if get_size(cvs_folder) > 2*1024*1024*1024:
            # si > 2G c'est pas normal
            return True
        return False

    @staticmethod
    def check_folders_size_to_avoid_dos():
        import os
        cvs_folder = os.path.join(UPLOAD_ROOT, CV.FOLDER)
        for team_cv_folder in os.listdir(cvs_folder):
            team_cv_folder_path = os.path.join(cvs_folder, team_cv_folder)
            if os.path.isdir(team_cv_folder_path):
                size_of_folder = 0
                for f in os.listdir(team_cv_folder_path):
                    file_path = os.path.join(team_cv_folder_path, f)
                    if os.path.isfile(file_path):
                        size_of_folder += os.path.getsize(file_path)
                    else:
                        import shutil
                        shutil.rmtree(file_path)
                if size_of_folder > 40 * 1024 * 1024:
                    # si le dossier > 40MB .. c'est déconné !
                    import shutil
                    shutil.rmtree(team_cv_folder_path)
            else:
                os.remove(team_cv_folder_path)
