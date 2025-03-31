import json
from typing import Optional

from pydantic_tfl_api import JourneyClient
from pydantic_tfl_api.core.package_models import ApiError
from pydantic_tfl_api.models import ItineraryResult

from tracks.data_model.journey_models import (
    DisambiguationOption,
    JourneyOption,
    get_journey_detail,
)

journey_client = JourneyClient()


def from_tfl_api_model(response: ItineraryResult) -> list[JourneyOption]:
    return list(map(get_journey_detail, response.journeys))


def from_tfl_api_entity_disambiguation(
    disambiguation: Optional[dict], field_name: str, original_input: str
) -> Optional[DisambiguationOption]:
    if disambiguation is None:
        return None
    # first check matchStatus
    match disambiguation.get("matchStatus"):
        case "empty":
            # Nothing to disambiguate
            return None
        case "identified":
            # Unique match, no disambiguation needed
            return None
        case "list":
            # Multiple options available
            return DisambiguationOption(
                original_input_field=field_name,
                original_input=original_input,
                options=[
                    (
                        option.get("place", {}).get("commonName"),
                        option.get("parameterValue"),
                        option.get("matchQuality"),
                    )
                    for option in disambiguation.get("disambiguationOptions", [])
                ],
            )
        case _:
            raise ValueError(
                f"Unknown matchStatus: {disambiguation.get('matchStatus')}"
            )


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
        try:
            response_json = json.loads(resp.message)
            print(json.dumps(response_json, indent=2))
            # Check if the response contains disambiguation options
            if (
                response_json.get("$type")
                == "Tfl.Api.Presentation.Entities.JourneyPlanner.DisambiguationResult, Tfl.Api.Presentation.Entities"
            ):
                # This is a disambiguation response
                disambiguations: list[DisambiguationOption] = []
                to_disambiguation = from_tfl_api_entity_disambiguation(
                    response_json.get("toLocationDisambiguation"),
                    "to",
                    finish,
                )
                if to_disambiguation:
                    disambiguations.append(to_disambiguation)
                from_disambiguation = from_tfl_api_entity_disambiguation(
                    response_json.get("fromLocationDisambiguation"),
                    "from",
                    start,
                )
                if from_disambiguation:
                    disambiguations.append(from_disambiguation)
                return disambiguations
            # This is an unknown error response
            raise Exception(f"API Error: {resp.message}")
        except json.JSONDecodeError:
            # Handle the case where the response is not valid JSON
            raise Exception(f"API Error: {resp.message}")
    return from_tfl_api_model(resp.content)


if __name__ == "__main__":
    # Example usage
    start = "Canada Water"
    finish = "London Bridge"
    print(plan_journey(start, finish))
