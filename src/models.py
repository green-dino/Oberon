import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    # Step 1: Connect to MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['mydatabase']  # Replace 'mydatabase' with your database name
    collection = db['mycollection']  # Replace 'mycollection' with your collection name

    # Step 2: Load JSON data
    with open('data.json') as file:
        data = json.load(file)

    # Step 3: Insert data into collection
    if isinstance(data, list):
        # If the JSON file contains a list of documents
        await collection.insert_many(data)
    else:
        # If the JSON file contains a single document
        await collection.insert_one(data)

    print("Data inserted successfully!")

# Run the async function
asyncio.run(main())
