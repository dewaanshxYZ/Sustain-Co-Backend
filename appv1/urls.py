from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/<user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/', GetAllUsersView.as_view(), name='all-users'),
    path('login/', LoginView.as_view(), name='login'),
    path('get_graph_data/', GraphDataView.as_view(), name='get_graph_data'),
    path('refetch_data/', RefetchGraphDataView.as_view(), name='refetch_data'),
    path('contact/', ContactView.as_view(), name='contact'),
]
