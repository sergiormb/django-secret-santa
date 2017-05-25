"""Views for the base app
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django_tables2 import RequestConfig

from base.models import Inscription, Group
from base.tables import InscriptionTable, InscriptionClosedTable, GroupTable
from base.forms import UserCreationForm


def home(request):
    """Initial landing page view
    Args:
        request (request): Request
    Returns:
        Returns a page
    """
    return render(request, 'base/home.html')


def signup(request):
    """Registration page
    Args:
        request (request): Request
    Returns:
        Returns a registration page
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('inscription_list')
    else:
        form = UserCreationForm()
    return render(request, 'base/signup.html', {'form': form})


@login_required
def inscription_list(request):
    """List of inscriptions
    Args:
        request (request): Request
    Returns:
        Returns a page with a list of closed and unopened
    """
    inscriptions_closed = Inscription.objects.filter(
        user=request.user).exclude(give_gift__isnull=True)
    table_closed = InscriptionClosedTable(inscriptions_closed)
    table = InscriptionTable(Inscription.objects.filter(
        user=request.user).exclude(give_gift__isnull=False))
    RequestConfig(request).configure(table)
    RequestConfig(request).configure(table_closed)
    return render(
        request,
        'base/inscriptions.html',
        {'table': table, 'table_closed': table_closed}
    )


@login_required
def group_close(request, pk):
    """Close the group
    Args:
        request (request): Request
        pk (int): Group identifier
    Returns:
        Redirects to group page
    """
    group = get_object_or_404(Group, pk=pk)
    if len(group.users) > 2:
        group.close_group()
        messages.success(request, 'Group successfully closed')
    else:
        messages.error(request, 'You need more participants')
    return redirect('group_detail', pk=pk)


class LoginRequiredSSMixin(LoginRequiredMixin):
    """Mixin Login required Secret Santa
    Attributes:
        login_url (str): Page login
        redirect_field_name (str): Field name to redirect
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class GroupListView(LoginRequiredSSMixin, ListView):
    """View class showing group list
    Attributes:
        model (Model): Model to list
    """
    model = Group

    def get_context_data(self, **kwargs):
        """Summary
        Args:
            **kwargs: arguments
        Returns:
            context: Dictionary to show
        """
        context = super(GroupListView, self).get_context_data(**kwargs)
        table = GroupTable(context.get('object_list'))
        RequestConfig(self.request).configure(table)
        context.update({'table': table})
        return context

    def get_queryset(self):
        """Custom Queryset

        Returns:
            List groups
        """
        return Group.objects.filter(status='open')


class GroupDetailView(LoginRequiredSSMixin, DetailView):
    """View class to display in detail a group

    Attributes:
        model (Model): Model to view
    """
    model = Group


class GroupCreateView(LoginRequiredSSMixin, CreateView):
    """Class of view to create a group

    Attributes:
        fields (list): Fields to show
        model (Model): Model to create
        success_url (str): Url to redirect
    """
    model = Group
    fields = ['name', 'end_date']
    success_url = '/groups'

    def get_initial(self):
        """Initial data in the form

        Returns:
            Initial data
        """
        return {
            'user': self.request.user,
        }

    def form_valid(self, form):
        """Validate form

        Args:
            form (Form): Form create

        Returns:
            Validate from
        """
        user = self.request.user
        form.instance.creator = user
        redirect = form.cleaned_data.get('next')
        if redirect:
            self.success_url = redirect
        return super(GroupCreateView, self).form_valid(form)


class InscriptionCreate(LoginRequiredSSMixin, CreateView):
    """Class of view to create a inscription

    Attributes:
        fields (list): Fields to show
        model (Model): Model to create
        success_url (str): Url to redirect
    """
    model = Inscription
    fields = ['preferences']
    success_url = '/inscriptions'

    def get_initial(self):
        """Initial data in the form

        Returns:
            TYPE: Description
        """
        group = get_object_or_404(Group, pk=self.kwargs.get('pk'))
        return {
            'group': group,
            'user': self.request.user,
        }

    def form_valid(self, form):
        """Validate form

        Args:
            form (Form): Form create

        Returns:
            Validate from
        """
        user = self.request.user
        form.instance.user = user
        group = get_object_or_404(Group, pk=self.kwargs.get('pk'))
        form.instance.group = group
        redirect = form.cleaned_data.get('next')
        if redirect:
            self.success_url = redirect
        return super(InscriptionCreate, self).form_valid(form)
