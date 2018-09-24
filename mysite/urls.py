from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
# from album.views import CalendarView

urlpatterns = [
    path('', views.welcome, name='welcome'),
    # path('', CalendarView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('account/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('album/', include(('album.urls', 'album'), namespace='album')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
