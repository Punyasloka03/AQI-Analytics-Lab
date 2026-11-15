
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AQI Analytics Lab",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #F5F1E8;
    color: #111D32;
}

header[data-testid="stHeader"] {
    background-color: transparent;
}

section[data-testid="stSidebar"] {
    background-color: #111D32;
}

section[data-testid="stSidebar"] * {
    color: #F5F1E8 !important;
}

section[data-testid="stSidebar"] label {
    color: #E9DFC9 !important;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: #111D32;
}

p, li {
    color: #33475B;
}

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E3D9C6;
    padding: 17px;
    border-radius: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #526579;
}

div[data-testid="stMetricValue"] {
    color: #111D32;
    font-weight: 700;
}

.stButton > button {
    background-color: #20B8A5;
    color: #111D32;
    border: none;
    border-radius: 9px;
    padding: 0.65rem 1.5rem;
    font-weight: 700;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background-color: #159A8B;
    color: white;
    transform: translateY(-2px);
}

div[data-testid="stDataFrame"] {
    border-radius: 10px;
}

/* White text inside the dark-blue Streamlit information callouts. */
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"],
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] li {
    color: #FFFFFF !important;
}

hr {
    border-color: #D8C8AD;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LANDING PAGE STATE
# ============================================================

if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False


# ============================================================
# ANIMATED LANDING PAGE
# ============================================================

if not st.session_state.show_dashboard:

    components.html(r"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body {
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: transparent;
        font-family: Arial, sans-serif;
    }

    .hero {
        position: relative;
        width: 100%;
        height: 570px;
        overflow: hidden;
        border-radius: 22px;
        background:
            radial-gradient(ellipse at 50% 110%, #24465a 0%, transparent 55%),
            linear-gradient(135deg, #111D32 0%, #172B40 55%, #102333 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #F5F1E8;
    }

    .glow {
        position: absolute;
        width: 450px;
        height: 450px;
        border-radius: 50%;
        background: #20B8A5;
        opacity: 0.07;
        filter: blur(100px);
        animation: breathe 7s ease-in-out infinite alternate;
    }

    @keyframes breathe {
        from {
            transform: scale(0.8);
            opacity: 0.04;
        }
        to {
            transform: scale(1.25);
            opacity: 0.12;
        }
    }

    .particle {
        position: absolute;
        bottom: -20px;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #70DCCB;
        opacity: 0;
        box-shadow: 0 0 12px #20B8A5;
        animation: floatUp linear infinite;
    }

    .p1 { left: 8%; animation-duration: 13s; }
    .p2 { left: 19%; animation-duration: 17s; animation-delay: 3s; width: 3px; height: 3px; }
    .p3 { left: 32%; animation-duration: 15s; animation-delay: 1s; }
    .p4 { left: 48%; animation-duration: 19s; animation-delay: 5s; width: 4px; height: 4px; }
    .p5 { left: 63%; animation-duration: 14s; animation-delay: 2s; }
    .p6 { left: 76%; animation-duration: 18s; animation-delay: 4s; width: 3px; height: 3px; }
    .p7 { left: 90%; animation-duration: 16s; animation-delay: 1s; }

    @keyframes floatUp {
        0% {
            transform: translateY(0) translateX(0);
            opacity: 0;
        }
        15% {
            opacity: 0.7;
        }
        50% {
            transform: translateY(-270px) translateX(25px);
            opacity: 0.5;
        }
        85% {
            opacity: 0.3;
        }
        100% {
            transform: translateY(-620px) translateX(-15px);
            opacity: 0;
        }
    }

    .wave-area {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 25px;
        width: 100%;
        height: 190px;
        opacity: 0.75;
    }

    .wave {
        fill: none;
        stroke: #20B8A5;
        stroke-width: 1.5;
        stroke-linecap: round;
        stroke-dasharray: 12 12;
        animation: flow 18s linear infinite;
    }

    .wave.second {
        stroke: #6B91C4;
        opacity: 0.65;
        stroke-width: 1;
        animation-duration: 25s;
        animation-direction: reverse;
    }

    @keyframes flow {
        to {
            stroke-dashoffset: -240;
        }
    }

    .data-point {
        fill: #9AE8D9;
        filter: drop-shadow(0 0 6px #20B8A5);
        animation: pulse 2.8s ease-in-out infinite alternate;
    }

    .d2 { animation-delay: 0.7s; }
    .d3 { animation-delay: 1.4s; }
    .d4 { animation-delay: 2s; }

    @keyframes pulse {
        from {
            opacity: 0.25;
            r: 2;
        }
        to {
            opacity: 1;
            r: 5;
        }
    }

    .hero-content {
        position: relative;
        z-index: 5;
        width: 90%;
        max-width: 850px;
        text-align: center;
        animation: reveal 1.5s ease-out both;
    }

    @keyframes reveal {
        from {
            opacity: 0;
            transform: translateY(22px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .eyebrow {
        color: #D8C8AD;
        font-size: 11px;
        letter-spacing: 4px;
        font-weight: 600;
        margin-bottom: 25px;
    }

    h1 {
        font-size: clamp(34px, 5vw, 57px);
        line-height: 1.15;
        font-weight: 700;
        letter-spacing: -1.8px;
        color: #F5F1E8;
    }

    h1 span {
        color: #20B8A5;
    }

    .description {
        max-width: 620px;
        margin: 22px auto 0;
        color: #C2CFD7;
        font-size: 15px;
        line-height: 1.8;
    }

    .stats {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 25px;
        margin-top: 37px;
        color: #E9DFC9;
        font-size: 11px;
        letter-spacing: 2px;
        font-weight: 600;
        flex-wrap: wrap;
    }

    .stat-divider {
        width: 1px;
        height: 17px;
        background: #527080;
    }

    @media (max-width: 600px) {
        .hero {
            height: 540px;
        }

        .eyebrow {
            font-size: 9px;
            letter-spacing: 2px;
        }

        .description {
            font-size: 13px;
        }

        .stats {
            gap: 12px;
            font-size: 9px;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
        }
    }

    </style>
    </head>

    <body>

    <div class="hero">

        <div class="glow"></div>

        <div class="particle p1"></div>
        <div class="particle p2"></div>
        <div class="particle p3"></div>
        <div class="particle p4"></div>
        <div class="particle p5"></div>
        <div class="particle p6"></div>
        <div class="particle p7"></div>

        <svg class="wave-area" viewBox="0 0 1200 190"
             preserveAspectRatio="none">

            <path class="wave"
                d="M0 110 C150 30 240 180 400 100
                S650 25 800 100 S1050 175 1200 70"/>

            <path class="wave second"
                d="M0 145 C180 70 280 190 450 125
                S700 55 870 125 S1080 170 1200 115"/>

            <circle class="data-point" cx="200" cy="92" r="3"/>
            <circle class="data-point d2" cx="450" cy="100" r="3"/>
            <circle class="data-point d3" cx="750" cy="90" r="3"/>
            <circle class="data-point d4" cx="1010" cy="125" r="3"/>

        </svg>

        <div class="hero-content">

            <div class="eyebrow">
                ANALYSING AIR QUALITY THROUGH MACHINE LEARNING
            </div>

            <h1>
                Understanding Air Quality.<br>
                <span>Predicting What Comes Next.</span>
            </h1>

            <p class="description">
                Exploring air pollution patterns, comparing machine learning
                approaches, and investigating how temporal models can predict
                the next-hour air quality category across Indian cities.
            </p>

            <div class="stats">
                <span>05 EXPERIMENTS</span>
                <div class="stat-divider"></div>
                <span>23 RETAINED CITIES</span>
                <div class="stat-divider"></div>
                <span>ML RESEARCH</span>
            </div>

        </div>

    </div>

    </body>
    </html>
    """, height=590, scrolling=False)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        if st.button("Explore the Research  →", use_container_width=True):
            st.session_state.show_dashboard = True
            st.rerun()

    st.stop()


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.sidebar.markdown("# 🌫️ AQI ANALYTICS LAB")
st.sidebar.caption("A Machine Learning Research Dashboard")
st.sidebar.markdown("---")

if st.sidebar.button("← Back to Landing Page", use_container_width=True):
    st.session_state.show_dashboard = False
    st.rerun()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Experiment comparison",
        "Temporal CNN",
        "City-wise evaluation",
        "Methodology & limitations"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("AQI Classification Comparative Study")
st.sidebar.caption("Research Dashboard | 2026")


# ============================================================
# DATA: EXPERIMENTS
# ============================================================

experiments = pd.DataFrame([
    {
        "Experiment": "Experiment 1",
        "Approach": "Classical ML",
        "Best Model / Setup": "Random Forest",
        "Accuracy (%)": 60.38,
        "Macro-F1": 0.5024,
        "Balanced Accuracy": 0.4963,
        "Focus": "Classical baseline"
    },
    {
        "Experiment": "Experiment 2",
        "Approach": "Imbalance handling",
        "Best Model / Setup": "XGBoost + SMOTE",
        "Accuracy (%)": 55.10,
        "Macro-F1": 0.4970,
        "Balanced Accuracy": 0.5439,
        "Focus": "Class imbalance"
    },
    {
        "Experiment": "Experiment 3",
        "Approach": "Feature analysis",
        "Best Model / Setup": "All seven features",
        "Accuracy (%)": 73.02,
        "Macro-F1": None,
        "Balanced Accuracy": None,
        "Focus": "Feature contribution"
    },
    {
        "Experiment": "Experiment 4",
        "Approach": "Temporal deep learning",
        "Best Model / Setup": "Temporal CNN",
        "Accuracy (%)": 82.50,
        "Macro-F1": 0.8382,
        "Balanced Accuracy": 0.8303,
        "Focus": "Next-hour prediction"
    },
    {
        "Experiment": "Experiment 5",
        "Approach": "Cross-city generalization",
        "Best Model / Setup": "Temporal CNN",
        "Accuracy (%)": 74.42,
        "Macro-F1": 0.6846,
        "Balanced Accuracy": 0.7570,
        "Focus": "Unseen cities"
    }
])


# ============================================================
# DATA: TEMPORAL CNN CLASSIFICATION REPORT
# ============================================================

class_report = pd.DataFrame([
    ["Good", 0.66, 0.83, 0.74, 10255],
    ["Moderate", 0.90, 0.78, 0.84, 26005],
    ["Poor", 0.83, 0.84, 0.84, 4504],
    ["Satisfactory", 0.83, 0.85, 0.84, 39041],
    ["Severe", 0.99, 0.83, 0.90, 645],
    ["Very Poor", 0.91, 0.85, 0.88, 2249]
], columns=[
    "AQI Category",
    "Precision",
    "Recall",
    "F1-score",
    "Support"
])


# ============================================================
# DATA: CITY-WISE EVALUATION
# ============================================================

cities = pd.DataFrame([
    ["Delhi", 9538, .8751, .7909, .8989, 6],
    ["Bengaluru", 9099, .8741, .5548, .7741, 6],
    ["Hyderabad", 8904, .9240, .9193, .9403, 6],
    ["Chennai", 6703, .7010, .6428, .6615, 6],
    ["Jaipur", 5202, .8900, .6902, .9009, 6],
    ["Visakhapatnam", 4815, .8415, .8378, .8299, 6],
    ["Thiruvananthapuram", 4794, .7793, .7446, .7449, 6],
    ["Patna", 4519, .7269, .6383, .7122, 6],
    ["Amritsar", 4435, .8223, .7248, .7320, 6],
    ["Mumbai", 3634, .6968, .7362, .8537, 6],
    ["Kolkata", 3613, .7628, .7840, .7653, 6],
    ["Amaravati", 2860, .8458, .7430, .6998, 6],
    ["Gurugram", 2793, .8314, .5934, .6067, 6],
    ["Guwahati", 2317, .7738, .7550, .7471, 6],
    ["Brajrajnagar", 1796, .9332, .6745, .6561, 6],
    ["Jorapokhar", 1445, .8408, .5794, .6264, 6],
    ["Talcher", 1392, .8132, .6581, .6595, 6],
    ["Chandigarh", 1362, .8186, .7384, .7053, 6],
    ["Bhopal", 1293, .7456, .5626, .5262, 6],
    ["Shillong", 775, .9200, .5362, .5288, 6],
    ["Coimbatore", 730, .6959, .6166, .8271, 6],
    ["Kochi", 384, .5391, .3179, .3621, 6],
    ["Aizawl", 296, 1.0000, 1.0000, None, 1]
], columns=[
    "City",
    "Test Samples",
    "Accuracy",
    "Macro-F1",
    "Balanced Accuracy",
    "Actual Classes"
])

cities["Evaluation Note"] = cities["Actual Classes"].apply(
    lambda x: "Single-class subset; not comparable" if x == 1 else "Multiclass evaluation"
)


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "Overview":

    st.title("AQI Analytics Lab")
    st.caption(
        "A comparative study of machine learning approaches "
        "for Air Quality Index classification."
    )

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Records", "707,875")
    c2.metric("Cities in Dataset", "26")
    c3.metric("Retained Cities", "23")
    c4.metric("Experiments", "05")

    st.markdown("## Research Overview")

    st.write(
        """
        This project investigates the use of machine learning and
        temporal deep learning techniques for classifying air quality
        categories using historical pollutant measurements.

        The study progresses from classical machine learning baselines
        to class imbalance analysis, feature contribution, temporal
        prediction and cross-city generalization.
        """
    )

    st.info(
        "The dashboard presents recorded experimental results. "
        "It is a research-results interface, not a live AQI monitoring "
        "or real-time prediction service."
    )

    st.markdown("## Experimental Journey")

    journey = [
        ("01", "Classical ML", "Establishing baseline performance"),
        ("02", "Imbalance Analysis", "Investigating class distribution strategies"),
        ("03", "Feature Analysis", "Evaluating pollutant contributions"),
        ("04", "Temporal CNN", "Predicting the next-hour AQI category"),
        ("05", "Cross-city Evaluation", "Testing generalization to unseen cities")
    ]

    for number, heading, description in journey:
        with st.container(border=True):
            st.markdown(f"### {number}  {heading}")
            st.write(description)

    st.markdown("## Experiment Summary")

    st.dataframe(
        experiments,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EXPERIMENT COMPARISON
# ============================================================

elif page == "Experiment comparison":

    st.title("Experiment Comparison")
    st.caption(
        "Comparing the five experimental stages of the AQI classification study."
    )

    st.markdown("---")

    st.markdown("## Accuracy Across Experiments")

    fig = px.bar(
        experiments,
        x="Experiment",
        y="Accuracy (%)",
        color="Approach",
        text="Accuracy (%)",
        color_discrete_sequence=[
            "#20B8A5",
            "#6B91C4",
            "#D8C8AD",
            "#26445B",
            "#A7B7C7"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#F5F1E8",
        font_color="#111D32",
        yaxis_range=[0, 100],
        xaxis_title=dict(text="Experimental Stage", font=dict(color="#26384A")),
        yaxis_title=dict(text="Accuracy (%)", font=dict(color="#26384A")),
        xaxis=dict(tickfont=dict(color="#26384A")),
        yaxis=dict(tickfont=dict(color="#26384A")),
        legend=dict(
            font=dict(color="#26384A"),
            title=dict(font=dict(color="#26384A"))
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## Detailed Results")

    st.dataframe(
        experiments,
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        """
        Important: These experiments do not all use identical data
        preparation, train-test splits or evaluation protocols.
        Their results should be interpreted in the context of their
        individual methodologies rather than as a perfectly controlled
        model leaderboard.
        """
    )

    st.markdown("## Key Observations")

    st.write(
        """
        - Classical models establish the initial performance baseline.
        - SMOTE improves balanced accuracy in the reported XGBoost
          comparison, although overall accuracy decreases.
        - Feature analysis indicates that all seven pollutant features
          together outperform the tested reduced feature groups.
        - The corrected temporal CNN experiment achieves 82.50%
          accuracy with a Macro-F1 of 0.8382.
        - Cross-city evaluation provides a separate test of performance
          on cities excluded from training.
        """
    )


# ============================================================
# TEMPORAL CNN PAGE
# ============================================================

elif page == "Temporal CNN":

    st.title("Temporal CNN Analysis")

    st.caption(
        "Next-hour AQI classification using 24-hour pollutant sequences."
    )

    st.markdown("---")

    st.markdown("## Model Performance")

    c1, c2, c3 = st.columns(3)

    c1.metric("Accuracy", "82.50%")
    c2.metric("Macro-F1", "0.8382")
    c3.metric("Balanced Accuracy", "0.8303")

    st.markdown("## Experimental Configuration")

    config_col1, config_col2 = st.columns(2)

    with config_col1:
        st.markdown("### Input Configuration")
        st.write("- Input window: 24 hours")
        st.write("- Prediction target: Next-hour AQI category")
        st.write("- Model: Temporal CNN")
        st.write("- Features: Seven pollutant measurements")

    with config_col2:
        st.markdown("### Data Preparation")
        st.write("- Per-city forward-only imputation")
        st.write("- Maximum imputation gap: 24 hours")
        st.write("- Chronological city-specific 80/20 split")
        st.write("- Scaler fitted on training period only")
        st.write("- Valid contiguous 24-hour sequences")

    st.markdown("## Dataset and Sequence Statistics")

    s1, s2, s3 = st.columns(3)

    s1.metric("Retained Records", "339,117")
    s2.metric("Training Sequences", "239,959")
    s3.metric("Test Sequences", "82,699")

    st.markdown("## Classification Report")

    st.dataframe(
        class_report,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("## Confusion Matrix Analysis")

    st.write(
        """
        The confusion matrices below show the raw prediction counts
        and normalized class-wise performance from Experiment 4.
        The two matrices preserve their original class-axis ordering.
        """
    )

    raw_matrix = RESULTS_DIR / "experiment4_confusion_matrix.png"
    normalized_matrix = RESULTS_DIR / "experiment4_normalized_confusion_matrix.png"

    matrix_col1, matrix_col2 = st.columns(2)

    with matrix_col1:
        st.markdown("### Raw-count Confusion Matrix")

        if raw_matrix.exists():
            st.image(
                str(raw_matrix),
                use_container_width=True
            )
        else:
            st.info(
                "Add experiment4_confusion_matrix.png "
                "to the results folder to display this matrix."
            )

    with matrix_col2:
        st.markdown("### Normalized Confusion Matrix")

        if normalized_matrix.exists():
            st.image(
                str(normalized_matrix),
                use_container_width=True
            )
        else:
            st.info(
                "Add experiment4_normalized_confusion_matrix.png "
                "to the results folder to display this matrix."
            )

    st.markdown("## Interpretation")

    st.write(
        """
        The corrected temporal CNN pipeline achieves 82.50% accuracy
        and 0.8382 Macro-F1.

        Most classes demonstrate reasonably strong class-wise
        performance. The model's errors are primarily concentrated
        among adjacent AQI categories, which is consistent with the
        overlap between neighbouring air-quality ranges.
        """
    )

    st.info(
        """
        The city-wise evaluation includes Aizawl, where only one
        actual AQI class is represented in the test subset. Its
        100% accuracy and Macro-F1 do not establish multiclass
        classification ability. Its balanced accuracy is undefined.
        """
    )


# ============================================================
# CITY-WISE EVALUATION
# ============================================================

elif page == "City-wise evaluation":

    st.title("City-wise Evaluation")

    st.caption(
        "Examining how the temporal CNN performs across individual cities."
    )

    st.markdown("---")

    st.markdown("## City Performance Explorer")

    selected_city = st.selectbox(
        "Select a city",
        cities["City"].tolist()
    )

    selected_data = cities[cities["City"] == selected_city].iloc[0]

    a, b, c, d = st.columns(4)

    a.metric(
        "Test Samples",
        f"{int(selected_data['Test Samples']):,}"
    )

    b.metric(
        "Accuracy",
        f"{selected_data['Accuracy']:.2%}"
    )

    c.metric(
        "Macro-F1",
        f"{selected_data['Macro-F1']:.4f}"
    )

    balanced_value = selected_data["Balanced Accuracy"]

    d.metric(
        "Balanced Accuracy",
        "N/A" if pd.isna(balanced_value) else f"{balanced_value:.4f}"
    )

    if selected_data["Actual Classes"] == 1:
        st.warning(
            """
            Aizawl has only one actual AQI class in its test subset.
            Its accuracy and Macro-F1 are therefore not meaningful
            indicators of multiclass generalization. Balanced accuracy
            is undefined for this subset.
            """
        )

    st.markdown("## City-wise Performance Table")

    st.dataframe(
        cities,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("## Accuracy Across Cities")

    fig_accuracy = px.bar(
        cities.sort_values("Accuracy", ascending=False),
        x="City",
        y="Accuracy",
        color="Accuracy",
        color_continuous_scale=["#D8C8AD", "#20B8A5", "#111D32"],
        hover_data=["Test Samples", "Actual Classes"]
    )

    fig_accuracy.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#F5F1E8",
        font_color="#111D32",
        xaxis_title=dict(text="City", font=dict(color="#26384A")),
        yaxis_title=dict(text="Accuracy", font=dict(color="#26384A")),
        xaxis=dict(tickfont=dict(color="#26384A")),
        yaxis=dict(tickfont=dict(color="#26384A"), tickformat=".0%"),
        coloraxis_colorbar=dict(
            tickfont=dict(color="#26384A"),
            title=dict(font=dict(color="#26384A"))
        )
    )

    st.plotly_chart(fig_accuracy, use_container_width=True)

    st.markdown("## Multiclass Macro-F1 Comparison")

    multiclass_cities = cities[cities["Actual Classes"] > 1].copy()

    fig_f1 = px.bar(
        multiclass_cities.sort_values("Macro-F1", ascending=False),
        x="City",
        y="Macro-F1",
        color="Macro-F1",
        color_continuous_scale=["#D8C8AD", "#20B8A5", "#111D32"],
        hover_data=["Test Samples"]
    )

    fig_f1.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#F5F1E8",
        font_color="#111D32",
        xaxis_title=dict(text="City", font=dict(color="#26384A")),
        yaxis_title=dict(text="Macro-F1", font=dict(color="#26384A")),
        xaxis=dict(tickfont=dict(color="#26384A")),
        yaxis=dict(tickfont=dict(color="#26384A")),
        coloraxis_colorbar=dict(
            tickfont=dict(color="#26384A"),
            title=dict(font=dict(color="#26384A"))
        )
    )

    st.plotly_chart(fig_f1, use_container_width=True)

    st.markdown("## Test Sample Distribution")

    fig_samples = px.bar(
        cities.sort_values("Test Samples", ascending=False),
        x="City",
        y="Test Samples",
        color="Test Samples",
        color_continuous_scale=["#D8C8AD", "#20B8A5", "#111D32"]
    )

    fig_samples.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#F5F1E8",
        font_color="#111D32",
        xaxis_title=dict(text="City", font=dict(color="#26384A")),
        yaxis_title=dict(text="Number of Test Sequences", font=dict(color="#26384A")),
        xaxis=dict(tickfont=dict(color="#26384A")),
        yaxis=dict(tickfont=dict(color="#26384A")),
        coloraxis_colorbar=dict(
            tickfont=dict(color="#26384A"),
            title=dict(font=dict(color="#26384A"))
        )
    )

    st.plotly_chart(fig_samples, use_container_width=True)

    st.caption(
        "Aizawl remains visible in the city table and sample-count "
        "chart, but is excluded from the multiclass Macro-F1 comparison."
    )


# ============================================================
# METHODOLOGY AND LIMITATIONS
# ============================================================

elif page == "Methodology & limitations":

    st.title("Methodology & Limitations")

    st.caption(
        "Understanding the experimental design, evaluation protocols "
        "and interpretation boundaries."
    )

    st.markdown("---")

    st.markdown("## Dataset Overview")

    dataset_col1, dataset_col2 = st.columns(2)

    with dataset_col1:
        st.metric("Total Observations", "707,875")
        st.metric("Original Cities", "26")
        st.metric("Selected Pollutants", "7")

    with dataset_col2:
        st.metric("Retained Temporal Cities", "23")
        st.metric("Selected Feature Missingness", "23.76%")
        st.metric("Duplicate City-Date Pairs", "0")

    st.write(
        """
        The dataset contains hourly air-quality measurements from
        multiple Indian cities. Seven pollutant features were selected:
        PM2.5, PM10, NO2, SO2, CO, O3 and NH3.

        The target variable is the categorical AQI bucket.
        """
    )

    st.markdown("## Experimental Methodology")

    with st.expander("Experiment 1 — Classical Machine Learning", expanded=True):
        st.write(
            """
            Evaluated KNN, Logistic Regression, SVM, Random Forest
            and XGBoost to establish classical classification baselines.

            Random Forest achieved 60.38% accuracy, Macro-F1 of
            0.5024 and balanced accuracy of 0.4963.

            This is a historical baseline using forward/backward
            filling before splitting and a chronological split.
            It should not be interpreted as a leakage-controlled
            comparison with the corrected temporal pipeline.
            """
        )

    with st.expander("Experiment 2 — Class Imbalance"):
        st.write(
            """
            Compared baseline XGBoost, class-weighted Random Forest
            and XGBoost with SMOTE.

            SMOTE was applied only to the training data.

            The SMOTE-based XGBoost result achieved 55.10% accuracy,
            0.4970 Macro-F1 and 0.5439 balanced accuracy.

            The strategies involved different models and configurations,
            so the results are not a perfectly isolated comparison
            of imbalance-handling methods.
            """
        )

    with st.expander("Experiment 3 — Feature Analysis"):
        st.write(
            """
            Evaluated the contribution of seven pollutant features.

            The full seven-feature configuration achieved 73.02%
            accuracy. Removing CO, O3 or PM2.5 resulted in the
            largest observed accuracy reductions among the
            tested individual feature removals.

            This experiment used a different stratified split and
            a globally filled dataset. Its results should be
            interpreted separately from the corrected temporal
            experiment.
            """
        )

    with st.expander("Experiment 4 — Temporal CNN"):
        st.write(
            """
            Used 24-hour pollutant input windows to predict the
            next-hour AQI category.

            The corrected pipeline applied per-city forward-only
            imputation capped at 24 hours, chronological city-specific
            80/20 splitting, training-only scaler fitting and valid
            contiguous sequences.

            The resulting evaluation retained 339,117 records
            across 23 cities.
            """
        )

    with st.expander("Experiment 5 — Cross-city Generalization"):
        st.write(
            """
            Evaluated generalization by holding out Kochi, Delhi,
            Aizawl, Coimbatore and Mumbai.

            The experiment used complete-case records, a scaler
            fitted on training cities only and 24-hour sequences
            with stride 3.

            Training records: 245,045
            Held-out records: 60,852
            Training sequences: 56,514
            Test sequences: 18,194

            This is a distinct protocol from Experiment 4, which
            uses capped forward imputation and a city-specific
            chronological split.
            """
        )

    st.markdown("## Important Limitations")

    limitations = [
        "Experiments use different preprocessing and evaluation protocols.",
        "Historical baseline results should not be treated as directly comparable to the corrected temporal evaluation.",
        "The dashboard displays saved experimental results rather than performing live AQI inference.",
        "City-wise performance varies with sample size and class distribution.",
        "Aizawl has only one actual class in its test subset, limiting multiclass interpretation.",
        "Cross-city evaluation is a separate generalization experiment and should not be directly equated with Experiment 4."
    ]

    for item in limitations:
        st.markdown(f"- {item}")

    st.info(
        "Responsible interpretation of evaluation results is an important "
        "part of this research. Accuracy alone does not capture every "
        "aspect of multiclass model performance."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:18px;
        color:#526579;
        font-size:12px;
    ">
        <b style="color:#111D32;">AQI ANALYTICS LAB</b><br>
        A Machine Learning Research Dashboard<br>
        Exploring air quality classification and temporal prediction
    </div>
    """,
    unsafe_allow_html=True
)
