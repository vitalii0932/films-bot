import pytest
from unittest.mock import AsyncMock, patch

from handlers.user import process_movie_search

@pytest.mark.asyncio
@patch('handlers.user.search_movie', new_callable=AsyncMock)
async def test_process_movie_search(mock_search):
    mock_search.return_value = [
        {'id': 1, 'title': 'Movie', 'release_date': '1980-01-01'}
    ]

    message = AsyncMock()
    message.text = 'Movie'
    message.answer = AsyncMock()

    state = AsyncMock()
    state.clear = AsyncMock()

    await process_movie_search(message, state)

    message.answer.assert_called()
    state.clear.assert_called()