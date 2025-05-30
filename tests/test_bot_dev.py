import pytest
from telegram import Message, Update
from telegram.ext import ContextTypes

from tracks.bot_dev import TrackBot


@pytest.fixture
def mock_bot_dev():
    """Fixture to mock the TrackBot class for testing."""

    # Create a mock instance of TrackBot
    bot = TrackBot(token="mock_token")

    return bot


async def test_start_command_sends_a_greeting_message(mock_bot_dev, mocker):
    # Given:
    # an update and a context
    mock_message = mocker.MagicMock(spec=Message)
    mock_update = mocker.MagicMock(spec=Update)
    mock_update.message = mock_message
    mock_context = mocker.MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    # When:
    # the start command is called
    await mock_bot_dev.start_command(mock_update, mock_context)

    # Then:
    # the reply_text method was called with the expected message
    mock_message.reply_text.assert_called_once_with(
        "Hi! I'm an echo bot. Send me any message and I'll repeat it back to you!"
    )
