from django.urls import path
from . import views
urlpatterns = [
    path(route="", view=views.home, name="home"),
    path(route="signin/", view=views.signin, name="signin"),
    path(route="signout/", view=views.signout, name="signout"),
    path(route="register/", view=views.register, name="register"),
    path(route="delete/<int:id>", view=views.deleteTodo, name="delete"),
    path(route="update/<int:id>", view=views.updateTodo, name="update"),
]