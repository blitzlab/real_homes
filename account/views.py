import unique_key
from . import forms
from .models import User
from django.shortcuts import render
from django.db import IntegrityError
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic import TemplateView, ListView
from django.contrib.auth import views as auth_view
from listings.models import Property
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class UserLoginView(auth_view.LoginView):
    template_name = "account/user_login.html"


class UserLogoutView(auth_view.LogoutView):
    template_name = "account/user_logout.html"

class UserSignupView(SuccessMessageMixin, FormView):
    form_class = forms.UserSignUpForm
    template_name = "account/user_signup.html"
    success_message = "Account created successfully, please login"
    success_url = '/account/login'


    # UNIQUE WILL BE HERE-----------------------------------------------------------------------------------------------------------------------------------------------------------


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save(commit=False)
        user.unique_id = unique_key.gen_unique_key()
        user = form.save()

        return super().form_valid(form)



class UserProfile(LoginRequiredMixin, ListView):
    model = Property
    paginate_by = 4
    context_object_name = 'my_properties'
    template_name = "account/account.html"


    def get_queryset(self):
       return super(UserProfile, self).get_queryset().filter(agent=self.request.user)
    # queryset = model.objects.filter(agent=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        my_property_count = Property.objects.filter(
            agent=self.request.user
        ).count()

        context.update({
            "my_property_count":my_property_count
        })
        return context
