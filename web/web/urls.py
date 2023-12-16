from django.contrib import admin
from django.urls import path, include
from globant.api import router
from globant.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls),),
    # docs
    path("", IndexView.as_view())
]
