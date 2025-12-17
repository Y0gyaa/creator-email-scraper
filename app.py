"""Flask backend API for the content creator email scraper."""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime
from scraper import ContentCreatorScraper
from config import FLASK_CONFIG, OUTPUT_DIR

app = Flask(__name__, static_folder='static')
CORS(app)

# Store active scraper instance
current_scraper = None
scraping_status = {
    'is_running': False,
    'progress': 0,
    'total': 0,
    'message': 'Ready'
}


@app.route('/')
def index():
    """Serve the main UI page."""
    return send_from_directory('static', 'index.html')


@app.route('/style.css')
def serve_css():
    """Serve CSS file."""
    return send_from_directory('static', 'style.css')


@app.route('/script.js')
def serve_js():
    """Serve JavaScript file."""
    return send_from_directory('static', 'script.js')


@app.route('/api/search', methods=['POST'])
def search_creators():
    """
    Search for content creators based on filters.
    
    Request body:
    {
        "niche": "gaming",
        "country": "USA",
        "city": "New York",
        "area": "Manhattan",
        "max_results": 50
    }
    """
    global current_scraper, scraping_status
    
    try:
        data = request.get_json()
        
        # Extract parameters
        niche = data.get('niche', '')
        country = data.get('country', '')
        city = data.get('city', '')
        area = data.get('area', '')
        max_results = int(data.get('max_results', 50))
        
        # Update status
        scraping_status['is_running'] = True
        scraping_status['message'] = 'Searching for creators...'
        
        # Create new scraper instance
        current_scraper = ContentCreatorScraper()
        
        # Perform search
        results = current_scraper.search_creators(
            niche=niche,
            country=country,
            city=city,
            area=area,
            max_results=max_results
        )
        
        # Update status
        scraping_status['is_running'] = False
        scraping_status['progress'] = len(results)
        scraping_status['total'] = len(results)
        scraping_status['message'] = f'Found {len(results)} creators'
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        scraping_status['is_running'] = False
        scraping_status['message'] = f'Error: {str(e)}'
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export', methods=['POST'])
def export_results():
    """
    Export results to CSV.
    
    Request body:
    {
        "results": [...],
        "filename": "creators.csv"
    }
    """
    try:
        data = request.get_json()
        results = data.get('results', [])
        filename = data.get('filename', f'creators_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        
        if not results:
            return jsonify({
                'success': False,
                'error': 'No results to export'
            }), 400
        
        # Create DataFrame
        df = pd.DataFrame(results)
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Save to CSV
        filepath = os.path.join(OUTPUT_DIR, filename)
        df.to_csv(filepath, index=False)
        
        # Return the file
        return send_file(
            filepath,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current scraping status."""
    return jsonify(scraping_status)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Content Creator Email Scraper - Backend Server")
    print("=" * 60)
    print(f"Server starting on http://localhost:{FLASK_CONFIG['port']}")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(
        host=FLASK_CONFIG['host'],
        port=FLASK_CONFIG['port'],
        debug=FLASK_CONFIG['debug']
    )
