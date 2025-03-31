import json

from pydantic_tfl_api import JourneyClient
from pydantic_tfl_api.core.package_models import ApiError
from pydantic_tfl_api.models import Journey, Leg

journey_client = JourneyClient()


def get_leg_detail(leg: Leg) -> dict:
    return {
        "duration": leg.duration,
        "instruction": leg.instruction.summary,
        "mode": leg.mode.name,
    }


def get_journey_detail(journey: Journey) -> dict:
    return {
        "duration": journey.duration,
        "fare": journey.fare.totalCost if journey.fare else None,
        "legs": list(map(get_leg_detail, journey.legs)),
    }


# TODO: Define a proper output format
def plan_journey(start: str, finish: str):
    # TODO: Add the full set of parameters
    resp = journey_client.JourneyResultsByPathFromPathToQueryViaQueryNationalSearchQueryDateQu(
        from_field=start, to=finish
    )
    if isinstance(resp, ApiError):
        # TODO: handle this properly. The response may return a list of
        # disambiguation options, which we should probably return to the user
        # for clarification
        print(json.dumps(json.loads(resp.message), indent=2))
        raise Exception(f"API Error: {resp.message}")
    resp_content = resp.content
    short_output = {
        "journeys": list(map(get_journey_detail, resp_content.journeys)),
    }
    print(json.dumps(short_output, indent=2))
    return short_output


if __name__ == "__main__":
    # Example usage
    start = "Canada Water Bus Station"
    finish = "Southwark, Southwark Station"
    plan_journey(start, finish)
