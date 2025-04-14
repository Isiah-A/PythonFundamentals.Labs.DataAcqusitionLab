import urllib.request
import urllib.error
import json

"""
Downloads location data from NOAA NCDC in chucks and saves each chunk into a separate JSON file
urllib makes web requests
the responses get placed into a dict and you are given a count of how many 
more requests you can make (results)

"""
site = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations'
token = 'ljkzVLMCygFZxDVnCBjNiCwWNEpCszHA'

def call_api(url, token):
    try:
        req = urllib.request.Request(url)
        req.add_header('token', token)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            return data, rate_limit_remaining


    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"UR: Error: {e.reason}")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e.msg}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def save_json_to_file(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent = 4)
            print(f"Data saved to {filename}")
    except IOError as e:
        print(f'File I/O Error: {e}')
    except Exception as e:
        print(f'Unexpected error occurred while saving the file: {e}')


if __name__ == '__main__':
    limit = 1000
    offset_increment = limit

    for i in range(0, 40):
        offset = i * offset_increment
        url = f'{site}?limit={limit}&offset={offset}'
        output_file = f'locations_{i}.json'

        print(f'Calling API with: {url}')
        response, remaining_requests = call_api(url, token)

        if response:
            results = response.get('results', [])
            print(f'Fetched {len(results)} records in this batch.')

            save_json_to_file(response, output_file)
            print(f'Data saved to {output_file}')


            if len(results) < limit:
                print("No more records to fetch.")
                break

        else:
            print(f"Failed to retrieve data for offset {offset}, exiting loop.")
            break

    print("All files saved successfully")
