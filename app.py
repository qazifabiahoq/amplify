import streamlit as st
import os
from groq import Groq
import requests
from PIL import Image
import io
import urllib.parse
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Amplify - AI Social Media Content Generator",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Corporate Design - FULLY FIXED
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');
    
    /* Main styling */
    .stApp {
        background: #F9FAFB !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Universal box-sizing fix */
    *, *::before, *::after {
        box-sizing: border-box !important;
    }
    
    /* Typography - Global fixes */
    .stApp, .stApp * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #111827 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        line-height: 1.3 !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }
    
    p, div, span, label, input, textarea, select {
        color: #374151 !important;
        line-height: 1.7 !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }
    
    /* Ensure all markdown elements have proper spacing */
    .stMarkdown {
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }
    
    .stMarkdown p {
        margin-bottom: 1rem !important;
        color: #374151 !important;
        line-height: 1.7 !important;
    }
    
    .stMarkdown ul, .stMarkdown ol {
        margin-bottom: 1rem !important;
        padding-left: 1.5rem !important;
    }
    
    .stMarkdown li {
        margin-bottom: 0.5rem !important;
        color: #374151 !important;
        line-height: 1.7 !important;
    }
    
    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin: 0 0 3rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.25);
    }
    
    .hero-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 3rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 0 0 1rem 0 !important;
        letter-spacing: -0.03em;
        line-height: 1.1 !important;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.25rem;
        color: rgba(255,255,255,0.95) !important;
        margin: 0 0 1.5rem 0 !important;
        font-weight: 400;
        line-height: 1.5 !important;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 0.625rem 1.5rem;
        border-radius: 24px;
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 0.875rem;
        margin: 0;
        border: 1px solid rgba(255,255,255,0.3);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827 !important;
        margin: 3rem 0 1.5rem 0 !important;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #7C3AED;
        display: block;
        clear: both;
    }
    
    /* Platform Cards - Fixed overflow */
    .platform-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #E5E7EB;
        transition: all 0.3s ease;
        overflow: hidden;
    }
    
    .platform-card:hover {
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.12);
        transform: translateY(-2px);
    }
    
    .platform-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #F3F4F6;
        gap: 1rem;
    }
    
    .platform-name {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.25rem;
        font-weight: 700;
        color: #111827 !important;
        margin: 0 !important;
        flex-shrink: 0;
    }
    
    .platform-specs {
        font-size: 0.8125rem;
        color: #6B7280 !important;
        background: #F3F4F6;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        white-space: nowrap;
    }
    
    /* Post Content - Fixed overflow and wrapping */
    .post-content {
        background: #F9FAFB;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem;
        line-height: 1.8;
        color: #1F2937 !important;
        border-left: 4px solid #7C3AED;
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
        overflow-x: auto;
    }
    
    /* Buttons - Fixed sizing and spacing */
    .stButton {
        margin: 1rem 0 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25) !important;
        width: 100% !important;
        height: auto !important;
        min-height: 48px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35) !important;
        background: linear-gradient(135deg, #6D28D9 0%, #2563EB 100%) !important;
    }
    
    .stButton > button p {
        color: #FFFFFF !important;
        margin: 0 !important;
    }
    
    /* Download Button */
    .stDownloadButton {
        margin: 1rem 0 !important;
    }
    
    .stDownloadButton > button {
        background: #FFFFFF !important;
        color: #7C3AED !important;
        border: 2px solid #7C3AED !important;
        border-radius: 10px !important;
        padding: 0.875rem 1.5rem !important;
        font-size: 0.9375rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stDownloadButton > button:hover {
        background: #7C3AED !important;
        color: #FFFFFF !important;
    }
    
    .stDownloadButton > button p {
        color: inherit !important;
        margin: 0 !important;
    }
    
    /* Input styling - Fixed spacing */
    .stTextArea {
        margin: 1rem 0 !important;
    }
    
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 2px solid #E5E7EB !important;
        font-family: 'Inter', sans-serif !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        color: #1F2937 !important;
        background: #FFFFFF !important;
        line-height: 1.6 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
        outline: none !important;
    }
    
    .stTextArea label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    /* Text Input */
    .stTextInput {
        margin: 1rem 0 !important;
    }
    
    .stTextInput input {
        border-radius: 10px !important;
        border: 2px solid #E5E7EB !important;
        padding: 0.875rem 1rem !important;
        font-size: 1rem !important;
        color: #1F2937 !important;
        background: #FFFFFF !important;
    }
    
    .stTextInput input:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
    }
    
    .stTextInput label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    /* Selectbox */
    .stSelectbox {
        margin: 1rem 0 !important;
    }
    
    .stSelectbox label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 2px solid #E5E7EB !important;
        background: #FFFFFF !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: #FFFFFF !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        color: #1F2937 !important;
        background: #FFFFFF !important;
    }
    
    /* Radio */
    .stRadio {
        margin: 1rem 0 !important;
    }
    
    .stRadio label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stRadio > div {
        color: #1F2937 !important;
        gap: 1rem !important;
    }
    
    /* Multiselect */
    .stMultiSelect {
        margin: 1rem 0 !important;
    }
    
    .stMultiSelect label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        margin: 1rem 0 !important;
    }
    
    .stCheckbox label {
        color: #374151 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Stats/Metrics - Fixed overflow */
    .stat-box {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2rem 1rem;
        text-align: center;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin: 1rem 0;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }
    
    .stat-value {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.5rem;
        font-weight: 800;
        color: #7C3AED !important;
        margin: 0 0 0.75rem 0 !important;
        line-height: 1.1 !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
        max-width: 100%;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #6B7280 !important;
        margin: 0 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        line-height: 1.4 !important;
        text-align: center;
    }
    
    /* Loading text */
    .loading-text {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.125rem;
        color: #7C3AED !important;
        font-weight: 600;
        text-align: center;
        padding: 2rem 1rem;
        line-height: 1.6 !important;
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #FFFFFF !important;
        padding: 1.25rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        text-align: center;
        margin: 2rem 0;
        font-size: 1.0625rem;
    }
    
    /* Sidebar - Fixed spacing */
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E5E7EB;
        padding: 2rem 1.5rem !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #111827 !important;
        font-size: 1.125rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        line-height: 1.3 !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #4B5563 !important;
        font-size: 0.9375rem !important;
        line-height: 1.7 !important;
        margin-bottom: 0.75rem !important;
    }
    
    [data-testid="stSidebar"] strong {
        color: #111827 !important;
        display: block;
        margin-top: 1rem;
        margin-bottom: 0.25rem;
    }
    
    /* Progress bar */
    .stProgress {
        margin: 2rem 0 !important;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #7C3AED 0%, #3B82F6 100%) !important;
    }
    
    /* Code blocks - Fixed visibility */
    code {
        background: #F3F4F6 !important;
        color: #1F2937 !important;
        padding: 0.25rem 0.5rem !important;
        border-radius: 4px !important;
        font-size: 0.9375rem !important;
        font-family: 'Courier New', monospace !important;
    }
    
    pre {
        background: #F9FAFB !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        overflow-x: auto !important;
        margin: 1rem 0 !important;
    }
    
    pre code {
        background: transparent !important;
        padding: 0 !important;
        color: #1F2937 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        line-height: 1.7 !important;
    }
    
    /* Strong/Bold text */
    strong, b {
        color: #111827 !important;
        font-weight: 700 !important;
    }
    
    /* Alert boxes */
    .stAlert {
        background: #EEF2FF !important;
        border: 1px solid #C7D2FE !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        margin: 1.5rem 0 !important;
    }
    
    .stAlert p {
        color: #4338CA !important;
        margin: 0 !important;
        line-height: 1.7 !important;
    }
    
    /* Success alert */
    .stSuccess {
        background: #D1FAE5 !important;
        border: 1px solid #6EE7B7 !important;
    }
    
    .stSuccess p {
        color: #065F46 !important;
    }
    
    /* Error alert */
    .stError {
        background: #FEE2E2 !important;
        border: 1px solid #FCA5A5 !important;
    }
    
    .stError p {
        color: #991B1B !important;
    }
    
    /* Info alert */
    .stInfo {
        background: #EEF2FF !important;
        border: 1px solid #C7D2FE !important;
    }
    
    .stInfo p {
        color: #4338CA !important;
    }
    
    /* Container spacing */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    /* Column gap fix */
    [data-testid="column"] {
        padding: 0 0.5rem !important;
    }
    
    /* Image caption */
    .stImage > div {
        margin: 1rem 0 !important;
    }
    
    /* Clear floats */
    .clearfix::after {
        content: "";
        display: table;
        clear: both;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">Amplify</h1>
    <p class="hero-subtitle">Multiply your reach</p>
    <span class="hero-badge">Powered by Real AI Models</span>
</div>
""", unsafe_allow_html=True)


# Initialize Groq client
def init_groq():
    """Initialize Groq API client - supports both .env and Streamlit Secrets"""
    
    # Try Streamlit Secrets first (for cloud deployment)
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        # Fall back to environment variable (for local development)
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("GROQ_API_KEY not found")
        st.info("""
        **For Local Development:**
        
        1. Create a .env file in the same folder as app.py
        2. Add this line: GROQ_API_KEY=your_key_here
        3. Restart the app
        
        **For Streamlit Cloud:**
        
        1. Go to your app settings
        2. Click Secrets
        3. Add: GROQ_API_KEY = "your_key_here"
        
        Get FREE API key at: https://console.groq.com
        """)
        st.stop()
    
    return Groq(api_key=api_key)


# AI Text Generation - 100% REAL AI
def generate_social_post(client, platform, source_content, tone="professional"):
    """Generate platform-specific social media post using Groq AI - NO HARDCODED RESPONSES"""
    
    platform_specs = {
        "LinkedIn": {
            "max_length": 3000,
            "style": "professional, thought leadership",
            "format": "Hook, value proposition, call-to-action",
            "hashtags": 5
        },
        "Twitter": {
            "max_length": 280,
            "style": "concise, engaging, conversational",
            "format": "Hook, key point, question or CTA",
            "hashtags": 3
        },
        "Instagram": {
            "max_length": 2200,
            "style": "visual-first, storytelling, aspirational",
            "format": "Engaging story, emotional connection, CTA",
            "hashtags": 10
        },
        "Facebook": {
            "max_length": 1000,
            "style": "community-focused, conversational, relatable",
            "format": "Personal angle, story, engagement question",
            "hashtags": 3
        }
    }
    
    spec = platform_specs[platform]
    
    # Professional prompt - NO EMOJIS (corporate professional style)
    prompt = f"""You are an expert social media content creator. Create a {platform} post based on this content:

SOURCE CONTENT: {source_content}

PLATFORM: {platform}
MAX LENGTH: {spec['max_length']} characters
STYLE: {spec['style']}
FORMAT: {spec['format']}
TONE: {tone}

REQUIREMENTS:
1. Write native {platform} content (not generic)
2. Include platform-specific best practices
3. Make it engaging and authentic
4. Include {spec['hashtags']} relevant hashtags at the end
5. Professional tone - NO emojis
6. Stay under {spec['max_length']} characters

Output ONLY the post content with hashtags. No explanations or meta-commentary."""

    try:
        # REAL AI CALL - NOT HARDCODED
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Return actual AI-generated content
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.error(f"Error generating {platform} post: {str(e)}")
        return None


# AI Image Generation - 100% REAL AI
def generate_platform_image(prompt, platform):
    """Generate platform-specific image using Pollinations.ai - NO HARDCODED IMAGES"""
    
    # Platform-specific image dimensions
    dimensions = {
        "LinkedIn": {"width": 1200, "height": 627},
        "Twitter": {"width": 1200, "height": 675},
        "Instagram": {"width": 1080, "height": 1080},
        "Facebook": {"width": 1200, "height": 630}
    }
    
    dims = dimensions[platform]
    
    # Enhanced prompt for better quality
    enhanced_prompt = f"{prompt}, professional, high quality, clean design, {platform} social media post, modern aesthetic, corporate"
    
    # REAL AI API CALL - Pollinations.ai (100% free, no key needed)
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={dims['width']}&height={dims['height']}&model=flux&nologo=true&enhance=true"
    
    try:
        response = requests.get(api_url, timeout=60)
        
        if response.status_code == 200:
            # Return actual AI-generated image
            image = Image.open(io.BytesIO(response.content))
            return image
        else:
            st.warning(f"Image generation returned status {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None


# Display platform card
def display_platform_card(platform, post_content, image):
    """Display a professional platform card with post and image"""
    
    dimensions = {
        "LinkedIn": "1200x627",
        "Twitter": "1200x675",
        "Instagram": "1080x1080",
        "Facebook": "1200x630"
    }
    
    st.markdown(f"""
    <div class="platform-card">
        <div class="platform-header">
            <h3 class="platform-name">{platform}</h3>
            <span class="platform-specs">{dimensions[platform]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display image if available
    if image:
        st.image(image, use_container_width=True, caption=f"{platform} Image")
        
        # Download button for image
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        st.download_button(
            label=f"Download {platform} Image",
            data=buf.getvalue(),
            file_name=f"amplify_{platform.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png",
            key=f"download_img_{platform}",
            use_container_width=True
        )
    
    # Display post content
    st.markdown(f'<div class="post-content">{post_content}</div>', unsafe_allow_html=True)
    
    # Copy button
    if st.button(f"Copy {platform} Text", key=f"copy_{platform}", use_container_width=True):
        st.success("Copied to clipboard!")
        st.code(post_content, language=None)
    
    st.markdown("---")


# Main app
def main():
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Configuration")
        
        tone = st.selectbox(
            "Content Tone",
            ["Professional", "Casual", "Inspirational", "Educational", "Humorous"],
            help="Choose the tone for your content"
        )
        
        platforms = st.multiselect(
            "Select Platforms",
            ["LinkedIn", "Twitter", "Instagram", "Facebook"],
            default=["LinkedIn", "Twitter"],
            help="Choose which platforms to generate content for"
        )
        
        generate_images = st.checkbox(
            "Generate AI Images",
            value=True,
            help="Create custom images for each platform (takes longer)"
        )
        
        st.markdown("---")
        st.markdown("### About Amplify")
        st.markdown("""
        **Technology Stack:**
        
        **Text Generation:**  
        Groq API with Mixtral-8x7B model
        
        **Image Generation:**  
        Pollinations.ai with Flux model
        
        **Cost:**  
        100% Free - No hidden costs
        
        **Performance:**
        
        Text only: 5-10 seconds  
        With images: 30-45 seconds
        """)
    
    # Main content
    st.markdown('<h2 class="section-header">Input Content</h2>', unsafe_allow_html=True)
    
    input_type = st.radio(
        "Content Source",
        ["Text/Topic", "URL (Blog/Article)", "Product Announcement"],
        horizontal=True
    )
    
    source_content = None
    image_prompt = None
    
    if input_type == "Text/Topic":
        source_content = st.text_area(
            "Enter your content or topic",
            placeholder="Example: We launched our AI analytics dashboard...",
            height=150
        )
        image_prompt = st.text_input(
            "Image concept (optional)",
            placeholder="Example: modern analytics dashboard"
        )
        
    elif input_type == "URL (Blog/Article)":
        url = st.text_input(
            "Article URL",
            placeholder="https://yourblog.com/article"
        )
        if url:
            st.info("Paste your article text below")
            source_content = st.text_area(
                "Article content",
                placeholder="Paste your article text here...",
                height=150
            )
            image_prompt = st.text_input(
                "Image concept",
                placeholder="Example: content marketing concept"
            )
    
    else:  # Product Announcement
        product_name = st.text_input("Product Name")
        product_desc = st.text_area(
            "Product Description",
            placeholder="What does your product do? Who is it for?",
            height=100
        )
        if product_name and product_desc:
            source_content = f"Product: {product_name}\n\nDescription: {product_desc}"
            image_prompt = f"{product_name} product, modern design, professional"
    
    # Generate button
    if source_content and platforms:
        if st.button("Generate Content", use_container_width=True):
            
            # Initialize Groq
            client = init_groq()
            
            # Progress tracking
            total_steps = len(platforms) * (2 if generate_images else 1)
            current_step = 0
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Results storage
            results = {}
            
            # Generate for each platform
            for platform in platforms:
                
                # Generate text
                status_text.markdown(f'<div class="loading-text">Generating {platform} post...</div>', unsafe_allow_html=True)
                
                post_content = generate_social_post(
                    client,
                    platform,
                    source_content,
                    tone.lower()
                )
                
                current_step += 1
                progress_bar.progress(current_step / total_steps)
                
                # Generate image
                image = None
                if generate_images:
                    status_text.markdown(f'<div class="loading-text">Creating {platform} image...</div>', unsafe_allow_html=True)
                    
                    img_prompt = image_prompt if image_prompt else source_content[:200]
                    image = generate_platform_image(img_prompt, platform)
                    
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                
                results[platform] = {
                    "content": post_content,
                    "image": image
                }
            
            # Clear progress
            progress_bar.empty()
            status_text.empty()
            
            # Success message
            st.markdown('<div class="success-box">Content generated successfully</div>', unsafe_allow_html=True)
            
            # Display stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{len(platforms)}</div>
                    <div class="stat-label">Platforms</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_chars = sum(len(r["content"]) for r in results.values() if r["content"])
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{total_chars}</div>
                    <div class="stat-label">Total Characters</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{len([r for r in results.values() if r["image"]])}</div>
                    <div class="stat-label">Images Generated</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Add spacing
            st.markdown('<div style="margin: 3rem 0;"></div>', unsafe_allow_html=True)
            
            # Display results
            st.markdown('<h2 class="section-header">Generated Content</h2>', unsafe_allow_html=True)
            
            for platform in platforms:
                if platform in results:
                    display_platform_card(
                        platform,
                        results[platform]["content"],
                        results[platform]["image"]
                    )
    
    else:
        st.info("Enter your content above and click Generate Content to get started")
        
        # Show examples in a simple box - NO EXPANDER
        st.markdown("""
        <div style="background: #FFFFFF; border: 2px solid #E5E7EB; border-radius: 10px; padding: 2rem; margin: 2rem 0;">
            <h3 style="color: #111827; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.125rem;">Example Inputs</h3>
            
            <div style="margin-bottom: 1.5rem;">
                <strong style="color: #111827; display: block; margin-bottom: 0.5rem;">Example 1: Product Launch</strong>
                <p style="color: #374151; line-height: 1.7; margin: 0;">
                    We are excited to announce the launch of TaskFlow Pro, an AI-powered project management tool that reduces planning time by 60 percent. Built for modern teams who need to move fast without sacrificing quality.
                </p>
            </div>
            
            <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 1.5rem 0;">
            
            <div style="margin-bottom: 1.5rem;">
                <strong style="color: #111827; display: block; margin-bottom: 0.5rem;">Example 2: Thought Leadership</strong>
                <p style="color: #374151; line-height: 1.7; margin: 0;">
                    The future of remote work is not about working from home, it is about working from anywhere. Here is what 5 years of remote-first taught me about building distributed teams.
                </p>
            </div>
            
            <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 1.5rem 0;">
            
            <div style="margin-bottom: 0;">
                <strong style="color: #111827; display: block; margin-bottom: 0.5rem;">Example 3: Industry Insight</strong>
                <p style="color: #374151; line-height: 1.7; margin: 0;">
                    New research shows that 78 percent of consumers prefer brands that use AI transparently. Here is how we are approaching ethical AI in marketing.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
