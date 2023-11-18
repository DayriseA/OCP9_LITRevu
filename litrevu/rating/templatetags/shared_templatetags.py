from django import template

register = template.Library()


@register.filter()
def add_classes(bound_field, new_classes):
    """Return the field with the given CSS classes added to its widget."""
    field = bound_field.field
    old_classes = field.widget.attrs.get("class", "")
    if old_classes:
        classes = f"{old_classes} {new_classes}"
    else:
        classes = new_classes
    field.widget.attrs["class"] = classes
    return bound_field


@register.filter()
def label_with_classes(field, classes):
    """
    Apply this filter to a field.
    Return the label with the given CSS classes, not the field itself.
    """
    return field.label_tag(attrs={"class": classes})


# Not used for now
# @register.filter(name="classes")
# def replace_classes(field, classes):
#     """Return the field with the given CSS classes instead of its own."""
#     field.widget.attrs["class"] = classes
#     return field
