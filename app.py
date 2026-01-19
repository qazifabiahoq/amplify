import streamlit as st
import os
from groq import Groq
import requests
from PIL import Image
import io
import base64
import time
import urllib.parse
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Amplify - AI Social Media Content Generator",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Corporate Design
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
    
    /* Typography fixes for Streamlit */
    .stApp, .stApp * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #111827 !important;
    }
    
    p, div, span, label, input, textarea, select {
        color: #374151 !important;
    }
    
    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin: 0 0 2.5rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.25);
    }
    
    .hero-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.75rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 0 0 0.75rem 0;
        letter-spacing: -0.03em;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.125rem;
        color: rgba(255,255,255,0.95) !important;
        margin: 0 0 1rem 0;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1.25rem;
        border-radius: 24px;
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 0.8125rem;
        margin: 0;
        border: 1px solid rgba(255,255,255,0.3);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.375rem;
        font-weight: 700;
        color: #111827 !important;
        margin: 2.5rem 0 1.25rem 0;
        padding-bottom: 0.625rem;
        border-bottom: 3px solid #7C3AED;
        display: inline-block;
    }
    
    /* Platform Cards */
    .platform-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.25rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #E5E7EB;
        transition: all 0.3s ease;
    }
    
    .platform-card:hover {
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.12);
        transform: translateY(-2px);
    }
    
    .platform-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.125rem;
        padding-bottom: 0.875rem;
        border-bottom: 2px solid #F3F4F6;
    }
    
    .platform-name {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.125rem;
        font-weight: 700;
        color: #111827 !important;
        margin: 0;
    }
    
    .platform-specs {
        font-size: 0.75rem;
        color: #6B7280 !important;
        margin-left: auto;
        background: #F3F4F6;
        padding: 0.375rem 0.875rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Post Content */
    .post-content {
        background: #F9FAFB;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin: 1.125rem 0;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9375rem;
        line-height: 1.7;
        color: #1F2937 !important;
        border-left: 4px solid #7C3AED;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* Buttons - Fixed Streamlit override */
    .stButton > button {
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.875rem 2rem !important;
        font-size: 0.9375rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25) !important;
        width: 100%;
        height: auto !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35) !important;
        background: linear-gradient(135deg, #6D28D9 0%, #2563EB 100%) !important;
    }
    
    .stButton > button p {
        color: #FFFFFF !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: #FFFFFF !important;
        color: #7C3AED !important;
        border: 2px solid #7C3AED !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        background: #7C3AED !important;
        color: #FFFFFF !important;
    }
    
    .stDownloadButton > button p {
        color: inherit !important;
    }
    
    /* Input styling */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 2px solid #E5E7EB !important;
        font-family: 'Inter', sans-serif !important;
        padding: 1rem !important;
        font-size: 0.9375rem !important;
        color: #1F2937 !important;
        background: #FFFFFF !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
        outline: none !important;
    }
    
    .stTextArea label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Text Input */
    .stTextInput input {
        border-radius: 10px !important;
        border: 2px solid #E5E7EB !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9375rem !important;
        color: #1F2937 !important;
    }
    
    .stTextInput input:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
    }
    
    .stTextInput label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }
    
    /* Selectbox */
    .stSelectbox label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
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
    .stRadio label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }
    
    .stRadio > div {
        color: #1F2937 !important;
    }
    
    /* Multiselect */
    .stMultiSelect label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #374151 !important;
        font-size: 0.9375rem !important;
    }
    
    /* Stats/Metrics */
    .stat-box {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    
    .stat-value {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.25rem;
        font-weight: 800;
        color: #7C3AED !important;
        margin: 0 0 0.375rem 0;
    }
    
    .stat-label {
        font-size: 0.8125rem;
        color: #6B7280 !important;
        margin: 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Loading animation */
    .loading-text {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem;
        color: #7C3AED !important;
        font-weight: 600;
        text-align: center;
        padding: 1rem;
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #FFFFFF !important;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        text-align: center;
        margin: 1.5rem 0;
        font-size: 0.9375rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E5E7EB;
        padding: 2rem 1.5rem !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #111827 !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #4B5563 !important;
        font-size: 0.875rem !important;
        line-height: 1.6 !important;
    }
    
    /* Info box */
    .info-box {
        background: #EEF2FF;
        border-left: 4px solid #7C3AED;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-box p {
        color: #4338CA !important;
        margin: 0;
        font-size: 0.875rem;
        line-height: 1.6;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #7C3AED 0%, #3B82F6 100%) !important;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #E5E7EB;
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
    """Initialize Groq API client"""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("GROQ_API_KEY not found in environment variables")
        st.info("""
        **Get your FREE Groq API key:**
        
        1. Visit https://console.groq.com
        2. Sign up (free)
        3. Create API key
        4. Add to .env file: `GROQ_API_KEY=your_key_here`
        """)
        st.stop()
    
    return Groq(api_key=api_key)


# AI Text Generation
def generate_social_post(client, platform, source_content, tone="professional"):
    """Generate platform-specific social media post using Groq AI"""
    
    platform_specs = {
        "LinkedIn": {
            "max_length": 3000,
            "style": "professional, thought leadership",
            "format": "Hook → Value → Call-to-action",
            "hashtags": 5
        },
        "Twitter": {
            "max_length": 280,
            "style": "concise, engaging, conversational",
            "format": "Hook → Key point → CTA/Question",
            "hashtags": 3
        },
        "Instagram": {
            "max_length": 2200,
            "style": "visual-first, storytelling, aspirational",
            "format": "Engaging story → Emotional connection → CTA",
            "hashtags": 10
        },
        "Facebook": {
            "max_length": 1000,
            "style": "community-focused, conversational, relatable",
            "format": "Personal angle → Story → Engagement question",
            "hashtags": 3
        }
    }
    
    spec = platform_specs[platform]
    
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
5. Use appropriate emojis for {platform}
6. Stay under {spec['max_length']} characters

Output ONLY the post content with hashtags. No explanations or meta-commentary."""

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Fast and high-quality
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.error(f"Error generating {platform} post: {str(e)}")
        return None


# AI Image Generation
def generate_platform_image(prompt, platform):
    """Generate platform-specific image using Pollinations.ai (FREE)"""
    
    # Platform-specific image dimensions
    dimensions = {
        "LinkedIn": {"width": 1200, "height": 627},
        "Twitter": {"width": 1200, "height": 675},
        "Instagram": {"width": 1080, "height": 1080},
        "Facebook": {"width": 1200, "height": 630}
    }
    
    dims = dimensions[platform]
    
    # Enhanced prompt for better quality
    enhanced_prompt = f"{prompt}, professional, high quality, clean design, {platform} social media post, modern aesthetic"
    
    # Pollinations.ai API (100% free, no key needed)
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={dims['width']}&height={dims['height']}&model=flux&nologo=true&enhance=true"
    
    try:
        response = requests.get(api_url, timeout=60)
        
        if response.status_code == 200:
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
        "LinkedIn": "1200×627",
        "Twitter": "1200×675",
        "Instagram": "1080×1080",
        "Facebook": "1200×630"
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
            key=f"download_img_{platform}"
        )
    
    # Display post content
    st.markdown(f'<div class="post-content">{post_content}</div>', unsafe_allow_html=True)
    
    # Copy button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(f"Copy Text", key=f"copy_{platform}"):
            st.success(f"Copied!")
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
            default=["LinkedIn", "Twitter", "Instagram"],
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
        - Text only: 5-10 seconds
        - With images: 30-45 seconds
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
            placeholder="Example: We just launched our new AI-powered analytics dashboard that helps businesses make data-driven decisions in real-time...",
            height=150
        )
        image_prompt = st.text_input(
            "Image concept (optional)",
            placeholder="Example: modern analytics dashboard with graphs and charts"
        )
        
    elif input_type == "URL (Blog/Article)":
        url = st.text_input(
            "Article URL",
            placeholder="https://yourblog.com/article"
        )
        if url:
            st.info("💡 Paste your article text below (URL fetching coming soon)")
            source_content = st.text_area(
                "Article content",
                placeholder="Paste your article text here...",
                height=150
            )
            image_prompt = st.text_input(
                "Image concept",
                placeholder="Example: content marketing strategy concept"
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
        st.info("Enter your content above and click 'Generate Content' to get started")
        
        # Show examples
        with st.expander("See Examples"):
            st.markdown("""
            **Example 1: Product Launch**
            ```
            We're excited to announce the launch of TaskFlow Pro - 
            an AI-powered project management tool that reduces 
            planning time by 60%. Built for modern teams who need 
            to move fast without sacrificing quality.
            ```
            
            **Example 2: Thought Leadership**
            ```
            The future of remote work isn't about working from home - 
            it's about working from anywhere. Here's what 5 years of 
            remote-first taught me about building distributed teams...
            ```
            
            **Example 3: Industry Insight**
            ```
            New research shows that 78% of consumers prefer brands 
            that use AI transparently. Here's how we're approaching 
            ethical AI in marketing...
            ```
            """)


if __name__ == "__main__":
    main()
