from __future__ import unicode_literals

import time

from django.core.cache.utils import make_template_fragment_key
from django.template import (
    Library, Node, TemplateSyntaxError, VariableDoesNotExist)

from cacheback.base import Job

register = Library()


class CacheJob(Job):
    """Class to handle asynchronous loading of all cacheback template tags"""

    def fetch(self, nodelist, context, expire_time, fragment_name, vary_on):
        """Render the node"""
        return self.nodelist.render(context)

    def expiry(self, nodelist, context, expire_time, fragment_name, vary_on):
        """When to expire"""
        return time.time() + expire_time

    def key(self, nodelist, context, expire_time, fragment_name, vary_on):
        """Make the cache key"""
        return make_template_fragment_key(fragment_name, vary_on)


class CacheNode(Node):
    def __init__(self, nodelist, expire_time_var, fragment_name, vary_on):
        self.nodelist = nodelist
        self.expire_time_var = expire_time_var
        self.fragment_name = fragment_name
        self.vary_on = vary_on

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError(
                '"cacheback" tag got an unknown variable: %r' % self.expire_time_var.var)
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError(
                '"cacheback" tag got a non-integer timeout value: %r' % expire_time)

        vary_on = [var.resolve(context) for var in self.vary_on]
        return CacheJob().get(self.nodelist, context, expire_time, self.fragment_name, vary_on)


@register.tag('cacheback')
def do_cacheback(parser, token):
    """
    This will cache the contents of a template fragment for a given amount
    of time.
    Usage::
        {% load cacheback %}
        {% cacheback [expire_time] [fragment_name] %}
            .. some expensive processing ..
        {% endcacheback %}
    This tag also supports varying by a list of arguments::
        {% load cacheback %}
        {% cacheback [expire_time] [fragment_name] [var1] [var2] .. %}
            .. some expensive processing ..
        {% endcacheback %}
    Each unique set of arguments will result in a unique cache entry.
    """
    nodelist = parser.parse(('endcacheback',))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise TemplateSyntaxError("'%r' tag requires at least 2 arguments." % tokens[0])
    return CacheNode(
        nodelist, parser.compile_filter(tokens[1]),
        tokens[2],  # fragment_name can't be a variable.
        [parser.compile_filter(t) for t in tokens[3:]],
    )
