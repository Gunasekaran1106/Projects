from django.shortcuts import render,redirect,get_object_or_404
from students.models import Students
from students.forms import StudentsForm

# Create your views here.

from django.shortcuts import render, redirect
from students.models import Students
from students.forms import StudentsForm

# Create your views here.

def student(request):
    if request.method == 'POST':
        form = StudentsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = StudentsForm()
    return render(request, 'index.html', {'form': form})

def show(request):
    students = Students.objects.all()
    return render(request, 'show.html', {'students': students})


def edit(request, id):
    # Use s_id instead of id for querying the student
    try:
        student = Students.objects.get(s_id=id)  # Corrected to s_id
        return render(request, 'edit.html', {'student': student})
    except Students.DoesNotExist:
        return redirect('/show')  # Handle the case where the student does not exist



def update(request, id):
    student = Students.objects.get(s_id=id)
    if request.method == 'POST':
        form = StudentsForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/show')
    return render(request, 'edit.html', {'student': student})


# views.py
from django.shortcuts import render, redirect
from students.models import Students

def delete(request, id):
    try:
        student = Students.objects.get(s_id=id)  # Use s_id instead of id
        student.delete()
    except Students.DoesNotExist:
        pass  # Handle the case where the student does not exist
    return redirect('/show')  # Redirect back to the list of students after deletion

