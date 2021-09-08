from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views  import generic
from .models import Lead, Category
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
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
      queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
    else:
      queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
      # agent filter for current logged in user
      queryset = queryset.filter(agent__user=user)
    return queryset
  
  def get_context_data(self, **kwargs):
    user = self.request.user
    context = super(LeadListView, self).get_context_data(**kwargs)
    if user.is_organizer:
      queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)
      context.update({
        "unassigned_leads": queryset
      })
    return context


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


class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
  template_name = 'leads/assign_agent.html'
  form_class = AssignAgentForm

  def get_form_kwargs(self, **kwargs):
    kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
    kwargs.update({
      'request': self.request
    })
    return kwargs

  def get_success_url(self):
    return reverse('leads:lead-list')

  def form_valid(self, form):
    agent = form.cleaned_data['agent']
    lead = Lead.objects.get(id=self.kwargs['pk'])
    lead.agent = agent
    lead.save()
    return super(AssignAgentView, self).form_valid(form)


class CategoryListView(OrganizerAndLoginRequiredMixin, generic.ListView):
  template_name = 'leads/category_list.html'
  context_object_name = 'category_list'

  def get_context_data(self, **kwargs):
    context = super(CategoryListView, self).get_context_data(**kwargs)
    user = self.request.user
    if user.is_organizer:
      queryset = Lead.objects.filter(organization=user.userprofile)
    else:
      queryset = Lead.objects.filter(organization=user.agent.organization)

    context.update({
      'unassigned_lead_count': queryset.filter(category__isnull=True).count()
    })
    return context

  def get_queryset(self):
    user = self.request.user
    if user.is_organizer:
      queryset = Category.objects.filter(organization=user.userprofile)
    else:
      queryset = Category.objects.filter(organization=user.agent.organization)
    return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = 'leads/category_detail.html'
  context_object_name = 'category'

  # def get_context_data(self, **kwargs):
  #   context = super(CategoryDetailView, self).get_context_data(**kwargs)
  #   leads = self.get_object().Leads.all()

  #   context.update({
  #     'leads': leads,
  #   })
  #   return context

  def get_queryset(self):
    user = self.request.user
    if user.is_organizer:
      queryset = Category.objects.filter(organization=user.userprofile)
    else:
      queryset = Category.objects.filter(organization=user.agent.organization)
    return queryset


  def get_queryset(self):
    user = self.request.user
    # Initial queryset of leads for an organizer
    if user.is_organizer:
      queryset = Category.objects.filter(organization=user.userprofile)
    else:
      queryset = Category.objects.filter(organization=user.agent.organization)
    return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
  template_name = 'leads/lead_category_update.html'
  form_class = LeadCategoryUpdateForm

  def get_queryset(self):
    user = self.request.user
    if user.is_organizer:
      queryset = Lead.objects.filter(organization=user.userprofile)
    else:
      queryset = Lead.objects.filter(organization=user.agent.organization)
    return queryset

  def get_success_url(self):
    return reverse('leads:lead-detail', kwargs={'pk': self.get_object().id})
