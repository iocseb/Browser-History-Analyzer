# Browser History Analyzer

A web-based tool that allows you to analyze browser history from Chrome, Firefox, and Safari. Upload history files from one or multiple browsers and get a searchable, sortable table of all your browsing history.

## Features

- Support for multiple browsers:
  - Google Chrome
  - Mozilla Firefox
  - Safari
- Multiple file upload support
- Drag and drop interface
- Privacy focused:
  - All processing is done locally
  - Files are deleted immediately after analysis
  - No data is stored on any server
- Rich data display:
  - Sortable columns
  - Search functionality
  - Adjustable page size
  - Truncated URLs with full text on hover
  - One-click URL copying
  - CSV export
- Clean, responsive interface
- Support for adding more files to existing analysis

## How to Use

1. Get your browser history file(s):

   **Chrome:**
   - Windows: `%LocalAppData%\Google\Chrome\User Data\Default\History`
   - Mac: `~/Library/Application Support/Google/Chrome/Default/History`
   - Linux: `~/.config/google-chrome/Default/History`

   **Firefox:**
   - Windows: `%APPDATA%\Mozilla\Firefox\Profiles\[profile-id]\places.sqlite`
   - Mac: `~/Library/Application Support/Firefox/Profiles/[profile-id]/places.sqlite`
   - Linux: `~/.mozilla/firefox/[profile-id]/places.sqlite`

   **Safari:**
   - Mac: `~/Library/Safari/History.db`

   > **Important:** Close your browser before copying the history file.

2. Upload the file(s):
   - Drag and drop files into the upload area, or
   - Click "Select Files" to choose files
   - Click "Analyze History Files"

3. View and analyze your history:
   - Sort by any column
   - Search across all data
   - Copy URLs with one click
   - Export to CSV
   - Add more files if needed

## Running Locally

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone the repository: 
```bash
git clone https://github.com/iocseb/Browser-History-Analyzer.git
cd Browser-History-Analyzer
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Technical Details

- Built with:
  - Flask (Python web framework)
  - SQLite3 (for reading browser databases)
  - DataTables (for table functionality)
  - Bootstrap 5 (for styling)
  - JavaScript (for frontend interactivity)

- Browser history files are SQLite databases with different schemas:
  - Chrome: Uses microseconds since 1601-01-01
  - Firefox: Uses microseconds since 1970-01-01
  - Safari: Uses seconds since 2001-01-01

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you find this tool useful, consider supporting me on [Patreon](https://www.patreon.com/iocseb).

## License

This project is licensed under the MIT License - see the LICENSE file for details.