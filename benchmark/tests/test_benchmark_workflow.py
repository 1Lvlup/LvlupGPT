import pytest
import requests
from time import sleep
from datetime import datetime, timezone, timedelta

URL_BENCHMARK = "http://localhost:8080/ap/v1"
URL_AGENT = "http://localhost:8000/ap/v1"

@pytest.fixture
def unique_eval_id():
    return f"{datetime.now(timezone.utc):%Y%m%d%H%M%S%f}"[:-3]

def get_task_id(response):
    return response.json()["task_id"]

def post_request_retry(url, json, retries=3, delay=1):
    for i in range(retries):
        response = requests.post(url, json=json)
        if response.status_code == 200:
            return response
        else:
            print(f"Request failed with status code {response.status_code}. Retrying in {delay} seconds...")
            sleep(delay)
    raise Exception(f"Request failed after {retries} retries")

def get_request_retry(url, retries=3, delay=1):
    for i in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            print(f"Request failed with status code {response.status_code}. Retrying in {delay} seconds...")
            sleep(delay)
    raise Exception(f"Request failed after {retries} retries")

@pytest.mark.parametrize(
    "input_text, expected_artifact_length, test_name, should_be_successful",
    [
        (
            "Write the word 'Washington' to a .txt file",
            0,
            "WriteFile",
            True,
        ),
        (
            "Read the file called file_to_read.txt and write its content to a file called output.txt",
            1,
            "ReadFile",
            False,
        ),
    ],
)
def test_entire_workflow(
    unique_eval_id, input_text, expected_artifact_length, test_name, should_be_successful, requests_retry_session
):
    task_request = {"eval_id": unique_eval_id, "input": input_text}

    # First POST request
    response = post_request_retry(f"{URL_BENCHMARK}/agent/tasks", json=task_request)
    task_id = get_task_id(response)

    response = get_request_retry(f"{URL_AGENT}/agent/tasks")
    task_count_after = response.json()["pagination"]["total_items"]
    assert task_count_after == 1 + 1

    timestamp_after_task_eval_created = datetime.now(timezone.utc)
    sleep(1.1)  # To make sure the 2 timestamps to compare are different

    response = get_request_retry(f"{URL_BENCHMARK}/agent/tasks/{task_id}")
    assert response.status_code == 200
    task_response_benchmark = response.json()
    assert task_response_benchmark["input"] == input_text

    response = get_request_retry(f"{URL_AGENT}/agent/tasks/{task_id}")
    assert response.status_code == 200
    response_task_agent = response.json()
    assert len(response_task_agent["artifacts"]) == expected_artifact_length

    step_request = {"input": input_text}

    response = post_request_retry(
        f"{URL_BENCHMARK}/agent/tasks/{task_id}/steps", json=step_request
    )
    assert response.status_code == 200
    step_response = response.json()
    assert step_response["is_last"] is True  # Assuming is_last is always True

    response = post_request_retry(
        f"{URL_BENCHMARK}/agent/tasks/{task_id}/evaluations", json={}
    )
    assert response.status_code == 200
    eval_response = response.json()
    print("eval_response")
    print(eval_response)
    assert eval_response["run_details"]["test_name"] == test
