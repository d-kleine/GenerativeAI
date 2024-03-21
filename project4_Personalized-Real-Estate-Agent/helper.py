import json
import openai
import chromadb

# Initialize clients
openai_client = openai.OpenAI()
# alternativly for local save: client = chromadb.PersistentClient(path="./")
chromadb_client = chromadb.Client()

# Database
collection = chromadb_client.get_or_create_collection(
    "real-estate-listings")

# Constants for OpenAI completion
COMPLETION_MODEL_NAME = "gpt-3.5-turbo-instruct"
MAX_ANSWER_TOKENS = 3000


def callOpenAi(prompt):
    try:
        response = openai_client.completions.create(
            model=COMPLETION_MODEL_NAME,
            prompt=prompt,
            max_tokens=MAX_ANSWER_TOKENS
        )
        text = response.choices[0].text.strip()
        # Remove invalid control characters from the response
        text = ''.join(c for c in text if ord(c) >= 32)
        return text
    except Exception as e:
        print(e)
        return ""


def generate_single_listing(listing_id):
    """
    Generate a single real estate listing.

    Args:
        listing_id (int): The ID for the listing.

    Returns:
        dict: A dictionary representing the generated listing.
    """
    json_example = {
        "id": 1,
        "neighborhood": "Green Oaks",
        "price": 800000,
        "bedrooms": 2,
        "bathrooms": 2,
        "size_sqft": 2000,
        "description": "Welcome to this eco-friendly oasis...",
        "neighborhood_description": "Green Oaks is a close-knit..."
    }
    prompt = f"""
    Generate a new real estate listing with the ID {listing_id} with the same keys but new values in same JSON format provided below:
    
    {json.dumps(json_example)}
    
    Make sure "description" is a text of up to 75 words.
    Make sure "neighborhood description" is a text of up to 50 words.
    """

    response = callOpenAi(prompt)

    listing = json.loads(response)

    return listing


def generate_listings(num_listings, filename):
    """
    Generate multiple real estate listings and save them to a file.

    Args:
        num_listings (int): The number of listings to generate.
        filename (str): The name of the file to save the listings to.

    Returns:
        dict: A dictionary containing the generated listings.
    """
    listings = {"listings": []}

    for i in range(1, num_listings + 1):
        listing = generate_single_listing(i)
        listings["listings"].append(listing)

    with open(filename, 'w') as file:
        json.dump(listings, file, indent=4)  # Setting indent for readability

    return listings


def read_from_file(input_file):
    """
    Read listings from a JSON file.

    Args:
        input_file (str): The name of the file to read from.

    Returns:
        dict: A dictionary containing the listings read from the file.
    """
    with open(input_file, "r") as read_content:
        return json.load(read_content)


def process_listings(listings_map):
    """
    Process real estate listings and store them in a database.

    Args:
        listings_map (dict): A dictionary containing the listings to process.
    """
    # Parse the cleaned JSON string into a list of dictionaries
    listings = listings_map["listings"]

    # Iterate through each listing in the listings list
    for listing in listings:
        # Ensure all required fields are present in the listing dictionary
        if all(field in listing for field in ["id"]):
            # Combine house and neighborhood preferences into a single document content
            document_content = (
                "House preferences: " + listing["description"] + "\n\n" +
                "Neighborhood preferences: " +
                listing["neighborhood_description"]
            )

            # Extract metadata for the document
            doc_meta_data = {
                field: listing[field]
                for field in ["neighborhood", "price", "bedrooms", "bathrooms", "size_sqft"]
            }

            # Add the record to the database collection
            collection.add(
                documents=[document_content],
                metadatas=[doc_meta_data],
                ids=[str(listing["id"])],
            )

        else:
            # Print a message if any required field is missing
            print(
                f"Skipping listing ID {listing.get('id')} due to missing fields.")


def check_db_listings(collection=collection):
    """
    Check function to list all collections, get details of a specific collection,
    and perform operations on the collection.
    """

    # List all collections
    collections = chromadb_client.list_collections()
    print("Collections:")
    for collection_name in collections:
        print(collection_name)

    # Get details of a specific collection
    # Modify this with your collection name
    if collection:
        print("\nCollection Details:")
        print(f"Name: {collection.name}")
        print(f"Number of Items: {collection.count()}")

        # Get all items in the collection
        all_items = collection.get()
        print("\nItems in Collection:")
        for item in all_items:
            print(item)
    else:
        print(f"\nCollection '{collection_name}' not found.")


def extract_price_range(price_range):
    """
    Extracts the minimum and maximum price range from a given string.

    Args:
        price_range (str): A string representing the price range.

    Returns:
        tuple: A tuple containing the minimum and maximum price range.
    """
    # If the price range is "$600k+", set minimum to 600,000 and maximum to a high value
    if price_range == "$600k+":
        return 600000, 999999999
    else:
        # Splitting the price range string into parts separated by "-"
        price_parts = price_range.split("-")

        # Extracting the minimum price and converting it to an integer
        price_min = int(price_parts[0].replace("$", "").replace("k", "000"))

        # Extracting the maximum price and converting it to an integer
        price_max = int(price_parts[1].replace("$", "").replace("k", "000"))

        # Returning the minimum and maximum prices as a tuple
        return price_min, price_max


def query_listings(bedrooms, bathrooms, location, price_min, price_max, property_type, other_prefs):
    collection = chromadb_client.get_or_create_collection(
        "real-estate-listings")
    """
    Queries real estate listings based on specified criteria.

    Args:
        bedrooms (int): Number of bedrooms.
        bathrooms (int): Number of bathrooms.
        location (str): Location of the property.
        price_min (int): Minimum price range.
        price_max (int): Maximum price range.
        property_type (str): Type of property.
        other_prefs (str): Other preferences.

    Returns:
        dict: A dictionary containing the queried listings.
    """
    # Constructing the query text based on the provided criteria
    query_text = f"Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Location: {location}, Price Range: {price_min}-{price_max}, Property Type: {property_type}, Other Requirements: {other_prefs}"

    # Performing the query using the constructed query text
    results = collection.query(query_texts=[query_text], n_results=1)

    # Returning the results of the query
    return results


def personalize_listing(document, bedrooms, bathrooms, location, price_range, property_type, other_prefs):
    """
    Personalizes a real estate listing description based on buyer preferences.

    Args:
        document (str): Original listing description.
        bedrooms (int): Number of bedrooms.
        bathrooms (int): Number of bathrooms.
        location (str): Location of the property.
        price_range (str): Price range of the property.
        property_type (str): Type of property.
        other_prefs (str): Other preferences.

    Returns:
        str: Personalized listing description.
    """
    # Constructing the prompt for personalizing the listing description
    prompt = f"""
    Personalize the following real estate listing description based on the buyer's preferences:

    Listing Description: {document}

    Buyer Preferences:
    - Bedrooms: {bedrooms}
    - Bathrooms: {bathrooms}
    - Location: {location} 
    - Price Range: {price_range}
    - Property Type: {property_type}
    - Other Requirements: {other_prefs}
    """

    # Calling an OpenAI model with the constructed prompt to personalize the listing description
    # Assuming callOpenAi is a function to interact with OpenAI API
    request = callOpenAi(prompt)

    # Returning the personalized listing description
    return request


def generate_listing_html(listing_id, neighborhood, price, bedrooms, bathrooms, size_sqft, personalized_description):
    """
    Generates HTML for a real estate listing.

    Args:
        listing_id (str): ID of the listing.
        neighborhood (str): Neighborhood of the property.
        price (str): Price of the property.
        bedrooms (int): Number of bedrooms.
        bathrooms (int): Number of bathrooms.
        size_sqft (int): Size of the property in square feet.
        personalized_description (str): Personalized listing description.

    Returns:
        str: HTML code for the listing.
    """
    return f"""
    <div class="listing-container">
        <div class="listing" id="listing-{listing_id}">
            <p>Neighborhood: {neighborhood}</p>
            <p>Price: {price}</p>
            <p>Bedrooms: {bedrooms}</p>
            <p>Bathrooms: {bathrooms}</p>
            <p>Size (sqft): {size_sqft}</p>
            <p>{personalized_description}</p>
        </div>
    </div>
    """


def get_personalized_listings(bedrooms, bathrooms, location, price_range, property_type, other_prefs):
    """
    Retrieves personalized real estate listings based on specified criteria.

    Args:
        bedrooms (int): Number of bedrooms.
        bathrooms (int): Number of bathrooms.
        location (str): Location of the property.
        price_range (str): Price range of the property.
        property_type (str): Type of property.
        other_prefs (str): Other preferences.

    Returns:
        str: HTML code containing the personalized listings.
    """
    price_min, price_max = extract_price_range(price_range)
    results = query_listings(bedrooms, bathrooms, location,
                             price_min, price_max, property_type, other_prefs)

    if len(results["ids"]) == 0:
        return "No matching listings found for the specified preferences."

    output_html = """
    <div class="listings-container">
    """
    for i in range(len(results["ids"])):
        listing_id = results["ids"][i]
        personalized_description = personalize_listing(
            results["documents"][i], bedrooms, bathrooms, location, price_range, property_type, other_prefs)
        output_html += f"<div>Listing ID: {listing_id}</div>"
        output_html += f"<div>Personalized Description: {personalized_description}</div>"

    output_html += """
    </div>
    """

    return output_html
