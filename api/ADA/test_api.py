import requests
import time

# Define the URL of the API endpoint
url = "http://localhost:8080/ada_extraction"

# Define the payload data as a dictionary
data = {
    "FilePath": r"D:\project\FSL\FSL_codebase\api\ADA\images\2027C43AD001_001.jpg"
}

try:
    # Measure the start time
    start_time = time.time()

    # Make the POST request with the JSON payload
    response = requests.post(url, json=data)

    # Measure the total time taken for execution
    total_time_taken = time.time() - start_time
    print(f"Total time taken for execution: {total_time_taken}")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response content
        print("Response:", response.json())
        print("Request was successful.")
    else:
        # If request was not successful, print error message
        print("Error:", response.content)
        print(f"Request failed with status code {response.status_code}")
except Exception as e:
    print("Error occurred during API call:", e)
