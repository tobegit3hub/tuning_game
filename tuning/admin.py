# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from tuning.models import Competition
from tuning.models import Participation
from tuning.models import Trial

admin.site.register(Competition)
admin.site.register(Participation)
admin.site.register(Trial)