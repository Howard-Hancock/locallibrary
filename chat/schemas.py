from ninja import ModelSchema
from ninja import Schema
from chat.models import Message, Room
from datetime import timedelta
from typing import Annotated
from ninja import FilterLookup, FilterSchema, Query
from django.utils import timezone
from django.db.models import Q
class MessageIn(ModelSchema):
    class Meta:
        model = Message
        fields = ["content"]

class Conflict(Schema):
    message: str
    existing_id: int

class RoomOut(ModelSchema):
    class Meta:
        model = Room
        fields = ["id", "name", "topic", "created_at"]

class RoomIn(ModelSchema):
    class Meta:
        model = Room
        fields = ["name", "topic"]

class RoomFilter(FilterSchema):
    search: Annotated[str | None, FilterLookup("name__icontains")] = None
    topic: Annotated[str | None, FilterLookup("topic__icontains")] = None
    recent: bool | None = None

    def filter_recent(self, value: bool) -> Q:
        week_ago = timezone.now() - timedelta(days=7)
        return Q(created_at__gte=week_ago) if value else Q(created_at__lt=week_ago)

class MessageOut(ModelSchema):
    room: RoomOut

    class Meta:
        model = Message
        fields = ["id", "author", "content", "created_at"]
