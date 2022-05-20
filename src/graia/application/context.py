from contextvars import ContextVar
from contextlib import contextmanager

from graia.application.entities import UploadMethods

application = ContextVar("application")
event = ContextVar("event")
event_loop = ContextVar("event_loop")
broadcast = ContextVar("broadcast")

# for image
# sendGroupMessage 等发送message的指令将set该上下文条目.
image_method = ContextVar("image_method")


@contextmanager
def enter_message_send_context(method: UploadMethods):
    t = image_method.set(method)
    yield
    image_method.reset(t)


@contextmanager
def enter_context(app=None, event_i=None):
    t3 = None
    t4 = None

    t1 = None
    if app:
        t1 = application.set(app)
        t3 = event_loop.set(app.broadcast.loop)
        t4 = broadcast.set(app.broadcast)
    t2 = event.set(event_i) if event_i else None
    yield
    try:
        if t1:
            application.reset(t1)

        if all([t2, t3, t4]):
            event.reset(t2)
            event_loop.reset(t3)
            broadcast.reset(t4)
    except ValueError:  # 在测试 Scheduler 时发现的问题...辣鸡 Python!
        pass
