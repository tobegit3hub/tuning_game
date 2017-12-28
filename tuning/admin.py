# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from tuning.models import Competition, Participation, Trial

admin.site.register(Competition)
admin.site.register(Participation)
admin.site.register(Trial)
