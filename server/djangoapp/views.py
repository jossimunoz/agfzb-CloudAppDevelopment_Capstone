from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, post_request

# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import urllib.parse
from .models import CarMake, CarModel


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}

    username = request.POST["username"]
    password = request.POST["password"]

    if request.method == "POST":
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/login.html", context)

    else:
        return render(request, "djangoapp/login.html", context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    logout(request)

    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    # If it is a POST request
    elif request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]

        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
            )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/registration.html", context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # Get dealers from the URL
        dealerships = get_dealers_from_cf("http://localhost:3000/dealerships/get")

        context["dealers"] = dealerships

        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}

    response = get_dealer_by_id_from_cf(
        "http://127.0.0.1:5000/api/get_reviews", dealerId=dealer_id
    )

    dealerships = get_dealers_from_cf(
        url="http://localhost:3000/dealerships/get", id=dealer_id
    )

    context["reviews"] = response

    context["dealership_name"] = dealerships[0].full_name

    return render(request, "djangoapp/dealer_details.html", context)


def add_review(request, dealer_id):
    context = {"dealer_id": dealer_id}

    if request.user.is_authenticated:
        if request.method == "POST":
            review = dict()
            review["id"] = 7
            review["name"] = request.user.last_name
            review["purchase"] = request.POST["purchasecheck"]
            review["purchase_date"] = datetime.now().strftime("%m/%d/%Y")
            review["dealership"] = dealer_id
            review["review"] = request.POST["purchasecheck"]
            review["car_make"] = "Audi"
            review["car_model"] = "A6"
            review["car_year"] = "2024"

            json_payload = dict()
            json_payload["review"] = review

            response = post_request(
                "http://127.0.0.1:5000/api/post_review", payload=json_payload
            )

            redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            dealerships = get_dealers_from_cf(
                url="http://localhost:3000/dealerships/get", id=dealer_id
            )

            context["dealership_name"] = dealerships[0].full_name

            context["cars"] = CarModel.objects.filter(
                dealer_id=dealer_id
            ).select_related("car_make")

            return render(request, "djangoapp/add_review.html", context)
    else:
        return HttpResponse("Not Authorized")
