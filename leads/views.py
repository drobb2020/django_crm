from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views  import generic
from .models import Lead
from .forms import LeadModelForm, CustomUserCreationForm
from agents.mixin import OrganizerAndLoginRequiredMixin


# CRUD+L - Create, Retrieve (Read), Update, Delete, and List


class SignupView(generic.CreateView):
  template_name = 'registration/signup.html'
  form_class = CustomUserCreationForm

  def get_success_url(self):
    return reverse('login')


class LandingPageView(generic.TemplateView):
  template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
  template_name = 'leads/lead_list.html'
  context_object_name = 'leads'

  def get_queryset(self):
    user = self.request.user
    # Initial queryset of leads for an organizer
    if user.is_organizer:
      queryset = Lead.objects.filter(organization=user.userprofile)
    else:
      queryset = Lead.objects.filter(organization=user.agent.organization)
      # agent filter for current logged in user
      queryset = queryset.filter(agent__user=user)
    return queryset


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = 'leads/lead_detail.html'
  context_object_name = 'lead'

  def get_queryset(self):
    user = self.request.user
    # Initial queryset of leads for an organizer
    if user.is_organizer:
      queryset = Lead.objects.filter(organization=user.userprofile)
    else:
      queryset = Lead.objects.filter(organization=user.agent.organization)
      # agent filter for current logged in user
      queryset = queryset.filter(agent__user=user)
    return queryset


class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
  template_name = 'leads/lead_create.html'
  form_class = LeadModelForm
  
  def get_success_url(self):
    return reverse('leads:lead-list')

  def form_valid(self, form):
    # TODO send email
    send_mail(
      subject='A lead has been created', 
      message='Please go to the CRM site to see details of the new lead', from_email='admin@test.com', 
      recipient_list=['test@test.com']
      )
    return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
  template_name = 'leads/lead_update.html'
  form_class = LeadModelForm

  def get_queryset(self):
    user = self.request.user
    return Lead.objects.filter(organization=user.userprofile)

  def get_success_url(self):
    return reverse('leads:lead-list')


class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
  template_name = 'leads/lead_delete.html'
  
  def get_queryset(self):
    user = self.request.user
    return Lead.objects.filter(organization=user.userprofile)

  def get_success_url(self):
    return reverse('leads:lead-list')
