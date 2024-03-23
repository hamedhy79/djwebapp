from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.Home.as_view(), name='home_api'),
    path('shop/', views.HomeList.as_view(), name='home_class'),
    path('<int:pk>/', views.CarDetail.as_view(), name='car_detail'),
    path('questions/', views.QuestionListView.as_view()),
    path('questions/create/', views.QuestionCreateView.as_view()),
    path('questions/update/<int:pk>/', views.QuestionUpdateView.as_view()),
    path('questions/delete/<int:pk>/', views.QuestionDeleteView.as_view()),
    path('post/<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('reply/<int:post_id>/<int:comment_id>', views.PostAddReplyView.as_view(), name='post_reply'),
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name='post_like'),
]
