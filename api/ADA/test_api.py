import requests
import time
# Define the URL of the API endpoint
url = "http://0.0.0.0:8080/ada_extraction"

# Define the payload data as a dictionary
data = {
    "FilePath": r"/Data/FSl_ML/Test_Data/New_ADA_test/TIFF/2025I4A9D015_001.tiff"
}
file_path = r"/Data/FSl_ML/Test_Data/New_ADA_test/TIFF/2025I4A9D015_001.tiff"


""""
try:
    # Measure the start time
    start_time = time.time()

    # Open the file in binary mode

    with open(file_path, "rb") as file:

        # Prepare the file to be uploaded

        files = {"file": file}

        # Send the POST request with the file

        response = requests.post(url, files=files)



    # Make the POST request with the JSON payload
   # response = requests.post(url, json=data)

    # Measure the total time taken for execution
    total_time_taken = time.time() - start_time
    print(f"Total time taken for execution: {total_time_taken}")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response content
       # print("Response:", response.json())
        print("Request was successful.")
    else:
        # If request was not successful, print error message
        print("Error:", response.content)
        print(f"Request failed with status code {response.status_code}")
except Exception as e:
    print("Error occurred during API call:", e)

"""

# Define the payload data as a dictionary

print("Second API")

try:

    # Measure the start time

    start_time = time.time()


    url = "http://0.0.0.0:8080/ada_extraction"
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




