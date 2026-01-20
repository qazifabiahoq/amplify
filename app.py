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

# Custom CSS - Professional Corporate Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        background: #F9FAFB !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    *, *::before, *::after {
        box-sizing: border-box !important;
    }
    
    .stApp, .stApp * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #111827 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        line-height: 1.3 !important;
    }
    
    p, div, span, label, input, textarea, select {
        color: #374151 !important;
        line-height: 1.7 !important;
    }
    
    /* Force textarea text to be visible */
    textarea {
        color: #1F2937 !important;
        background: #FFFFFF !important;
    }
    
    textarea::placeholder {
        color: #9CA3AF !important;
    }
    
    input {
        color: #1F2937 !important;
        background: #FFFFFF !important;
    }
    
    input::placeholder {
        color: #9CA3AF !important;
    }
    
    /* File uploader visibility fix */
    [data-testid="stFileUploader"] {
        background: #FFFFFF !important;
        border: 2px dashed #E5E7EB !important;
        border-radius: 10px !important;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: #F9FAFB !important;
        border: 2px dashed #D1D5DB !important;
        border-radius: 8px !important;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        color: #374151 !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #6B7280 !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: #7C3AED !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
    }
    
    /* Drag and drop text visibility */
    .uploadedFile {
        background: #FFFFFF !important;
        color: #1F2937 !important;
    }
    
    .st-emotion-cache-0 {
        color: #374151 !important;
    }
    
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
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.25rem;
        color: rgba(255,255,255,0.95) !important;
        margin: 0 0 1.5rem 0 !important;
        font-weight: 400;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.625rem 1.5rem;
        border-radius: 24px;
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 0.875rem;
        border: 1px solid rgba(255,255,255,0.3);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .section-header {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827 !important;
        margin: 3rem 0 1.5rem 0 !important;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #7C3AED;
    }
    
    .platform-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #E5E7EB;
    }
    
    .platform-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #F3F4F6;
    }
    
    .platform-name {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.25rem;
        font-weight: 700;
        color: #111827 !important;
    }
    
    .platform-specs {
        font-size: 0.8125rem;
        color: #6B7280 !important;
        background: #F3F4F6;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .post-content {
        background: #F9FAFB;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        font-size: 1rem;
        line-height: 1.8;
        color: #1F2937 !important;
        border-left: 4px solid #7C3AED;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        min-height: 48px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35) !important;
    }
    
    .stButton > button p {
        color: #FFFFFF !important;
    }
    
    .stDownloadButton > button {
        background: #FFFFFF !important;
        color: #7C3AED !important;
        border: 2px solid #7C3AED !important;
        width: 100% !important;
    }
    
    .stDownloadButton > button:hover {
        background: #7C3AED !important;
        color: #FFFFFF !important;
    }
    
    .stat-box {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2rem 1rem;
        text-align: center;
        border: 1px solid #E5E7EB;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #7C3AED !important;
        margin-bottom: 0.75rem;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #6B7280 !important;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .success-box {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #FFFFFF !important;
        padding: 1.25rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        text-align: center;
        margin: 2rem 0;
    }
    
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E5E7EB;
        padding: 2rem 1.5rem !important;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #7C3AED 0%, #3B82F6 100%) !important;
    }
    
    .example-box {
        background: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .example-box h3 {
        margin-top: 0 !important;
        margin-bottom: 1.5rem !important;
    }
    
    .example-item {
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .example-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    .example-title {
        font-weight: 700;
        color: #111827 !important;
        margin-bottom: 0.5rem;
    }
    
    .example-text {
        color: #374151 !important;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">Amplify</h1>
    <p class="hero-subtitle">Multiply your reach</p>
    <span class="hero-badge">Powered by Real AI Models</span>
</div>
""", unsafe_allow_html=True)


def analyze_image_with_vision(image):
    """Analyze uploaded image using FREE Hugging Face Vision API"""
    try:
        # Convert image to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        
        # Use Hugging Face Inference API (FREE, no key needed!)
        API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
        
        response = requests.post(API_URL, data=img_bytes, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                caption = result[0].get('generated_text', '')
                
                # Enhance the caption with more detail
                enhanced = f"Image shows: {caption}. This appears to be suitable for social media content about {caption.split()[0] if caption else 'this subject'}."
                return enhanced
            else:
                st.warning("Image analysis returned unclear results. Please describe the image manually below.")
                return None
        else:
            st.warning("Image analysis service is busy. Please describe the image manually below.")
            return None
            
    except Exception as e:
        st.warning(f"Could not auto-analyze image. Please describe it manually below.")
        return None


def init_groq():
    """Initialize Groq client"""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("GROQ_API_KEY not found")
        st.info("Add your Groq API key in Streamlit Secrets or .env file")
        st.stop()
    
    return Groq(api_key=api_key)


def generate_social_post(client, platform, source_content, tone="professional"):
    """Generate platform-specific post using Groq AI"""
    
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
    
    prompt = f"""Create a {platform} post based on this content:

SOURCE: {source_content}

PLATFORM: {platform}
MAX LENGTH: {spec['max_length']} characters
STYLE: {spec['style']}
FORMAT: {spec['format']}
TONE: {tone}

REQUIREMENTS:
1. Write native {platform} content
2. Make it engaging and authentic
3. Include {spec['hashtags']} relevant hashtags at the end
4. Professional tone, no emojis
5. Stay under {spec['max_length']} characters

Output ONLY the post content with hashtags."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Latest working model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def generate_platform_image(prompt, platform):
    """Generate platform image using Pollinations.ai with retry"""
    
    dimensions = {
        "LinkedIn": {"width": 1200, "height": 627},
        "Twitter": {"width": 1200, "height": 675},
        "Instagram": {"width": 1080, "height": 1080},
        "Facebook": {"width": 1200, "height": 630}
    }
    
    dims = dimensions[platform]
    enhanced_prompt = f"{prompt}, professional, high quality, clean design, {platform} social media, modern, corporate"
    
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={dims['width']}&height={dims['height']}&model=flux&nologo=true&enhance=true"
    
    # Try 3 times with increasing timeout
    for attempt in range(3):
        try:
            timeout = 60 + (attempt * 30)  # 60s, 90s, 120s
            response = requests.get(api_url, timeout=timeout)
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
        except requests.Timeout:
            if attempt < 2:
                continue
            st.warning(f"Image generation timed out for {platform}")
            return None
        except Exception as e:
            if attempt < 2:
                continue
            st.warning(f"Image generation failed for {platform}")
            return None
    
    return None


def display_platform_card(platform, post_content, image):
    """Display platform card"""
    
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
    
    if image:
        st.image(image, use_container_width=True)
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
    else:
        st.info(f"Image generation skipped or timed out for {platform}. You can still use the text content below.")
    
    if post_content:
        st.markdown(f'<div class="post-content">{post_content}</div>', unsafe_allow_html=True)
        
        if st.button(f"Copy {platform} Text", key=f"copy_{platform}", use_container_width=True):
            st.success("Copied!")
            st.code(post_content, language=None)
    else:
        st.error(f"Failed to generate content for {platform}. Please try again.")
    
    st.markdown("---")


def main():
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Configuration")
        
        tone = st.selectbox(
            "Content Tone",
            ["Professional", "Casual", "Inspirational", "Educational", "Humorous"]
        )
        
        platforms = st.multiselect(
            "Select Platforms",
            ["LinkedIn", "Twitter", "Instagram", "Facebook"],
            default=["LinkedIn", "Twitter"]
        )
        
        generate_images = st.checkbox(
            "Generate AI Images",
            value=True,
            help="Create custom images (takes longer)"
        )
        
        st.markdown("---")
        st.markdown("### About Amplify")
        st.markdown("""
        **Text:** Groq Llama-3.3-70B  
        **Images:** Pollinations.ai Flux  
        **Vision:** Hugging Face BLIP
        
        **Cost:** 100% Free
        
        **Speed:**  
        Text: 5-10s  
        Images: 30-90s  
        Vision: 10-15s
        """)
    
    # Main content
    st.markdown('<h2 class="section-header">Input Content</h2>', unsafe_allow_html=True)
    
    input_type = st.radio(
        "Content Source",
        ["Text/Topic", "Upload Image", "Product Announcement"],
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
        
    elif input_type == "Upload Image":
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png"],
            help="AI will analyze your photo and generate content"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Try auto-analysis with Hugging Face
            with st.spinner("Analyzing image with AI..."):
                vision_analysis = analyze_image_with_vision(image)
            
            if vision_analysis:
                st.success("Image analyzed successfully!")
                st.info(f"AI sees: {vision_analysis}")
                
                # Allow user to edit/enhance the description
                enhanced_description = st.text_area(
                    "Edit AI's description (optional)",
                    value=vision_analysis,
                    height=100,
                    help="AI analyzed your image. You can edit this description to be more specific."
                )
                
                source_content = f"Based on this image: {enhanced_description}"
                image_prompt = enhanced_description[:200]
            else:
                # Manual fallback
                st.warning("Auto-analysis unavailable. Please describe your image:")
                manual_description = st.text_area(
                    "Image description",
                    placeholder="Example: A team celebrating in a modern office with confetti and champagne",
                    height=100,
                    help="Describe what's in the image"
                )
                
                if manual_description:
                    source_content = f"Based on this image: {manual_description}"
                    image_prompt = manual_description[:200]
                else:
                    source_content = None
    
    else:  # Product Announcement
        product_name = st.text_input("Product Name")
        product_desc = st.text_area(
            "Product Description",
            placeholder="What does your product do?",
            height=100
        )
        if product_name and product_desc:
            source_content = f"Product: {product_name}\n\nDescription: {product_desc}"
            image_prompt = f"{product_name} product, modern design, professional"
    
    # Generate button
    if source_content and platforms:
        if st.button("Generate Content", use_container_width=True):
            
            client = init_groq()
            total_steps = len(platforms) * (2 if generate_images else 1)
            current_step = 0
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            results = {}
            
            for platform in platforms:
                status_text.text(f"Generating {platform} post...")
                
                post_content = generate_social_post(client, platform, source_content, tone.lower())
                current_step += 1
                progress_bar.progress(current_step / total_steps)
                
                image = None
                if generate_images:
                    status_text.text(f"Creating {platform} image...")
                    img_prompt = image_prompt if image_prompt else source_content[:200]
                    image = generate_platform_image(img_prompt, platform)
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                
                results[platform] = {"content": post_content, "image": image}
            
            progress_bar.empty()
            status_text.empty()
            
            st.markdown('<div class="success-box">Content generated successfully</div>', unsafe_allow_html=True)
            
            # Stats
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
                    <div class="stat-label">Characters</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{len([r for r in results.values() if r["image"]])}</div>
                    <div class="stat-label">Images</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<h2 class="section-header">Generated Content</h2>', unsafe_allow_html=True)
            
            for platform in platforms:
                if platform in results:
                    display_platform_card(platform, results[platform]["content"], results[platform]["image"])
    
    else:
        st.info("Enter your content and click Generate Content to get started")
        
        # Examples - Using native Streamlit components
        st.markdown("### Example Inputs")
        
        st.markdown("**Product Launch**")
        st.write("We are excited to announce TaskFlow Pro, an AI project management tool that reduces planning time by 60 percent. Built for modern teams.")
        st.divider()
        
        st.markdown("**Thought Leadership**")
        st.write("The future of remote work is not about working from home, it is about working from anywhere. Here is what 5 years taught me.")
        st.divider()
        
        st.markdown("**Industry Insight**")
        st.write("Research shows 78 percent of consumers prefer brands that use AI transparently. Here is our approach to ethical AI.")


if __name__ == "__main__":
    main()
