from django.db import models

# Create your models here.
class Skill(models.Model):
    skillName=models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.skillName

class College(models.Model):
    collegeName=models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.collegeName

class Company(models.Model):
    companyName=models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.companyName

class Degree(models.Model):
    degreeName=models.CharField(max_length=200,unique=True)
    def __str__(self):
        return self.degreeName

class PersonalDetails(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=13)
    email=models.CharField(max_length=100)
    company = models.ManyToManyField(Company, blank=True)
    college = models.ManyToManyField(College, blank=True)
    def __str__(self):
        return self.name

class UserSkillCount(models.Model):
    user=models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, null=True)
    userSkill=models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)
    userSkillCount = models.PositiveIntegerField()

    def __str__(self):
        return self.user.name

class DegreeYear(models.Model):
    user=models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, null=True)
    userDegree=models.ForeignKey(Degree, on_delete=models.CASCADE, null=True)
    userDegreeYear=models.CharField(max_length=50)
    def __str__(self):
        return self.user.name
