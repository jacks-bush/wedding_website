from django.shortcuts import render
from wedding_website.forms import SignUpForm, SearchForm, RSVPForm
from django.http import HttpResponse
from wedding_database.models import Invitee, Group
from django.forms import formset_factory

def login(request):
	return render(request, 'login.html')
	
def sign_up(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			return HttpResponse("You did it!")
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})
	
# def contact(request):
	# if request.method == 'POST':
		# form = ContactForm(request.POST)
		# if form.is_valid():
			# cd = form.cleaned_data
			# send_mail(cd['subject'], cd['message'], cd.get('email', 'noreply@example.com'), ['siteowner@example.com'],)
			# return HttpResponseRedirect('/contact/thanks')
	# else:
		# form = ContactForm()
	# return render(request, 'contact_form.html', {'form': form})
	
def base(request):
	return render(request, 'base.html')
	
def home(request):
	return render(request, 'home.html')
	
def about(request):
	return render(request, 'about.html')
	
def wedding_info(request):
	return render(request, 'weddinginfo.html')

def rsvp(request):
	if request.method == 'POST':
		if 'search' in request.POST:
			form = SearchForm(request.POST)
			if form.is_valid():
				first_name = form.cleaned_data['first_name']
				last_name = form.cleaned_data['last_name']
				try:
					group = Invitee.objects.get(first_name__iexact = str(first_name), last_name__iexact = str(last_name))
					coming = Group.objects.get(group_name = group.group)
					form.fields['first_name'].initial = first_name
					form.fields['last_name'].initial = last_name
					invitees = coming.invitee_set.all()
				except:
					from django.forms.utils import ErrorList
					form.add_error('first_name', u"No records were found with that first and last name. Check yo spelling bruh.")
					return render(request, 'rsvp.html', {'form': form})
				return render(request, 'rsvp.html', {'form' : form, 'group_name' : coming.group_name, 'num_coming' : coming.num_coming, 'num_invited' : coming.num_invited, 'invitees' : invitees})
			
			else:
				form = SearchForm()
				return render(request, 'rsvp.html', {'form' : form})
		else:
			confirmed_list = list(request.POST.getlist('checkbox'))
			group_name = request.POST.get('group_name')
			group = Group.objects.get(group_name = group_name)
			group.confirmed = True
			group.num_coming = len(confirmed_list)
			group.save()
			for person in confirmed_list:
				person_list = person.split()
				invitee = Invitee.objects.get(first_name__iexact = person_list[0], last_name__iexact = person_list[1])
				invitee.confirmed = True
				invitee.save()
				
			#print str(confirmed_list) + " " + str(group_name) + "length of list: " + str(len(list(confirmed_list)))
			return render(request, 'rsvp-thanks.html')
	else:
		form = SearchForm()
	return render(request, 'rsvp.html', {'form' : form})
	
	
def rsvp_thanks(request):
	return render(request, 'rsvp-thanks.html')

	
# def rsvp(request):
	# if request.method == 'POST':
		# form = SearchForm(request.POST)
		# if form.is_valid():
			# first_name = form.cleaned_data['first_name']
			# last_name = form.cleaned_data['last_name']
			# try:
				# group = Invitee.objects.get(first_name__iexact = str(first_name), last_name__iexact = str(last_name))
				# coming = Group.objects.get(group_name = group.group)
				# form.fields['first_name'].initial = first_name
				# form.fields['last_name'].initial = last_name
				# invitees = coming.invitee_set.all()
			# except:
				# from django.forms.util import ErrorList
				# form.add_error('first_name', u"No records were found with that first and last name. Check yo spelling bruh.")
				# return render(request, 'rsvp.html', {'form': form})
			# return render(request, 'rsvp.html', {'form' : form, 'group_name' : coming.group_name, 'num_coming' : coming.num_coming, 'num_invited' : coming.num_invited, 'invitees' : invitees})
		# else:
			# form = SearchForm()
			# return render(request, 'rsvp.html', {'form' : form})
	# else:
		# form = SearchForm()
	# return render(request, 'rsvp.html', {'form' : form})
	
def registry(request):
	return render(request, 'registry.html')
	
def contact(request):
	return render(request, 'contact.html')
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	