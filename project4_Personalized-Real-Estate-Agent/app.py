import gradio as gr
import chromadb
import openai

openai_client = openai.OpenAI()

client = chromadb.Client()
collection = client.get_or_create_collection("real-estate-listings")


def get_personalized_listings(bedrooms, bathrooms, location, price_range, property_type, other_prefs):
    # Convert price range to numeric values
    price_min, price_max = price_range.split("-")
    price_min = int(price_min.replace("$", "").replace("k", "000"))
    price_max = int(price_max.replace("$", "").replace("k", "000"))

    # Query the Chroma database based on user preferences
    results = collection.query(
        query_texts=[
            f"Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Location: {location}, Price Range: {price_min}-{price_max}, Property Type: {property_type}, Other Requirements: {other_prefs}"],
        n_results=5,
    )

    personalized_listings = []
    for i in range(len(results["ids"])):
        listing_id = results["ids"][i]
        listing_metadata = results["metadatas"][i]
        document = results["documents"][i]

        # Personalize the listing description using OpenAI
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
        response = openai_client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.70,
        )
        personalized_description = response.choices[0].text.strip()

        personalized_listings.append({
            "id": listing_id,
            "neighborhood": listing_metadata,
            "price": listing_metadata[1],
            "bedrooms": listing_metadata[2],
            "bathrooms": listing_metadata[3],
            "size_sqft": listing_metadata[4],
            "description": personalized_description,
        })

    return personalized_listings


with gr.Blocks() as demo:
    gr.Markdown(
        """
    # Real Estate Buyer Preferences
    Please enter your preferences for your home search below:
    """)

    with gr.Row():
        with gr.Column():
            bedrooms = gr.Number(label="Number of Bedrooms", value=3)
            bathrooms = gr.Number(label="Number of Bathrooms", value=2)
            location = gr.Textbox(label="Preferred Location")
        with gr.Column():
            price_range = gr.Radio(["$100k-200k", "$200k-400k", "$400k-600k", "$600k+"],
                                   label="Price Range", value="$400k-600k")
            property_type = gr.Dropdown(["House", "Condo", "Townhouse", "Multi-Family"],
                                        label="Property Type", value="House")

    other_prefs = gr.Textbox(label="Other Preferences", lines=3,
                             placeholder="Enter any other requirements (e.g. yard, garage, etc.)")

    btn = gr.Button("Search Listings")
    output = gr.JSON(label="Personalized Listings")

    btn.click(get_personalized_listings,
              inputs=[bedrooms, bathrooms, location,
                      price_range, property_type, other_prefs],
              outputs=output)

demo.launch()
