# Main Solara app
import solara
from typing import Optional

# State management
search_query = solara.reactive("")
selected_database = solara.reactive("arXiv")

@solara.component
def Page():
    """Main paper finder application"""
    
    # Hero Section
    with solara.Column(style={"padding": "40px 20px", "max-width": "1200px", "margin": "0 auto"}):
        # Header
        with solara.Column(style={"text-align": "center", "margin-bottom": "60px"}):
            solara.HTML(
                tag="h1",
                unsafe_innerHTML="📚 Academic Paper Finder",
                style={
                    "font-size": "3rem",
                    "margin-bottom": "20px",
                    "color": "#1e293b",
                    "font-weight": "700"
                }
            )
            solara.Markdown(
                """
                *Discover, explore, and organize academic papers from leading research databases*
                """,
                style={"font-size": "1.2rem", "color": "#64748b", "margin-bottom": "40px"}
            )
        
        # Search Section
        with solara.Card(
            style={
                "padding": "40px",
                "box-shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                "border-radius": "12px",
                "margin-bottom": "40px"
            }
        ):
            solara.HTML(
                tag="h2",
                unsafe_innerHTML="🔍 Search for Papers",
                style={"margin-bottom": "20px", "color": "#334155"}
            )
            
            # Search input
            solara.InputText(
                label="Enter keywords, topic, or author",
                value=search_query.value,
                on_value=search_query.set,
                style={"width": "100%", "margin-bottom": "20px"}
            )
            
            # Database selector
            with solara.Row(style={"margin-bottom": "20px", "align-items": "center"}):
                solara.Markdown("**Select Database:**", style={"margin-right": "20px"})
                solara.ToggleButtonsSingle(
                    value=selected_database.value,
                    on_value=selected_database.set,
                    values=["arXiv", "PubMed", "IEEE", "Google Scholar"]
                )
            
            # Search button
            with solara.Row(style={"justify-content": "center"}):
                solara.Button(
                    "Search Papers",
                    on_click=lambda: search_papers(),
                    color="primary",
                    style={
                        "padding": "12px 32px",
                        "font-size": "1.1rem",
                        "border-radius": "8px"
                    }
                )
        
        # Features Section
        with solara.Row(style={"gap": "30px", "margin-bottom": "40px"}):
            # Feature 1
            with solara.Card(style={"flex": "1", "padding": "30px", "text-align": "center"}):
                solara.HTML(
                    tag="div",
                    unsafe_innerHTML="🎯",
                    style={"font-size": "3rem", "margin-bottom": "15px"}
                )
                solara.Markdown("**Smart Search**")
                solara.Markdown(
                    "Advanced algorithms to find the most relevant papers for your research",
                    style={"color": "#64748b", "font-size": "0.9rem"}
                )
            
            # Feature 2
            with solara.Card(style={"flex": "1", "padding": "30px", "text-align": "center"}):
                solara.HTML(
                    tag="div",
                    unsafe_innerHTML="📊",
                    style={"font-size": "3rem", "margin-bottom": "15px"}
                )
                solara.Markdown("**Filter & Sort**")
                solara.Markdown(
                    "Organize results by date, citations, relevance, and more",
                    style={"color": "#64748b", "font-size": "0.9rem"}
                )
            
            # Feature 3
            with solara.Card(style={"flex": "1", "padding": "30px", "text-align": "center"}):
                solara.HTML(
                    tag="div",
                    unsafe_innerHTML="💾",
                    style={"font-size": "3rem", "margin-bottom": "15px"}
                )
                solara.Markdown("**Save & Export**")
                solara.Markdown(
                    "Export citations in multiple formats (BibTeX, APA, MLA)",
                    style={"color": "#64748b", "font-size": "0.9rem"}
                )
        
        # Results placeholder
        if search_query.value:
            with solara.Card(style={"padding": "30px", "margin-top": "20px"}):
                solara.Markdown(f"### Search Results for: *{search_query.value}*")
                solara.Markdown(f"**Database:** {selected_database.value}")
                solara.Info("Search functionality will be implemented soon. Stay tuned!")
        
        # Footer
        with solara.Column(style={"text-align": "center", "margin-top": "60px", "padding-top": "30px", "border-top": "1px solid #e2e8f0"}):
            solara.Markdown(
                "Built with ❤️ using [Solara](https://solara.dev) | Open Source",
                style={"color": "#94a3b8"}
            )

def search_papers():
    """Placeholder function for paper search"""
    if search_query.value.strip():
        print(f"Searching for: {search_query.value} in {selected_database.value}")
    else:
        print("Please enter a search query")

