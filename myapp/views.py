from datetime import date
import smtplib,ssl
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Advertise, UserDetail, Contact, Location, Category,Favorites
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import template
from django.contrib.auth import update_session_auth_hash, authenticate, logout, login as auth_login
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    data = Advertise.objects.all()[0:6]
    today_data = Advertise.objects.order_by('-date_created')[:10]
    print(today_data)

    return render(request, 'index.html', {'data': data,
                                          'today_data':today_data,

                                          'category': Category.objects.all(),
                                          'location': Location.objects.all(),
                                          })


def listing(request):
    data1= Advertise.objects.all()
    # today_data = Advertise.objects.filter(date_created=date.today())[0:6]
    today_data = Advertise.objects.order_by('-date_created')[:10]

    page = request.GET.get('page', 1)
    paginator = Paginator(data1, 4)
    try:
        data1 = paginator.page(page)
    except PageNotAnInteger:
        data1 = paginator.page(1)
    except EmptyPage:
        data1 = paginator.page(paginator.num_pages)
    return render(request, 'listings.html', {'data1': data1,
                                             'today_data':today_data,

                                             'category': Category.objects.all(),
                                             'location': Location.objects.all()

                                             })


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email_id')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        data = UserDetail(
            user=user,
            )

        data.save()
        return redirect('user_login')
    else:
        return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.INFO, 'The username and/or password you specified are not correct.')
            return redirect('user_login')
    else:
        return render(request, 'loginad.html')


@login_required(login_url='/login/')
def myads(request):
    data1 = Advertise.objects.filter(user=request.user.id)
    return render(request, 'myads.html',{'data1': data1})


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/login/')
def post_ad(request):
    if request.method == 'POST':
        title = request.POST.get('ad_title')
        description = request.POST.get('ad_des')
        location = request.POST.get('loc')
        category = request.POST.get('cat')
        contact = request.POST.get('cont_no')
        price = request.POST.get('price')
        image = request.FILES.get('picture')
        image1 = request.FILES.get('picture1')
        image2 = request.FILES.get('picture2')
        object = Advertise(
            user=request.user.id,
            title=title,
            description=description,
            image=image,
            image1=image1,
            image2=image2,
            location=Location.objects.get(pk=location),
            category=Category.objects.get(pk=category),
            contact=contact,
            price=price
        )
        object.save()
        return redirect('home')
    else:
        return render(request, 'postad.html',
                      {
                          'category': Category.objects.all(),
                          'location': Location.objects.all()
                      })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        todo = Contact(name=name, email=email, subject=subject, message=message)
        todo.save()
        connection = smtplib.SMTP('smtp.gmail.com', 587)
        connection.ehlo()
        connection.starttls()
        connection.login('anhadbatra1998@gmail.com', '')
        connection.sendmail('anhadbatra1998@gmail.com', email,
                            ("Subject: " + str(subject) + "\n\n" + "Hello " + str(
                                name) + "\n Your email address:- " + str(
                                email) + "\n Thank You for sending message \n" + str(message)))
        connection.sendmail('anhadbatra1998@gmail.com', 'anhadbatra1998@gmail.com',
                            ("Subject: " + str(subject) + "\n\n" + "Name of the sender :- " + str(
                                name) + "\n email address:- " + str(email) + "\n Message:- \n" + str(message)))
        connection.quit()
        return redirect('/')
    else:
        return render(request, 'contact.html')


def advertise(request, id=None):
    advertise = Advertise.objects.get(pk=id)
    today_data = Advertise.objects.filter(date_created=date.today())

    return render(request, 'listing_single.html', {'advertise': advertise,
                                                   'today_data': today_data,
                                                   'category': Category.objects.all(),
                                                   'location': Location.objects.all()
                                                   })


@login_required(login_url='/login/')
def editad(request, id=None):
    if request.method == 'POST':
        data = Advertise.objects.get(pk=id)
        data.title = request.POST.get('ad_title')
        data.description = request.POST.get('ad_des')
        data.location = Location.objects.get(pk=request.POST.get('loc'))
        data.category = Category.objects.get(pk=request.POST.get('cat'))
        data.contact = request.POST.get('cont_no')
        data.price = request.POST.get('price')
        data.image = request.FILES.get('picture')
        data.save()
        return redirect('home')
    else:
        editad = Advertise.objects.get(pk=id)
        return render(request,'editad.html',{'editad' : editad ,
                                             'category': Category.objects.all(),
                                             'location': Location.objects.all()
                                             })


@login_required(login_url='/login/')
def change_pass(request):
    if request.method=='POST':
        id = request.user.id
        data = User.objects.get(pk=id)
        print(data)
        data.set_password(request.POST.get('new_pass1'))

        # data = UserDetail.objects.get(pk=request.user.id)
        # data.old_password = request.POST.get('old_pass')
        # data.password1  = request.POST.get('new_pass')
        # data.password2  = request.POST.get('new_pass')
        # print(request.POST.get('new_pass1'))
        data.set_password = request.POST.get('new_pass1')
        data.save()
        messages.success(request, _('Your password was successfully updated!'))
        return redirect('home')

    else:
        return render(request,'change_pass.html',{})


def search_item(request):
    if request.method == 'POST':
        today_data = Advertise.objects.order_by('-date_created')[:10]
        keyword = request.POST.get('keyword')
        location = request.POST.get('location')
        categories = request.POST.get('categories')
        print(keyword)
        print(location)
        print(categories)
        search_items = ''

        if location and categories and keyword:
            search_items = Advertise.objects.filter(location=location,category=categories,title=keyword)

        elif categories and keyword:
            search_items = Advertise.objects.filter(category=categories,title=keyword)

        elif location and categories:
            search_items = Advertise.objects.filter(location=location,category=categories)

        elif location and keyword:
            search_items = Advertise.objects.filter(location=location,title=keyword)

        elif location:
            search_items = Advertise.objects.filter(location=location)

        elif categories:
            search_items = Advertise.objects.filter(category=categories)

        elif keyword:
            search_items = Advertise.objects.filter(title=keyword)

        return render(request, 'search.html', {'search_items': search_items,
                                               'today_data': today_data,
                                               'category': Category.objects.all(),
                                               'location': Location.objects.all()
                                               })
    else:
        today_data = Advertise.objects.order_by('-date_created')[:10]
        return render(request,'search.html',{
                                    'today_data': today_data,
                                    'category': Category.objects.all(),
                                     'location': Location.objects.all()
                                         })


@login_required(login_url='/login/')
def favourites(request,id=None):
    if request.method == 'POST':
        data = Advertise.objects.get(pk=id)
        print(data.id)
        product_id = data.id
        favourite = Favorites(
                user=request.user.id,
                product_id=product_id,
            )
        favourite.save()
        return render(request,'index.html',{})
    else:
        return render(request,'favourites.html',{})



def deletead(request , id=None):
    ad_obj = Advertise.objects.get(pk=id)
    ad_obj.delete()
    messages.add_message(request, messages.INFO, 'Deleted Successfully...!')
    return redirect('myads')

