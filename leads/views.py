from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Agent, Lead, User
from .forms import LeadForm, LeadModelForm


class LandingPageView(TemplateView):
  template_name = 'landing.html'


class LeadListView(ListView):
  template_name = 'leads/lead_list.html'
  queryset = Lead.objects.all()
  context_object_name = 'leads'


class LeadDetailView(DetailView):
  template_name = 'leads/lead_detail.html'
  queryset = Lead.objects.all()
  context_object_name = 'lead'


class LeadCreateView(CreateView):
  template_name = 'leads/lead_create.html'
  form_class = LeadModelForm
  
  def get_success_url(self):
    return reverse('leads:lead-list')


class LeadUpdateView(UpdateView):
  template_name = 'leads/lead_update.html'
  queryset = Lead.objects.all()
  form_class = LeadModelForm

  def get_success_url(self):
    return reverse('leads:lead-list')


class LeadDeleteView(DeleteView):
  template_name = 'leads/lead_delete.html'
  queryset = Lead.objects.all()

  def get_success_url(self):
    return reverse('leads:lead-list')
