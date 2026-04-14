import streamlit as st
import pandas as pd
import requests
from io import StringIO

# ============================================
# CONFIGURATION - UPDATE THESE URLs
# ============================================
CSV_URL = 'https://raw.githubusercontent.com/jonathanlau97/caudalieprizepool/main/overthink_sales_final.csv'

# Background images from GitHub
# Replace these with your actual raw GitHub image URLs
# Format: https://raw.githubusercontent.com/USER/REPO/BRANCH/PATH/image.jpg

DESKTOP_BG_URL = 'https://raw.githubusercontent.com/jonathanlau97/overthinkprizepool/main/desktop_bg.jpeg'
MOBILE_BG_URL  = 'https://raw.githubusercontent.com/jonathanlau97/overthinkprizepool/main/mobile_bg.jpeg'

# Breakpoint (px) below which mobile background is used
MOBILE_BREAKPOINT = 768

# Fallback gradient (used when images fail to load)
FALLBACK_GRADIENT = 'linear-gradient(135deg, #0d4f4f 0%, #0a7a7a 25%, #00b3b3 55%, #00cccc 75%, #004d4d 100%)'

# Overlay opacity over background image (0.0 = no overlay, 1.0 = full colour overlay)
# Increase this if text is hard to read over your background image
OVERLAY_OPACITY = 0.45
OVERLAY_COLOR   = '0, 30, 30'  # RGB for the dark teal overlay tint
# ============================================


# --- Page Configuration ---
st.set_page_config(
    page_title="Overthink : Crew Sales Performance",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def check_image_url(url: str) -> bool:
    """Return True if the URL responds with a valid image content-type."""
    try:
        r = requests.head(url, timeout=5)
        content_type = r.headers.get('Content-Type', '')
        return r.status_code == 200 and 'image' in content_type
    except Exception:
        return False


def apply_background_css(desktop_url: str, mobile_url: str):
    """
    Inject CSS that:
    - Uses desktop_url for screens wider than MOBILE_BREAKPOINT px
    - Uses mobile_url for narrower screens
    - Falls back to FALLBACK_GRADIENT if either URL is invalid
    - Adds a semi-transparent overlay so content stays legible
    - Dynamically adapts layout spacing to the background image dimensions
    """
    # Validate URLs (skip in production to avoid latency; keep for dev)
    desktop_valid = check_image_url(desktop_url)
    mobile_valid  = check_image_url(mobile_url)

    desktop_bg = f'url("{desktop_url}")' if desktop_valid else FALLBACK_GRADIENT
    mobile_bg  = f'url("{mobile_url}")'  if mobile_valid  else FALLBACK_GRADIENT

    # If an image is used we want cover; if gradient, no-repeat is irrelevant
    desktop_size   = 'cover' if desktop_valid else 'auto'
    mobile_size    = 'cover' if mobile_valid  else 'auto'
    desktop_repeat = 'no-repeat' if desktop_valid else 'no-repeat'
    mobile_repeat  = 'no-repeat' if mobile_valid  else 'no-repeat'

    css = f"""
    <style>
        /* ── Reset ──────────────────────────────────────────── */
        #MainMenu  {{ visibility: hidden; }}
        footer     {{ visibility: hidden; }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            position: relative;
            z-index: 1;
        }}

        /* ── Root background element ─────────────────────────
           We use a ::before pseudo-element on .stApp so we can
           layer an opacity overlay on top without affecting
           the content z-stack.
        ─────────────────────────────────────────────────────── */
        .stApp {{
            position: relative;
            min-height: 100vh;
            background: {desktop_bg} center center / {desktop_size} {desktop_repeat} fixed,
                        {FALLBACK_GRADIENT};
        }}

        /* Semi-transparent overlay for readability */
        .stApp::before {{
            content: '';
            position: fixed;
            inset: 0;
            background: rgba({OVERLAY_COLOR}, {OVERLAY_OPACITY});
            z-index: 0;
            pointer-events: none;
        }}

        /* ── Mobile background swap ──────────────────────────── */
        @media (max-width: {MOBILE_BREAKPOINT}px) {{
            .stApp {{
                background: {mobile_bg} center top / {mobile_size} {mobile_repeat} fixed,
                            {FALLBACK_GRADIENT};
            }}
        }}

        /* ── Glassmorphism cards ─────────────────────────────── */
        .glass-card {{
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.20);
            padding: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.30);
            color: white;
            transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
            height: 100%;
        }}

        .glass-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 14px 48px 0 rgba(0, 0, 0, 0.40);
            background: rgba(255, 255, 255, 0.20);
        }}

        /* ── Podium cards ────────────────────────────────────── */
        .podium-card {{
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }}

        .rank-1 {{
            min-height: 260px;
            background: rgba(255, 215, 0, 0.17) !important;
            border: 2px solid rgba(255, 215, 0, 0.35) !important;
        }}
        .rank-2 {{
            min-height: 220px;
            background: rgba(192, 192, 192, 0.17) !important;
            border: 2px solid rgba(192, 192, 192, 0.35) !important;
        }}
        .rank-3 {{
            min-height: 180px;
            background: rgba(205, 127, 50, 0.17) !important;
            border: 2px solid rgba(205, 127, 50, 0.35) !important;
        }}

        .podium-rank {{
            position: absolute;
            top: -15px;
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.30);
        }}

        .other-card {{
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .rank-badge {{
            background: rgba(255, 255, 255, 0.25);
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.95rem;
            flex-shrink: 0;
        }}

        h1, h2 {{
            color: white !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.45);
        }}

        /* ── Responsive adjustments ──────────────────────────── */
        @media (max-width: {MOBILE_BREAKPOINT}px) {{
            .glass-card      {{ padding: 1rem; }}
            .rank-1          {{ min-height: 200px; margin-bottom: 1rem; }}
            .rank-2          {{ min-height: 180px; margin-bottom: 1rem; }}
            .rank-3          {{ min-height: 160px; margin-bottom: 1rem; }}
            .other-card      {{ min-height: 100px; margin-bottom: 0.75rem; }}
            .podium-rank     {{ width: 36px; height: 36px; font-size: 1.1rem; top: -12px; }}

            [data-testid="column"] {{ padding: 0 0.5rem !important; }}
        }}

        /* ── Background-image status banner (debug only) ─────── */
        .bg-status {{
            font-size: 0.7rem;
            opacity: 0.55;
            color: white;
            text-align: center;
            padding-bottom: 0.5rem;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    return desktop_valid, mobile_valid


# --- Load CSV Data ---
@st.cache_data(ttl=300)
def load_csv_from_github(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        last_modified = response.headers.get('Last-Modified', None)
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        return df, last_modified, None
    except Exception as e:
        return None, None, str(e)


# --- Process Data ---
def process_sales_data(df):
    aggregated = df.groupby(['Airline_Code', 'Crew_ID', 'Crew_Name']).agg(
        {'crew_sold_quantity': 'sum'}
    ).reset_index()
    aggregated = aggregated.sort_values(
        ['Airline_Code', 'crew_sold_quantity'], ascending=[True, False]
    )
    return aggregated


# --- Main App ---
def main():
    # Apply background and CSS; capture validity flags
    desktop_valid, mobile_valid = apply_background_css(DESKTOP_BG_URL, MOBILE_BG_URL)

    # Header
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 0.5rem 0;'>
        <h1 style='font-size: 2.75rem; font-weight: 700; margin: 0;'>
            Caudalie&nbsp;: Crew Sales Performance
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    df, last_modified, error = load_csv_from_github(CSV_URL)

    if error:
        st.error(f"Error loading data: {error}")
        return

    if df is None or df.empty:
        st.warning("No data available.")
        return

    # Last refreshed
    from datetime import datetime, timezone
    if last_modified:
        try:
            refresh_date   = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
            formatted_date = refresh_date.strftime('%B %d, %Y at %I:%M %p UTC')
        except Exception:
            formatted_date = last_modified
    else:
        formatted_date = datetime.now(timezone.utc).strftime('%B %d, %Y at %I:%M %p UTC')

    st.markdown(f"""
    <div style='text-align: center; padding: 0 0 2rem 0;'>
        <p style='color: rgba(255,255,255,0.75); font-size: 0.9rem; margin: 0;'>
            Last refreshed: {formatted_date}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Process and render
    processed_df = process_sales_data(df)
    carriers     = sorted(processed_df['Airline_Code'].unique())
    carrier_cols = st.columns(len(carriers))

    for carrier_idx, carrier in enumerate(carriers):
        with carrier_cols[carrier_idx]:
            carrier_data = (
                processed_df[processed_df['Airline_Code'] == carrier]
                .reset_index(drop=True)
            )

            st.markdown(f"""
            <h2 style='font-size:1.75rem; font-weight:600; margin-bottom:1.5rem; text-align:center;'>
                ✈️ {carrier}
            </h2>
            """, unsafe_allow_html=True)

            top_3 = carrier_data.head(3)

            # ── Podium (top 3) ──────────────────────────────
            if len(top_3) >= 1:
                podium_cols = st.columns([1, 1, 1], gap="medium")

                for col_idx in range(min(3, len(top_3))):
                    row        = top_3.iloc[col_idx]
                    rank       = col_idx + 1
                    rank_class = f'rank-{rank}'

                    with podium_cols[col_idx]:
                        st.markdown(f"""
                        <div class="glass-card podium-card {rank_class}">
                            <div class="podium-rank">{rank}</div>
                            <div style="font-size:1.25rem; font-weight:700; margin-bottom:1rem; line-height:1.3;">
                                {row['Crew_Name']}
                            </div>
                            <div style="font-size:0.7rem; text-transform:uppercase; opacity:0.7;
                                        letter-spacing:0.05em; margin-bottom:0.5rem;">
                                Total Sales (MYR)
                            </div>
                            <div style="font-size:2rem; font-weight:800;">
                                {int(row['crew_sold_quantity']):,}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

            # ── Ranks 4–10 ──────────────────────────────────
            next_7 = carrier_data.iloc[3:10]

            if len(next_7) > 0:
                st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

                for _, crew in next_7.iterrows():
                    rank = int(crew.name) + 1
                    st.markdown(f"""
                    <div class="glass-card other-card">
                        <div style="display:flex; align-items:center; gap:0.75rem;">
                            <span class="rank-badge">{rank}</span>
                            <div style="flex:1; min-width:0;">
                                <div style="font-weight:600; font-size:0.9rem;
                                            white-space:nowrap; overflow:hidden;
                                            text-overflow:ellipsis;">
                                    {crew['Crew_Name']}
                                </div>
                            </div>
                        </div>
                        <div style="text-align:right; margin-top:0.5rem;">
                            <div style="font-size:1.25rem; font-weight:700;">
                                {int(crew['crew_sold_quantity']):,}
                            </div>
                            <div style="font-size:0.65rem; opacity:0.65;">MYR</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
