import streamlit as st
import wikipedia
import requests

# Unsplash API Key
UNSPLASH_ACCESS_KEY = "9Wf4-MTnejSSgAinCov5BSVJrAbVDA1AOCAGJF7p_o8"

# Image search
def search_unsplash(query):
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
    try:
        response = requests.get(url).json()
        if "results" in response and response["results"]:
            return response["results"][0]["urls"]["regular"]
    except:
        return None
    return None

# Streamlit UI
# Top of your file
st.set_page_config(page_title="Image + Infomation Explorer", layout="wide")

# Stylish title
st.markdown("<h1 style='text-align: center; color: #CD5C5C;'>🔍 Image + Information Explorer</h1>", unsafe_allow_html=True)

query = st.text_input("Enter a topic (e.g., apple):", key="search")

if query:
    col1, col2 = st.columns([1, 2])

    with col1:
        with st.spinner("Fetching image..."):
            image_url = search_unsplash(query)
            if image_url:
                st.image(image_url, caption=f"Image of {query}", use_column_width=True)
            else:
                st.warning("No image found.")

    with col2:
        with st.spinner("Fetching Wikipedia info..."):
            try:
                wikipedia.set_lang("en")
                search_results = wikipedia.search(query)
                if search_results:
                    for result in search_results:
                        try:
                            page = wikipedia.page(result, auto_suggest=False)
                            st.subheader(f"📘 About: {page.title}")
                            with st.expander("📖 Read Wikipedia Content"):
                                st.write(page.content[:2000] + "...")
                                st.markdown(f"[🔗 Read full article]({page.url})")
                            break
                        except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
                            continue
                    else:
                        st.warning("No valid Wikipedia page found.")
                else:
                    st.warning("No results from Wikipedia.")
            except Exception as e:
                st.error(f"Error fetching Wikipedia info: {e}")
