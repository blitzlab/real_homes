import unique_key
from django.shortcuts import render,redirect
from .forms import PropertyForm, GalleryForm
from message.forms import MessageForm
from .models import Property, Gallery
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from sorl.thumbnail import ImageField, get_thumbnail
from .filters import PropertyFilter
from django.core import serializers
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.

# class AddListingView(FormView):
#
#     template_name = 'listings/add_listing.html'
#     form_class = PropertyForm
#     success_url = '/listings/new-listing'
#
#     # def post(self, request, *args, **kwargs):
#     #     form_class = self.get_form_class()
#     #     form = self.get_form(form_class)
#     #     files = request.FILES.getlist('gallery')
#     #     if form.is_valid():
#     #         fs = FileSystemStorage()
#     #         for f in files:
#     #             fs.save(f.name, f)
#     #         return self.form_valid(form)
#     #
#     # def form_valid(self, form):
#     #     listing_form = form.save(commit=False)
#     #     listing_form.agent = self.request.user
#     #     listing_form = form.save()
#     #     return super().form_valid(form)
#     def form_valid(self, form):
#         # listing_form = form.save(commit=False)
#         object = form.save(commit=False)
#         object.agent = self.request.user
#         form.save()
#         if self.request.FILES:
#             for afile in self.request.FILES.getlist('gallery'):
#                 img = object.images.create(image=afile)
#         # listing_form = form.save()
#         return super().form_valid(form)
def index_view(request):
    filter_form = PropertyFilter()
    if request.GET.get("submitsearch"):
        filter_query = PropertyFilter(request.GET, queryset=Property.objects.all())
        print("New Search")
        return render(request, "listings/filtered_list.html", {"filtered_properties":filter_query})
    context = {"filter_form": filter_form}
    return render(request, "index.html", context)


def create_listing_view(request):
    property_form = PropertyForm()
    gallery_form = GalleryForm()

    if request.method == "POST" or None:

        form = PropertyForm(request.POST, request.FILES)
        gallery_form = GalleryForm(request.FILES)
        # other_data = MemberDataForm(data = request.POST)
        #
        if form.is_valid() and gallery_form.is_valid():
            save_form = form.save(commit = False)
            save_form.agent = request.user
            save_form.save()
            for afile in request.FILES.getlist('image'):
                # resized_image=get_thumbnail(afile, '596x446', quality=99, format='JPEG')
                Gallery.objects.create(property=save_form, image=afile)
                messages.success(request, "Listing successfully submitted")

        else:
            property_form = PropertyForm(request.POST, request.FILES)
            gallery_form = GalleryForm(request.FILES)
            # gallery_form = GalleryForm(request.FILES)

    return render(request, "listings/add_listing.html", {"form1":property_form, "form2":gallery_form})


class ListingsView(ListView):
    model = Property
    paginate_by = 4
    context_object_name = 'properties'
    template_name = "listings/property_list.html"

    queryset = model.objects.filter(status="active").order_by('-published_on')
    # data = serializers.serialize("xml", SomeModel.objects.all())

def handle_property_detail_and_contact(request, slug):
    property = Property.objects.get(slug=slug)
    contact_form = MessageForm()
    gallery = Gallery.objects.filter(property=property)

    if request.method == "POST" or None:
        if request.user.is_authenticated:
            form = MessageForm(request.POST)

            if form.is_valid():
                form = form.save(commit=False)
                form.property = property
                form.sender = request.user
                form.consumer = property.agent
                form.type = "request"
                form.conversation_id = unique_key.gen_unique_key()
                form.save()
                # Send notification message Here
                messages.success(request, "Message sent to successful", extra_tags="message_sent")
            else:
                messages.error(request, "Message not sent")
                contact_form = MessageForm(request.POST)
        else:
            messages.error(request, "Please login to send message")
    context = {
        "property":property,
        "form": contact_form,
        "images":gallery
    }
    return render(request, "listings/property_detail.html", context)


class PropertyDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Property
    success_url = reverse_lazy('account:account')
    success_message = "Property Deleted Successfully"


class PropertyUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Property
    fields = [
        "address", "description", "category", "type", "price", "city",
        "featured_image", "bedrooms", "bathrooms", "garage", "area_size"
    ]
    success_message = "Property Updated Successfully"
    template_name = 'listings/property_update.html'
    extra_tags ="property_updated"

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message, extra_tags=self.extra_tags)
        return response

    def get_success_url(self):
        return reverse("listings:listing_detail", kwargs={'slug': self.object.slug})


def get_xml(request):
    if request.is_ajax or None:
        query_set = Property.objects.all()
        xml = render_to_string('listings/xml_.xml', {'query_set': query_set})

        print(xml)


    return HttpResponse(xml, content_type="application/xml")
