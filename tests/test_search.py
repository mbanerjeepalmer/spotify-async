import pytest
from spotipython.helpers import get_spotify_token

from spotipython import AuthenticatedClient
from spotipython.api.search import search
from spotipython.models.paging_track_object import PagingTrackObject
from spotipython.models.search_response_200 import SearchResponse200
from spotipython.models.search_type_item import SearchTypeItem

from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)

load_dotenv()


@pytest.mark.asyncio
async def test_take_on_me():
    token = await get_spotify_token()
    async with AuthenticatedClient(
        base_url="https://api.spotify.com/v1",
        token=token,
        raise_on_unexpected_status=True,
    ) as client:
        while True:
            resp = await search.asyncio_detailed(
                q="Take on Me",
                type_=[SearchTypeItem.TRACK],
                limit=1,
                client=client,
            )

            results = resp.parsed
            assert isinstance(results, SearchResponse200), (
                "results wasn't a SearchResponse200"
            )
            assert isinstance(results.tracks, PagingTrackObject), (
                "tracks wasn't a PagingTrackObject"
            )
            assert isinstance(results.tracks.items, list), "items wasn't a list"
            for t in results.tracks.items:
                assert t.name == "Take on Me", "Track name wasn't 'Take on Me'"
            break
