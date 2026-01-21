import streamlit as st
import os
from groq import Groq
import requests
from PIL import Image
import io
import urllib.parse
from datetime import datetime
import time
import base64
import numpy as np

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
    
    /* MULTISELECT FIXES */
    [data-baseweb="select"] {
        background: #FFFFFF !important;
    }
    
    [data-baseweb="tag"] {
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    
    [data-baseweb="tag"] span {
        color: #FFFFFF !important;
    }
    
    [data-baseweb="tag"] svg {
        fill: #FFFFFF !important;
    }
    
    [data-baseweb="popover"] {
        background: #FFFFFF !important;
    }
    
    [role="option"] {
        background: #FFFFFF !important;
        color: #1F2937 !important;
    }
    
    [role="option"]:hover {
        background: #F3F4F6 !important;
        color: #111827 !important;
    }
    
    [aria-selected="true"] {
        background: #EDE9FE !important;
        color: #7C3AED !important;
        font-weight: 600 !important;
    }
    
    [data-baseweb="select"] input {
        color: #1F2937 !important;
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
    
    .analysis-box {
        background: #EDE9FE;
        border: 2px solid #7C3AED;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .analysis-box h4 {
        margin-top: 0 !important;
        color: #7C3AED !important;
    }
    
    .analysis-box p {
        color: #1F2937 !important;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">Amplify</h1>
    <p class="hero-subtitle">Multiply your reach across 6 platforms</p>
    <span class="hero-badge">Powered by Computer Vision + AI</span>
</div>
""", unsafe_allow_html=True)


def analyze_image_with_vision(image):
    """Analyze image using free vision APIs: Google Vision → Amazon Rekognition → CLIP"""
    
    # Convert to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=95)
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    # ============================================
    # TIER 1: Google Cloud Vision (if API key exists)
    # ============================================
    try:
        google_key = st.secrets.get("google", {}).get("vision_api_key")
        
        if google_key:
            response = requests.post(
                f"https://vision.googleapis.com/v1/images:annotate?key={google_key}",
                json={
                    "requests": [{
                        "image": {"content": img_base64},
                        "features": [
                            {"type": "LABEL_DETECTION", "maxResults": 15},
                            {"type": "OBJECT_LOCALIZATION", "maxResults": 10},
                            {"type": "TEXT_DETECTION"},
                            {"type": "IMAGE_PROPERTIES"}
                        ]
                    }]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()['responses'][0]
                
                labels = [label['description'] for label in result.get('labelAnnotations', [])]
                objects = [obj['name'] for obj in result.get('localizedObjectAnnotations', [])]
                texts = [text.get('description', '') for text in result.get('textAnnotations', [])[:3]]
                colors_data = result.get('imagePropertiesAnnotation', {}).get('dominantColors', {}).get('colors', [])
                
                dominant_color = "neutral"
                if colors_data:
                    rgb = colors_data[0].get('color', {})
                    dominant_color = rgb_to_color_name(rgb.get('red', 0), rgb.get('green', 0), rgb.get('blue', 0))
                
                return {
                    "labels": labels[:10],
                    "objects": objects[:5],
                    "text": texts[:3],
                    "colors": [dominant_color],
                    "source": "Google Vision"
                }
    except:
        pass
    
    # ============================================
    # TIER 2: Amazon Rekognition (if AWS credentials exist)
    # ============================================
    try:
        aws_key = st.secrets.get("aws", {}).get("access_key_id")
        aws_secret = st.secrets.get("aws", {}).get("secret_access_key")
        
        if aws_key and aws_secret:
            import boto3
            
            client = boto3.client(
                'rekognition',
                aws_access_key_id=aws_key,
                aws_secret_access_key=aws_secret,
                region_name='us-east-1'
            )
            
            response = client.detect_labels(
                Image={'Bytes': buffered.getvalue()},
                MaxLabels=15,
                MinConfidence=70
            )
            
            labels = [label['Name'] for label in response['Labels']]
            
            # Try to detect text
            try:
                text_response = client.detect_text(Image={'Bytes': buffered.getvalue()})
                texts = [text['DetectedText'] for text in text_response.get('TextDetections', [])[:3]]
            except:
                texts = []
            
            dominant_color = extract_dominant_color(image)
            
            return {
                "labels": labels[:10],
                "objects": [],
                "text": texts,
                "colors": [dominant_color],
                "source": "Amazon Rekognition"
            }
    except:
        pass
    
    # ============================================
    # TIER 3: CLIP (Always works - no API key)
    # ============================================
    return analyze_with_clip(image)


def analyze_with_clip(image):
    """Fallback CLIP analysis"""
    try:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        
        headers = {"Content-Type": "application/octet-stream"}
        API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"
        
        # Better detection categories - more specific
        categories = [
            "laptop computer technology", "smartphone mobile phone", "tablet device screen",
            "headphones audio earbuds", "camera photography equipment", "watch timepiece wearable",
            "dashboard analytics interface", "graph chart visualization", "software application screenshot",
            "office workspace desk", "person human portrait", "meeting conference presentation",
            "product merchandise item", "food meal cuisine", "beverage drink coffee",
            "clothing fashion apparel", "furniture chair table", "building architecture exterior",
            "nature landscape outdoor", "indoor interior room", "text document paper",
            "logo brand symbol", "illustration graphic design", "photograph picture image"
        ]
        
        response = requests.post(
            API_URL,
            headers=headers,
            data=img_bytes,
            params={"candidate_labels": ",".join(categories)},
            timeout=20
        )
        
        labels = []
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                # Get top results and extract meaningful keywords
                for item in result[:10]:
                    label_text = item['label']
                    score = item.get('score', 0)
                    
                    # Only include if confidence is reasonable
                    if score > 0.1:
                        # Extract the main word (first word of label)
                        words = label_text.split()
                        labels.append(words[0])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_labels = []
        for label in labels:
            if label.lower() not in seen:
                seen.add(label.lower())
                unique_labels.append(label)
        
        # Get dominant color
        dominant_color = extract_dominant_color(image)
        
        return {
            "labels": unique_labels[:8] if unique_labels else ["technology", "digital", "product"],
            "objects": [],
            "text": [],
            "colors": [dominant_color],
            "source": "CLIP"
        }
        
    except:
        return {
            "labels": ["technology", "digital", "product"],
            "objects": [],
            "text": [],
            "colors": ["neutral"],
            "source": "fallback"
        }


def rgb_to_color_name(r, g, b):
    """Convert RGB to color name"""
    if r < 50 and g < 50 and b < 50:
        return "black"
    elif r > 200 and g > 200 and b > 200:
        return "white"
    elif r > g and r > b:
        if r > 150 and g < 100:
            return "red"
        else:
            return "orange"
    elif g > r and g > b:
        return "green"
    elif b > r and b > g:
        return "blue"
    elif r > 150 and g > 100 and b < 100:
        return "brown"
    elif r > 150 and g > 150 and b < 100:
        return "yellow"
    elif r > 100 and g < 100 and b > 100:
        return "purple"
    else:
        return "neutral"


def extract_dominant_color(image):
    """Extract dominant color from image"""
    img_array = np.array(image.resize((100, 100)))
    pixels = img_array.reshape(-1, 3)
    avg_color = np.mean(pixels, axis=0).astype(int)
    return rgb_to_color_name(avg_color[0], avg_color[1], avg_color[2])


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


def generate_social_post(client, platform, source_content, image_analysis, tone="professional"):
    """Generate platform-specific post using BOTH text content AND image analysis"""
    
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
        },
        "Pinterest": {
            "max_length": 500,
            "style": "visual-first, inspirational, discovery-focused",
            "format": "Eye-catching description, benefits, visual appeal",
            "hashtags": 20
        },
        "Threads": {
            "max_length": 500,
            "style": "casual, conversational, authentic",
            "format": "Personal take, relatable insight, engagement",
            "hashtags": 3
        }
    }
    
    spec = platform_specs[platform]
    
    # Build context from BOTH sources
    context_parts = [f"USER CONTENT: {source_content}"]
    
    if image_analysis:
        context_parts.append(f"\nIMAGE CONTAINS: {', '.join(image_analysis['labels'][:5])}")
        if image_analysis['objects']:
            context_parts.append(f"OBJECTS DETECTED: {', '.join(image_analysis['objects'][:3])}")
        if image_analysis['text']:
            context_parts.append(f"TEXT IN IMAGE: {', '.join([t for t in image_analysis['text'] if t])}")
        if image_analysis['colors'][0] != "neutral":
            context_parts.append(f"DOMINANT COLOR: {image_analysis['colors'][0]}")
    
    full_context = "\n".join(context_parts)
    
    prompt = f"""Create a {platform} post based on this content:

{full_context}

PLATFORM: {platform}
MAX LENGTH: {spec['max_length']} characters
STYLE: {spec['style']}
FORMAT: {spec['format']}
TONE: {tone}

REQUIREMENTS:
1. Write native {platform} content that references what's in the image
2. Make it engaging and authentic
3. Include {spec['hashtags']} relevant hashtags at the end
4. Professional tone, no emojis
5. Stay under {spec['max_length']} characters
6. Be specific about the product/content shown

Output ONLY the post content with hashtags."""

    # Try multiple models
    models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
    ]
    
    for model_name in models:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000,
                timeout=15
            )
            return response.choices[0].message.content.strip()
        except:
            continue
    
    st.error(f"Could not generate {platform} post. Please try again.")
    return None


def generate_platform_image(prompt, platform, image_analysis=None):
    """Generate platform image with enhanced prompt from image analysis"""
    
    dimensions = {
        "LinkedIn": {"width": 1200, "height": 627},
        "Twitter": {"width": 1200, "height": 675},
        "Instagram": {"width": 1080, "height": 1080},
        "Facebook": {"width": 1200, "height": 630},
        "Pinterest": {"width": 1000, "height": 1500},
        "Threads": {"width": 1080, "height": 1080}
    }
    
    dims = dimensions[platform]
    
    # Enhance prompt with image analysis
    enhanced_prompt = f"{prompt}, professional, high quality, clean design, {platform} social media, modern, corporate"
    
    if image_analysis:
        # Add detected elements to prompt
        elements = ", ".join(image_analysis['labels'][:3])
        color = image_analysis['colors'][0]
        enhanced_prompt = f"{elements}, {color} tones, {enhanced_prompt}"
    
    # Try Pollinations
    try:
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={dims['width']}&height={dims['height']}&model=flux&nologo=true&enhance=true"
        
        response = requests.get(api_url, timeout=45)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except:
        pass
    
    # Try faster Pollinations
    try:
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={dims['width']}&height={dims['height']}&nologo=true"
        response = requests.get(api_url, timeout=45)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except:
        pass
    
    # Try HF SDXL
    try:
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        payload = {"inputs": enhanced_prompt}
        
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            image = image.resize((dims['width'], dims['height']), Image.Resampling.LANCZOS)
            return image
    except:
        pass
    
    return None


def display_platform_card(platform, post_content, image):
    """Display platform card"""
    
    dimensions = {
        "LinkedIn": "1200×627",
        "Twitter": "1200×675",
        "Instagram": "1080×1080",
        "Facebook": "1200×630",
        "Pinterest": "1000×1500",
        "Threads": "1080×1080"
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
        st.image(image, use_container_width=False, width=600, caption=f"{platform} Image")
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
        st.markdown("### Settings")
        
        tone = st.selectbox(
            "Writing Style",
            ["Professional", "Casual", "Inspirational", "Educational", "Humorous"],
            help="How should your posts sound?"
        )
        
        generate_images = True
        
        st.markdown("---")
        st.markdown("### How It Works")
        st.markdown("""
        1. Select platforms
        
        2. Upload image (auto-analyzed!)
        
        3. Add description (optional)
        
        4. Get AI-generated posts
        
        **Computer Vision:**  
        Detects objects, text, colors automatically!
        
        **100% Free**
        """)
        
        st.markdown("---")
        st.markdown("### Supported Platforms")
        st.markdown("""
        **LinkedIn** - Professional  
        **Twitter** - Microblog  
        **Instagram** - Visual  
        **Facebook** - Social  
        **Pinterest** - Discovery  
        **Threads** - Conversational  
        """)
    
    # Main content
    st.markdown('<h2 class="section-header">Input Content</h2>', unsafe_allow_html=True)
    
    # Platform selector
    st.markdown("**Select Platforms:**")
    platforms = st.multiselect(
        "Choose which platforms to generate content for",
        ["LinkedIn", "Twitter", "Instagram", "Facebook", "Pinterest", "Threads"],
        default=["LinkedIn", "Twitter", "Instagram", "Facebook"],
        help="Select the platforms where you want to post",
        label_visibility="collapsed"
    )
    
    if not platforms:
        st.warning("Please select at least one platform above")
    
    st.markdown("---")
    
    input_type = st.radio(
        "Content Source",
        ["Text/Topic", "Product/Visual Content"],
        horizontal=True
    )
    
    source_content = None
    image_prompt = None
    image_analysis = None
    
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
        
    elif input_type == "Product/Visual Content":
        st.markdown("**Upload image - AI will analyze it automatically!**")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload image",
                type=["jpg", "jpeg", "png"],
                help="Upload product photo, event pic, or any visual"
            )
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Your Image", use_container_width=True)
                
                # AUTO-ANALYZE IMAGE
                with st.spinner("Analyzing image with Computer Vision..."):
                    image_analysis = analyze_image_with_vision(image)
                
                # Show analysis results
                if image_analysis:
                    st.markdown(f"""
                    <div class="analysis-box">
                        <h4>Image Analysis ({image_analysis['source']})</h4>
                        <p><strong>Detected:</strong> {', '.join(image_analysis['labels'][:5])}</p>
                        {f"<p><strong>Objects:</strong> {', '.join(image_analysis['objects'][:3])}</p>" if image_analysis['objects'] else ""}
                        {f"<p><strong>Text:</strong> {', '.join([t for t in image_analysis['text'] if t][:2])}</p>" if image_analysis['text'] else ""}
                        <p><strong>Color:</strong> {image_analysis['colors'][0]}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            product_name = st.text_input(
                "Product/Topic Name (optional)",
                placeholder="Example: MindFlow AI Dashboard"
            )
            
            product_desc = st.text_area(
                "Additional Description (optional)",
                placeholder="Add more context about what's in the image...",
                height=200,
                help="AI already analyzed the image - this is optional extra context"
            )
        
        # Build source content
        content_parts = []
        
        if product_name:
            content_parts.append(f"Product/Topic: {product_name}")
        
        if product_desc:
            content_parts.append(f"Description: {product_desc}")
        
        # If they uploaded image but no text, use image analysis
        if not content_parts and image_analysis:
            content_parts.append(f"Image showing: {', '.join(image_analysis['labels'][:5])}")
        
        if content_parts:
            source_content = "\n\n".join(content_parts)
            image_prompt = product_desc[:200] if product_desc else product_name
        else:
            source_content = None
    
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
                status_text.text(f"{platform}: Writing with image context...")
                
                post_content = generate_social_post(client, platform, source_content, image_analysis, tone.lower())
                current_step += 1
                progress_bar.progress(current_step / total_steps)
                
                image = None
                if generate_images:
                    status_text.text(f"{platform} image: Generating...")
                    img_prompt = image_prompt if image_prompt else source_content[:200]
                    image = generate_platform_image(img_prompt, platform, image_analysis)
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                
                results[platform] = {"content": post_content, "image": image}
            
            progress_bar.empty()
            status_text.empty()
            
            st.markdown('<div class="success-box">Content generated with image analysis!</div>', unsafe_allow_html=True)
            
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
        st.info("Upload an image and AI will analyze it automatically, or enter text content!")


if __name__ == "__main__":
    main()
