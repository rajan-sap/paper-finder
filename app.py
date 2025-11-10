"""
Paper Finder - Refactored with Component Architecture
Clean, maintainable code with reusable components
"""

import solara
from search_engine import search_papers, Paper, RankingCriteria

# =============================================================================
# STATE MANAGEMENT
# =============================================================================
search_query = solara.reactive("")
selected_database = solara.reactive("arXiv")
search_results = solara.reactive([])
ranking_criteria = solara.reactive(None)
is_searching = solara.reactive(False)
search_error = solara.reactive("")
visible_results_count = solara.reactive(5)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def perform_search():
    """Execute paper search with error handling"""
    if not search_query.value.strip():
        search_error.set("Please enter a search query")
        return
    
    is_searching.set(True)
    search_error.set("")
    search_results.set([])
    ranking_criteria.set(None)
    visible_results_count.set(5)
    
    try:
        papers, criteria = search_papers(
            query=search_query.value,
            source=selected_database.value,
            max_results=10,
            sort_by="relevance"
        )
        search_results.set(papers)
        ranking_criteria.set(criteria)
        
    except Exception as e:
        search_error.set(str(e))
    finally:
        is_searching.set(False)


# =============================================================================
# STYLE COMPONENTS
# =============================================================================

@solara.component
def GlobalStyles():
    """Global CSS styles for animations and effects"""
    solara.HTML(unsafe_innerHTML="""
    <style>
        /* Remove underline from input fields */
        .v-text-field__slot input {
            border-bottom: none !important;
        }
        .v-text-field > .v-input__control > .v-input__slot:before,
        .v-text-field > .v-input__control > .v-input__slot:after {
            border-bottom: none !important;
        }
        .v-input__slot:before,
        .v-input__slot:after {
            display: none !important;
        }
        
        .paper-card {
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .paper-card:hover {
            box-shadow: 0 20px 50px rgba(59, 130, 246, 0.25), 0 8px 10px rgba(0, 0, 0, 0.15) !important;
            border-color: #3b82f6 !important;
            border-left-width: 6px !important;
        }
        .action-btn {
            background-color: #dbeafe !important;
            color: #3b82f6 !important;
            transition: all 0.3s ease !important;
        }
        .action-btn:hover {
            background-color: #3b82f6 !important;
            color: #ffffff !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        }
        .action-btn.secondary {
            background-color: #e0e7ff !important;
            color: #4338ca !important;
        }
        .action-btn.secondary:hover {
            background-color: #6366f1 !important;
            color: #ffffff !important;
        }
        .search-btn {
            background-color: #73acec !important;
            color: #1e3a8a !important;
            transition: all 0.3s ease !important;
        }
        .search-btn:hover {
            background-color: #3b82f6 !important;
            color: #ffffff !important;
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3) !important;
        }
        .load-more-btn {
            transition: all 0.3s ease !important;
        }
        .load-more-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 16px rgba(59, 130, 246, 0.2) !important;
            background-color: #3b82f6 !important;
            color: #ffffff !important;
        }
        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeInUp 0.6s ease-out;
        }
    </style>
    """)


# =============================================================================
# UI COMPONENTS
# =============================================================================

@solara.component
def Header():
    """Application header with title and subtitle"""
    with solara.Column(style={
        "text-align": "center", 
        "margin-bottom": "50px",
        "padding": "50px 40px",
        "background": "rgba(255, 255, 255, 0.8)",
        "border-radius": "24px",
        "backdrop-filter": "blur(10px)",
        "box-shadow": "0 8px 32px rgba(0, 0, 0, 0.08)"
    }):
        solara.HTML(
            tag="h1",
            unsafe_innerHTML="📚 Paper Finder",
            style={
                "font-size": "4rem",
                "margin-bottom": "20px",
                "color": "#1e293b",
                "font-weight": "800",
                "letter-spacing": "-0.02em"
            }
        )
        solara.HTML(
            tag="p",
            unsafe_innerHTML="<em>Discover, explore, and organize academic papers with transparent ranking and real-time citations</em>",
            style={
                "font-size": "1.4rem",
                "color": "#475569",
                "margin": "0",
                "font-weight": "400",
                "max-width": "900px",
                "margin-left": "auto",
                "margin-right": "auto"
            }
        )


@solara.component
def SearchSection():
    """Search input and button component"""
    with solara.Card(style={
        "padding": "45px",
        "box-shadow": "0 10px 40px rgba(0, 0, 0, 0.12)",
        "border-radius": "16px",
        "margin-bottom": "40px",
        "background": "#ffffff",
        "border": "1px solid rgba(226, 232, 240, 0.8)"
    }):
        # Header with database selector
        with solara.Row(style={
            "margin-bottom": "25px",
            "align-items": "center",
            "justify-content": "space-between"
        }):
            solara.HTML(
                tag="h2",
                unsafe_innerHTML="🔍 Search for Papers",
                style={"color": "#0f172a", "margin": "0", "font-weight": "700", "font-size": "1.5rem"}
            )
            with solara.Row(style={"align-items": "center", "gap": "12px"}):
                solara.Markdown("Database:", style={"margin": "0", "color": "#64748b", "font-size": "0.95rem"})
                solara.ToggleButtonsSingle(
                    value=selected_database.value,
                    on_value=selected_database.set,
                    values=["arXiv", "PubMed", "IEEE", "Google Scholar"]
                )
        
        # Search input with examples
        with solara.Column(style={"margin-bottom": "24px"}):
            solara.InputText(
                label="Enter keywords, topic, or author",
                value=search_query.value,
                on_value=lambda value: (search_query.set(value), perform_search() if value.strip() else None),
                style={
                    "width": "100%",
                    "border": "2px solid #e2e8f0",
                    "border-radius": "12px",
                    "padding": "14px 18px",
                    "font-size": "1.05rem",
                    "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.05)",
                    "transition": "all 0.3s ease",
                    "outline": "none",
                    "text-decoration": "none"
                },
                continuous_update=False
            )
            solara.HTML(
                tag="div",
                unsafe_innerHTML="💡 Try: <em>\"machine learning transformers\"</em>, <em>\"climate change models\"</em>, or <em>\"quantum computing\"</em>",
                style={"font-size": "0.85rem", "color": "#64748b", "margin-top": "8px"}
            )
        
        # Search button
        with solara.Row(style={"justify-content": "center"}):
            solara.Button(
                "🔎 Search Papers",
                on_click=perform_search,
                color="primary",
                classes=["search-btn"],
                style={
                    "padding": "14px 40px",
                    "font-size": "1.1rem",
                    "font-weight": "600",
                    "border-radius": "12px",
                    "box-shadow": "0 4px 12px rgba(59, 130, 246, 0.25)",
                    "transition": "all 0.3s ease",
                    "text-transform": "none",
                    "letter-spacing": "0.02em"
                }
            )


@solara.component
def LoadingState():
    """Skeleton loading cards during search"""
    with solara.Column(style={"margin-top": "30px", "gap": "24px"}):
        solara.Markdown("🔍 **Searching for papers...**",
                       style={"font-size": "1.3rem", "color": "#0369a1", "text-align": "center", "margin-bottom": "10px"})
        
        # Skeleton cards
        for i in range(3):
            with solara.Card(style={
                "padding": "28px",
                "background": "linear-gradient(90deg, #f8fafc 0%, #e0e7ff 50%, #f8fafc 100%)",
                "background-size": "200% 100%",
                "animation": "shimmer 1.5s infinite",
                "border-radius": "16px",
                "border": "1px solid #e2e8f0",
                "min-height": "180px"
            }):
                # Title skeleton
                solara.HTML(tag="div", unsafe_innerHTML="", style={
                    "height": "24px",
                    "width": "80%",
                    "background": "#cbd5e1",
                    "border-radius": "6px",
                    "margin-bottom": "16px"
                })
                # Metadata skeleton
                with solara.Row(style={"gap": "16px", "margin-bottom": "16px"}):
                    for j in range(3):
                        solara.HTML(tag="div", unsafe_innerHTML="", style={
                            "height": "18px",
                            "width": "120px",
                            "background": "#cbd5e1",
                            "border-radius": "4px"
                        })
                # Content skeleton
                for k in range(3):
                    solara.HTML(tag="div", unsafe_innerHTML="", style={
                        "height": "16px",
                        "width": f"{90 - k * 10}%",
                        "background": "#cbd5e1",
                        "border-radius": "4px",
                        "margin-bottom": "10px"
                    })


@solara.component
def ErrorState():
    """Error message display"""
    if search_error.value:
        with solara.Card(style={
            "padding": "30px",
            "margin-top": "20px",
            "background": "#fef2f2",
            "border-left": "4px solid #ef4444",
            "border-radius": "12px"
        }):
            solara.Error(f"Error: {search_error.value}")


@solara.component
def CitationBadge(count: int):
    """Citation count badge component"""
    solara.Markdown(f"📊 **{count:,}** citations",
                   style={"margin": "0", "font-size": "0.9rem", "color": "#059669", "font-weight": "700"})


@solara.component
def PaperCard(paper: Paper, index: int):
    """Individual paper card component"""
    with solara.Column(style={
        "padding": "28px",
        "margin": "0 0 28px 0",
        "border": "1px solid #e2e8f0",
        "border-left": "5px solid #3b82f6",
        "background": "linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #eff6ff 100%)",
        "border-radius": "16px",
        "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.06), 0 1px 3px rgba(0, 0, 0, 0.03)",
        "gap": "12px",
        "transition": "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
        "cursor": "default"
    }, classes=["paper-card"]):
        
        # Title, Action Buttons, and Relevance Score (all in one row)
        with solara.Row(style={"justify-content": "space-between", "align-items": "center", "gap": "15px"}):
            solara.Markdown(f"**{index}. {paper.title}**",
                           style={"flex": "1", "margin": "0", "font-size": "1.1rem", "color": "#0f172a", "font-weight": "700"})
            
            # Action Buttons
            with solara.Row(style={"gap": "8px", "align-items": "center"}):
                solara.Button(
                    "🔗 View",
                    href=paper.url,
                    target="_blank",
                    color="primary",
                    text=False,
                    style={
                        "padding": "6px 12px",
                        "font-size": "0.85rem",
                        "font-weight": "600",
                        "border-radius": "6px",
                        "transition": "all 0.3s ease",
                        "text-transform": "none",
                        "min-width": "70px",
                        "border": "1px solid #93c5fd"
                    },
                    classes=["action-btn", "secondary"]
                )
                if paper.pdf_url:
                    solara.Button(
                        "📥 PDF",
                        href=paper.pdf_url,
                        target="_blank",
                        color="secondary",
                        text=False,
                        style={
                            "padding": "6px 12px",
                            "font-size": "0.85rem",
                            "font-weight": "600",
                            "border-radius": "6px",
                            "transition": "all 0.3s ease",
                            "text-transform": "none",
                            "min-width": "70px",
                            "border": "1px solid #6366f1"
                        },
                        classes=["action-btn", "secondary"]
                    )
                
                # Relevance Score
                with solara.v.Html(tag="div", style_="background: #dbeafe; padding: 6px 12px; border-radius: 20px;"):
                    solara.Markdown(f"**{paper.relevance_score:.2f}**",
                                   style={"color": "#1e40af", "font-size": "0.85rem", "margin": "0", "font-weight": "700"})
        
        # Metadata: Authors, Date, Citations, Affiliations
        with solara.Row(style={"gap": "24px", "flex-wrap": "wrap", "align-items": "center", "margin-bottom": "4px"}):
            # Authors
            author_text = ', '.join(paper.authors[:3])
            if len(paper.authors) > 3:
                author_text += " *et al.*"
            solara.Markdown(f"👤 {author_text}",
                           style={"margin": "0", "font-size": "0.98rem", "color": "#475569", "line-height": "1.5"})
            
            # Date
            solara.Markdown(f"📅 {paper.published_date.strftime('%b %d, %Y')}",
                           style={"margin": "0", "font-size": "0.98rem", "color": "#64748b", "line-height": "1.5"})
            
            # Citations
            CitationBadge(paper.citation_count)
            
            # Affiliations (if available)
            if paper.affiliations:
                solara.Markdown(f"🏛️ {', '.join(paper.affiliations)}",
                               style={"margin": "0", "font-size": "0.92rem", "color": "#6366f1", "font-weight": "600", "line-height": "1.5"})
        
        # Abstract
        abstract = paper.abstract[:280] + "..." if len(paper.abstract) > 280 else paper.abstract
        solara.Markdown(abstract,
                       style={"margin": "8px 0 0 0", "font-size": "1.02rem", "line-height": "1.75", "color": "#334155", "letter-spacing": "0.01em"})


@solara.component
def ResultsSection():
    """Search results display with pagination"""
    if search_results.value:
        solara.Markdown(f"### Found {len(search_results.value)} papers",
                       style={"margin-top": "10px", "margin-bottom": "25px", "font-weight": "700", "color": "#0f172a", "font-size": "1.4rem"})
        
        # Display visible papers
        visible_papers = search_results.value[:visible_results_count.value]
        for idx, paper in enumerate(visible_papers, 1):
            PaperCard(paper=paper, index=idx)
        
        # Load More button
        if len(search_results.value) > visible_results_count.value:
            with solara.Row(style={"justify-content": "center", "margin-top": "32px"}):
                remaining = len(search_results.value) - visible_results_count.value
                solara.Button(
                    f"📚 Load More Papers ({remaining} remaining)",
                    on_click=lambda: visible_results_count.set(visible_results_count.value + 5),
                    color="primary",
                    outlined=True,
                    classes=["load-more-btn"],
                    style={
                        "padding": "14px 32px",
                        "font-size": "1.05rem",
                        "font-weight": "600",
                        "border-radius": "12px",
                        "border-width": "2px",
                        "transition": "all 0.3s ease",
                        "box-shadow": "0 2px 8px rgba(59, 130, 246, 0.15)"
                    }
                )


@solara.component
def RankingCriteriaCard():
    """Display ranking methodology"""
    if search_results.value and ranking_criteria.value:
        with solara.Card(style={
            "padding": "28px",
            "margin-top": "35px",
            "background": "linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)",
            "border-radius": "16px",
            "border": "1px solid #93c5fd",
            "border-left": "5px solid #3b82f6",
            "box-shadow": "0 4px 12px rgba(59, 130, 246, 0.15)"
        }):
            solara.Markdown("### 📊 Search Methodology",
                           style={"margin": "0 0 15px 0", "font-size": "1.25rem", "font-weight": "700", "color": "#1e3a8a"})
            
            with solara.Row(style={"gap": "25px", "flex-wrap": "wrap", "font-size": "0.95rem"}):
                solara.Markdown(f"**Source:** {ranking_criteria.value.source}", style={"margin": "0", "color": "#1e40af"})
                solara.Markdown(f"**Sort:** {ranking_criteria.value.sort_method}", style={"margin": "0", "color": "#1e40af"})
                solara.Markdown(f"**Max Results:** {ranking_criteria.value.max_results}", style={"margin": "0", "color": "#1e40af"})
            
            solara.Markdown(ranking_criteria.value.description,
                           style={"margin": "12px 0 0 0", "font-size": "0.95rem", "color": "#334155", "line-height": "1.6"})
            
            with solara.Details("View Applied Filters"):
                for filter_item in ranking_criteria.value.filters_applied:
                    solara.Markdown(f"• {filter_item}", style={"margin": "4px 0", "font-size": "0.9rem", "color": "#475569"})


@solara.component
def FeaturesSection():
    """Feature cards display - shown on landing page and after results"""
    with solara.Row(style={"gap": "30px", "margin-bottom": "20px", "margin-top": "40px"}):
        features = [
            ("🎯", "Smart Search", "Advanced algorithms to find the most relevant papers for your research"),
            ("📊", "Transparent Ranking", "Clear documentation of search criteria and ranking methodology"),
            ("📄", "Direct Access", "Quick links to papers and PDFs from multiple research databases")
        ]
        
        for icon, title, description in features:
            with solara.Card(style={"flex": "1", "padding": "30px", "text-align": "center"}):
                solara.Markdown(icon, style={"font-size": "3rem", "margin-bottom": "15px"})
                solara.Markdown(f"**{title}**")
                solara.Markdown(description, style={"color": "#64748b", "font-size": "0.9rem"})


@solara.component
def Footer():
    """Application footer"""
    with solara.Column(style={
        "text-align": "center",
        "margin-top": "60px",
        "padding-top": "30px",
        "border-top": "1px solid #e2e8f0"
    }):
        solara.Markdown(
            "Built with [Solara](https://solara.dev) | [GitHub](https://github.com/rajan-sap/paper-finder)",
            style={"color": "#94a3b8"}
        )


# =============================================================================
# MAIN PAGE
# =============================================================================

@solara.component
def Page():
    """Main application page"""
    GlobalStyles()
    
    with solara.Column(style={
        "width": "100%",
        "min-height": "100vh",
        "background": "linear-gradient(to bottom, #f8fafc 0%, #e0e7ff 100%)",
        "padding": "60px 0 60px 0",
        "box-sizing": "border-box",

    }):
        with solara.Column(style={
            "width": "95%",
            "margin": "100 auto 0 10",
            "max-width": "1800px",
            "padding": "0 20px"
        }):
            Header()
            SearchSection()
            
            # Show features on landing page (before any search)
            if not search_results.value and not is_searching.value and not search_error.value:
                FeaturesSection()
            
            if is_searching.value:
                LoadingState()
            elif search_error.value:
                ErrorState()
            elif search_results.value:
                ResultsSection()
                RankingCriteriaCard()
                # Show features after results (above footer)
                FeaturesSection()
            
            Footer()
