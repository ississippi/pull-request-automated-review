from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    print(f'Entered /prreview endpoint')
    return jsonify({'status': 'healthy', 'message': 'pr-notifications Flask app is running'}), 200

@app.route('/prnotifications', methods=['GET'])
def get_notifications():
    """Return a greeting message, optionally using a name from query params."""
    return jsonify({'message': f'Hello from pr-notifications!'}), 200

if __name__ == '__main__':
    app.run(debug=True)