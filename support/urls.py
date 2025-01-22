from django.urls import path,include

from rest_framework_nested import routers

from .views import MessageViewSet,TicketViewSet

router = routers.DefaultRouter()
router.register('tickets', TicketViewSet, basename='tickets')

tickets_router = routers.NestedDefaultRouter(router, 'tickets', lookup='ticket')
tickets_router.register('messages', MessageViewSet, basename='ticket-messages')


urlpatterns =[
    path('',include(router.urls)),
    path('',include(tickets_router.urls)),
]