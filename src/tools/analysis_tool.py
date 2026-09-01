from agents import function_tool


@function_tool
def diagnose_error(
    error_code: str,
) -> str:
    """
    Provide a deterministic first-pass diagnosis
    for common demo support error codes.
    """

    table = {

        "AUTH-401":
            "Authentication failed. "
            "Verify token expiry, clock skew, "
            "and credentials.",

        "RATE-429":
            "Rate limit exceeded. "
            "Retry with exponential backoff "
            "and inspect request volume.",

        "DB-503":
            "Database service unavailable. "
            "Check health status and retry "
            "after a short delay.",

        "TIMEOUT":
            "Upstream request timed out. "
            "Check latency, retry policy, "
            "and dependency health.",
    }


    return table.get(
        error_code.upper(),
        (
            "Unknown error code; "
            "inspect logs and dependency health."
        ),
    )