import streamlit as st



from langchain_helper import create_vector_store, get_answer_from_vector_store


st.title("AI News Researcher")
st.sidebar.title("News Article URLs")

default_urls = [
    "https://www.livemint.com/entertainment/samay-raina-fans-can-t-keep-calm-as-indias-got-latent-clips-returns-to-youtube-igl-will-be-back-soon-11750324037759.html",
    "https://www.ndtv.com/world-news/israel-iran-cluster-bombs-netanyahu-khamenei-satellite-images-show-massive-damage-to-irans-arak-nuclear-facility-8713718",
    "https://www.livemint.com/news/trends/70-lpa-not-enough-to-live-in-metro-city-linkedin-post-says-think-twice-before-taking-a-housing-loan-11750307646630.html"
]

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i + 1}", value=default_urls[i], key=f"url_{i}")
    if url:
        urls.append(url)

if 'urls_processed' not in st.session_state:
    st.session_state['urls_processed'] = False

if st.sidebar.button("Process URLs"):
    create_vector_store(urls=urls, main_progress_bar=st.empty())
    st.session_state['urls_processed'] = True

if st.session_state['urls_processed']:
    query = st.text_input("Question:", key="query_input", value="Why 70 LPA not enough to live in metro city?")
    if st.button('Send'):
        print(st.session_state.query_input)
        main_progress_bar=st.empty()
        main_progress_bar.text("Thinking...")
        response = get_answer_from_vector_store(st.session_state.query_input)
        main_progress_bar.empty()
        # Display answer
        st.header('Answer')
        st.subheader(response.get('result','NA'))

        # Display sources
        sources = set()
        for doc in response["source_documents"]:
            source_url = doc.metadata.get("source")
            if source_url:
                sources.add(source_url)

        st.subheader("Sources:")
        for url in sources:
            st.write(url)
