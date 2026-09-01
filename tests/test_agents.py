def test_classification():

    from src.agents.orchestrator import (
        classify_query
    )


    assert (
        classify_query(
            {
                "query":
                    "How do I reset "
                    "my password?",

                "trace": [],
            }
        )["query_type"]
        == "faq"
    )


    assert (
        classify_query(
            {
                "query":
                    "API returns AUTH-401",

                "trace": [],
            }
        )["query_type"]
        == "technical"
    )


    assert (
        classify_query(
            {
                "query":
                    "I need a human manager",

                "trace": [],
            }
        )["query_type"]
        == "escalation"
    )