import os
from django.db import models
from django.utils.text import slugify

from user_manager.models import TeamProfile


class CTFSettings(models.Model):
    is_running = models.BooleanField(default=False)


class ChallengeManagerNoDisabled(models.Manager):
    def get_queryset(self):
        return super(ChallengeManagerNoDisabled, self).get_queryset().exclude(is_enabled=False)


def upload_path_chall_file(instance, filename):
    return os.path.join('challenges', slugify(instance.name) + '_files')


class Challenge(models.Model):
    MISC = 'MIC'
    WEB = 'WEB'
    CRACKING = 'CRK'
    BINARIES = 'BIN'
    CRYPTO = 'CRY'
    CATEGORY_CHOICES = (
        (MISC, 'MISC'),
        (WEB, 'Web'),
        (CRACKING, 'Cracking'),
        (BINARIES, 'Binaries'),
        (CRYPTO, 'Cryptography'),
    )

    # Nombre de points que vaut le chall
    nb_points = models.PositiveIntegerField(default=50)
    # nom du challenge
    name = models.CharField(max_length=50, unique=True)
    # slug du chall, généré à partir du nom (identifiant unique pour l'url)
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    # description du challenge, de l'histoire..
    description = models.TextField()
    # Auteurs du challenge
    authors = models.CharField(max_length=50)
    # genre du challenge
    category = models.CharField(max_length=3,
                                choices=CATEGORY_CHOICES,
                                default=WEB)
    # toutes les équipes ayant flagué (ordonnées par date de flag)
    flaggers = models.ManyToManyField(TeamProfile, through='TeamFlagChall', blank=True,
                                      related_name='validated_challenges')
    # le flag du challenge
    flag = models.CharField(max_length=255)
    # le challenge est-il online ?
    is_enabled = models.BooleanField(default=False)
    # fichier (ou archive) du challenge
    chall_file = models.FileField(upload_to=upload_path_chall_file, blank=True, null=True, max_length=4 * 1024 * 1024)

    # managers
    # is_enabled=False exclus
    objects = ChallengeManagerNoDisabled()
    # tous les challs
    all_objects = models.Manager()

    # Incrément de points si first blood
    @property
    def nb_points_first_blood(self):
        return int(self.nb_points / 3)

    # Incrément de points si second blood
    @property
    def nb_points_second_blood(self):
        return int(self.nb_points / 4)

    # Incrément de points si third blood
    @property
    def nb_points_third_blood(self):
        return int(self.nb_points / 6)

    def __str__(self):
        return self.name


class TeamFlagChall(models.Model):
    flagger = models.ForeignKey(TeamProfile)
    chall = models.ForeignKey(Challenge)
    date_flagged = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_flagged"]
        unique_together = (("flagger", "chall"),)

    def __str__(self):
        return str(self.flagger) + " flagged " + str(self.chall)
