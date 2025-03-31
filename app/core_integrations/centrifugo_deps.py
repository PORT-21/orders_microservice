import logging
from centrifuge import (
    ClientEventHandler,
    ConnectedContext,
    ConnectingContext,
    DisconnectedContext,
    ErrorContext,
    JoinContext,
    LeaveContext,
    PublicationContext,
    SubscribedContext,
    SubscribingContext,
    SubscriptionErrorContext,
    UnsubscribedContext,
    SubscriptionEventHandler,
    ServerSubscribedContext,
    ServerSubscribingContext,
    ServerUnsubscribedContext,
    ServerPublicationContext,
    ServerJoinContext,
    ServerLeaveContext,
)

from lib.utils import get_settings_value

# TODO: сделать так, чтобы logging направлял логи в openobserve, 
# если openbserve включен в настройках

class ClientEventLoggerHandler(ClientEventHandler):
    """Check out comments of ClientEventHandler methods to see when they are called."""

    async def on_connecting(self, ctx: ConnectingContext) -> None:
        logging.info("connecting: %s", ctx)

    async def on_connected(self, ctx: ConnectedContext) -> None:
        logging.info("connected: %s", ctx)

    async def on_disconnected(self, ctx: DisconnectedContext) -> None:
        logging.info("disconnected: %s", ctx)

    async def on_error(self, ctx: ErrorContext) -> None:
        logging.error("client error: %s", ctx)

    async def on_subscribed(self, ctx: ServerSubscribedContext) -> None:
        logging.info("subscribed server-side sub: %s", ctx)

    async def on_subscribing(self, ctx: ServerSubscribingContext) -> None:
        logging.info("subscribing server-side sub: %s", ctx)

    async def on_unsubscribed(self, ctx: ServerUnsubscribedContext) -> None:
        logging.info("unsubscribed from server-side sub: %s", ctx)

    async def on_publication(self, ctx: ServerPublicationContext) -> None:
        logging.info("publication from server-side sub: %s", ctx.pub.data)

    async def on_join(self, ctx: ServerJoinContext) -> None:
        logging.info("join in server-side sub: %s", ctx)

    async def on_leave(self, ctx: ServerLeaveContext) -> None:
        logging.info("leave in server-side sub: %s", ctx)


class SubscriptionEventLoggerHandler(SubscriptionEventHandler):
    """Check out comments of SubscriptionEventHandler methods to see when they are called."""

    async def on_subscribing(self, ctx: SubscribingContext) -> None:
        logging.info("subscribing: %s", ctx)

    async def on_subscribed(self, ctx: SubscribedContext) -> None:
        logging.info("subscribed: %s", ctx)

    async def on_unsubscribed(self, ctx: UnsubscribedContext) -> None:
        logging.info("unsubscribed: %s", ctx)

    async def on_publication(self, ctx: PublicationContext) -> None:
        logging.info("publication: %s", ctx.pub.data)

    async def on_join(self, ctx: JoinContext) -> None:
        logging.info("join: %s", ctx)

    async def on_leave(self, ctx: LeaveContext) -> None:
        logging.info("leave: %s", ctx)

    async def on_error(self, ctx: SubscriptionErrorContext) -> None:
        logging.error("subscription error: %s", ctx)


async def get_subscription_token(channel: str) -> str:
    # To reject subscription raise centrifuge.UnauthorizedError() exception:
    # raise centrifuge.UnauthorizedError()
    logging.info("get subscription token called for channel %s", channel)
    token = get_settings_value("CENTRIFUGO_TOKEN")
    return token


async def get_client_token() -> str:
    # To reject connection raise centrifuge.UnauthorizedError() exception:
    # raise centrifuge.UnauthorizedError()

    logging.info("get client token called")
    token = get_settings_value("CENTRIFUGO_TOKEN")
    return token
