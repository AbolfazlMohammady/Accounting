from django.urls import path, include

from .views import LoginOrRegisterView, ProfileViewSet

profile_viewset = ProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'update',
})

change_password_view = ProfileViewSet.as_view({
    'post': 'change_password',
})
delete_account_view = ProfileViewSet.as_view({
    'post': 'delete_account',
})


urlpatterns = [
    path('login/', LoginOrRegisterView.as_view(), name='login'),
    path('profile/', profile_viewset, name='profile'),
    path('profile/change_password/', change_password_view, name='change_password'),
    path('profile/delete_account/', delete_account_view, name='delete_account'),
]
