import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url, params=None, api_key=None):
    print(params)
    print("GET from {} ".format(url))
    try:
        if api_key:
            # Call get method of requests library with URL and parameters
            response = requests.get(
                url,
                headers={"Content-Type": "application/json"},
                params=params,
                auth=HTTPBasicAuth("apikey", api_key),
            )
        else:
            # no authentication GET
            response = requests.get(
                url, headers={"Content-Type": "application/json"}, params=params
            )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def post_request(url, payload, **kwargs):
    response = requests.post(url=url, params=kwargs, json=payload)

    return response


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    dealers = get_request(url, kwargs)

    if dealers:
        # Get the row list in JSON as dealers

        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                state=dealer["state"],
                zip=dealer["zip"],
                st=dealer["st"],
            )

            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    params = dict()
    params["id"] = dealerId
    reviews = get_request(url, params)

    if reviews:
        # For each dealer object
        for review in reviews:
            # Create a CarDealer object with values in `doc`

            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment=analyze_review_sentiments(review["review"]),
                id=review["id"],
            )

            results.append(review_obj)

    return results

    # review_obj.sentiment = analyze_review_sentiments(review_obj.review)


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


def analyze_review_sentiments(dealerreview):
    api_key = "KapeCt7MQ4OXbHsU0zo_yAkfrMaCoNmXqvZhF5-9oycy"

    params = dict()
    params["text"] = dealerreview
    params["version"] = "2023-04-04"
    params["features"] = "sentiment"
    params["return_analyzed_text"] = "true"
    params[
        "language"
    ] = "en"  # fix {'error': 'not enough text for language id', 'code': 422}
    response = get_request(
        url="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/173b0e1e-4531-491a-9f82-2fd6e0f66d9e/v1/analyze",
        params=params,
        api_key=api_key,
    )

    try:
        sentiment = response["sentiment"]["document"]["label"]
    except KeyError:
        sentiment = "could_not_be_analyzed"

    return sentiment
