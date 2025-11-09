# Main Solara app
import solara

@solara.component
def Page():
    """Main paper finder application"""
    with solara.Column():
        solara.Markdown("# Paper Finder")
        solara.Markdown("Welcome to the Paper Finder application!")

