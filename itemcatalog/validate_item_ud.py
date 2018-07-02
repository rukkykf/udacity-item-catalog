class ValidateItemUD():

    """Validate the editing and deleting of items.

    There are two goals with this validation.
    First, to ensure the user making the changes is the creator of the item.
    Second, to ensure the item being changed, is the item the user wanted to change.
    This way simply changing the action attribute on the html form
    won't lead to a valid update.

    """

    def __init__(self):
        self.item = None
        self.user = None

    def is_valid(self, newitem):
        error = None

        if self.item is None or self.user is None:
            return error

        if self.item.id != newitem.id:
            error = "You are trying to edit the wrong item"

        if self.user.id != newitem.user.id:
            error = "You are not authorlized to edit this item"

        return error
