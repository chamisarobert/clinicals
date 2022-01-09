from django.shortcuts import render
from clinicalsApp.models import Patient, ClinicalData
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from clinicalsApp.forms import ClinicalDataForm
from django.shortcuts import redirect, render

# Create your views here.
# Patient : use class-based views
# 1. List of Patients
class PatientListView(ListView):
    model = Patient

# 2. Create new Patient
class PatientCreateView(CreateView):
    model = Patient
    # where to go on successful creation
    success_url = reverse_lazy('index')
    # which fields to render
    fields = ['firstName', 'lastName', 'age']

# 3. Update Patient
class PatientUpdateView(UpdateView):
    model = Patient
    # where to go on successful update
    success_url = reverse_lazy('index')
    # which fields to render
    fields = ['firstName', 'lastName', 'age']

# 4. Delete Patient
class PatientDeleteView(DeleteView):
    model = Patient
    # where to go on successful delete
    success_url = reverse_lazy('index')


# ClinicalData : use function-based views because we have special logic
# **kwargs : needed for retrieval of Patient Id from the url
def addDataView(request, **kwargs):
    form = ClinicalDataForm()
    # get Patient for whom we want to add ClinicalData
    patient = Patient.objects.get(id=kwargs['pk'])
    # is the form being submitted?
    if request.method == 'POST':
        # get entered form data from the POSt request
        form = ClinicalDataForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    return render(request, 'clinicalsApp/clinicaldata_form.html', {'form':form, 'patient':patient})

# Analyze View : for analyzing the data & calculating BMI
# Use function-based-view because there's logic to implement
# **kwargs : needed for retrieval of Patient Id from the url
def analyzeView(request, **kwargs):
    # get Patient's ClinicalData from the db/ ORM
    data = ClinicalData.objects.filter(patient_id=kwargs['pk'])
    # do responseData to be sent to template
    responseData = []
    for eachEntry in data:
        if eachEntry.componentName == 'hw':
            # saved in db as '6/180' so split into array
            heightAndWeight = eachEntry.componentValue.split('/')
            # do we have BOTH height and weight? Arr length must be > 1
            if len(heightAndWeight) > 1:
                # height is in Feet; convert to Meters
                heightInMetres = float(heightAndWeight[0]) * 0.4536
                # BMI = weight/height**2
                BMI = float(heightAndWeight[1])/heightInMetres**2
                # Create a new ClinicalData entry for the calculated BMI
                bmiEntry = ClinicalData()
                bmiEntry.componentName = 'BMI'
                bmiEntry.componentValue = BMI
                # Add entry to the responseData
                responseData.append(bmiEntry)
        # Add all other metrics/components (eachEntry) to responseData as well
        responseData.append(eachEntry)

    return render(request, 'clinicalsApp/generateReport.html',{'data':responseData})















#
