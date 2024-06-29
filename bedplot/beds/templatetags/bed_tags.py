"""
Currently unneccessary override of neapolitan's object_list template tag.
"""

from django import template
from django.utils.safestring import mark_safe

from neapolitan.views import Role
from neapolitan.templatetags.neapolitan import action_links

register = template.Library()


@register.inclusion_tag("neapolitan/partial/list.html")
def bed_listings(objects, view):
    """
    Renders a list of objects with the given fields.

    Inclusion tag usage::

        {% object_list objects view %}

    Template: ``neapolitan/partial/list.html`` — Will render a table of objects
    with links to view, edit, and delete views.
    """

    fields = view.fields
    headers = [objects[0]._meta.get_field(f).verbose_name for f in fields]
    object_list = [
        {
            "object": object,
            "fields": [
                object._meta.get_field(f).value_to_string(object) for f in fields
            ],
            "actions": action_links(view, object),
        }
        for object in objects
    ]
    return {
        "headers": headers,
        "object_list": object_list,
    }
