from unittest.mock import patch

from src.mcp.tools import get_customer


@patch(
    "src.mcp.tools.get_collection"
)
def test_customer_not_found(
    mock_collection,
):

    mock_collection.return_value.find_one.return_value = None

    result = get_customer(
        "DOES-NOT-EXIST"
    )

    assert result["found"] is False