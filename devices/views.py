
# import urllib, csv
# from datetime import datetime

# from django.forms.formsets import formset_factory
# from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
# from django.http import HttpResponse

# from django.core.files import File
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.contrib.admin.views.decorators import staff_member_required

# from django.db.models import Q, F
# from django.utils import simplejson

from devices.models import Phone,Switch,AP,UPS
from django.shortcuts import get_object_or_404,render_to_response,render, redirect
from django.http import HttpResponseRedirect, HttpResponse 
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone



def index(request,model):

	print model
	if (model == "switches"):
		render_to_response("devices/switch_list.html", {
        	"objects": Switch.objects.all(),
			"model": model,
			"tableTitle": "Switches",
   	 	}, context_instance=RequestContext(request))
	elif (model == "phones"):
		context = {"objects": Phone.objects.all(),
		"model": model}
		return render(request, "devices/template.html",context)
	elif(model == "AP"):
		context = {"objects":AP.objects.all(),
		"model": model}
		return render(request, "devices/template.html",context)
	elif (model == "UPS"):
		context = {"objects":UPS.objects.all(),
		"model": model}
		return render(request, "devices/template.html",context)
	return redirect("devices_index","switches")
	# context = {"objects": Switch.objects.all()}
	# return render(request, "devices/index.html", context)

    # return HttpResponse("THIS IS NOT WORKING??????")



# # display a list of all the objects of a model
# # either a switch, a phone, a AP, or a UPS
# # default is Switch list view
# def model_list(request, model):
    
#     if (model == "Switches"):
#     	return render_to_response("devices/index.html", {
#         	"objects": Switch.objects.all(),
# 		"modelName": model,
# 		"tableTitle": "Switches",
#    	 }, context_instance=RequestContext(request))
#     elif (model == "Phones"):
#     	return render_to_response("devices/phone_list.html", {
#         	"objects": Phone.objects.all().order_by('name'),
# 		"modelName": model,
# 		"tableTitle": "Phones",
#    	 }, context_instance=RequestContext(request))
#     elif (model == "APs"):
#     	return render_to_response("devices/ap_list.html", {
#     		"objects": AP.objects.all().order_by("serialno"),
#     	"modelName": model,
#     	"tableTitle": "AP",
#     }, context_instance=RequestContext(request))
#     elif (model == "UPSes"):
#     	return render_to_response("devices/ups_list.html", {
#     		"objects": UPS.objects.all(),
#     	"modelName": model,
#     	"tableTitle": "UPS",
#     }, context_instance=RequestContext(request))
#     return redirect("devices_model_list", 'Switches')


