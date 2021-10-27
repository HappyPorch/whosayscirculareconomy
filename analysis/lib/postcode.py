import time, requests
from requests.exceptions import HTTPError


def lookup_coords(postcode):
    try:
        response = requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
        response.raise_for_status()
        jsonResponse = response.json()
        if "result" in jsonResponse:
            postcode_coords = {
                "longitude": jsonResponse["result"]["longitude"],
                "latitude": jsonResponse["result"]["latitude"],
                "admin_district": jsonResponse["result"]["admin_district"]
            }
            return postcode_coords
        else:
            print(f"   Postcode: {postcode} - Result not found, Entire JSON response:")
            print(jsonResponse)

    except HTTPError as http_err:
        print(f'   Postcode: {postcode} - HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'   Postcode: {postcode} - Other error occurred: {err}')

    #be polite to api
    time.sleep(5)