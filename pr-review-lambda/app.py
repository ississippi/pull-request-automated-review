from flask import Flask, jsonify, request
import boto3
import json
import os
import requests

app = Flask(__name__)

@app.route('/sns', methods=['POST'])
def handle_sns():
    try:
        # Extract SNS message
        body = request.get_json()
        if not isinstance(body, dict) or 'Records' not in body:
            return jsonify({'error': 'Invalid SNS message format'}), 400

        # Process each SNS record
        for record in body['Records']:
            if record.get('EventSource') != 'aws:sns':
                continue

            sns_message = json.loads(record['Sns']['Message'])
            pr_number = sns_message.get('pr_number')
            repo = sns_message.get('repo')
            pr_title = sns_message.get('pr_title')
            user_login = sns_message.get('user_login')
            html_url = sns_message.get('url')
            created_at = sns_message.get('created_at')
            pr_state = sns_message.get('pr_state')
            base_ref = sns_message.get('base_ref')

            # Make REST API call to external service (placeholder)
            external_service_url = os.environ.get('EXTERNAL_SERVICE_URL', 'https://api.example.com/review')
            payload = {
                'pr_number': pr_number,
                'repo': repo,
                'pr_title': pr_title,
                'user_login': user_login,
                'url': html_url,
                'created_at': created_at,
                'state': pr_state,
                'base_ref': base_ref
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(external_service_url, json=payload, headers=headers, timeout=10)

            # Check response
            if response.status_code != 200:
                raise Exception(f'External service returned {response.status_code}: {response.text}')

            # Publish to new SNS topic
            sns_client = boto3.client('sns')
            processed_message = {
                'pr_number': pr_number,
                'repo': repo,
                'external_service_response': response.json(),
                'processed_at': record['Sns']['Timestamp']
            }
            sns_client.publish(
                TopicArn=os.environ['PROCESSED_SNS_TOPIC_ARN'],
                Message=json.dumps(processed_message),
                Subject=f'PR #{pr_number} Review Processed'
            )

        return jsonify({'message': 'SNS message processed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/prreview', methods=['POST'])
def handle_pr_review():
    try:
        body = request.get_json()
        if not isinstance(body, dict):
            return jsonify({'error': 'Body is not a valid JSON object'}), 400

        # Placeholder: Manual trigger for testing
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