import json

import requests

BASE_URL = "http://mlops-lab-alb-1226201309.us-east-1.elb.amazonaws.com"


def test_health_endpoint():
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200, "Health endpoint should return 200"
    assert "status" in response.json(), "Response should contain 'status' field"


def test_predict_endpoint():
    print("\n=== Testing Predict Endpoint ===")

    test_data = {"text": "Amazing!"}

    response = requests.post(f"{BASE_URL}/predict", json=test_data)

    print(f"Status Code: {response.status_code}")
    print(f"Request Data: {json.dumps(test_data, indent=2)}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200, "Predict endpoint should return 200"
    result = response.json()
    assert "prediction" in result, "Response should contain 'prediction' field"


def run_all_tests():
    test_health_endpoint()
    test_predict_endpoint()


if __name__ == "__main__":
    run_all_tests()
