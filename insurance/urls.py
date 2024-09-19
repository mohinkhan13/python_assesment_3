from django.urls import path
from .views import *

urlpatterns = [

	path('', dashboard, name='dashboard'),
	path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('manage-questions/', manage_questions, name='manage_questions'),
    path('create-question/', create_question, name='create_question'),
    path('update-question/<int:question_id>/<str:status>/', update_question_status, name='update_question_status'),
    path('delete-question/<int:question_id>/', delete_question, name='delete_question'),
    path('category', category, name='category'),
    path('create_category', create_category, name='create_category'),
    path('delete_category/<int:id>/', delete_category, name='delete_category'),
    path('policy', policy, name='policy'),
    path('create_policy', create_policy, name='create_policy'),
    path('create_policy_holder', create_policy_holder, name='create_policy_holder'),
    path('delete_policy/<int:id>/', delete_policy, name='delete_policy'),
    path('policy_holder_list/', policy_holder_policy_list, name='policy_holder_policy_list'),
    path('policy/approve/<int:policy_id>/', approve_policy, name='approve_policy'),
    path('policy/reject/<int:policy_id>/', reject_policy, name='reject_policy'),
    
]