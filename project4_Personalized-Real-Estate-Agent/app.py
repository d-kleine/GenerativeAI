import gradio as gr
from helper import get_personalized_listings

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
    output = gr.HTML(label="Personalized Listings")

    btn.click(get_personalized_listings,
              inputs=[bedrooms, bathrooms, location,
                      price_range, property_type, other_prefs],
              outputs=output)

demo.launch()
