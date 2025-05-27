import gradio as gr
import requests

API_URL = "http://localhost:8000/recommendations" 

def get_recommendations(prompt, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": prompt}
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Error: {e}"

    if not data:
        return "No recommendations found."

    html_parts = []
    for activity in data:
        title = activity.get("title", "No title")
        overview = activity.get("overview", "No overview")
        location = activity.get("location", {})
        loc_str = f"{location.get('city', '')}, {location.get('region', '')}, {location.get('country', '')}"
        price = activity.get("price_per_person", "N/A")
        duration = activity.get("duration", {})
        hours = duration.get("hours")
        minutes = duration.get("minutes")
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        dur_str = f"{hours}h {minutes}m"
        images = activity.get("images_url", [])

        first_image_html = ""
        if images:
            first_image_html = f'<img src="{images[0]}" width="300" style="margin-right:10px;"/>'
        html = f"""
        <div style="border:1px solid #ccc; padding:15px; margin-bottom:20px; border-radius:8px;">
            <h3>{title}</h3>
            <p><b>Location:</b> {loc_str}</p>
            <p><b>Duration:</b> {dur_str}</p>
            <p><b>Price per person:</b> {price}</p>
            <p>{overview}</p>
            <div>{first_image_html}</div>
        </div>
        """
        html_parts.append(html)

    return "".join(html_parts)

with gr.Blocks() as demo:
    gr.Markdown("# Отримати рекомендації активностей")
    token_input = gr.Textbox(label="Bearer Token", type="password")
    prompt_input = gr.Textbox(label="Введіть ваш запит англійською", lines=2)
    output_html = gr.HTML()
    btn = gr.Button("Отримати рекомендації")
    btn.click(fn=get_recommendations, inputs=[prompt_input, token_input], outputs=output_html)

demo.launch()
