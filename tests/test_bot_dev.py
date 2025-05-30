import pytest
from telegram import Message, Update
from telegram.ext import ContextTypes, Application

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


async def test_application_routing_echo(mocker):
    """Test that the application routes commands correctly."""
    # Given:
    mock_bot_dev = TrackBot(token="mock_token")
    mock_bot_dev.start_command = mocker.AsyncMock()
    mock_bot_dev.echo_command = mocker.AsyncMock()
    mock_bot_dev.error_handler = mocker.AsyncMock()
    application = mock_bot_dev._get_application()
    application._initialized = True

    # When:
    # the application processes an update with a message
    await application.process_update(
        Update(
            message=Message(text="start", message_id=1, date=None, chat=None),
            update_id=1,
        )
    )

    # Then:
    # the echo command was called
    mock_bot_dev.echo_command.assert_called_once()


# NOTE: the start_command cannot be tested easily because it requires additional fields to be set correctly for messages with commands.


async def test_application_handles_error(mocker):
    """Test that the application routes commands correctly."""
    # Given:
    mock_bot_dev = TrackBot(token="mock_token")
    mock_bot_dev.start_command = mocker.AsyncMock()

    # If:
    # the echo command raises an exception

    mock_bot_dev.echo_command = mocker.AsyncMock(side_effect=Exception("Test error"))
    mock_bot_dev.error_handler = mocker.AsyncMock()
    application = mock_bot_dev._get_application()
    application._initialized = True

    # When:
    # the application processes an update which causes an error
    await application.process_update(
        Update(
            message=Message(text="start", message_id=1, date=None, chat=None),
            update_id=1,
        )
    )

    # Then:
    # the echo command was called
    # the error handler was called
    mock_bot_dev.echo_command.assert_called_once()
    mock_bot_dev.error_handler.assert_called_once()
