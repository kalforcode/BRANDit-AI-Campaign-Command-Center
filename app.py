
import html
import os
from datetime import date
from pathlib import Path
from typing import Dict, Tuple

import streamlit as st
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
USE_AI = os.getenv("USE_AI", "true").lower() in {"1", "true", "yes", "y"}

st.set_page_config(
    page_title="BRANDit AI Campaign Command Center",
    page_icon="AI",
    layout="wide",
)

# -----------------------------
# AI-native dark UI styling
# -----------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

        :root {
            --bg-base:      #090E1A;
            --bg-surface:   #0D1424;
            --bg-card:      #111827;
            --bg-card-hover:#141f33;
            --border:       rgba(255,255,255,0.07);
            --border-glow:  rgba(0,255,200,0.18);
            --teal:         #00FFC8;
            --teal-dim:     rgba(0,255,200,0.12);
            --teal-mid:     rgba(0,255,200,0.55);
            --blue:         #0EA5E9;
            --blue-dim:     rgba(14,165,233,0.12);
            --text-primary: #F0F6FF;
            --text-secondary:#8B9BB4;
            --text-muted:   #4A5568;
            --mono:         'JetBrains Mono', monospace;
            --sans:         'DM Sans', sans-serif;
        }

        /* ── Base ── */
        .stApp {
            background: var(--bg-base) !important;
            font-family: var(--sans) !important;
        }
        .main .block-container {
            padding-top: 1.4rem;
            padding-bottom: 3rem;
            max-width: 1260px;
        }

        /* ── Global text override ── */
        body, main, p, li, label, span, div, h1, h2, h3, h4, h5, h6,
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3 {
            color: var(--text-primary) !important;
            font-family: var(--sans) !important;
        }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background: var(--bg-surface) !important;
            border-right: 1px solid var(--border) !important;
        }
        section[data-testid="stSidebar"] * {
            color: var(--text-primary) !important;
            font-family: var(--sans) !important;
        }
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea,
        section[data-testid="stSidebar"] [data-baseweb="select"] > div {
            background-color: var(--bg-card) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
        }
        section[data-testid="stSidebar"] input:focus,
        section[data-testid="stSidebar"] textarea:focus {
            border-color: var(--teal-mid) !important;
            box-shadow: 0 0 0 2px var(--teal-dim) !important;
        }
        section[data-testid="stSidebar"] input::placeholder,
        section[data-testid="stSidebar"] textarea::placeholder {
            color: var(--text-muted) !important;
        }
        section[data-testid="stSidebar"] label {
            color: var(--text-secondary) !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
        }

        /* Multiselect tags */
        [data-baseweb="tag"] {
            background-color: var(--teal-dim) !important;
            border: 1px solid var(--border-glow) !important;
            border-radius: 6px !important;
        }
        [data-baseweb="tag"] span,
        [data-baseweb="tag"] svg {
            color: var(--teal) !important;
            fill: var(--teal) !important;
        }

        /* ── Sidebar header card ── */
        .sidebar-title {
            padding: 16px;
            background: linear-gradient(135deg, #0D1F3C 0%, #0a2a3a 100%);
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
        }
        .sidebar-title::before {
            content: '';
            position: absolute;
            top: -30px; right: -30px;
            width: 80px; height: 80px;
            background: radial-gradient(circle, rgba(0,255,200,0.15), transparent 70%);
            border-radius: 50%;
        }
        .sidebar-title h3 {
            color: var(--teal) !important;
            font-family: var(--mono) !important;
            font-size: 0.92rem !important;
            font-weight: 700 !important;
            margin: 0 0 4px 0 !important;
            letter-spacing: 0.05em;
        }
        .sidebar-title p {
            color: var(--text-secondary) !important;
            font-size: 0.76rem !important;
            margin: 0 !important;
            line-height: 1.5;
        }

        /* ── Hero banner ── */
        .brand-hero {
            position: relative;
            overflow: hidden;
            padding: 36px 38px 32px 38px;
            border-radius: 20px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            margin-bottom: 20px;
        }
        .brand-hero::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse at top right, rgba(0,255,200,0.08) 0%, transparent 55%),
                radial-gradient(ellipse at bottom left, rgba(14,165,233,0.06) 0%, transparent 50%);
            pointer-events: none;
        }
        /* Decorative grid */
        .brand-hero::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image:
                linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
        }
        .brand-hero, .brand-hero * { color: var(--text-primary) !important; }

        .brand-kicker {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 12px;
            border-radius: 6px;
            background: var(--teal-dim);
            border: 1px solid var(--border-glow);
            font-family: var(--mono) !important;
            font-size: 0.68rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--teal) !important;
            margin-bottom: 1rem;
        }
        .brand-kicker::before {
            content: '';
        }

        .brand-hero h1 {
            font-family: var(--sans) !important;
            font-size: clamp(1.9rem, 3.5vw, 2.8rem) !important;
            font-weight: 700 !important;
            line-height: 1.05 !important;
            margin: 0 0 0.7rem 0 !important;
            letter-spacing: -0.03em;
            color: var(--text-primary) !important;
        }
        .brand-hero h1 span {
            color: var(--teal) !important;
        }
        .brand-hero p {
            font-size: 1rem !important;
            color: var(--text-secondary) !important;
            max-width: 860px;
            margin: 0 !important;
            line-height: 1.6;
        }

        /* ── Flow pills ── */
        .flow-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 0 0 22px 0;
            align-items: center;
        }
        .flow-label {
            font-family: var(--mono);
            font-size: 0.7rem;
            color: var(--text-muted) !important;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-right: 4px;
        }
        .flow-pill {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary) !important;
            font-family: var(--mono);
            letter-spacing: 0.03em;
        }
        .flow-pill.active {
            background: var(--teal-dim);
            border-color: var(--border-glow);
            color: var(--teal) !important;
        }
        .flow-arrow {
            color: var(--text-muted) !important;
            font-size: 0.75rem;
        }

        /* ── Mini cards ── */
        .mini-card {
            padding: 22px;
            border-radius: 16px;
            border: 1px solid var(--border);
            background: var(--bg-card);
            height: 100%;
            min-height: 140px;
            position: relative;
            overflow: hidden;
            transition: border-color 0.2s ease;
        }
        .mini-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--teal), var(--blue), transparent);
            opacity: 0.7;
        }
        .mini-card .card-icon {
            font-size: 1.4rem;
            margin-bottom: 10px;
            display: block;
        }
        .mini-card h3 {
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            margin: 0 0 8px 0 !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.01em;
        }
        .mini-card p {
            font-size: 0.85rem !important;
            margin: 0 !important;
            color: var(--text-secondary) !important;
            line-height: 1.55;
        }

        /* ── Section note ── */
        .section-note {
            padding: 12px 16px;
            border-radius: 10px;
            background: var(--blue-dim);
            border: 1px solid rgba(14,165,233,0.2);
            margin: 0.5rem 0 1.2rem 0;
            color: #7DD3FC !important;
            font-size: 0.88rem;
            font-weight: 500;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }
        .section-note::before {
            content: 'ℹ';
            font-weight: 700;
            color: var(--blue) !important;
            flex-shrink: 0;
            margin-top: 1px;
        }

        /* ── AI output box ── */
        .generated-box {
            padding: 26px 28px;
            border-radius: 16px;
            background: var(--bg-card) !important;
            border: 1px solid var(--border);
            border-left: 3px solid var(--teal);
            box-shadow: 0 0 30px rgba(0,255,200,0.04), inset 0 0 40px rgba(0,0,0,0.1);
            margin-top: 14px;
            margin-bottom: 16px;
            position: relative;
        }
        .generated-box::before {
            content: '// AI OUTPUT';
            position: absolute;
            top: 10px; right: 14px;
            font-family: var(--mono);
            font-size: 0.65rem;
            color: var(--teal) !important;
            opacity: 0.5;
            letter-spacing: 0.1em;
        }
        .generated-box, .generated-box * {
            color: var(--text-primary) !important;
            opacity: 1 !important;
        }
        .generated-box pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 0;
            padding: 0;
            background: transparent !important;
            border: none !important;
            font-family: var(--mono) !important;
            font-size: 0.88rem;
            line-height: 1.75;
            color: var(--text-primary) !important;
        }

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: var(--bg-surface);
            padding: 6px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 10px 18px;
            background: transparent;
            border: none !important;
            color: var(--text-secondary) !important;
            font-family: var(--mono) !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.03em;
            transition: all 0.15s ease;
        }
        .stTabs [aria-selected="true"] {
            background: var(--teal-dim) !important;
            color: var(--teal) !important;
            border: 1px solid var(--border-glow) !important;
        }
        .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
            background: rgba(255,255,255,0.04) !important;
            color: var(--text-primary) !important;
        }

        /* ── Buttons ── */
        .stButton > button {
            background: var(--teal-dim) !important;
            border: 1px solid var(--border-glow) !important;
            border-radius: 10px !important;
            color: var(--teal) !important;
            font-family: var(--mono) !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.04em;
            min-height: 46px;
            transition: all 0.15s ease;
        }
        .stButton > button:hover {
            background: rgba(0,255,200,0.2) !important;
            box-shadow: 0 0 16px rgba(0,255,200,0.15) !important;
        }
        div[data-testid="stDownloadButton"] button {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            color: var(--text-secondary) !important;
            font-family: var(--mono) !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            min-height: 40px;
        }
        div[data-testid="stDownloadButton"] button:hover {
            border-color: var(--teal-mid) !important;
            color: var(--teal) !important;
        }

        /* ── Markdown headings inside tabs ── */
        div[data-testid="stMarkdownContainer"] h3 {
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            margin-bottom: 4px !important;
            letter-spacing: -0.01em;
        }

        /* ── Dataframe ── */
        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border) !important;
        }
        div[data-testid="stDataFrame"] * {
            color: var(--text-primary) !important;
            background: var(--bg-card) !important;
        }

        /* ── Textarea ── */
        textarea {
            color: var(--text-primary) !important;
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            font-family: var(--mono) !important;
            font-size: 0.82rem !important;
        }

        /* ── Success / info boxes ── */
        div[data-testid="stAlert"] {
            background: var(--teal-dim) !important;
            border: 1px solid var(--border-glow) !important;
            border-radius: 10px !important;
            color: var(--teal) !important;
        }
        div[data-testid="stAlert"] * {
            color: var(--teal) !important;
        }

        /* ── Spinner ── */
        div[data-testid="stSpinner"] * {
            color: var(--teal) !important;
        }

        /* ── HR ── */
        hr {
            border: none;
            border-top: 1px solid var(--border);
            margin: 1.6rem 0;
        }

        /* ── Footer ── */
        .footer-box {
            margin-top: 2.4rem;
            padding: 18px 24px;
            border-radius: 14px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-secondary) !important;
            text-align: center;
            font-family: var(--mono) !important;
            font-size: 0.8rem;
            letter-spacing: 0.04em;
            position: relative;
            overflow: hidden;
        }
        .footer-box::before {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--teal), transparent);
            opacity: 0.4;
        }
        .footer-box, .footer-box * { color: var(--text-secondary) !important; }
        .footer-box b { color: var(--teal) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Fallback content
# -----------------------------
def fallback_response(module: str, brief: Dict[str, str]) -> str:
    destination = brief.get("destination", "Maldives Tourism")
    cities = brief.get("cities", "Mumbai, Delhi, Bengaluru")
    tone = brief.get("tone", "Premium + aspirational")
    language = brief.get("language", "English + Hinglish")

    fallbacks = {
        "strategy": f"""CAMPAIGN BIG IDEA
{destination} should be positioned in India as more than a luxury honeymoon destination. The campaign should turn Maldives into a set of Indian travel moments: romance, family time, wellness, destination weddings, luxury escapes, creator-led breaks and short international holidays.

CORE POSITIONING
From one luxury island image to many Indian travel moments.

TAGLINE OPTIONS
1. Maldives: Just One Blue Away
2. One Destination. Many Indian Travel Moments.
3. Your Island Story Begins Here
4. Beyond Luxury, Into Experience
5. A Short Flight to a Different World

AUDIENCE SEGMENTS
- Honeymooners: privacy, overwater villas, sunsets and once-in-a-lifetime romance
- Families: safety, food comfort, water activities and easy short-haul travel
- Luxury travellers: premium resorts, curated dining, seaplanes and exclusivity
- Gen Z / friends: reels, island hopping, adventure and bucket-list content
- Destination weddings: scenic ceremonies, Indian celebrations and premium hospitality
- Wellness travellers: spa, blue therapy, digital detox and slow travel

INDIA MARKET APPROACH
Start with {cities} and use {language} messaging. Keep the tone {tone}, but make the content practical through itineraries, cost explainers, creator stories, FAQs and save-worthy reels.

EXPECTED IMPACT
The campaign widens Maldives from a single honeymoon image to multiple bookable motivations, helping BRANDit create sharper PR stories, social content, creator briefs and client conversations.""",

        "content": f"""30-DAY SOCIAL MEDIA CONTENT ENGINE

WEEK 1: AWARENESS
- Reel: Think Maldives is only for honeymooners? Think again.
- Carousel: 6 Indian travel moments Maldives is perfect for
- Story Poll: What is your Maldives mood: romance, family, wedding, luxury or wellness?

WEEK 2: CONSIDERATION
- Reel: Maldives itinerary from India in 4 days
- Carousel: Villa vs beach stay: what should Indian travellers choose?
- Creator Video: First-time Maldives guide for Indian travellers

WEEK 3: TRUST BUILDING
- Reel: What nobody tells you before booking Maldives
- Post: Maldives for Indian weddings and celebrations
- Story Q&A: Flights, food, best months, budgets and resort selection

WEEK 4: CONVERSION
- Reel: Save this Maldives mini-itinerary
- Carousel: Best Maldives trip ideas for couples, families and friends
- CTA Story: Pick your Maldives moment and enquire now

SAMPLE REEL SCRIPT
Hook: Maldives is not only for honeymooners anymore.
Scene 1: Couple sunset villa
Scene 2: Family water activities
Scene 3: Friends on a sandbank
Scene 4: Wedding setup
Scene 5: Spa and wellness
CTA: Save this for your next international escape.

SAMPLE CAPTION
Maldives is not one holiday. It is many Indian travel moments in one destination - romance, family, weddings, wellness and pure blue luxury. Which Maldives moment would you choose?""",

        "pr": f"""PR STORY ENGINE

STORY ANGLE 1: BEYOND HONEYMOONS
Headline: Beyond Honeymoons: Maldives Repositions Itself for the New Indian Traveller
Angle: Show Maldives as a destination for families, friends, weddings, wellness and luxury escapes.

STORY ANGLE 2: SHORT-HAUL LUXURY
Headline: A Short Flight to a Different World: Why Indian Travellers Are Choosing Maldives
Angle: Convenience, premium experiences and international appeal close to India.

STORY ANGLE 3: INDIAN DESTINATION WEDDINGS
Headline: Maldives Emerges as a Dream Canvas for Indian Destination Weddings
Angle: Celebration-ready resorts, scenic backdrops and premium hospitality.

STORY ANGLE 4: WELLNESS + BLUE THERAPY
Headline: The Rise of Blue Wellness: Why Maldives Fits India's Slow Travel Mood
Angle: Wellness, spa, digital detox and experience-led luxury.

SAMPLE MEDIA PITCH OPENING
Hi [Editor Name],
Maldives is often seen by Indian travellers as a honeymoon destination, but the market is evolving. Families, wedding planners, wellness seekers and luxury travellers are now looking at Maldives as a short-haul international escape with multiple experiences in one destination.

We would love to explore a story on how Maldives is expanding its appeal for the new Indian traveller through luxury, family travel, destination weddings and wellness-led holidays.

AI VALUE FOR BRANDIT
AI can help the PR team create media-specific pitch versions, summarize coverage, identify story gaps, track sentiment and convert campaign activity into client-ready reporting.""",
    }
    return fallbacks.get(module, fallbacks["strategy"])

# -----------------------------
# AI functions
# -----------------------------
def build_prompt(module: str, brief: Dict[str, str]) -> str:
    base_context = f"""
You are an AI transformation strategist working for BRANDit, a branding, PR, marketing, travel and tourism representation agency in India.
Create practical, business-ready outputs for a tourism campaign.

Campaign brief:
- Destination/client: {brief.get('destination')}
- Main campaign goal: {brief.get('campaign_goal')}
- Audience: {brief.get('audience')}
- Indian city focus: {brief.get('cities')}
- Tone: {brief.get('tone')}
- Language style: {brief.get('language')}
- Budget level: {brief.get('budget')}
- Campaign duration: {brief.get('duration')}

Rules:
- Make the answer crisp, original and presentation-ready.
- Use Indian market thinking.
- Focus only on campaign strategy, social content and PR storytelling.
- Do not make unverifiable claims.
"""

    module_prompts = {
        "strategy": "Generate a campaign strategy: big idea, positioning, 5 tagline options, audience segmentation, content pillars and expected business impact.",
        "content": "Generate a 30-day social media content plan with reel ideas, captions, story ideas, hooks, CTAs and creator-led concepts.",
        "pr": "Generate PR story angles, media pitch headlines, sample pitch opening, media target categories and AI-assisted PR reporting ideas.",
    }
    return base_context + "\nTask: " + module_prompts[module]


def call_llm(prompt: str, module: str, brief: Dict[str, str], max_new_tokens: int = 2000) -> Tuple[str, str]:
    """Return (response, mode_used). Falls back to demo content when API is unavailable."""
    if not USE_AI or not HF_TOKEN:
        return fallback_response(module, brief), "Demo output ready"

    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import PromptTemplate
        from langchain_huggingface import HuggingFaceEndpoint

        llm = HuggingFaceEndpoint(
            repo_id=HF_MODEL,
            task="text-generation",
            max_new_tokens=max_new_tokens,
            temperature=0.55,
            top_p=0.9,
            repetition_penalty=1.08,
            huggingfacehub_api_token=HF_TOKEN,
        )
        prompt_template = PromptTemplate.from_template("{prompt}")
        chain = prompt_template | llm | StrOutputParser()
        result = chain.invoke({"prompt": prompt})
        if result and len(result.strip()) > 80:
            return result.strip(), "AI-assisted output ready"
    except Exception:
        pass

    try:
        from huggingface_hub import InferenceClient

        client = InferenceClient(model=HF_MODEL, token=HF_TOKEN)
        system_msg = "You are a concise, business-focused AI strategist for tourism marketing and PR."
        completion = client.chat_completion(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_new_tokens,
            temperature=0.55,
        )
        content = completion.choices[0].message.content
        if content and len(str(content).strip()) > 80:
            return str(content).strip(), "AI-assisted output ready"
    except Exception:
        pass

    return fallback_response(module, brief), "Demo output ready"

# -----------------------------
# Helpers
# -----------------------------
def get_brief_from_sidebar() -> Dict[str, str]:
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-title">
                <h3>CAMPAIGN BRIEF</h3>
                <p>Configure inputs to generate strategy, content and PR outputs.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        destination = st.text_input("Destination / Client", "Maldives Tourism")
        campaign_goal = st.text_area(
            "Campaign Goal",
            "Position Maldives Tourism in the Indian market as a multi-segment travel destination beyond only luxury and honeymoon travel.",
            height=92,
        )
        audience = st.multiselect(
            "Audience Segments",
            [
                "Honeymooners",
                "Families",
                "Luxury Travellers",
                "Gen Z Friends",
                "Destination Weddings",
                "Wellness Travellers",
                "MICE / Corporate Groups",
            ],
            default=[
                "Honeymooners",
                "Families",
                "Luxury Travellers",
                "Gen Z Friends",
                "Destination Weddings",
                "Wellness Travellers",
            ],
        )
        cities = st.text_input("Indian City Focus", "Mumbai, Delhi, Bengaluru, Ahmedabad, Hyderabad")
        tone = st.selectbox(
            "Tone",
            ["Premium + aspirational", "Youthful + social-first", "Luxury + editorial", "Warm + family-friendly"],
            index=0,
        )
        language = st.selectbox(
            "Language Style",
            ["English + Hinglish", "English only", "Hindi + English", "Regional language adaptation"],
            index=0,
        )
        budget = st.selectbox("Budget Level", ["Lean pilot", "Mid-size campaign", "Premium integrated campaign"], index=1)
        duration = st.selectbox("Campaign Duration", ["30 days", "60 days", "90 days", "6 months"], index=1)

    return {
        "destination": destination,
        "campaign_goal": campaign_goal,
        "audience": ", ".join(audience),
        "cities": cities,
        "tone": tone,
        "language": language,
        "budget": budget,
        "duration": duration,
    }


def show_generated_text(text: str):
    safe_text = html.escape(text)
    st.markdown(
        f"""
        <div class="generated-box">
            <pre>{safe_text}</pre>
        </div>
        """,
        unsafe_allow_html=True,
    )


def generate_button(module: str, brief: Dict[str, str], label: str):
    key = f"output_{module}"
    mode_key = f"mode_{module}"
    if st.button(label, use_container_width=True):
        with st.spinner("Generating..."):
            prompt = build_prompt(module, brief)
            result, mode = call_llm(prompt, module, brief)
            st.session_state[key] = result
            st.session_state[mode_key] = mode
    if key in st.session_state:
        st.success(st.session_state.get(mode_key, "Output ready"))
        show_generated_text(st.session_state[key])
        st.download_button(
            "Download output",
            st.session_state[key],
            file_name=f"brandit_{module}_output.txt",
            mime="text/plain",
            use_container_width=True,
        )

# -----------------------------
# Main UI
# -----------------------------
brief = get_brief_from_sidebar()

st.markdown(
    """
    <div class="brand-hero">
        <div class="brand-kicker">AI Prototype · Tourism Marketing · India Market</div>
        <h1>BRANDit <span>AI</span> Campaign Command Center</h1>
        <p><strong style="color:#F0F6FF !important;">Maldives India Edition</strong> - converts a tourism campaign brief into strategy, social content and PR storytelling outputs using generative AI.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="flow-strip">
        <span class="flow-label">workflow</span>
        <span class="flow-pill active">01 Brief</span>
        <span class="flow-arrow">→</span>
        <span class="flow-pill">02 Strategy</span>
        <span class="flow-arrow">→</span>
        <span class="flow-pill">03 Content</span>
        <span class="flow-arrow">→</span>
        <span class="flow-pill">04 PR</span>
        <span class="flow-arrow">→</span>
        <span class="flow-pill">05 Submit</span>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class='mini-card'>
        <h3>Campaign Strategy</h3>
        <p>Generates positioning, audience segments, taglines, content pillars and business impact.</p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class='mini-card'>
        <h3>Social Content Engine</h3>
        <p>Creates reels, captions, hooks, content buckets and a 30-day social direction.</p>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class='mini-card'>
        <h3>PR Story Engine</h3>
        <p>Builds media angles, pitch headlines and press-ready storytelling ideas.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

tabs = st.tabs([
    "01 · Brief",
    "02 · AI Strategy",
    "03 · Content Engine",
    "04 · PR Engine",
    "05 · Submission Note",
])

# -----------------------------
# Tab 1
# -----------------------------
with tabs[0]:
    st.markdown("### Campaign Brief Snapshot")
    st.markdown("<div class='section-note'>This structured brief powers all prototype outputs. It can be adapted for any tourism board, hotel brand or hospitality campaign.</div>", unsafe_allow_html=True)

    # Build HTML table manually so it renders correctly in dark mode
    rows_html = ""
    for k, v in brief.items():
        field = k.replace("_", " ").title()
        rows_html += f"<tr><td class='bf'>{field}</td><td>{html.escape(str(v))}</td></tr>"

    st.markdown(
        f"""
        <table class="brief-table">
            <thead><tr><th>Field</th><th>Value</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        <style>
        .brief-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'DM Sans', sans-serif;
            font-size: 0.88rem;
            margin-bottom: 1.2rem;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.07);
        }}
        .brief-table th {{
            background: #1a2540;
            color: #8B9BB4 !important;
            padding: 10px 16px;
            text-align: left;
            font-size: 0.74rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 700;
            border-bottom: 1px solid rgba(255,255,255,0.07);
        }}
        .brief-table td {{
            padding: 10px 16px;
            color: #F0F6FF !important;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            vertical-align: top;
            line-height: 1.5;
        }}
        .brief-table td.bf {{
            color: #8B9BB4 !important;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            white-space: nowrap;
            width: 180px;
        }}
        .brief-table tr:last-child td {{ border-bottom: none; }}
        .brief-table tr:nth-child(even) td {{ background: rgba(255,255,255,0.02); }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Why this prototype fits BRANDit")
    st.markdown(
        """
        - Connects **tourism positioning** with **PR and social media execution**.
        - Shows how AI can convert a campaign brief into usable strategy, content and media ideas.
        - Keeps the workflow simple for teams while still showing clear business value.
        - Reflects the AI Transformation Associate role through GenAI, prompt design, execution thinking and business applicability.
        """
    )

# -----------------------------
# Tab 2
# -----------------------------
with tabs[1]:
    st.markdown("### AI Campaign Strategy Generator")
    st.markdown("<div class='section-note'>Generates a campaign big idea, positioning, taglines, audience segmentation and expected business impact.</div>", unsafe_allow_html=True)
    generate_button("strategy", brief, "Generate Campaign Strategy")

# -----------------------------
# Tab 3
# -----------------------------
with tabs[2]:
    st.markdown("### Social Media Content Engine")
    st.markdown("<div class='section-note'>Generates reels, hooks, captions, content buckets and creator-led ideas for a 30-day plan.</div>", unsafe_allow_html=True)
    generate_button("content", brief, "Generate Content Plan")

    st.markdown("### Sample Content Calendar Structure")
    calendar_rows = [
        ["Awareness", "Reel", "Think Maldives is only for honeymooners?", "Save/share", "Honeymoon + Gen Z"],
        ["Consideration", "Carousel", "Maldives in 4 days from India", "Link click", "Families + Couples"],
        ["Trust", "Creator Vlog", "What nobody tells Indians before Maldives", "Comments", "First-time travellers"],
        ["Conversion", "Story + Poll", "Pick your Maldives mood", "DM / Lead", "All segments"],
    ]
    cal_headers = ["Funnel Stage", "Format", "Hook", "CTA", "Audience"]
    cal_head_html = "".join(f"<th>{h}</th>" for h in cal_headers)
    cal_rows_html = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>"
        for row in calendar_rows
    )
    st.markdown(
        f"""
        <table class="brief-table">
            <thead><tr>{cal_head_html}</tr></thead>
            <tbody>{cal_rows_html}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Tab 4
# -----------------------------
with tabs[3]:
    st.markdown("### PR Pitch + Media Story Engine")
    st.markdown("<div class='section-note'>Generates story angles, headlines, pitch openings and media target categories.</div>", unsafe_allow_html=True)
    generate_button("pr", brief, "Generate PR Plan")

# -----------------------------
# Tab 5
# -----------------------------
with tabs[4]:
    st.markdown("### Ready-to-Attach Submission Note")
    today = date.today().strftime("%d %B %Y")
    summary = f"""
BRANDit AI Campaign Command Center - Maldives India Edition
Prepared as an additional AI prototype for the AI Transformation Associate assignment.
Date: {today}

WHAT THIS DEMO SHOWS
- AI-assisted campaign planning for Maldives Tourism in the Indian market
- Audience segmentation and campaign theme generation
- Social media reel, hook and caption ideation
- PR story angle and pitch draft generation
- A simple brief-to-output workflow that can be adapted for tourism boards, hotels and hospitality brands

HOW THIS CAN HELP BRANDit
This prototype demonstrates how BRANDit can use AI to move faster from campaign brief to strategic direction, content planning and PR storytelling while keeping human review at the center.

TOOLS USED / SUPPORTED
- Python + Streamlit for the prototype UI
- Hugging Face LLM configured through environment variables
- LangChain for LLM workflow orchestration
- Pandas for structured campaign tables

PERSONAL IMPLEMENTATION ANGLE
I have worked on AI and analytics workflows such as document parsing, semantic matching, ranking systems, chatbot-style classification and reporting concepts. This prototype applies the same implementation thinking to tourism marketing, PR planning and campaign ideation.

CLOSING LINE
My goal is not only to use AI for faster content creation, but to help BRANDit build smarter workflows where every campaign becomes easier to plan, personalize and improve.

Prepared by: Kalpanasingh Chauhan
Contact: +91 8850159663 | chauhankalpana2020@gmail.com
""".strip()
    st.text_area("Copy this into your assignment submission", summary, height=430)
    st.download_button(
        "Download Submission Note",
        summary,
        file_name="BRANDit_AI_Prototype_Submission_Note.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.markdown(
    """
    <div class="footer-box">
        Prepared by <b>Kalpanasingh Chauhan</b> &nbsp;·&nbsp; +91 8850159663 &nbsp;·&nbsp; chauhankalpana2020@gmail.com
    </div>
    """,
    unsafe_allow_html=True,
)