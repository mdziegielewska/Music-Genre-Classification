from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.main_page, name='index'),
    path('mgc', views.main_page, name='index'),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url('favicon.ico')),),
    path('sign-in', views.sign_in, name='sign-in.html'),
    path('sign-up', views.sign_up, name='sign-up.html'),
    path('logout', views.user_logout),
    path('404', views.error_404, name='404.html'),
    path('reset', views.reset_password, name='reset-password.html'),
    path('new-password', views.new_password, name='new-password.html'),
    path('new-password?uidb64=<uid>&token=<token>', views.new_password, name='new-password.html'),
    path('history', views.saved_history, name='saved-history.html'),
    path('results', views.results, name='results.html'),
    path('save', views.save_song, name='save-song.html'),
    path('edit-page', views.edit_page, name='edit-page.html'),
    path('delete-account', views.delete_account),
    path('delete-song', views.delete_song),
    path('search', views.search, name='search-results.html')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)