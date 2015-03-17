# This is the url pattern match and redirect file

from django.conf.urls import patterns, url
from devices import views


urlpatterns = patterns('', 

	# 
	# url(r'\0', views.index, name = "index"),
	url(r'^(?P<model>\w+)/$', views.index, name='devices_index'),

	)



# 



# urlpatterns = patterns('',

# 	# url(r'^$', views.IndexView.as_view(), name = "index")
# 	# url(r'^$', views.model_list, name = "model_list")
# 	# url(r"^(?P<model>\w+)/$", 'views.model_list', name='devices_model_list'),
# 	)