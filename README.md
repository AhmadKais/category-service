# Category Service

The Category Service is part of a Personal Finance Tracker application. It allows users to manage categories for their financial transactions, enabling better organization and reporting of spending.

## Features

- Create new categories
- Retrieve existing categories
- Update categories
- Delete categories

## Technologies Used

- Python 3.9
- Flask
- DynamoDB (AWS)
- Boto3 (AWS SDK for Python)

## API Endpoints

### Create Category

- **POST** `/categories`
- **Request Body:**
  ```json
  {
    "name": "Food",
    "description": "Expenses related to food"
  }
