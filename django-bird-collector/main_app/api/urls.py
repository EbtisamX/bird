from django.urls import path
from .views import BirdListAPI,CreateVetAPI,add_accessory_to_bird,remove_accessory_from_bird,SignUpView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('birds/', BirdListAPI.as_view(), name='api_birds'),
    path('birds/<int:bird_id>/add-vet', CreateVetAPI.as_view(), name='api_add_vet'),
    path('birds/<int:bird_id>/add-accessory/<int:accessory_id>/', add_accessory_to_bird, name='api_add_accessory_to_bird'),
    path('birds/<int:bird_id>/remove-accessory/<int:accessory_id>/', remove_accessory_from_bird, name='api_remove_accessory_from_bird'),
    #path('birds/<int:bird_id>/add-accessory/<int:accessory_id>/', AddAccessoryToBirdAPI.as_view(), name='add_accessory_to_bird'),
    #path('birds/<int:bird_id>/remove-accessory/<int:accessory_id>/', RemoveAccessoryFromBirdAPI.as_view(), name='remove_accessory_from_bird'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='signup')

]