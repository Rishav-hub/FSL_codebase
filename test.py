import requests
import time

# Define the URL of the API endpoint
url = "http://localhost:5003/ub_extraction"

# Define the file path of the image you want to upload
file_path = r"D:\project\FSL\FSL_codebase\api\HCFA\images\BSC7N4PAO004_001.tiff"

try:
    # Measure the start time
    start_time = time.time()

    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Define the files dictionary to send the file with the request
        files = {'file': (file_path, f)}

        # Make the POST request with the file as form-data
        response = requests.post(url, files=files)

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