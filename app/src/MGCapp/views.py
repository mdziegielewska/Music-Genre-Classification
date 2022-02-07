import random
from django.core.mail.message import EmailMessage
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.utils.safestring import mark_safe
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from MGCapp.models import SimilarSong
from MGCproject.settings import LOGIN_REDIRECT_URL
from MGCapp.models import Profile, SavedSongs
from predict_genre import predict
from BruteBuster.models import FailedAttempt
from django.db.models import Sum


def error_404(request, exception):
    return render(request, '404.html')


def main_page(request):
    return render(request, 'index.html')


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            if User.objects.filter(username=username).exists():
                user = auth.authenticate(username=username, password=password)

                if user is not None:
                    auth.login(request, user)
                    return HttpResponseRedirect(request.GET.get('next', LOGIN_REDIRECT_URL))
                else:
                    total_failed = FailedAttempt.objects.filter(username=username).aggregate(total_failures = Sum('failures'))['total_failures']

                    if total_failed == 3:
                        response = 'Do you want to reset your password?'
                        total_failed = 0
                    else:
                        response = 'Invalid password' 
                
                    messages.info(request, response)
                    return render(request, 'sign-in.html')
            else:
                messages.info(request, "User with this username does not exist")
                return render(request, 'sign-in.html')
        else:
            return render(request, 'sign-in.html')


def user_logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('csrftoken')
    response.delete_cookie('sessionid')
    return response


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['password-confirmation']

            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username taken')
                    return redirect('sign-up.html')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email taken')
                    return redirect('sign-up.html')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    profile = Profile(user=user)
                    mail_subject = 'Confirmation E-mail'
                    message = render_to_string('activation-email.html', {
                            'user': user
                        })
                    to_email = user.email
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    user.save()
                    profile.save()
                    messages.success(request, mark_safe('Your account has been created.<br/> You can login now.'))
                    return redirect('sign-in.html')
            else:
                messages.info(request, 'Passwords do not match')
                return redirect('sign-up.html')
        else:
            return render(request, 'sign-up.html')


def reset_password(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            associated_users = User.objects.filter(Q(email=email))

            if associated_users.exists():
                for user in associated_users:
                    mail_subject = 'Password reset'
                    email = render_to_string('reset-password-email.html', {
                        'user': user.username,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user)
                    })

                    send_mail(mail_subject, email, 'MusicGenreClassification.app@gmail.com', [user.email], fail_silently=False)

                    messages.success(request, ('A message with reset password instructions has been sent to your inbox.'))
            else:
                messages.info(request, 'Invalid email')
                return redirect('reset-password.html')

        return render(request, 'reset-password.html')


def new_password(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'GET':
            uid = request.GET['uidb64']
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)

        if request.method == 'POST':
            username = request.POST['username']
            user = User.objects.get(username=username)
            password = request.POST['password']
            password2 = request.POST['new-password-confirmation']

            if password == password2:
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been reset.')
                return redirect('sign-in.html')
            else:
                messages.info(request, 'Passwords do not match')
                return render(request, 'new-password.html', context = { 'user' : user })

        return render(request, 'new-password.html', context = { 'user' : user })


def results(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name

        fs = FileSystemStorage(location='/temp/media/')
        fs.save(file_name, uploaded_file)

        genre = predict(uploaded_file.name)

        similar_songs = []
        for s in SimilarSong.objects.raw('SELECT * FROM MGCapp_similarsong WHERE genre = %s', [genre]):
            similar_songs.append(s.source)
        
        i = random.randint(0, 9)
        j = random.randint(0, 9)

        if i == j: j = i-1

        return render(request, 'results.html', context = { 
            'genre': genre, 'source': uploaded_file.name, 'similar_song1': similar_songs[i], 'similar_song2': similar_songs[j] })

    return render(request, 'results.html')


def save_song(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            genre = request.GET['genre']
            source = request.GET['source']
            return render(request, 'save-song.html', context = { 'genre': genre, 'source': source })
        
        if request.method == 'POST':
            user = request.user
            name = request.POST['song-name']
            genre = request.POST['genre']
            source = request.POST['source']

            if SavedSongs.objects.filter(user=user, song_name=name).exists():
                messages.info(request, mark_safe('You already have a song <br/> with this name saved.'))
                return render(request, 'save-song.html', context = { 'genre': genre, 'source': source })
            else:
                song = SavedSongs(user=user, song_name=name, genre=genre, source=source)
                song.save()
                messages.success(request, 'Your song has been saved.')
                return render(request, 'save-song.html', context = { 'genre': genre, 'source': source })
    else:
        return redirect('sign-in.html')


def saved_history(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            saved_songs = []

            for idx,s in enumerate(SavedSongs.objects.raw('SELECT * FROM MGCapp_savedsongs WHERE user_id = %s ORDER BY date DESC', [user.id])):
                song_name = s.song_name
                genre = s.genre
                source = s.source
                date = s.date
                saved_songs.append({'idx': idx+1, 'song_name': song_name, 'genre': genre, 'source': source, 'date': date})

            return render(request, 'saved-history.html', context = {'saved_songs': saved_songs})
    else:
        return redirect('sign-in.html')


def search(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            search = request.GET['search-phrase']
            user = request.user
            saved_songs = []
            search_phrase = '%' + search + '%'

            for idx,s in enumerate(SavedSongs.objects.raw('SELECT * FROM `MGCapp_savedsongs` WHERE `user_id` = %s AND (`song_name` LIKE  %s) OR (`genre` LIKE  %s) OR (`source` LIKE  %s) OR (`date` LIKE  %s) ORDER BY date DESC', [user.id, search_phrase, search_phrase, search_phrase, search_phrase])):
                song_name = s.song_name
                genre = s.genre
                source = s.source
                date = s.date
                saved_songs.append({'idx': idx+1, 'song_name': song_name, 'genre': genre, 'source': source, 'date': date})

            return render(request, 'search-results.html', context = {'saved_songs': saved_songs, 'search': search, 'length': len(saved_songs)})
    else:
        return redirect('sign-in.html')


def edit_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            username = request.POST['chusername']
            password = request.POST['npassword']
            password2 = request.POST['password-confirmation']
            uploaded_file = request.FILES['avatar'] if 'avatar' in request.FILES else False
            
            if username != "":
                if User.objects.filter(username=username).exists():
                    if username == user.username:
                        messages.info(request, "Why do you want to change your username to the old one?")
                    else:
                        messages.info(request, 'Username taken')
                else:
                    user.username = username
                    user.save()
                    messages.success(request, 'Your username has been changed')
            
            if uploaded_file is not False:
                uploaded_file = request.FILES['avatar']
                avatar = uploaded_file.name
                Profile.objects.filter(user=user).update(image=avatar)
                image = FileSystemStorage()
                image.save(avatar, uploaded_file)
                messages.success(request, 'Your profile picture has been changed')
            
            if password != "": 
                if password2 != "":
                    if password == password2:
                        user.set_password(password)
                        user.save()
                        messages.success(request, 'Your password has been reset.')
                    else:
                        messages.info(request, 'Passwords do not match')
                        return render(request, 'edit-page.html')
                else:
                    messages.info(request, 'Both passwords are required')
                    return redirect('edit-page.html')
            
            if password2 != "": 
                if password != "":
                    pass
                else:
                    messages.info(request, 'Both passwords are required')
                    return redirect('edit-page.html')
            return render(request, 'edit-page.html')
            
        return render(request, 'edit-page.html')
    else:
       return redirect('sign-in.html')


def delete_song(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            song_name = request.POST['song_name']
            SavedSongs.objects.filter(song_name=song_name, user=user).delete()

        return redirect('saved-history.html')
    else:
        return redirect('sign-in.html')

    
def delete_account(request):
    if request.user.is_authenticated:
        user= request.user
        user.delete() 
        return redirect('/')
    else:
        return redirect('sign-in.html')
        