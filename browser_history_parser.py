import sqlite3
import os
from datetime import datetime, timedelta

def parse_chrome_history(filepath):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT visits.visit_time, urls.url, urls.title
        FROM urls JOIN visits ON urls.id = visits.url
        ORDER BY visits.visit_time DESC
    """)
    results = cursor.fetchall()
    conn.close()
    
    return [(
        datetime.fromtimestamp(visit_time / 1000000 - 11644473600),
        url,
        title
    ) for visit_time, url, title in results]

def parse_firefox_history(filepath):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT visit_date, url, title
        FROM moz_places JOIN moz_historyvisits ON moz_places.id = moz_historyvisits.place_id
        ORDER BY visit_date DESC
    """)
    results = cursor.fetchall()
    conn.close()
    
    return [(
        datetime.fromtimestamp(visit_date / 1000000),
        url,
        title
    ) for visit_date, url, title in results]

def parse_safari_history(filepath):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    
    # Updated Safari schema query to include titles from history_visits
    cursor.execute("""
        SELECT 
            history_visits.visit_time,
            history_items.url,
            history_visits.title
        FROM history_visits 
        JOIN history_items ON history_visits.history_item = history_items.id
        ORDER BY history_visits.visit_time DESC
    """)
    results = cursor.fetchall()
    conn.close()
    
    # Safari stores timestamps as macOS time (seconds since 2001-01-01)
    mac_epoch = datetime(2001, 1, 1)
    
    return [(
        mac_epoch + timedelta(seconds=visit_time),
        url,
        title if title else url  # Fallback to URL if title is None
    ) for visit_time, url, title in results]

def parse_browser_history(filepath, filename):
    filename_lower = filename.lower()
    
    try:
        if ('history' in filename_lower and not filename_lower.endswith('.db')) or os.path.basename(filename_lower) == 'history':
            data = parse_chrome_history(filepath)
            browser = 'Chrome'
        elif 'places.sqlite' in filename_lower:
            data = parse_firefox_history(filepath)
            browser = 'Firefox'
        elif 'history.db' in filename_lower:
            data = parse_safari_history(filepath)
            browser = 'Safari'
        else:
            raise ValueError("Unknown browser history file")
        
        return [{
            'timestamp': entry[0],
            'url': entry[1],
            'title': entry[2],
            'browser': browser,
            'filename': filename
        } for entry in data]
    except sqlite3.DatabaseError as e:
        raise ValueError(f"Error reading database: {str(e)}. Make sure the browser is closed before copying the history file.") 