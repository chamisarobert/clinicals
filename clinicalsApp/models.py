from django.db import models

# Create your models here.
class Patient(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    age = models.IntegerField()

class ClinicalData(models.Model):
    #Drop-down for component names
    COMPONENT_NAMES = [('hw','Height/Weight'),('bp','Blood Pressure'),('hr','Heart Rate')]
    componentName = models.CharField(choices=COMPONENT_NAMES,max_length=20)
    componentValue = models.CharField(max_length=20)
    #Auto use current date
    measuredDate = models.DateTimeField(auto_now_add=True)
    #ONE_TO_MANY rel (1 Patient : Many ClinicalData)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
