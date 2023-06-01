
from django.shortcuts import render
from .models import User,Game,Event
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Event, Booking,Payment,Result
from django.contrib.auth import logout
from django.urls import reverse
from datetime import date
from django.db.models import Q


# Create your views here.
def index(request):
    a=Game.objects.all()
    b=Game.objects.all().order_by('-timestamp')[:3]
    all={'a':a,
         'b':b}
    return render(request,'index.html',all)
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import User

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        location = request.POST.get('location')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image=request.FILES['image']

        # Check if email already exists in the database
        if User.objects.filter(email=email).exists():
            context = {'error': 'Email already exists!'}
            return render(request, 'register.html', context)

        # Hash the password before saving it to the database
    

        # Create a new user object and save it to the database
        user = User(name=name, age=age, location=location, phone_number=phone_number,
                    address=address, email=email, password=password,image=image)
        user.save()

        # Redirect the user to the login page
        return redirect('/login')

    # If the request method is GET, render the registration page
    return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        check=User.objects.filter(email=email,password=password)
        if check.filter(email=email,password=password).exists():
            for i in check:
                id=i.id
                email=i.email
                request.session['id']=id
                request.session['email']=email
            return redirect('/user_home')
        else:
            msg='Incorrect Email Or Password'
            return render(request,'login.html',{"msg":msg})
    return render(request,'login.html')

def user_home(request):
    id=request.session['id']
    user=User.objects.filter(id=id)
    a=Game.objects.all()
    b=Game.objects.all().order_by('-timestamp')[:3]
    all={'a':a,
         'b':b,
         'user':user}
    return render(request,'user_home.html',all)

def logout_view(request):
    logout(request)
    return redirect('/login')

def all_games(request):
    id=request.session['id']
    user=User.objects.filter(id=id)
    a=Game.objects.all()
    all={'user':user,
         'a':a}
    return render(request,'all_games.html',all)
from datetime import date

def view_events(request):
    id = request.session['id']
    today = date.today()
    events = Event.objects.filter(Q(start_time__gte=today)).order_by('-timestamp')
    user = User.objects.filter(id=id)

    # Calculate days left for each event
    for event in events:
        days_left = (event.start_time - today).days
        event.days_left = days_left

    context = {
        'user': user,
        'events': events
    }
    return render(request, 'all_events.html', context)


def book_event(request, id,gid):
    # get the event object
    userid=request.session['id']
    user=User.objects.get(id=userid)
    event = Event.objects.get(id=id)
    game=Game.objects.get(id=gid)
    # check if the event has any available slots
    if event.max_players == 0:
        messages.error(request, 'This event is fully booked.')
        return redirect('/allevents')
    # create a new booking object
    booking = Booking(user=user, event=event,game=game)
    # update the slots available for the event
    event.max_players -= 1
    event.save()
    # save the booking object
    booking.save()
    messages.success(request, 'Event booked successfully.')
    return redirect(reverse('payment', args=[booking.id]))




def mybookings(request):
    id=request.session['id']
    user=User.objects.filter(id=id)
    booking=Booking.objects.filter(user=id)
    all={'user':user,'booking':booking}
    return render(request,'myevents.html',all)


def cancel(request,id):
    a=Booking.objects.get(id=id)
    a.delete()
    return redirect('/my')

from django.http import JsonResponse


def make_payment(request, booking_id):
    if request.method == 'POST':
        book = get_object_or_404(Booking, id=booking_id)
        payment_amount = 100
        payment = Payment.objects.create(
            bookid=book,
            cname=request.POST.get('cname'),
            amount=payment_amount,
            cardno=request.POST.get('cardno'),
            cvv=request.POST.get('cvv')
        )

        book.payment = payment
        book.save()
        id = request.session['id']
        user = User.objects.filter(id=id)
        user=User.objects.filter(id=id)
        booking=Booking.objects.filter(user=id)
        # all={'user':user,'booking':booking,'msg':'Booking Succesfull'}
        # return render(request,'myevents.html',all)
        return redirect(mybookings)
    else:
        id = request.session['id']
        user = User.objects.filter(id=id)
        book = get_object_or_404(Booking, id=booking_id)
        payment_amount = 100
        return render(request, 'payment.html', {'user': user, 'payment_amount': payment_amount})


def upload_result(request,id):
    if request.method=='POST':
        event=Event.objects.get(id=id)
        result=request.FILES['result']
        feedback=request.POST.get('feedback')
        Result.objects.create(event=event,result=result,feedback=feedback)
        return redirect('/my')
    else:
        id=request.session['id']
        user=User.objects.filter(id=id)
        return render(request,'upload.html',{'user':user})



def viewprofile(request):
    id=request.session['id']
    a=User.objects.filter(id=id)
    return render(request,'viewprofile.html',{'user':a})


def editprofile(request):
    if request.method == 'POST':
        id = request.session['id']
        user = User.objects.filter(id=id)
        up = User.objects.get(id=id)
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        if 'image' in request.FILES:
            image = request.FILES['image']
            up.image = image

        up.name = name
        up.address = address
        up.phone_number = phone_number
        up.email = email

        up.save()
        ud = User.objects.filter(email=request.session['email'])
        context = {'details': ud,
                   'user': user,
                   'msg': 'Profile Details Updated'}

        return redirect('/view')
    else:
        id = request.GET.get('id')
        id = request.session['id']
        up = User.objects.filter(id=id)
        user =User.objects.filter(id=id)
        all_data = {
            'user': user,
            'details': up,
        }
        return render(request, 'editprofile.html', all_data)
def changepassword(request):
    id = request.session['id']
    print(id)
    user = User.objects.filter(id=id)
    all = {
        'user': user,
    }
    if request.method == 'POST':
        email = request.session['email']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print('Email Is:' + email)
        print("Current_password" + str(current_password))
        try:

            ul = User.objects.get(email=email, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                msg =  'Password Changed Successfully'
                all = {
                    'user': user,
                    'msg': msg
                }
                return render(request, 'change_password.html',all)
            else:
                context =  'Your Old Password is Wrong'
                all = {
                    'user': user,
                    'msg': context
                }
                return render(request, 'change_password.html',all)

        except User.DoesNotExist:
            context =  'Your Old Password is Wrong'
            all = {
                'user': user,
                'msg': context
            }
            return render(request, 'change_password.html',all)
    else:
        return render(request, 'change_password.html',all)