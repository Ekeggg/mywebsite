from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification, HelpRequest, Reply, Skill, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

subject_list = ["Math","Physics","Chemistry","Biology","Computer Science", "History","English","Other"]
# Create your views here.
def request_list(request):
    reqs = HelpRequest.objects.all().order_by('-created_at')
    return render(request, 'helpdesk/request_list.html',
    { "requests": reqs} )
def request_detail(request, request_id):
    req = get_object_or_404(HelpRequest, id=request_id)
    return render(request, 'helpdesk/request_detail.html',
    { "request": req,})
@login_required
def create_request(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        title = request.POST.get('title')
        help_request = HelpRequest.objects.create(
            User=request.user,
            subject=subject,
            description=description,
            title=title
        )
        if subject:
            helpers = Profile.objects.exclude(user=request.user)
            for helper in helpers:
                if(subject in helper.subjects):
                    Notification.objects.create(
                        user=helper.user,
                        request=help_request
                    )
        return redirect('request_list')
    return render(request, 'helpdesk/create_request.html')
@login_required
def reply_request(request, request_id):
    help_request = get_object_or_404(HelpRequest, id=request_id)
    if request.method == 'POST':
        message = request.POST.get('text')
        Reply.objects.create(
            help_request=help_request,
            responder=request.user,
            message=message
        )
        return redirect('request_detail', request_id=request_id)
    return render(request, 'helpdesk/reply_request.html',{ "request": help_request})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user, subjects="")
            return redirect('editprofile')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
def editprofile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        selected = request.POST.getlist('skills') 
        skill_string = ",".join(selected)
        profile.subjects = skill_string
        profile.save()
        return redirect('request_list')
    return render(request, "helpdesk/editprofile.html", {
        "skills": subject_list,
        "selected": profile.subjects.split(",")})
def notifications(request):
    notes = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, "helpdesk/notifications.html", {"notes": notes})
