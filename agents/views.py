from django.views import generic
from django.shortcuts import reverse
from django.core.mail import send_mail
from leads.models import Agent
from .forms import AgentModelForm
from .mixin import OrganizerAndLoginRequiredMixin
import random


# CRUD+L - Create, Retrieve (Read), Update, Delete, and List


class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
  template_name = 'agents/agent_list.html'
  
  def get_queryset(self):
    organization = self.request.user.userprofile
    return Agent.objects.filter(organization=organization)


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
  template_name = 'agents/agent_create.html'
  form_class = AgentModelForm

  def get_success_url(self):
    return reverse('agents:agent-list')
  
  def form_valid(self, form):
    user = form.save(commit=False)
    user.is_agent = True
    user.is_organizer = False
    user.set_password(f"{random.randint(0, 1000000)}")
    user.save()
    Agent.objects.create(
      user=user, 
      organization=self.request.user.userprofile
      )
    send_mail(
      subject='Global CRM has invited you to be an Agent',
      message='You were added as an agent on Global CRM. Please come and login to start working with your assigned leads.',
      from_email='invite@globalcrm.org',
      recipient_list=[user.email]
    )
    return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
  template_name = 'agents/agent_detail.html'
  context_object_name = 'agent'

  def get_queryset(self):
    organization = self.request.user.userprofile
    return Agent.objects.filter(organization=organization)


class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
  template_name = 'agents/agent_update.html'
  form_class = AgentModelForm
  
  def get_success_url(self):
    return reverse('agents:agent-list')
  
  def get_queryset(self):
    return Agent.objects.all()


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
  template_name = 'agents/agent_delete.html'
  context_object_name = 'agent'

  def get_success_url(self):
    return reverse('agents:agent-list')

  def get_queryset(self):
    organization = self.request.user.userprofile
    return Agent.objects.filter(organization=organization)
