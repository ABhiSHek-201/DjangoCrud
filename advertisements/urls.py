from django.urls import path, include
from .views import AllAdvertisements,PublishedAdvertisements, AddAdvertisements, PublishAds, EditAds, DeleteAds, ViewAd

urlpatterns = [
    path('', PublishedAdvertisements.as_view()),
    path('all', AllAdvertisements.as_view()),
    path('create', AddAdvertisements.as_view()),
    path('view/<int:adv_id>', ViewAd.as_view()),
    path('publish/<int:adv_id>', PublishAds.as_view()),
    path('edit/<int:adv_id>', EditAds.as_view()),
    path('delete/<int:adv_id>', DeleteAds.as_view())
]