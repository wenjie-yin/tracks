import json

from pydantic_tfl_api import JourneyClient
from pydantic_tfl_api.core.package_models import ApiError
from pydantic_tfl_api.models import ItineraryResult

from data_model.journey_models import (
    DisambiguationOption,
    JourneyOption,
    get_journey_detail,
)

journey_client = JourneyClient()


def from_tfl_api_model(response: ItineraryResult) -> list[JourneyOption]:
    return list(map(get_journey_detail, response.journeys))


# Note: Consumers of this function should handle the conversion of the data models to relevant formats for LLM input.
def plan_journey(
    start: str, finish: str
) -> list[DisambiguationOption] | list[JourneyOption]:
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
    return from_tfl_api_model(resp.content)


if __name__ == "__main__":
    # Example usage
    start = "Canada Water Bus Station"
    finish = "Southwark, Southwark Station"
    plan_journey(start, finish)
