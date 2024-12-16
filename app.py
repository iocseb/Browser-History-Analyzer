from flask import Flask, render_template, request, flash, jsonify
from werkzeug.utils import secure_filename
import os
from browser_history_parser import parse_browser_history

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'history_files' not in request.files:
            return jsonify({'error': 'No files selected'})
        
        files = request.files.getlist('history_files')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'})

        all_history_data = []
        errors = []

        for file in files:
            if file:
                try:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    print(f"Saving file to: {filepath}")
                    
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file.save(filepath)
                    
                    if not os.path.exists(filepath):
                        raise Exception("File was not saved successfully")
                    
                    try:
                        history_data = parse_browser_history(filepath, filename)
                        all_history_data.extend(history_data)
                    except Exception as e:
                        errors.append(f"Error processing {filename}: {str(e)}")
                    finally:
                        if os.path.exists(filepath):
                            os.remove(filepath)
                except Exception as e:
                    errors.append(f"Error handling {file.filename}: {str(e)}")

        # Convert datetime objects to strings for JSON serialization
        for entry in all_history_data:
            entry['timestamp'] = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        return jsonify({
            'success': True,
            'history_data': all_history_data,
            'errors': errors,
            'append': request.args.get('append') == 'true'  # New flag to indicate append mode
        })

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True) 