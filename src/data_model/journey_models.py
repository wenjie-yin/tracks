from typing import Optional

from pydantic import BaseModel
from pydantic_tfl_api.models import Leg
from pydantic_tfl_api.models.ItineraryResult import Journey


class DisambiguationOption(BaseModel):
    original_input: str
    options: list[tuple[str, str]]  # List of tuples (name, id)


class JourneyOption(BaseModel):
    duration: Optional[int]
    fare: Optional[int]  # in pence
    legs: list[Leg]


class LegInfo(BaseModel):
    duration: Optional[int]
    instruction_summary: Optional[str]
    instruction_detail: Optional[str]
    mode: Optional[str]


# Convert tfl_api models to our own models
def get_leg_detail(leg: Leg) -> LegInfo:
    return LegInfo(
        duration=leg.duration,
        instruction_summary=leg.instruction.summary if leg.instruction else None,
        instruction_detail=leg.instruction.detailed if leg.instruction else None,
        mode=leg.mode.name if leg.mode else None,
    )


def get_journey_detail(journey: Journey) -> JourneyOption:
    return JourneyOption(
        duration=journey.duration,
        fare=journey.fare.totalCost if journey.fare else None,
        legs=list(map(get_leg_detail, journey.legs)) if journey.legs else [],
    )
