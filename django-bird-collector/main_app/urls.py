from django.urls import path
from .views import BirdListView, CreateBirdView, UpdateBirdView, DeleteBirdView,bird_detail_view,add_appointment,assoc_accessory,dessoc_accessory,CreateAccessoryView,AccessoryListView,UpdateAccessoryView,DeleteAccessoryView,home,signup


urlpatterns = [
    path('', home, name='home'),
    path('all-birds/', BirdListView.as_view(), name='bird_list'),
    path('all-birds/<int:bird_id>/', bird_detail_view, name='bird_detail'),
    path('all-birds/add', CreateBirdView.as_view(), name='bird_create'),
    path('all-birds/<int:pk>/update/', UpdateBirdView.as_view(), name='bird_update'),
    path('all-cats/<int:pk>/delete', DeleteBirdView.as_view(), name='bird_delete'),
    path('all-birds/<int:bird_id>/add-appointment', add_appointment, name='add_appointment'),
    path('all-birds/<int:bird_id>/assoc-accessory/<int:accessory_id>', assoc_accessory, name='assoc_accessory'),
    path('all-birds/<int:bird_id>/dessoc-accessory/<int:accessory_id>', dessoc_accessory, name='dessoc_accessory'),
    path('all-birds/accessories/add/', CreateAccessoryView.as_view(), name='accessory_create'),
    path('all-birds/accessories/', AccessoryListView.as_view(), name='accessory_list'),
    path('all-birds/accessories/<int:pk>/update/', UpdateAccessoryView.as_view(), name='accessory_update'),
    path('all-birds/accessories/<int:pk>/delete/', DeleteAccessoryView.as_view(), name='accessory_delete'),
    path('accounts/signup', signup, name='signup'),
]