from django.contrib import admin
from .models import PersonalDetails, Skill, College, Company, Degree, UserSkillCount, DegreeYear

admin.site.register(PersonalDetails)
admin.site.register(Skill)
admin.site.register(College)
admin.site.register(Company)
admin.site.register(Degree)
admin.site.register(UserSkillCount)
admin.site.register(DegreeYear)

# Register your models here.
