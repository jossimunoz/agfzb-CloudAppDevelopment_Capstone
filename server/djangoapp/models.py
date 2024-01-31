from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Car Make: {self.name}, Description: {self.description}"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


class CarModel(models.Model):
    # Many-To-One relationship with CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()

    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    OTHER = "Other"
    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (OTHER, "Other"),
    ]
    car_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=SEDAN)
    year = models.DateField()  # Default to today's date

    def __str__(self):
        return (
            f"Car Make: {self.car_make.name}, "
            + f"Model Name: {self.name}, "
            + f"Dealer ID: {self.dealer_id}, "
            + f"Type: {self.car_type}, "
            + f"Year: {self.year.strftime('%Y')}"
        )


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
    
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, state, zip, st):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.state = state

        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name   


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Dealership ID
        self.dealership = dealership
        # Reviewer's name
        self.name = name
        # Whether the reviewer made a purchase
        self.purchase = purchase
        # The review text
        self.review = review
        # The date of purchase
        self.purchase_date = purchase_date
        # Make of the car
        self.car_make = car_make
        # Model of the car
        self.car_model = car_model
        # Year of the car
        self.car_year = car_year
        # Sentiment of the review, this attribute will be determined by Watson NLU service.
        self.sentiment = sentiment 
        # Review id
        self.id = id

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Review: {self.review}, Sentiment: {self.sentiment}"
