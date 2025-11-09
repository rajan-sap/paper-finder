# Solara Paper Finder

A web application for finding and exploring academic papers, built with Solara.

## Features

- Search academic papers
- Filter and sort results
- Interactive UI powered by Solara

## Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd solara-paper-finder
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   solara run app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:8765`

## Project Structure

```
solara-paper-finder/
│
├── app.py           # Main Solara app
├── requirements.txt # All Python dependencies
├── README.md        # Project info and setup guide
├── .gitignore       # Ignore files for Git
└── data/            # (optional) Cache or results if needed
```

## Technologies

- [Solara](https://solara.dev/) - Reactive web framework
- Python 3.11+

## License

MIT License
