import requests
import base64 
import argparse

# Function to send image to the API Gateway and get the analysis result
def analyze_image(url, image):

    with open(image, 'rb') as image_file:
        image_bytes = image_file.read()
        data = base64.b64encode(image_bytes).decode("utf8")
        payload = {"image": data}
    # Send POST request to the API Gateway
    response = requests.post(url, json=payload)
    return response.json()

# Main function to parse arguments and call the analyze_image function
def main():
        try:
            parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)
            parser.add_argument("api_gateway_url", help="The url of your API Gateway")
            parser.add_argument("image_path", help="The local image that you want to analyze.")
            args = parser.parse_args()
            
            result = analyze_image(args.api_gateway_url, args.image_path)
            status = result['statusCode']

            if status == 200:
                print(result['body']) 
            else:
                print(f"Error: {result['statusCode']}")
                print(f"Message: {result['body']}")
        except Exception as error:
            print("Error: ")
            print(error)
            print("Please check your arguments.")
            print("Usage: python interact.py <api_gateway_url> <image_path>")

if __name__ == "__main__":
    main()


