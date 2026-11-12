
import streamlit as st
import sys
from pathlib import Path

# =========================================================
# 1. PROJECT CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.generation.chain import FinConRAGPipeline
from src.ingestion.run_ingestion import run_ingestion_pipeline

st.set_page_config(
    page_title="FinCon AI | Financial Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. CUSTOM CSS - NAVY & BLUE
# =========================================================

st.markdown("""
<style>

/* Global */
.stApp {
    background-color: #F5F7FB;
    color: #172B4D;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #10233F;
    border-right: 1px solid #203B5E;
}

[data-testid="stSidebar"] * {
    color: #EAF1FB !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #B8C9DF !important;
}

[data-testid="stSidebar"] hr {
    border-color: #304966;
}

/* Main Header */
.main-header {
    background: linear-gradient(120deg, #10233F 0%, #174A7E 60%, #246DB2 100%);
    padding: 30px 34px;
    border-radius: 18px;
    margin-bottom: 26px;
    color: white;
    box-shadow: 0 8px 24px rgba(16, 35, 63, 0.12);
}

.main-header h1 {
    color: white !important;
    font-size: 30px;
    font-weight: 750;
    margin-bottom: 8px;
}

.main-header p {
    color: #D7E6F7 !important;
    font-size: 14px;
    margin-bottom: 0;
}

/* Section Titles */
.section-title {
    color: #17365D;
    font-size: 21px;
    font-weight: 700;
    margin: 22px 0 12px 0;
}

/* Cards */
.info-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #E3EAF3;
    box-shadow: 0 3px 12px rgba(24, 52, 85, 0.04);
    margin-bottom: 15px;
}

.info-card h4 {
    color: #17365D;
    font-size: 15px;
    margin-bottom: 8px;
}

.info-card p {
    color: #64748B;
    font-size: 13px;
    margin-bottom: 0;
}

/* Search Area */
[data-testid="stTextInput"] input {
    background: white;
    border: 1px solid #D7E2EF;
    border-radius: 10px;
    padding: 13px;
    color: #172B4D;
}

[data-testid="stTextInput"] input:focus {
    border-color: #347FC1;
    box-shadow: 0 0 0 2px rgba(52, 127, 193, 0.12);
}

/* Buttons */
.stButton > button {
    background: #205F9D;
    color: white !important;
    border: none;
    border-radius: 9px;
    font-weight: 600;
    padding: 10px 18px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #174A7E;
    color: white !important;
    border: none;
}

/* Metrics */
[data-testid="stMetric"] {
    background: white;
    padding: 17px;
    border: 1px solid #E3EAF3;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #64748B;
}

[data-testid="stMetricValue"] {
    color: #174A7E;
}

/* Answer */
.answer-card {
    background: white;
    padding: 24px;
    border-radius: 14px;
    border-left: 5px solid #347FC1;
    border-top: 1px solid #E3EAF3;
    border-right: 1px solid #E3EAF3;
    border-bottom: 1px solid #E3EAF3;
    line-height: 1.8;
    color: #263B53;
    margin: 12px 0 20px 0;
}

/* Expander */
[data-testid="stExpander"] {
    background: white;
    border: 1px solid #E3EAF3;
    border-radius: 12px;
    margin-bottom: 12px;
}

/* Captions */
[data-testid="stCaptionContainer"] {
    color: #718096;
}

/* Divider */
hr {
    border-color: #E3EAF3;
}

/* Footer */
.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 12px;
    padding: 24px 0 8px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="padding: 12px 0 22px 0;">
        <h2 style="color:white; margin-bottom:3px;">💼 FinCon AI</h2>
        <p style="font-size:12px; color:#AFC4DE;">
            Financial Intelligence Assistant
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### ⚙️ Pipeline Configuration")

    top_k = st.slider(
        "Top-K Rerank Results",
        min_value=1,
        max_value=8,
        value=3,
        help="Number of relevant child chunks returned after reranking."
    )

    st.markdown("---")

    st.markdown("### 📂 Document Management")

    if st.button("🔄 Run Document Ingestion", use_container_width=True):

        with st.spinner("Processing documents and building indexes..."):

            try:
                run_ingestion_pipeline()

                # Refresh the existing cached pipeline if initialized
                if "pipeline" in st.session_state:
                    st.session_state.pipeline.refresh_parent_store()

                st.success("Documents indexed successfully!")

            except Exception as e:
                st.error(f"Ingestion failed: {e}")

    st.markdown("---")

    st.markdown("### 📊 Financial Standards Queries")

    sample_queries = [
        "What is the mandatory timeline for Form 8-K disclosure under SEC Item 1.05 for material cybersecurity incidents?",

        "What are the differences between Scope 1, Scope 2, and Scope 3 emissions under IFRS S2 in 2026?",

        "What are the eligibility criteria and turnover thresholds for EU CSRD Wave 2 compliance in 2026?",

        "What is the Basel III Endgame capital output floor percentage for risk-weighted assets?",

        "What confidence level is required for Expected Shortfall under the FRTB market risk framework?"
    ]

    selected_sample = st.selectbox(
        "Explore example questions",
        [""] + sample_queries
    )

    st.markdown("---")

    st.markdown("""
    <div style="font-size:12px; color:#AFC4DE; line-height:1.8;">
        <b>Powered by:</b><br>
        ChromaDB • BM25 • RRF<br>
        Cross-Encoder • Groq AI
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 4. PIPELINE INITIALIZATION
# =========================================================

@st.cache_resource
def get_pipeline():
    return FinConRAGPipeline()


try:
    pipeline = get_pipeline()
except Exception as e:
    st.error(f"Pipeline initialization failed: {e}")
    st.stop()


# =========================================================
# 5. MAIN HEADER
# =========================================================

st.markdown("""
<div class="main-header">
    <h1>Financial & Regulatory Intelligence</h1>
    <p>
        An intelligent RAG-powered assistant for financial controlling,
        accounting standards and regulatory research.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 6. INTRODUCTION CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>🔎 Hybrid Retrieval</h4>
        <p>Combines semantic and keyword-based search for better financial document retrieval.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>🧠 Intelligent Reranking</h4>
        <p>Cross-Encoder reranking improves relevance and reduces unrelated results.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>📚 Grounded Answers</h4>
        <p>Uses retrieved financial documents to generate context-aware answers.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 7. QUESTION INPUT
# =========================================================

st.markdown(
    '<div class="section-title">💬 Ask FinCon AI</div>',
    unsafe_allow_html=True
)

st.caption(
    "Ask questions about IFRS, accounting standards, financial controlling and regulations."
)

user_query = st.text_input(
    "Your financial question",
    value=selected_sample if selected_sample else "",
    placeholder="e.g. What is the impact of IFRS 16 on EBITDA?",
    label_visibility="collapsed"
)

search_col, clear_col = st.columns([3, 1])

with search_col:
    search_clicked = st.button(
        "🔍 Search & Analyze",
        type="primary",
        use_container_width=True
    )

with clear_col:
    clear_clicked = st.button(
        "✕ Clear",
        use_container_width=True
    )

if clear_clicked:
    st.rerun()


# =========================================================
# 8. QUERY EXECUTION
# =========================================================

if search_clicked:

    if not user_query.strip():

        st.warning("Please enter a financial question first.")

    else:

        try:

            with st.spinner(
                "Analyzing your question, retrieving documents and generating an answer..."
            ):

                result = pipeline.run(
                    query=user_query,
                    top_k_rerank=top_k
                )

            st.markdown("---")

            # -------------------------------------------------
            # FINANCIAL ANSWER
            # -------------------------------------------------

            st.markdown(
                '<div class="section-title">📝 Financial Analysis</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="answer-card">
                    {result["answer"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # ENTITIES
            # -------------------------------------------------

            entities = result.get("entities", [])

            if entities:

                st.markdown("### 🏷️ Recognized Financial Entities")

                entity_text = " • ".join(
                    [
                        f"**{e.get('text', '')}** ({e.get('label', '')})"
                        for e in entities
                    ]
                )

                st.markdown(entity_text)

            # -------------------------------------------------
            # QUERY EXPANSION
            # -------------------------------------------------

            expanded_query = result.get("expanded_query")

            if expanded_query and expanded_query != user_query:

                with st.expander("🔄 Query Expansion Details"):

                    st.write(
                        "The original question was enriched with relevant domain terminology."
                    )

                    st.info(expanded_query)

            # -------------------------------------------------
            # SOURCES
            # -------------------------------------------------

            st.markdown("---")

            st.markdown(
                '<div class="section-title">📚 Sources & References</div>',
                unsafe_allow_html=True
            )

            sources = result.get("sources", [])

            if sources:

                source_cols = st.columns(min(len(sources), 3))

                for i, source in enumerate(sources):

                    with source_cols[i % len(source_cols)]:

                        st.markdown(
                            f"""
                            <div class="info-card">
                                <h4>📄 Source {i + 1}</h4>
                                <p>{source}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            else:

                st.info("No source documents were returned.")

            # -------------------------------------------------
            # RETRIEVAL METRICS
            # -------------------------------------------------

            retrieved_chunks = result.get("retrieved_child_chunks", [])

            metric1, metric2 = st.columns(2)

            with metric1:
                st.metric(
                    "Retrieved Child Chunks",
                    len(retrieved_chunks)
                )

            with metric2:
                st.metric(
                    "Source Documents",
                    len(sources)
                )

            # -------------------------------------------------
            # CHILD CHUNKS
            # -------------------------------------------------

            with st.expander(
                "🔍 Deep Dive: Retrieved Child Chunks & Reranker Scores"
            ):

                if not retrieved_chunks:

                    st.info("No child chunks were retrieved.")

                for idx, chunk in enumerate(retrieved_chunks, start=1):

                    st.markdown(f"#### Rank {idx}")

                    st.code(
                        chunk.get("id", "Unknown"),
                        language="text"
                    )

                    score1, score2 = st.columns(2)

                    with score1:
                        st.metric(
                            "Cross-Encoder Score",
                            f"{chunk.get('rerank_score', 0.0):.4f}"
                        )

                    with score2:
                        st.metric(
                            "RRF Score",
                            f"{chunk.get('rrf_score', 0.0):.4f}"
                        )

                    st.text_area(
                        f"Child Chunk #{idx} Content",
                        chunk.get("text", ""),
                        height=120,
                        key=f"child_{idx}"
                    )

                    st.caption(
                        f"Parent ID: {chunk.get('parent_id', 'N/A')}"
                    )

                    st.json(
                        chunk.get("metadata", {})
                    )

                    st.markdown("---")

            # -------------------------------------------------
            # PARENT CONTEXT
            # -------------------------------------------------

            with st.expander(
                "📖 Deep Dive: Full Parent Context Sent to LLM"
            ):

                st.code(
                    result.get("context_used", ""),
                    language="markdown"
                )

        except Exception as e:

            st.error(f"An error occurred while processing your query: {e}")


# =========================================================
# 9. FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    FinCon AI • Financial & Regulatory Intelligence Assistant
    <br>
    Hierarchical Hybrid RAG | ChromaDB | BM25 | Cross-Encoder | Groq
</div>
""", unsafe_allow_html=True)
