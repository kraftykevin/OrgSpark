from django.contrib import admin
from .models import Story, Submission, Story_by_submission, Story_by_paragraph

admin.site.register(Story)
admin.site.register(Submission)
admin.site.register(Story_by_submission)
admin.site.register(Story_by_paragraph)
