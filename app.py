from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import uuid

app = Flask(__name__)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('CategoriesTable')


@app.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    category_id = str(uuid.uuid4())
    name = data['name']

    try:
        table.put_item(
            Item={
                'category_id': category_id,
                'name': name,
                'description': data.get('description', '')
            }
        )
        return jsonify({"message": "Category created successfully", "category_id": category_id}), 201
    except ClientError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        response = table.scan()
        return jsonify(response['Items']), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    try:
        response = table.get_item(Key={'category_id': category_id})
        item = response.get('Item')
        if item:
            return jsonify(item), 200
        else:
            return jsonify({"error": "Category not found"}), 404
    except ClientError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.json
    name = data['name']
    description = data.get('description', '')

    try:
        table.update_item(
            Key={'category_id': category_id},
            UpdateExpression="set #name = :name, description = :description",
            ExpressionAttributeNames={'#name': 'name'},
            ExpressionAttributeValues={':name': name, ':description': description}
        )
        return jsonify({"message": "Category updated successfully"}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        table.delete_item(Key={'category_id': category_id})
        return jsonify({"message": "Category deleted successfully"}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
