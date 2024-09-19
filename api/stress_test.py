import aiohttp
import asyncio

async def post_request(session, url, data):
    async with session.post(url, json=data) as response:
        result = await response.text()
        print(f"Response status: {response.status}, Result: {result}")

async def main():
    url = 'http://127.0.0.1:5000/request'  # Replace with your URL
    json_data = {"text": "magic", "language": "en", "video": "https://www.youtube.com/watch?v=3o3uUOkcGqA"}  # Replace with your JSON data

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(1000):
            tasks.append(post_request(session, url, json_data))

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())

