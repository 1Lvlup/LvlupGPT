import os
import pytest
import pytest_asyncio
from botocore.exceptions import ClientError
from typing import List, Tuple, Union
from pathlib import Path

import boto3
from boto3.session import Session

from autogpt.file_workspace.s3 import S3FileWorkspace, S3FileWorkspaceConfiguration

pytest_plugins = "pytest_asyncio"


@pytest.fixture
def s3_client() -> boto3.client:
    session = Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    )
    return session.client("s3")


@pytest.fixture
def s3_resource(s3_client: boto3.client) -> boto3.resource:
    session = Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    )
    return session.resource("s3")


@pytest.fixture
def s3_bucket_name() -> str:
    return f"test-bucket-{str(uuid.uuid4())[:8]}"


@pytest.fixture
def s3_bucket(s3_resource: boto3.resource, s3_bucket_name: str) -> boto3.Bucket:
    bucket = s3_resource.Bucket(s3_bucket_name)
    bucket.create()
    yield bucket
    bucket.delete()


@pytest.fixture
def s3_workspace_uninitialized(s3_bucket: boto3.Bucket) -> S3FileWorkspace:
    os.environ["WORKSPACE_STORAGE_BUCKET"] = s3_bucket.name
    ws_config = S3FileWorkspaceConfiguration.from_env()
    ws_config.root = Path("/workspaces/AutoGPT-some-unique-task-id")
    workspace = S3FileWorkspace(ws_config)
    yield workspace  # type: ignore
    del os.environ["WORKSPACE_STORAGE_BUCKET"]


def test_initialize(s3_bucket: boto3.Bucket, s3_workspace_uninitialized: S3FileWorkspace):
    s3 = s3_workspace_uninitialized._s3

    # test that the bucket doesn't exist yet
    with pytest.raises(ClientError):
        s3.meta.client.head_bucket(Bucket=s3_bucket.name)

    s3_workspace_uninitialized.initialize()

    # test that the bucket has been created
    s3.meta.client.head_bucket(Bucket=s3_bucket.name)


def test_workspace_bucket_name(
    s3_workspace: S3FileWorkspace,
    s3_bucket: boto3.Bucket,
):
    assert s3_workspace._bucket.name == s3_bucket.name


@pytest.fixture
def s3_workspace(s3_workspace_uninitialized: S3FileWorkspace) -> S3FileWorkspace:
    (s3_workspace := s3_workspace_uninitialized).initialize()
    yield s3_workspace  # type: ignore

    # Empty & delete the test bucket
    for obj in s3_workspace._bucket.objects.all():
        obj.delete()


NESTED_DIR = "existing/test/dir"
TEST_FILES: List[Tuple[Union[str, Path], str]] = [
    ("existing_test_file_1", "test content 1"),
    ("existing_test_file_2.txt", "test content 2"),
    (Path("existing_test_file_3"), "test content 3"),
    (Path(f"{NESTED_DIR}/test/file/4"), "test content 4"),
]


@pytest_asyncio.fixture
async def s3_workspace_with_files(s3_workspace: S3FileWorkspace) -> S3FileWorkspace:
    for file_name, file_content in TEST_FILES:
        s3_workspace._bucket.Object(str(s3_workspace.get_path(file_name))).put(
            Body=file_content
        )
    yield s3_workspace  # type: ignore


@pytest.mark.asyncio
async def test_read_file(s3_workspace_with_files: S3FileWorkspace):
    for file_name, file_content in TEST_FILES:
        content = s3_workspace_with_files.read_file(file_name)
        assert content == file_content

    with pytest.raises(ClientError):
        s3_workspace_with_files.read_file("non_existent_file")


def test_list_files(s3_workspace_with_files: S3FileWorkspace):
    # List at root level
    assert (files := s3_workspace_with_files.list()) == s3_workspace_with_files.list()
    assert len(files) > 0
    assert set(files) == set(Path(file_name) for file_name, _ in TEST_FILES)

    # List at nested path
    assert (
        nested_files := s3_workspace_with_files.list(NESTED_DIR)
    ) == s3_workspace_with_files.list(NESTED_DIR)
    assert len(nested_files) > 0
    assert set(nested_files) == set(
        p.relative_to(NESTED_DIR)
        for file_name,
