import typing

if typing.TYPE_CHECKING:
    pass


class Provider:
    name = "provider"

    async def register(self, app: "FastAPIAdmin"):
        setattr(app, self.name, self)
