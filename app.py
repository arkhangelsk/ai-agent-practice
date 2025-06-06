import streamlit as st
import feedparser
import requests
from datetime import datetime
import urllib.parse

# Set page config
st.set_page_config(page_title="Software Testing News", page_icon="📰", layout="wide")

# Custom CSS with improved color scheme
st.markdown(
    """
<style>
    .main {
        padding: 0rem 1rem;
        background-color: #f8f9fa;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #0d6efd;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #0b5ed7;
        transform: translateY(-2px);
    }
    .news-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #e9ecef;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .news-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .news-title {
        color: #2c3e50;
        text-decoration: none;
        font-size: 1.25rem;
        font-weight: 600;
        line-height: 1.4;
        display: block;
        margin-bottom: 0.5rem;
    }
    .news-title:hover {
        color: #0d6efd;
    }
    .news-meta {
        color: #6c757d;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .news-description {
        color: #495057;
        font-size: 1rem;
        line-height: 1.6;
        margin-top: 0.75rem;
    }
    .app-header {
        text-align: center;
        padding: 2.5rem 0;
        background: linear-gradient(135deg, #0d6efd 0%, #0dcaf0 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .app-header h1 {
        margin: 0;
        padding: 0;
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .app-header p {
        margin-top: 1rem;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        border-top: 1px solid #dee2e6;
        margin-top: 3rem;
        background-color: white;
        border-radius: 12px;
    }
    .load-more {
        margin-top: 2rem;
        text-align: center;
    }
    .pagination-info {
        text-align: center;
        color: #6c757d;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
<div class="app-header">
    <h1>📰 Software Testing News Hub</h1>
    <p>Stay updated with the latest trends, tools, and practices in software testing!</p>
</div>
""",
    unsafe_allow_html=True,
)


# Function to format date
def format_date(date_str):
    try:
        date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        return date.strftime("%B %d, %Y")
    except:
        return date_str


# Function to fetch news
def fetch_testing_news():
    try:
        query = urllib.parse.quote("Software Testing AI News")
        url = f"https://news.google.com/rss/search?q={query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        with st.spinner("🔄 Fetching latest news..."):
            response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            return feed.entries
        else:
            st.error(f"Failed to fetch feed. Status code: {response.status_code}")
            return []

    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []


# Initialize session state for pagination
if "show_entries" not in st.session_state:
    st.session_state.show_entries = 20

# Add a refresh button in a container with some padding
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Refresh News Feed"):
            st.experimental_rerun()

# Fetch news
news_items = fetch_testing_news()

# Display news with pagination
if news_items:
    total_entries = len(news_items)
    displayed_items = news_items[: st.session_state.show_entries]

    # Display pagination info
    st.markdown(
        f"""
    <div class="pagination-info">
        Showing {min(st.session_state.show_entries, total_entries)} of {total_entries} news items
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Display news items
    for item in displayed_items:
        st.markdown(
            f"""
        <div class="news-card">
            <a href="{item.link}" target="_blank" class="news-title">{item.title}</a>
            <div class="news-meta">
                <span>📅 {format_date(item.published)}</span>
            </div>
            {f'<div class="news-description">{item.description}</div>' if hasattr(item, 'description') else ''}
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Load more button
    if st.session_state.show_entries < total_entries:
        st.markdown(
            """
        <div class="load-more">
        """,
            unsafe_allow_html=True,
        )
        if st.button("Load More News"):
            st.session_state.show_entries += 20
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ No news items found. Please try again later.")

# Footer
st.markdown(
    """
<div class="footer">
    <p>📰 Data sourced from Google News RSS • Updated in real-time</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">Bringing you the latest in software testing innovation</p>
</div>
""",
    unsafe_allow_html=True,
)
