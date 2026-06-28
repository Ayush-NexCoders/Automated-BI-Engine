def calculate_wow(current: float, previous: float) -> float:
    """
    Calculate Week-over-Week percentage change.
    """

    if previous == 0:
        return 0.0

    return round(
        ((current - previous) / previous) * 100,
        2
    )


def aggregate_kpis(current_week: dict, previous_week: dict) -> dict:
    """
    Aggregate KPI WoW metrics.
    """

    return {
        "reach_wow": calculate_wow(
            current_week.get("reach", 0),
            previous_week.get("reach", 0)
        ),

        "impressions_wow": calculate_wow(
            current_week.get("impressions", 0),
            previous_week.get("impressions", 0)
        ),

        "engagements_wow": calculate_wow(
            current_week.get("engagements", 0),
            previous_week.get("engagements", 0)
        )
    }
    
def calculate_wow(current: float, previous: float) -> float:
    """
    Calculate Week-over-Week percentage change.
    """

    if previous == 0:
        return 0.0

    return round(
        ((current - previous) / previous) * 100,
        2
    )


def aggregate_kpis(current_week: dict, previous_week: dict) -> dict:
    """
    Aggregate KPI WoW metrics.
    """

    return {
        "reach_wow": calculate_wow(
            current_week.get("reach", 0),
            previous_week.get("reach", 0)
        ),

        "impressions_wow": calculate_wow(
            current_week.get("impressions", 0),
            previous_week.get("impressions", 0)
        ),

        "engagements_wow": calculate_wow(
            current_week.get("engagements", 0),
            previous_week.get("engagements", 0)
        )
    }
    
def calculate_wow(current: float, previous: float) -> float:
    """
    Calculate Week-over-Week percentage change.
    """

    if previous == 0:
        return 0.0

    return round(
        ((current - previous) / previous) * 100,
        2
    )


def aggregate_kpis(current_week: dict, previous_week: dict) -> dict:
    """
    Aggregate KPI WoW metrics.
    """

    return {
        "reach_wow": calculate_wow(
            current_week.get("reach", 0),
            previous_week.get("reach", 0)
        ),

        "impressions_wow": calculate_wow(
            current_week.get("impressions", 0),
            previous_week.get("impressions", 0)
        ),

        "engagements_wow": calculate_wow(
            current_week.get("engagements", 0),
            previous_week.get("engagements", 0)
        )
    }