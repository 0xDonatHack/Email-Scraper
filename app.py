from flask import Flask, render_template, jsonify
import os , sys , subprocess , time

app = Flask(__name__)

# Route for the main dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route for the map page
@app.route('/map')
def map():
    global last_update_timestamp
    # Simulate map update
    last_update_timestamp = int(time.time())  # Update timestamp when map content changes
    return render_template('map.html')  # Map HTML content

# Route to get the timestamp of the last map update
@app.route('/map-timestamp')
def map_timestamp():
    # Path to the map file
    map_path = os.path.join(app.template_folder, 'map.html')
    # Get the last modification time of map.html, or return 0 if it doesn't exist
    timestamp = os.path.getmtime(map_path) if os.path.exists(map_path) else 0
    return jsonify({"timestamp": timestamp})
@app.route('/scrap')
def scrap():
    subprocess.run([sys.executable, "GoogleMap.py"])
    
if __name__ == '__main__':
    app.run(debug=True)
