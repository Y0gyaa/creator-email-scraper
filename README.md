# Content Creator Email Scraper

A powerful web application to find and extract contact emails from content creators, influencers, streamers, and bloggers based on niche, location, and other filters.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## ✨ Features

- 🔍 **Smart Search**: Find creators by niche, country, city, and area
- 📧 **Email Extraction**: Automatically extract contact emails from public sources
- 🎯 **Multi-Platform**: Search across YouTube, Instagram, Twitter/X, TikTok, and blogs
- 📊 **Export Results**: Download results as CSV for easy use
- 🎨 **Modern UI**: Beautiful dark-themed interface with smooth animations
- ⚡ **Real-time Results**: Live search with progress indicators

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone or navigate to the project directory.**
   
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser**:
   Navigate to `http://localhost:5000`

## 📖 Usage

### Basic Search

1. Fill in the search filters:
   - **Niche/Category**: e.g., "tech", "gaming", "fashion"
   - **Country**: e.g., "USA", "UK", "Canada"
   - **City**: e.g., "New York", "London"
   - **Area/Region**: e.g., "Manhattan", "Downtown"
   - **Max Results**: Number of results to return (1-100)

2. Click "Search Creators"

3. Wait for results to load

4. View creator information in the table

5. Click "Export CSV" to download results

### Example Searches

**Tech influencers in USA**:
- Niche: `tech`
- Country: `USA`
- Max Results: `50`

**Gaming streamers in UK**:
- Niche: `gaming`
- Country: `UK`
- City: `London`
- Max Results: `30`

**Fashion bloggers**:
- Niche: `fashion`
- Max Results: `40`

## 🏗️ Project Structure

```
creator-email-scraper/
├── app.py              # Flask backend API
├── scraper.py          # Web scraping logic
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── static/
│   ├── index.html     # Main UI page
│   ├── style.css      # Styling
│   └── script.js      # Frontend logic
├── output/            # CSV exports (auto-created)
└── README.md          # Documentation
```

## 🛠️ Configuration

Edit `config.py` to customize:

- **Scraping delays**: Adjust `delay_between_requests` for rate limiting
- **Timeout settings**: Change `timeout` value
- **Max results**: Modify `max_results` default
- **User agents**: Add more user agent strings

## 📡 API Endpoints

### POST `/api/search`
Search for content creators

**Request Body**:
```json
{
  "niche": "tech",
  "country": "USA",
  "city": "New York",
  "area": "Manhattan",
  "max_results": 50
}
```

**Response**:
```json
{
  "success": true,
  "count": 10,
  "results": [
    {
      "name": "Creator Name",
      "email": "contact@example.com",
      "platform": "YouTube",
      "niche": "tech",
      "url": "https://...",
      "country": "USA",
      "city": "New York"
    }
  ]
}
```

### POST `/api/export`
Export results to CSV

**Request Body**:
```json
{
  "results": [...],
  "filename": "creators.csv"
}
```

### GET `/api/status`
Get current scraping status

## ⚠️ Legal Disclaimer

**IMPORTANT**: This tool is provided for educational and legitimate business purposes only. Please ensure you:

- ✅ Comply with local data protection laws (GDPR, CCPA, etc.)
- ✅ Respect website terms of service
- ✅ Only use publicly available information
- ✅ Use scraped data responsibly and ethically
- ✅ Obtain consent before sending marketing emails
- ❌ Do not use for spam or harassment
- ❌ Do not violate platform policies

**The developers are not responsible for misuse of this tool.**

## 🔧 Troubleshooting

### Server won't start
- Make sure port 5000 is not in use
- Check that all dependencies are installed: `pip install -r requirements.txt`

### No results found
- Try broader search criteria
- Check internet connection
- Some platforms may have anti-scraping measures

### Export not working
- Ensure the `output/` directory exists
- Check browser download settings

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with Flask, BeautifulSoup, and modern web technologies
- Designed for ethical content creator outreach

---

**Made with ❤️ for ethical marketing and collaboration**
