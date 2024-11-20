import httpx
import asyncio

async def call_chat_api():
    url = "http://localhost:8000/api/chat"  # Replace with the actual URL of your FastAPI app
    headers = {
        "Content-Type": "application/json"
    }
    
    # Define the request payload (example messages)
    payload = {
  "messages": [
    {
      "role": "user",
      "content": "how many customers are there in the database?"
    }
  ],
  "model": "gemma2-9b-it"
}

    
    async with httpx.AsyncClient() as client:
        try:
            # Send the POST request to the chat endpoint
            response = await client.post(url, json=payload, headers=headers)

            # Check if the response is successful
            if response.status_code == 200:
                response_data = response.json()
                print("Response from API:", response_data["content"])  # Display the content in terminal
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except httpx.RequestError as e:
            print(f"An error occurred while making the request: {e}")

# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(call_chat_api())
