import os
import json
import streamlit as st
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="🍎 Food AI Analyzer",
    page_icon="🍎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Playfair+Display:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* Hide default streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Hero title */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 6vw, 3.2rem);
    font-weight: 800;
    background: linear-gradient(90deg, #f9d423, #ff4e50, #fc913a, #f9d423);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
    text-align: center;
    line-height: 1.2;
    margin-bottom: 0.2rem;
}

@keyframes shimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

.hero-sub {
    text-align: center;
    color: rgba(255,255,255,0.65);
    font-size: clamp(0.85rem, 2.5vw, 1rem);
    margin-bottom: 1.5rem;
    letter-spacing: 0.05em;
}

/* Card container */
.card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Section headers */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.1rem, 3.5vw, 1.4rem);
    font-weight: 700;
    color: #f9d423;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Freshness badge */
.badge-fresh { background: linear-gradient(135deg, #11998e, #38ef7d); color: white; padding: 0.5rem 1.2rem; border-radius: 50px; font-weight: 800; font-size: 1rem; display: inline-block; }
.badge-moderate { background: linear-gradient(135deg, #f7971e, #ffd200); color: #222; padding: 0.5rem 1.2rem; border-radius: 50px; font-weight: 800; font-size: 1rem; display: inline-block; }
.badge-notfresh { background: linear-gradient(135deg, #cb2d3e, #ef473a); color: white; padding: 0.5rem 1.2rem; border-radius: 50px; font-weight: 800; font-size: 1rem; display: inline-block; }

/* Score ring */
.score-ring {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    font-weight: 900;
    font-size: 1.4rem;
    box-shadow: 0 0 20px rgba(249,212,35,0.4);
    border: 4px solid #f9d423;
    color: #f9d423;
    background: rgba(249,212,35,0.1);
}

/* Nutrient pill */
.nutri-pill {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 0.5rem 0.8rem;
    text-align: center;
    color: white;
    font-size: 0.82rem;
}
.nutri-pill strong { display: block; font-size: 1rem; color: #f9d423; }

/* Tag pills */
.tag { background: rgba(249,212,35,0.15); border: 1px solid rgba(249,212,35,0.3); color: #f9d423; padding: 0.25rem 0.7rem; border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block; margin: 0.2rem; }
.tag-red { background: rgba(255,78,80,0.15); border: 1px solid rgba(255,78,80,0.3); color: #ff6b6b; }
.tag-green { background: rgba(56,239,125,0.12); border: 1px solid rgba(56,239,125,0.3); color: #38ef7d; }
.tag-blue { background: rgba(100,160,255,0.15); border: 1px solid rgba(100,160,255,0.3); color: #64a0ff; }

/* Expander override */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #f9d423, #ff4e50) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 4px 20px rgba(255,78,80,0.4) !important;
    transition: transform 0.15s ease !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; }

/* Divider */
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 1rem 0; }

/* Info boxes */
.info-box {
    background: rgba(100,160,255,0.1);
    border-left: 3px solid #64a0ff;
    border-radius: 0 12px 12px 0;
    padding: 0.7rem 1rem;
    color: rgba(255,255,255,0.85);
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

/* Progress bar */
.progress-bar-wrap { background: rgba(255,255,255,0.1); border-radius: 50px; height: 10px; overflow: hidden; margin: 0.3rem 0; }
.progress-bar-fill { height: 100%; border-radius: 50px; background: linear-gradient(90deg, #11998e, #38ef7d); }

/* Text color overrides for dark theme */
p, li, label, .stMarkdown { color: rgba(255,255,255,0.87) !important; }
h1,h2,h3 { color: white !important; }
.stAlert { border-radius: 12px !important; }

/* Table */
.stTable { background: rgba(255,255,255,0.04) !important; border-radius: 12px !important; }

/* Mobile */
@media (max-width: 600px) {
    .stApp { padding: 0 !important; }
    .card { padding: 1rem; border-radius: 14px; }
    .score-ring { width: 65px; height: 65px; font-size: 1.1rem; }
}
</style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown('<div class="hero-title">🍎 Food AI Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">✨ Snap · Analyze · Eat Smart · Powered by Google Gemini</div>', unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if GEMINI_API_KEY:
        st.success("✅ Gemini API connected")
    else:
        st.error("❌ GEMINI_API_KEY missing!\nAdd it to your `.env` file.")

    st.markdown("---")
    st.markdown("### 🧠 About")
    st.markdown("""
    This app uses **Google Gemini Vision** to deeply analyze any food photo — freshness, nutrition, recipes, and more.

    📸 Take a photo or upload  
    🔍 Get instant AI analysis  
    🍽️ Discover recipes & tips
    """)
    st.markdown("---")
    st.markdown("### 📊 Features")
    features = ["Freshness scoring", "Nutrition breakdown", "Recipe ideas", "Diet compatibility", "Allergen check", "Glycemic impact", "Storage tips", "Waste reduction tips", "Mood-based snacks"]
    for f in features:
        st.markdown(f"✦ {f}")

# ====================== IMAGE INPUT ======================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📸 Capture Your Food</div>', unsafe_allow_html=True)

col_cam, col_up = st.columns([1, 1])
with col_cam:
    use_camera = st.checkbox("📷 Use Camera", value=False, help="Turn on to use your device camera")
with col_up:
    st.markdown(" ")

uploaded_file = st.file_uploader("📁 Upload an image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
camera_file = st.camera_input("📸 Take a photo", label_visibility="collapsed") if use_camera else None

image_file = camera_file or uploaded_file
st.markdown('</div>', unsafe_allow_html=True)

if image_file:
    image = Image.open(image_file)

    # Show image nicely - FIXED: use_container_width instead of deprecated use_column_width
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col_img, col_info = st.columns([2, 1])
    with col_img:
        st.image(image, caption="Your Food 📷", use_container_width=True)
    with col_info:
        st.markdown("**Image loaded ✅**")
        st.markdown(f"Size: `{image.size[0]}×{image.size[1]}`")
        st.markdown(f"Mode: `{image.mode}`")
        st.markdown("Ready for analysis!")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Analyze My Food!", type="primary"):
        with st.spinner("🤖 Gemini is analyzing your food (10–20 sec)..."):
            try:
                if GEMINI_API_KEY:
                    from google import genai
                    from google.genai import types

                    client = genai.Client(api_key=GEMINI_API_KEY)

                    prompt = """
You are a world-class food scientist, nutritionist, chef, and food safety expert. Analyze this food image with extreme visual precision and return ONLY valid JSON (no markdown, no code blocks, no extra text) with this exact structure:

{
  "food_name": "Full primary name with alternate names, regional names, and origin country/cuisine",
  "food_emoji": "1-2 relevant food emojis",
  "description": "2-3 sentence vivid description of what this food is, its taste profile, and cultural significance",
  "freshness": "Fresh | Moderately Fresh | Not Fresh",
  "freshness_reason": "Detailed visual reasoning — color, texture, spots, moisture, shape, smell indicators",
  "freshness_score": 8,
  "shelf_life": "X days at room temp; Y weeks refrigerated; Z months frozen",
  "storage_tips": "Specific storage methods, containers, temperature recommendations",
  "nutrition": {
    "calories": "52 kcal per 100g",
    "protein": "0.3g",
    "carbs": "13.8g",
    "fat": "0.2g",
    "fiber": "2.4g",
    "vitamins": "C, K, B6",
    "minerals": "Potassium, Magnesium",
    "sugar_content": "10.4g natural sugars",
    "water_content": "86%",
    "health_score": 8
  },
  "ingredients": ["list of main components/ingredients visible"],
  "recipes": [
    {"name": "Recipe Name", "description": "long recipe description", "time": "15 min", "difficulty": "Easy"},
    {"name": "Recipe Name 2", "description": "long recipe description", "time": "30 min", "difficulty": "Medium"},
    {"name": "Recipe Name 3", "description": "long recipe description", "time": "45 min", "difficulty": "Hard"}
  ],
  "suitable_diets": ["Vegan", "Gluten-free", "Keto", "Paleo", "Low-carb"],
  "not_suitable_for": ["Diabetics (high sugar)", "Specific conditions"],
  "allergens": ["list or None detected"],
  "glycemic_impact": "Low | Medium | High",
  "glycemic_index": 36,
  "glycemic_explanation": "Brief explanation of blood sugar impact",
  "storage_method": "Fridge | Freezer | Pantry | Counter",
  "ideal_temp": "0-4°C refrigerated",
  "ripening_guide": "How this food ripens and how to identify peak freshness",
  "shelf_life_extension": "Specific tips to extend freshness — freezing, vacuum seal, etc.",
  "food_pairings": ["Cheddar cheese", "Peanut butter", "Cinnamon", "Walnuts"],
  "cooking_hacks": ["Tip 1", "Tip 2", "Tip 3"],
  "flavor_profile": ["Sweet", "Tart", "Crisp"],
  "texture": "Crunchy, juicy",
  "aroma": "Mild, fruity",
  "portion_suggestions": "Suggested serving size and how to reduce waste",
  "leftover_ideas": ["Creative leftover recipe 1", "Creative leftover recipe 2"],
  "ripeness_score": 9,
  "expiration_countdown": "12-18 days",
  "visual_indicator": "Eat Now | Store Safely | Use Soon | Discard",
  "snack_suggestions": ["Snack idea 1 with mood/diet context", "Snack idea 2"],
  "fun_fact": "1 interesting/surprising fact about this food",
  "origin_story": "Brief cultural or historical origin of this food",
  "sustainability_tip": "Eco-friendly usage tip or environmental note",
  "mood_pairing": "Best mood or occasion to enjoy this food",
  "confidence": "High | Medium | Low",
  "warning": "Any safety warning if food appears spoiled or potentially dangerous — else null"
}
"""

                    img_bytes = BytesIO()
                    image.save(img_bytes, format="PNG")
                    img_bytes.seek(0)

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            prompt,
                            types.Part.from_bytes(
                                data=img_bytes.getvalue(),
                                mime_type="image/png"
                            )
                        ]
                    )

                    text = response.text.strip()
                    if text.startswith("```json"):
                        text = text.split("```json")[1].split("```")[0].strip()
                    elif text.startswith("```"):
                        text = text.split("```")[1].strip()

                    analysis = json.loads(text)

                else:
                    st.warning("⚠️ Using demo data — no API key detected")
                    analysis = {
                        "food_name": "Fresh Red Apple (Malus domestica)",
                        "food_emoji": "🍎",
                        "description": "A crisp, juicy red apple with vibrant color and firm flesh. Known for its perfect balance of sweet and tart flavors, apples are one of the most widely consumed fruits globally with origins in Central Asia.",
                        "freshness": "Fresh",
                        "freshness_reason": "Vibrant red skin with no bruising, firm texture, no wrinkles or soft spots visible.",
                        "freshness_score": 9,
                        "shelf_life": "7-10 days room temp; 4-6 weeks refrigerated; 8-12 months frozen (sliced)",
                        "storage_tips": "Store in fridge crisper drawer in a perforated bag. Keep away from onions and ethylene-sensitive produce.",
                        "nutrition": {
                            "calories": "52 kcal per 100g",
                            "protein": "0.3g",
                            "carbs": "13.8g",
                            "fat": "0.2g",
                            "fiber": "2.4g",
                            "vitamins": "C, K, B6",
                            "minerals": "Potassium, Magnesium",
                            "sugar_content": "10.4g natural sugars",
                            "water_content": "86%",
                            "health_score": 8
                        },
                        "ingredients": ["Apple"],
                        "recipes": [
                            {"name": "Cinnamon Baked Apples", "description": "Warm, spiced apples baked until tender", "time": "20 min", "difficulty": "Easy"},
                            {"name": "Apple Walnut Salad", "description": "Crisp apple with walnuts and honey dressing", "time": "10 min", "difficulty": "Easy"},
                            {"name": "Homemade Applesauce", "description": "Smooth, naturally sweetened apple puree", "time": "30 min", "difficulty": "Medium"}
                        ],
                        "suitable_diets": ["Vegan", "Gluten-free", "Paleo", "Low-fat", "Whole30"],
                        "not_suitable_for": ["High fructose diets"],
                        "allergens": ["None detected"],
                        "glycemic_impact": "Low",
                        "glycemic_index": 36,
                        "glycemic_explanation": "Low GI due to fiber content slowing sugar absorption.",
                        "storage_method": "Fridge",
                        "ideal_temp": "0-4°C",
                        "ripening_guide": "Apples are harvested ripe. A slight give to pressure means peak sweetness.",
                        "shelf_life_extension": "Slice and freeze in single layers; lemon juice prevents browning.",
                        "food_pairings": ["Cheddar cheese", "Peanut butter", "Cinnamon", "Walnuts", "Honey"],
                        "cooking_hacks": ["Lemon juice prevents browning", "Microwave 2 min for quick applesauce", "Freeze slices for smoothies"],
                        "flavor_profile": ["Sweet", "Tart", "Crisp"],
                        "texture": "Crunchy, juicy",
                        "aroma": "Mild, fruity, sweet",
                        "portion_suggestions": "1 medium apple (182g) per serving. Use peels in tea.",
                        "leftover_ideas": ["Apple crumble topping", "Apple chutney", "Dried apple chips"],
                        "ripeness_score": 9,
                        "expiration_countdown": "12-18 days",
                        "visual_indicator": "Eat Now",
                        "snack_suggestions": ["Apple slices + almond butter (post-workout)", "Apple + Greek yogurt parfait (light evening snack)"],
                        "fun_fact": "There are over 7,500 known apple cultivars worldwide! 🌍",
                        "origin_story": "Apples originated in Central Asia near Kazakhstan and have been cultivated for at least 4,000 years.",
                        "sustainability_tip": "Apple cores and peels make excellent compost. Buy local varieties to reduce food miles.",
                        "mood_pairing": "Perfect for a focused work session or a refreshing midday snack.",
                        "confidence": "High",
                        "warning": None
                    }

                # ====================== DISPLAY RESULTS ======================
                if analysis.get("warning"):
                    st.markdown(f"""
                    <div style='background:linear-gradient(135deg,#cb2d3e,#ef473a);color:white;padding:1rem;border-radius:14px;margin-bottom:1rem;font-weight:700;'>
                        ⚠️ SAFETY WARNING: {analysis["warning"]}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style='text-align:center;padding:0.5rem 0 1rem;'>
                    <span style='font-size:3rem;'>{analysis.get('food_emoji','🍽️')}</span>
                    <h2 style='color:white;font-family:Playfair Display,serif;margin:0.3rem 0 0;'>{analysis.get('food_name','Unknown Food')}</h2>
                    <span style='background:rgba(249,212,35,0.15);border:1px solid rgba(249,212,35,0.3);color:#f9d423;padding:0.2rem 0.8rem;border-radius:20px;font-size:0.8rem;font-weight:700;'>Confidence: {analysis.get('confidence','Medium')}</span>
                </div>
                """, unsafe_allow_html=True)

                if analysis.get("description"):
                    st.markdown(f'<div class="info-box">{analysis["description"]}</div>', unsafe_allow_html=True)

                if analysis.get("fun_fact"):
                    st.markdown(f"""
                    <div style='background:rgba(100,160,255,0.12);border-left:3px solid #64a0ff;border-radius:0 12px 12px 0;padding:0.7rem 1rem;color:rgba(255,255,255,0.85);font-size:0.88rem;margin:0.5rem 0 1rem;'>
                        💡 <strong>Fun Fact:</strong> {analysis["fun_fact"]}
                    </div>
                    """, unsafe_allow_html=True)

                # ---- FRESHNESS ----
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">🌿 Freshness Report</div>', unsafe_allow_html=True)

                freshness = analysis.get("freshness", "Unknown")
                badge_class = {"Fresh": "badge-fresh", "Moderately Fresh": "badge-moderate", "Not Fresh": "badge-notfresh"}.get(freshness, "badge-moderate")
                score = analysis.get("freshness_score", analysis.get("ripeness_score", 7))
                try:
                    score_val = int(str(score).replace("/10", "").strip())
                except:
                    score_val = 7

                col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
                with col_f1:
                    st.markdown(f'<div class="{badge_class}">{freshness}</div>', unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:0.88rem;margin-top:0.5rem;'>{analysis.get('freshness_reason','')}</p>", unsafe_allow_html=True)
                with col_f2:
                    st.markdown(f"""
                    <div class='score-ring'>{score_val}<span style='font-size:0.5rem;'>/10</span></div>
                    <div style='font-size:0.7rem;color:rgba(255,255,255,0.5);text-align:center;margin-top:0.3rem;'>Freshness</div>
                    """, unsafe_allow_html=True)
                with col_f3:
                    vi = analysis.get("visual_indicator", "Store")
                    vi_colors = {"Eat Now": "#38ef7d", "Store Safely": "#64a0ff", "Use Soon": "#ffd200", "Discard": "#ff4e50"}
                    vi_color = vi_colors.get(vi, "#ffd200")
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.07);border-radius:12px;padding:0.6rem;text-align:center;border:1px solid {vi_color}40;'>
                        <div style='color:{vi_color};font-weight:800;font-size:0.85rem;'>{vi}</div>
                        <div style='color:rgba(255,255,255,0.5);font-size:0.7rem;'>Status</div>
                    </div>
                    <div style='background:rgba(255,255,255,0.07);border-radius:12px;padding:0.6rem;text-align:center;margin-top:0.5rem;'>
                        <div style='color:#f9d423;font-weight:800;font-size:0.85rem;'>⏰ {analysis.get("expiration_countdown","N/A")}</div>
                        <div style='color:rgba(255,255,255,0.5);font-size:0.7rem;'>Days Left</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # ---- NUTRITION ----
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">📊 Nutrition Breakdown</div>', unsafe_allow_html=True)
                nutri = analysis.get("nutrition", {})

                if nutri:
                    hs = nutri.get("health_score", 7)
                    try: 
                        hs_val = int(str(hs).replace("/10","").strip())
                    except: 
                        hs_val = 7
                    
                    st.markdown(f"""
                    <div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:0.8rem;'>
                        <span style='color:rgba(255,255,255,0.6);font-size:0.85rem;white-space:nowrap;'>Health Score</span>
                        <div class='progress-bar-wrap' style='flex:1;'>
                            <div class='progress-bar-fill' style='width:{hs_val*10}%;'></div>
                        </div>
                        <span style='color:#38ef7d;font-weight:800;font-size:0.9rem;'>{hs_val}/10</span>
                    </div>
                    """, unsafe_allow_html=True)

                    cols_n = st.columns(4)
                    n_items = [
                        ("🔥", "Calories", nutri.get("calories","—")),
                        ("💪", "Protein", nutri.get("protein","—")),
                        ("🌾", "Carbs", nutri.get("carbs","—")),
                        ("🧈", "Fat", nutri.get("fat","—")),
                    ]
                    for i, (em, label, val) in enumerate(n_items):
                        with cols_n[i]:
                            st.markdown(f"""
                            <div class='nutri-pill'>
                                <span style='font-size:1.2rem;'>{em}</span>
                                <strong>{val}</strong>
                                <div style='color:rgba(255,255,255,0.5);font-size:0.72rem;'>{label}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    cols_n2 = st.columns(4)
                    n_items2 = [
                        ("🌿", "Fiber", nutri.get("fiber","—")),
                        ("💧", "Water", nutri.get("water_content","—")),
                        ("🍬", "Sugar", nutri.get("sugar_content","—")),
                        ("🧪", "Vitamins", nutri.get("vitamins","—")),
                    ]
                    for i, (em, label, val) in enumerate(n_items2):
                        with cols_n2[i]:
                            st.markdown(f"""
                            <div class='nutri-pill'>
                                <span style='font-size:1.2rem;'>{em}</span>
                                <strong style='font-size:0.82rem;'>{val}</strong>
                                <div style='color:rgba(255,255,255,0.5);font-size:0.72rem;'>{label}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown(f"🪨 **Minerals:** {nutri.get('minerals','—')}", unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # ---- GLYCEMIC & DIET ----
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">🩸 Glycemic & Diet Info</div>', unsafe_allow_html=True)

                gi_val = analysis.get("glycemic_index", 50)
                try: gi_num = int(str(gi_val))
                except: gi_num = 50
                gi_color = "#38ef7d" if gi_num < 55 else "#ffd200" if gi_num < 70 else "#ff4e50"
                gi_label = analysis.get("glycemic_impact", "Medium")

                col_gi1, col_gi2 = st.columns([1, 2])
                with col_gi1:
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.07);border-radius:14px;padding:0.8rem;text-align:center;border:1px solid {gi_color}30;'>
                        <div style='color:{gi_color};font-size:1.8rem;font-weight:900;'>{gi_num}</div>
                        <div style='color:{gi_color};font-size:0.75rem;font-weight:700;'>GI Index</div>
                        <div style='color:rgba(255,255,255,0.5);font-size:0.7rem;'>{gi_label} Impact</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_gi2:
                    st.markdown(f"<p style='font-size:0.88rem;color:rgba(255,255,255,0.8);'>{analysis.get('glycemic_explanation','')}</p>", unsafe_allow_html=True)
                    if analysis.get("suitable_diets"):
                        diets_html = "".join([f"<span class='tag tag-green'>{d}</span>" for d in analysis["suitable_diets"]])
                        st.markdown(diets_html, unsafe_allow_html=True)

                if analysis.get("not_suitable_for"):
                    not_suitable = "".join([f"<span class='tag tag-red'>⚠️ {d}</span>" for d in analysis["not_suitable_for"]])
                    st.markdown(f"<div><span style='font-size:0.8rem;color:rgba(255,255,255,0.5);'>Not ideal for: </span>{not_suitable}</div>", unsafe_allow_html=True)

                if analysis.get("allergens"):
                    allergens_list = analysis["allergens"]
                    if allergens_list and allergens_list != ["None detected"]:
                        allergens_html = "".join([f"<span class='tag tag-red'>🚨 {a}</span>" for a in allergens_list])
                        st.markdown(f"<div><span style='font-size:0.8rem;color:rgba(255,255,255,0.5);'>Allergens: </span>{allergens_html}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("✅ **No common allergens detected**")

                st.markdown('</div>', unsafe_allow_html=True)

                # ---- RECIPES ----
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">🍳 Recipe Ideas</div>', unsafe_allow_html=True)
                recipes = analysis.get("recipes", [])
                if recipes:
                    for recipe in recipes:
                        if isinstance(recipe, dict):
                            diff_color = {"Easy": "#38ef7d", "Medium": "#ffd200", "Hard": "#ff4e50"}.get(recipe.get("difficulty","Easy"), "#38ef7d")
                            st.markdown(f"""
                            <div style='background:rgba(255,255,255,0.06);border-radius:14px;padding:0.8rem 1rem;margin-bottom:0.6rem;border-left:3px solid {diff_color};'>
                                <div style='font-weight:800;color:white;'>🍽️ {recipe.get("name","")}</div>
                                <div style='color:rgba(255,255,255,0.7);font-size:0.85rem;margin:0.2rem 0;'>{recipe.get("description","")}</div>
                                <div style='display:flex;gap:0.5rem;'>
                                    <span class='tag'>⏱️ {recipe.get("time","")}</span>
                                    <span style='background:rgba(255,255,255,0.08);border-radius:20px;padding:0.2rem 0.6rem;color:{diff_color};font-size:0.75rem;font-weight:700;'>{recipe.get("difficulty","")}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                with st.expander("🥂 Food Pairings & Cooking Hacks"):
                    if analysis.get("food_pairings"):
                        pairs_html = "".join([f"<span class='tag'>🤝 {p}</span>" for p in analysis["food_pairings"]])
                        st.markdown(f"**Perfect Pairings:** {pairs_html}", unsafe_allow_html=True)
                    if analysis.get("cooking_hacks"):
                        st.markdown("**🔧 Cooking Hacks:**")
                        for h in analysis["cooking_hacks"]:
                            st.markdown(f"• {h}")

                st.markdown('</div>', unsafe_allow_html=True)

                # ---- STORAGE ----
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">🧊 Storage & Shelf Life</div>', unsafe_allow_html=True)
                col_st1, col_st2 = st.columns([1, 1])
                with col_st1:
                    sm = analysis.get("storage_method", "Fridge")
                    sm_icons = {"Fridge": "🧊", "Freezer": "❄️", "Pantry": "🏠", "Counter": "🍽️"}
                    sm_icon = sm_icons.get(sm, "📦")
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.07);border-radius:12px;padding:0.8rem;text-align:center;'>
                        <div style='font-size:2rem;'>{sm_icon}</div>
                        <div style='color:#f9d423;font-weight:800;'>{sm}</div>
                        <div style='color:rgba(255,255,255,0.5);font-size:0.75rem;'>{analysis.get("ideal_temp","")}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_st2:
                    st.markdown(f"📅 **Shelf Life:** {analysis.get('shelf_life','N/A')}")
                    st.markdown(f"💡 {analysis.get('storage_tips','')}")

                with st.expander("🔬 Ripening & Extension Tips"):
                    st.markdown(f"**Ripening Guide:** {analysis.get('ripening_guide','')}")
                    st.markdown(f"**Extend Freshness:** {analysis.get('shelf_life_extension','')}")

                st.markdown('</div>', unsafe_allow_html=True)

                # Final footer note
                st.markdown("""
                <div style='text-align:center;padding:1rem 0;color:rgba(255,255,255,0.35);font-size:0.75rem;'>
                    Analysis powered by Google Gemini • Results are AI estimates based on visual analysis
                </div>
                """, unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("⚠️ Couldn't parse Gemini's response as JSON.")
                with st.expander("Raw Response (debug)"):
                    st.code(text)
            except Exception as e:
                st.error(f"❌ Analysis Error: {str(e)}")

else:
    # Empty state
    st.markdown("""
    <div style='text-align:center;padding:3rem 1rem;background:rgba(255,255,255,0.04);border-radius:20px;border:2px dashed rgba(255,255,255,0.15);margin-top:1rem;'>
        <div style='font-size:3.5rem;margin-bottom:0.8rem;'>📷</div>
        <div style='color:white;font-size:1.1rem;font-weight:700;'>No image yet</div>
        <div style='color:rgba(255,255,255,0.5);font-size:0.88rem;margin-top:0.3rem;'>Upload a photo or enable the camera above to get started!</div>
        <div style='margin-top:1.2rem;display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;'>
            <span style='background:rgba(249,212,35,0.12);border:1px solid rgba(249,212,35,0.3);color:#f9d423;padding:0.35rem 0.9rem;border-radius:20px;font-size:0.8rem;font-weight:700;'>🌿 Freshness Check</span>
            <span style='background:rgba(249,212,35,0.12);border:1px solid rgba(249,212,35,0.3);color:#f9d423;padding:0.35rem 0.9rem;border-radius:20px;font-size:0.8rem;font-weight:700;'>📊 Nutrition Facts</span>
            <span style='background:rgba(249,212,35,0.12);border:1px solid rgba(249,212,35,0.3);color:#f9d423;padding:0.35rem 0.9rem;border-radius:20px;font-size:0.8rem;font-weight:700;'>🍳 Recipes</span>
            <span style='background:rgba(249,212,35,0.12);border:1px solid rgba(249,212,35,0.3);color:#f9d423;padding:0.35rem 0.9rem;border-radius:20px;font-size:0.8rem;font-weight:700;'>🧊 Storage Tips</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;padding:1.5rem 0 0.5rem;color:rgba(255,255,255,0.25);font-size:0.72rem;letter-spacing:0.1em;'>
    🍎 FOOD AI ANALYZER • POWERED BY GOOGLE GEMINI
</div>
""", unsafe_allow_html=True)