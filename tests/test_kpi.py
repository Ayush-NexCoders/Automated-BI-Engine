from modules.kpi_aggregator import aggregate_kpis


def test_kpi_aggregation():

    previous = {
        "reach": 100,
        "impressions": 200,
        "engagements": 50
    }

    current = {
        "reach": 120,
        "impressions": 180,
        "engagements": 55
    }

    result = aggregate_kpis(
        current,
        previous
    )

    assert result["reach_wow"] == 20.0
    assert result["impressions_wow"] == -10.0
    assert result["engagements_wow"] == 10.0