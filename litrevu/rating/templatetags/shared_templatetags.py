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


@register.filter(name="classes")
def replace_classes(field, classes):
    field.widget.attrs["class"] = classes
    return field
