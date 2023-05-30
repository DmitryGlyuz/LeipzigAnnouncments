import json
import parser_planlos
import parser_sachsenpunk
import parser_songkick
from itertools import chain


# planlos_events = parser_planlos.events
# sachsenpunk_events = parser_sachsenpunk.events
# songkick_events = parser_songkick.events

# all_dates = list(set(chain(planlos_events, sachsenpunk_events, songkick_events)))
# all_dates.sort()
print(parser_planlos.events)
