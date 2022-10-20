from typing import Any, Optional

from baserow_enterprise.models import Team
from baserow_enterprise.signals import team_created

from baserow.core.exceptions import TrashItemDoesNotExist
from baserow.core.models import TrashEntry
from baserow.core.trash.registries import TrashableItemType


class TeamTrashableItemType(TrashableItemType):
    type = "team"
    model_class = Team

    def get_parent(self, trashed_item: Any, parent_id: int) -> Optional[Any]:
        return trashed_item.group

    def get_name(self, trashed_item: Team) -> str:
        return trashed_item.name

    def restore(self, trashed_item: Team, trash_entry: TrashEntry):
        super().restore(trashed_item, trash_entry)
        team_created.send(
            self,
            team=trashed_item,
            user=None,
        )

    def permanently_delete_item(self, trashed_item: Team, trash_item_lookup_cache=None):
        """Deletes the team."""

        try:
            Team.objects_and_trash.get(id=trashed_item.id)
        except Team.DoesNotExist:
            raise TrashItemDoesNotExist()

        trashed_item.delete()