import streamlit as st
import google.generativeai as genai
import trafilatura
import os
from dotenv import load_dotenv
import validators
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class ArticleAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def extract_article(self, url):
        try:
            # Download the webpage
            downloaded = trafilatura.fetch_url(url)
            
            if downloaded is None:
                raise Exception("Failed to fetch the webpage")

            # Extract the main content
            article_text = trafilatura.extract(downloaded)
            
            if article_text is None:
                raise Exception("Failed to extract article content")

            # Get title using BeautifulSoup as backup
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.title.string if soup.title else "Title not found"

            return {
                'title': title,
                'text': article_text,
                'url': url,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'success': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error extracting article: {str(e)}"
            }

    def analyze_bias(self, article_data):
        prompt = f"""
        Analyze the following news article for bias. Consider:
        1. Political leaning (if any)
        2. Emotional language usage
        3. Factual reporting assessment
        4. Balance of perspectives
        5. Source credibility indicators
        
        Title: {article_data['title']}
        Article Text: {article_data['text'][:4000]}
        
        Provide a detailed analysis with:
        1. Bias Score (-5 to +5, where -5 is extremely biased and +5 is completely neutral)
        2. Key findings
        3. Examples of biased language (if any)
        4. Recommendations for more neutral reporting
        
        Format the response in a clear, structured manner.
        """

        try:
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'analysis': response.text
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error in analysis: {str(e)}"
            }

def main():
    st.set_page_config(
        page_title="News Bias Analyzer",
        page_icon="📰",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stAlert {
            margin-top: 1rem;
        }
        .article-info {
            padding: 1rem;
            background-color: #f0f2f6;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
        }
        .header-container {
            background-color: #1E1E1E;
            padding: 2rem;
            border-radius: 0.5rem;
            color: white;
            margin-bottom: 2rem;
        }
        .results-container {
            background-color: #1E1E1E;
            padding: 2rem;
            border-radius: 0.5rem;
            margin-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div class='header-container'>
            <h1>📰 News Article Bias Analyzer</h1>
            <p>Powered by Google's Gemini AI, this tool analyzes news articles for potential bias.
            Simply paste a news article URL below to get started.</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize analyzer
    analyzer = ArticleAnalyzer()

    # URL Input
    url = st.text_input("Enter News Article URL:", placeholder="https://example.com/news-article")

    if url:
        if not validators.url(url):
            st.error("⚠️ Please enter a valid URL")
            return

        with st.spinner("🔍 Analyzing article..."):
            # Extract article
            with st.status("📥 Extracting article content...") as status:
                article_data = analyzer.extract_article(url)
                
                if not article_data['success']:
                    st.error(f"❌ {article_data['error']}")
                    return
                
                status.update(label="✅ Article extracted successfully!", state="complete")

            # Display article info
            with st.expander("📄 Article Information", expanded=True):
                st.markdown("### Article Details")
                st.markdown(f"**Title:** {article_data['title']}")
                st.markdown(f"**URL:** {article_data['url']}")
                st.markdown(f"**Analysis Date:** {article_data['date']}")

            # Analyze bias
            with st.status("🤖 Analyzing bias...") as status:
                analysis_result = analyzer.analyze_bias(article_data)
                
                if not analysis_result['success']:
                    st.error(f"❌ {analysis_result['error']}")
                    return
                
                status.update(label="✅ Analysis complete!", state="complete")

            # Display results
            st.markdown("""
                <div class='results-container'>
                    <h2>🎯 Analysis Results</h2>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(analysis_result['analysis'])

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center'>
            <p></p>
            <p style='font-size: 0.8em; color: #666;'>
                Note: This tool provides an AI-based analysis and should be used as a supplementary resource.
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()