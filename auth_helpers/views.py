from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import urlquote


class GroupRequiredMixin(object):

    """A mixin that requires the user is a member of a particular group

    You should set 'required_group_name' on the class that uses this
    mixin to the name of the group that the user must be a member of."""

    permission_denied_template = 'auth_helpers/group_permission_denied.html'

    def dispatch(self, request, *args, **kwargs):
        login_url = reverse('account_login')
        next_path = request.path
        login_url += '?next=' + urlquote(next_path)
        if not request.user.is_authenticated():
            return HttpResponseRedirect(login_url)
        required_group = Group.objects.get(name=self.required_group_name)
        if required_group not in request.user.groups.all():
            return render(request, self.permission_denied_template, status=403)
        return super(GroupRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )
