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


@pytest.fixture
def mock_update(mocker):
    """Fixture to create a mock Update object."""
    mock_update = mocker.MagicMock(spec=Update)
    mock_message = mocker.MagicMock(spec=Message)
    mock_update.message = mock_message

    return mock_update


@pytest.fixture
def mock_context(mocker):
    """Fixture to create a mock ContextTypes object."""
    return mocker.MagicMock(spec=ContextTypes.DEFAULT_TYPE)


async def test_start_command_sends_a_greeting_message(
    mock_bot_dev, mock_update, mock_context
):

    # When:
    # the start command is called
    await mock_bot_dev.start_command(mock_update, mock_context)

    # Then:
    # the reply_text method was called with the expected message
    mock_update.message.reply_text.assert_called_once_with(
        "Hi! I'm an echo bot. Send me any message and I'll repeat it back to you!"
    )


async def test_echo_command_repeats_user_message(
    mock_bot_dev, mock_update, mock_context
):
    # Given:
    # a user message
    mock_update.message.text = "Hello, world!"

    # When:
    # the echo command is called
    await mock_bot_dev.echo_command(mock_update, mock_context)

    # Then:
    # the reply_text method was called with the user message
    mock_update.message.reply_text.assert_called_once_with("Hello, world!")
