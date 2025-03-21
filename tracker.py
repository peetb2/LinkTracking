import pyodbc
from flask import Flask, request, redirect
from user_agents import parse

app = Flask(__name__)

# ✅ 1. Function to Connect to SQL Server
def get_db_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-CIHEM95\\MSSQLSERVER01;"  # Use double backslashes
        "Database=ClickTracker;"
        "Trusted_Connection=yes;"
    )

# ✅ 2. Function to Store Click Data
def log_click(link_id, platform, device_type, browser, ip_address):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Clicks (link_id, platform, device_type, browser, ip_address)
        VALUES (?, ?, ?, ?, ?)
    """, (link_id, platform, device_type, browser, ip_address))
    conn.commit()
    conn.close()

# ✅ 3. Route to Track Clicks
@app.route('/track')
def track():
    link_id = request.args.get('link_id', 'unknown')

    # ✅ Get user details
    user_agent_string = request.headers.get("User-Agent")
    user_agent = parse(user_agent_string) if user_agent_string else None

    platform = user_agent.os.family if user_agent else "Unknown"
    browser = user_agent.browser.family if user_agent else "Unknown"
    device_type = "Mobile" if user_agent.is_mobile else "Desktop"
    ip_address = request.remote_addr

    # ✅ Store the click in the database
    log_click(link_id, platform, device_type, browser, ip_address)

    # ✅ Redirect to final website
    return redirect("https://clicktrackerdatabase.netlify.app/")

# ✅ 4. Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's port, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
