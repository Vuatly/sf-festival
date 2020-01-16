from django.urls import path
from festival_app.views import CreateApplication, ViewApplications, AppAcceptToggle, AppDeniedToggle, ErrorView, WayView,\
    ViewApplicationDetailCensor, AppLikeToggle, AppDislikeToggle, ViewApplicationDetailMusican, AppAbstainToggle

app_name = 'festival_app'

urlpatterns = [
    path('application-create', CreateApplication.as_view(), name='application-create'),
    path('view-applications', ViewApplications.as_view(), name='view-applications'),
    path('view-app-musican/<slug:slug>/', ViewApplicationDetailMusican.as_view(), name='view-app-musican'),
    path('view-app-censor/<slug:slug>/', ViewApplicationDetailCensor.as_view(), name='view-app-censor'),
    path('view-app-censor/<slug:slug>/abstain', AppAbstainToggle.as_view(), name='abstain'),
    path('view-app-censor/<slug:slug>/like', AppLikeToggle.as_view(), name='like'),
    path('view-app-censor/<slug:slug>/dislike', AppDislikeToggle.as_view(), name='dislike'),
    path('view-app-censor/<slug:slug>/accept', AppAcceptToggle.as_view(), name='accepted'),
    path('view-app-censor/<slug:slug>/denied', AppDeniedToggle.as_view(), name='denied'),
    path('error', ErrorView.as_view(), name='error'),
    path('way', WayView.as_view(), name='way'),
]