from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/prreview', methods=['POST'])
def handle_pr_review():
    try:
        body = request.get_json()
        if not isinstance(body, dict):
            return jsonify({'error': 'Body is not a valid JSON object'}), 400

        # Placeholder: Add your PR review logic here
        # Example: Process review data and return a response
        review_id = body.get('review_id')
        pr_number = body.get('pr_number')
        status = body.get('status')

        return jsonify({
            'message': 'PR review processed successfully',
            'review_id': review_id,
            'pr_number': pr_number,
            'status': status
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    stage = os.environ.get('STAGE', 'unknown')
    return jsonify({
        'status': 'healthy',
        'message': f'PR Review Flask app is running in {stage} stage'
    }), 200