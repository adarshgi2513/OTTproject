from django.shortcuts import render,redirect
from.forms import customUserCreatonForm,SubscriptionForm,UserProfileForm
from.models import UserProfile,Movie,Subscription
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
import stripe
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

# Create your views here.
class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = customUserCreatonForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = customUserCreatonForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            user = form.save()
            UserProfile.objects.create(user=user, email=email, phone_number=phone_number)
            login(request, user)
            return redirect('signin')

class SigninView(View):
    template_name = 'signin.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            request.session['username'] = username
            if user is not None:
                login(request, user)
                return redirect("index")
        return render(request, self.template_name, {'form': form})

class SignoutView(View):
    def get(self, request):
        if 'username' in request.session:
            del request.session['username']
        logout(request)
        return redirect('signin')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(view_user_details)  # Assuming 'view_user_details' is the correct URL name
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'changepass.html', {"form": form})
    
class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        if request.user.is_authenticated:
            if Subscription.objects.filter(user=request.user).exists():
                return redirect('movie_list')
            return render(request, self.template_name, {})
        else:
            return redirect('signin')

class MovieListView(View):
    template_name = 'movies_list.html'

    
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, self.template_name, {'movies': movies})



def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            subscription_plan = form.cleaned_data['subscription_plan']
            if subscription_plan == 'basic':
                return redirect('https://buy.stripe.com/test_fZe28Kan29L6fwkcMM')
            elif subscription_plan == 'standard':
                return redirect('https://buy.stripe.com/test_bIYfZA0Ms7CY6ZO5kl')
            elif subscription_plan == 'premium':
                return redirect('https://buy.stripe.com/test_bIY6p09iY1eA97WbIK')

    else:
        form = SubscriptionForm()

    return render(request, 'subscribe.html', {'form': form})



def movie_tamil(request):
    # Filter movies by language (e.g., Tamil)
    tamil_movies = Movie.objects.filter(language='Tamil')

    context = {'movies': tamil_movies}
    return render(request, 'tamil.html', context)


def movie_malayalam(request):
    # Filter movies by language (e.g., Tamil)
    tamil_movies = Movie.objects.filter(language='Malayalam')

    context = {'movies': tamil_movies}
    return render(request, 'malayalam.html', context)

def movie_telugu(request):
    # Filter movies by language (e.g., Tamil)
    tamil_movies = Movie.objects.filter(language='Telugu')

    context = {'movies': tamil_movies}
    return render(request, 'telugu.html', context)



def movie_english(request):
    # Filter movies by language (e.g., Tamil)
    tamil_movies = Movie.objects.filter(language='English')

    context = {'movies': tamil_movies}
    return render(request, 'english.html', context)


def movie_hindi(request):
    # Filter movies by language (e.g., Tamil)
    tamil_movies = Movie.objects.filter(language='hindi')

    context = {'movies': tamil_movies}
    return render(request, 'hindi.html', context)

def view_user_details(request):
    user= UserProfile.objects.get(user=request.user)
    return render(request, 'view_profile.html', {'user':user })



def edit_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If UserProfile doesn't exist, create a new one
        UserProfile.objects.create(user=request.user, email='', phone_number='', image='')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect(view_user_details)  # You can change the URL name as needed
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_user_profile.html', {'form': form})


from django.utils import timezone
from django.shortcuts import HttpResponse


class expsub(View):
    def auto_delete_basic_plan(request):
        # Get all basic plans created more than one month ago
        one_month_ago = timezone.now() - timezone.timedelta(days=1)
        basic_subscriptions_to_delete = Subscription.objects.filter(
             subscription_plan='basic', 
             created_at__lt=one_month_ago
        )

         # Delete the basic plans
        basic_subscriptions_to_delete.delete()

        return HttpResponse("Basic plans older than one month have been deleted.")
    
    def auto_delete_standard_plan(request):
        # Get all basic plans created more than one month ago
        two_months_ago= timezone.now() - timezone.timedelta(days=60)
        standard_subscriptions_to_delete = Subscription.objects.filter(
             subscription_plan='standard', 
             created_at__lt= two_months_ago
        )

         # Delete the basic plans
        standard_subscriptions_to_delete .delete()

        return HttpResponse("standard  plans older than tow month have been deleted.")

    def auto_delete_premium_plan(request):
        # Get all basic plans created more than one month ago
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        premium_subscriptions_to_delete = Subscription.objects.filter(
             subscription_plan='premium', 
             created_at__lt=  six_months_ago 
        )

         # Delete the basic plans
        premium_subscriptions_to_delete .delete()

        return HttpResponse("standard  plans older than tow month have been deleted.")
  
 
class searchview(View):

    def get(self,request):
        query=request.GET.get('data','')
        print(query,"fyfuhuyftuihuhg")
        results = Movie.objects.filter(title__icontains=query).values(
            'title', 'description', 'language', 'video','thumbnail'
        )
        data = list(results)
        return JsonResponse({'data':data},safe=False)


  
def searchtemp(request):
        return render(request, 'search.html')