from django.urls import path
from .views import PersonView


urlpatterns = [ 
    path('api', PersonView.as_view(), name='person'),
    path('api/<int:user_id>', PersonView.as_view(), name='get-person-by-user_id'),
]