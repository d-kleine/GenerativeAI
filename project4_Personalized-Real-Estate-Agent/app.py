import gradio as gr
import chromadb
import openai

openai_client = openai.OpenAI()

client = chromadb.Client()
collection = client.get_or_create_collection("real-estate-listings")


def get_personalized_listings(bedrooms, bathrooms, location, price_range, property_type, other_prefs):
    # Extract price range values
    price_parts = price_range.split("-")
    price_min = price_parts[0].replace("$", "").replace("k", "000")
    price_max = price_parts[1].replace("$", "").replace("k", "000")

    # Convert price range to numeric values
    price_min = int(price_min)
    price_max = int(price_max)

    # Query the Chroma database based on user preferences
    results = collection.query(
        query_texts=[
            f"Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Location: {location}, Price Range: {price_min}-{price_max}, Property Type: {property_type}, Other Requirements: {other_prefs}"],
        n_results=3,
    )

    if len(results["ids"]) == 0:
        return "No matching listings found for the specified preferences."

    output_html = ""
    for i in range(len(results["ids"])):
        document = results["documents"][i]
        listing_id = results["ids"][i]

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
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.70,
        )
        personalized_description = response.choices[0].text.strip()

        # Generate HTML for the listing
        listing_html = f"""
        <div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">
            <p><strong>ID:</strong> {listing_id}</p>
            <p><strong>Description:</strong> {personalized_description}</p>
        </div>
        """
        output_html += listing_html

    return output_html


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
            price_range = gr.Radio(["$100k-200k", "$200k-400k", "$400k-600k"],
                                   label="Price Range", value="$400k-600k")
            property_type = gr.Dropdown(["House", "Condo", "Townhouse", "Multi-Family"],
                                        label="Property Type", value="House")

    other_prefs = gr.Textbox(label="Other Preferences", lines=3,
                             placeholder="Enter any other requirements (e.g. yard, garage, etc.)")

    btn = gr.Button("Search Listings")
    output = gr.HTML(label="Personalized Listings")

    btn.click(get_personalized_listings,
              inputs=[bedrooms, bathrooms, location,
                      price_range, property_type, other_prefs],
              outputs=output)

demo.launch()
