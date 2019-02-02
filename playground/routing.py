from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
        # (http->django view is added by default)
    })
