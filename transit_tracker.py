# Main Driver class
import requests
import time

def query_api(locList):
    APP_ID = 'DD09D08BE8A1CD85158AD99DB'
    loc_ids = ",".join(map(str, locList))

    # API call
    api_url = f'http://developer.trimet.org/ws/v2/arrivals/locIDs/{loc_ids}/appID/{APP_ID}'

    try:
        response = requests.get(api_url)

        # 1. Throws an error if the server returned a 400 or 500 range status code
        response.raise_for_status()

        # 2. Safely parse and return JSON directly using requests' built-in method
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Server response text: {response.text}") # Inspect what the API actually returned
    except requests.exceptions.JSONDecodeError:
        print("Error: The response from the server was not valid JSON.")
        print(f"Raw Text received: {response.text}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

    return None

def parse_results(output):
    locations = {}
    for stop in output["resultSet"]["location"]:
        locations[stop["id"]] = stop["desc"]


    output_table = []
    output_table.append(["Location", "Line", "ETA (min)"])
    for item in output["resultSet"]["arrival"]:
        location = locations[item["locid"]]
        line = item["shortSign"]
        # match item["routeSubType"]:
        #     case "Bus":
        #         line = item["signRoute"]
        #     case "Light Rail":
        #         line = item["shortSign"].split()[0]
        #     case _:
        #         line = item["routeSubType"]
        estimated = None
        match item["status"]:
            case "scheduled":
                estimated = item.get("scheduled")
            case "estimated":
                estimated = item.get("estimated")

        if estimated is None:
            continue
        eta = estimated - int(time.time() * 1000)
        etaMin = round(eta/60000,1)
        output_table.append([location, line, etaMin])

    return output_table


def lookup(locList):
    results = query_api(locList)
    if results is not None:
        return parse_results(results)
    return ["nothing returned with api call"]