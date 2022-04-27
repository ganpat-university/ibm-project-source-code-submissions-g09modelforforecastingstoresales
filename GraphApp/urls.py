from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name="index"),
    path('index1', views.index1, name="index1"),
    path('login/', views.loginUser, name="login"),
    path('register/', views.register, name="register"),
    path('register1/', views.register, name="register1"),
    path('forgetp/', views.forgetp, name="forgetpassword"),
    path('signup/', views.signup, name="signup"),
    path('passwordr/', views.passwordr, name="passwordr"),
    path('GraphPublish/', login_required(views.GraphPublish.as_view()), name="GraphPublish"),
    path('GraphPublish/<str:SelectPublisher>/',login_required(views.GraphPublish1.as_view()), name="GraphPublishPub"),
    # path('test/', views.test, name="test"),
    # path('',views.graph,name="graph"),
    # path('graph/',views.mg,name="graph"),
    # path('file',views.GIClinicStateCount.as_view(), name="graph1"),
    path('BookListView/',login_required(views.BookListView.as_view()), name="BookListView"),
    path('GraphPredict/',login_required(views.GraphPredict.as_view()), name="GraphPredict"),
    path('graph/',login_required(views.GIClinicStateCount.as_view()), name="graph"),
    path('graphGenre/',login_required(views.GraphGenre.as_view()), name="GraphGenre"),
    path('graphGenre/<str:Selectyear>/',login_required(views.GraphGenre.as_view()), name="GraphGenreYear"),
    path('upload/', login_required(views.csv_upload), name="csv_upload"),

    path('logout/',views.LogOutView.as_view(),name='logout'),

]


# get API for post model -> URL: post_type_list
