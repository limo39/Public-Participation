from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count 
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Bill, Topic, Message, User, Vote 
from .forms import BillForm, UserForm, MyUserCreationForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        national_id = request.POST.get('national_id')  # Get the national_id
        password = request.POST.get('password')

        try:
            user = User.objects.get(national_id=national_id)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'base/login_register.html', {'page': page})

        user = authenticate(request, username=national_id, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'National ID OR password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q', '')

    bills = Bill.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[:5]  # Using slicing for top 5 topics
    bill_count = bills.count()
    bill_messages = Message.objects.filter(
        Q(bill__topic__name__icontains=q)
    )[:3]

    context = {
        'bills': bills,
        'topics': topics,
        'bill_count': bill_count,
        'bill_messages': bill_messages
    }
    return render(request, 'base/home.html', context)

def bill(request, pk):
    bill = Bill.objects.get(id=pk)
    bill_messages = bill.message_set.all()
    participants = bill.participants.all()

    upvotes = bill.votes.filter(vote_type=1).count()
    downvotes = bill.votes.filter(vote_type=-1).count()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            bill=bill,
            body=request.POST.get('body')
        )
        bill.participants.add(request.user)
        return redirect('bill', pk=bill.id)

    context = {
        'bill': bill,
        'bill_messages': bill_messages,
        'participants': participants,
        'upvotes': upvotes,
        'downvotes': downvotes,
    }
    return render(request, 'base/bill.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    bills = user.bill_set.all()
    bill_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'bills': bills,
        'bill_messages': bill_messages,
        'topics': topics
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createbill(request):
    # Check if the user is an admin (staff)
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to add bills.')
        return redirect('home') 

    User = get_user_model()
    user_instance = User.objects.get(pk=request.user.pk)

    form = BillForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Bill.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        messages.success(request, 'Bill created successfully!')
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/bill_form.html', context)

@login_required(login_url='login')
def updatebill(request, pk):
    bill = Bill.objects.get(id=pk)
    form = BillForm(instance=bill)
    topics = Topic.objects.all()
    if request.user != bill.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        bill.name = request.POST.get('name')
        bill.topic = topic
        bill.description = request.POST.get('description')
        bill.save()
        messages.success(request, 'Bill updated successfully!')
        return redirect('home')

    context = {'form': form, 'topics': topics, 'bill': bill}
    return render(request, 'base/bill_form.html', context)

@login_required(login_url='login')
def deletebill(request, pk):
    bill = Bill.objects.get(id=pk)

    if request.user != bill.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        bill.delete()
        messages.success(request, 'Bill deleted successfully!')
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': bill})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully!')
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q', '')
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    bill_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'bill_messages': bill_messages})

@login_required(login_url='login')
def vote_bill(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    vote_type = request.POST.get('vote_type')  # Change to 'vote_type'
    
    if vote_type is not None:
        vote_type = int(vote_type)  # Convert the vote type to an integer

        # Check for existing vote
        vote, created = Vote.objects.get_or_create(user=request.user, bill=bill)
        vote.value = vote_type  # Assuming you have a 'value' field in the Vote model
        vote.save()
        messages.success(request, 'Vote recorded successfully!')

    return redirect('bill', pk=bill.pk)


def bill_votes_by_location(request, pk):
    bill = get_object_or_404(Bill, id=pk)

    # Group votes by location and count them
    votes_by_location = Vote.objects.filter(bill=bill).values('latitude', 'longitude').annotate(vote_count=Count('id'))

    context = {
        'bill': bill,
        'votes_by_location': votes_by_location,
    }
    return render(request, 'base/votes_by_location.html', context)

def bill_statistics(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill_count = Bill.objects.count()
    upvote_count = Vote.objects.filter(vote_type=1).count()
    downvote_count = Vote.objects.filter(vote_type=-1).count()

    context = {
        'bill_count': bill_count,
        'upvote_count': upvote_count,
        'downvote_count': downvote_count,
    }
    return render(request, 'base/statistics_template.html', {'bill': bill})