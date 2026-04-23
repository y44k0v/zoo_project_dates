from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView,
    FormView, RedirectView,
)
from django.views.generic.dates import (
    ArchiveIndexView, YearArchiveView, MonthArchiveView,
    WeekArchiveView, DayArchiveView, TodayArchiveView,
    DateDetailView,
)

from .models import Animal
from .forms import AnimalSearchForm


# ---------------------------------------------------------------------------
# RedirectView — redirects /zoo/ to the home page
# ---------------------------------------------------------------------------
class ZooRedirectView(RedirectView):
    """
    RedirectView issues an HTTP redirect without rendering a template.
    'permanent=False' means it sends a 302 (temporary) redirect.
    'url' is the destination. You can also use 'pattern_name' to redirect
    to a named URL.
    """
    permanent = False
    pattern_name = 'animals:home'   # Redirect to the named 'home' URL


# ---------------------------------------------------------------------------
# TemplateView — Home / landing page
# ---------------------------------------------------------------------------
class HomeView(TemplateView):
    """
    TemplateView renders a fixed template with no model involved.
    We override get_context_data() to inject extra variables:
      - total_animals: total count of animals in the zoo
      - captive_count: how many were born in captivity
      - page_title: a string used in the <title> tag
    """
    template_name = 'animals/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Welcome to the Zoo'
        context['total_animals'] = Animal.objects.count()
        context['captive_count'] = Animal.objects.filter(born_in_captivity=True).count()
        context['wild_count'] = Animal.objects.filter(born_in_captivity=False).count()
        return context


# ---------------------------------------------------------------------------
# ListView — All animals
# ---------------------------------------------------------------------------
class AnimalListView(ListView):
    """
    ListView queries all Animal objects and passes them to the template
    as 'object_list' (or 'animal_list' since model = Animal).
    
    paginate_by splits results into pages of 5. In the template,
    the 'page_obj' and 'paginator' context variables are automatically
    provided by Django for building pagination links.

    Extra context added:
      - page_title: for the browser tab and heading
      - total_count: total number of animals across all pages
    """
    model = Animal
    template_name = 'animals/animal_list.html'
    context_object_name = 'animals'   # Renames 'object_list' to 'animals' in template
    paginate_by = 5

    def get_queryset(self):
        # Default ordering is defined in Meta; you can override it here.
        return Animal.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'All Animals'
        context['total_count'] = Animal.objects.count()
        return context


# ---------------------------------------------------------------------------
# DetailView — Single animal
# ---------------------------------------------------------------------------
class AnimalDetailView(DetailView):
    """
    DetailView looks up a single Animal by its pk (from the URL).
    It passes the object to the template as 'object' or 'animal'
    (because context_object_name = 'animal').

    Extra context added:
      - page_title: uses the animal's name
      - is_elderly: a derived boolean — True if the animal is over 15 years old
    """
    model = Animal
    template_name = 'animals/animal_detail.html'
    context_object_name = 'animal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.get_object()
        context['page_title'] = f'Animal: {animal.name}'
        context['is_elderly'] = animal.age > 15   # Extra derived variable
        context['weight_category'] = self._weight_category(animal.weight)
        return context

    @staticmethod
    def _weight_category(weight):
        """Returns a human-readable weight category label."""
        if weight < 10:
            return 'Small'
        elif weight < 100:
            return 'Medium'
        elif weight < 500:
            return 'Large'
        return 'Very Large'


# ---------------------------------------------------------------------------
# CreateView — Add a new animal
# ---------------------------------------------------------------------------
class AnimalCreateView(CreateView):
    """
    CreateView displays a blank ModelForm for Animal and saves a new
    instance on valid POST. After saving, it redirects to the URL
    returned by Animal.get_absolute_url() (defined in the model).

    We use 'fields' to let Django auto-generate the form from the model.

    Extra context added:
      - page_title: shown in the heading
      - form_action: a string describing what the form does (used in template)
    """
    model = Animal
    fields = ['name', 'age', 'weight', 'born_in_captivity', 'date_added']
    template_name = 'animals/animal_form.html'
    # success_url is not needed because Animal.get_absolute_url() is defined.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add New Animal'
        context['form_action'] = 'Create'
        return context


# ---------------------------------------------------------------------------
# UpdateView — Edit an existing animal
# ---------------------------------------------------------------------------
class AnimalUpdateView(UpdateView):
    """
    UpdateView is identical to CreateView but pre-fills the form with
    the existing Animal data (looked up by pk from the URL).

    Extra context added:
      - page_title: includes the animal's current name
      - form_action: tells the template this is an edit operation
    """
    model = Animal
    fields = ['name', 'age', 'weight', 'born_in_captivity', 'date_added']
    template_name = 'animals/animal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit: {self.object.name}'
        context['form_action'] = 'Update'
        return context


# ---------------------------------------------------------------------------
# DeleteView — Delete an animal
# ---------------------------------------------------------------------------
class AnimalDeleteView(DeleteView):
    """
    DeleteView shows a confirmation page on GET, then deletes the object
    and redirects to success_url on POST.

    reverse_lazy() is used instead of reverse() because at class definition
    time the URL conf may not be loaded yet.

    Extra context added:
      - page_title: warns the user which animal they are deleting
    """
    model = Animal
    template_name = 'animals/animal_confirm_delete.html'
    success_url = reverse_lazy('animals:animal-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Delete: {self.object.name}'
        return context


# ---------------------------------------------------------------------------
# FormView — Search animals
# ---------------------------------------------------------------------------
class AnimalSearchView(FormView):
    """
    FormView for searching animals. Uses GET so results are bookmarkable.
    We override get() to run the search whenever query params are present.
    form_valid() is not used since we process the form in get() directly.

    Extra context added:
      - page_title: describes the page
      - results: the QuerySet of matching animals (after form submission)
      - search_performed: boolean flag so the template knows to show results
    """
    template_name = 'animals/animal_search.html'
    form_class = AnimalSearchForm

    def get_form_kwargs(self):
        """
        By default, FormView only binds form data on POST.
        This override also binds GET params so the form validates on GET.
        """
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET' and self.request.GET:
            kwargs['data'] = self.request.GET
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Search Animals'
        context['results'] = None
        context['search_performed'] = False

        form = context['form']
        if self.request.GET and form.is_valid():
            data = form.cleaned_data
            queryset = Animal.objects.all()

            if data.get('name'):
                queryset = queryset.filter(name__icontains=data['name'])
            if data.get('min_age') is not None:
                queryset = queryset.filter(age__gte=data['min_age'])
            if data.get('max_age') is not None:
                queryset = queryset.filter(age__lte=data['max_age'])
            if data.get('min_weight') is not None:
                queryset = queryset.filter(weight__gte=data['min_weight'])
            if data.get('max_weight') is not None:
                queryset = queryset.filter(weight__lte=data['max_weight'])
            if data.get('born_in_captivity') is not None:
                queryset = queryset.filter(born_in_captivity=data['born_in_captivity'])

            context['results'] = queryset
            context['result_count'] = queryset.count()
            context['search_performed'] = True

        return context

# ---------------------------------------------------------------------------
# ArchiveIndexView — All years that have animals
# ---------------------------------------------------------------------------
class AnimalArchiveIndexView(ArchiveIndexView):
    """
    ArchiveIndexView groups all objects by year using 'date_field'.
    It provides 'date_list' in the context: a list of years that have records.
    'allow_empty=True' prevents a 404 when there are no animals.

    Extra context added:
      - page_title
      - total_years: how many distinct years have animals
    """
    model = Animal
    date_field = 'date_added'
    template_name = 'animals/animal_archive.html'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Animal Archive'
        context['total_years'] = len(context.get('date_list') or [])
        return context


# ---------------------------------------------------------------------------
# YearArchiveView — Animals added in a specific year
# ---------------------------------------------------------------------------
class AnimalYearArchiveView(YearArchiveView):
    """
    YearArchiveView filters objects whose date_field falls in the given year.
    The year is captured from the URL (e.g. /archive/2024/).
    'make_object_list=True' puts the actual objects (not just month dates)
    in the context as 'object_list'.

    Extra context added:
      - page_title: includes the year
      - animal_count: number of animals added that year
    """
    model = Animal
    date_field = 'date_added'
    template_name = 'animals/animal_archive_year.html'
    make_object_list = True
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Animals Added in {self.get_year()}'
        context['animal_count'] = len(context.get('object_list') or [])
        return context


# ---------------------------------------------------------------------------
# MonthArchiveView — Animals added in a specific month
# ---------------------------------------------------------------------------
class AnimalMonthArchiveView(MonthArchiveView):
    """
    MonthArchiveView filters by year + month.
    URL example: /archive/2024/3/
    'month_format' allows numeric months (%m) instead of the default %b (Jan).

    Extra context added:
      - page_title: includes year and month name
    """
    model = Animal
    date_field = 'date_added'
    template_name = 'animals/animal_archive_month.html'
    month_format = '%m'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_name = context['month'].strftime('%B')   # e.g. "March"
        year = self.get_year()
        context['page_title'] = f'Animals Added in {month_name} {year}'
        return context


# ---------------------------------------------------------------------------
# WeekArchiveView — Animals added in a specific week
# ---------------------------------------------------------------------------
class AnimalWeekArchiveView(WeekArchiveView):
    """
    WeekArchiveView filters by year + ISO week number.
    URL example: /archive/2024/week/12/

    Extra context added:
      - page_title: includes year and week number
    """
    model = Animal
    date_field = 'date_added'
    template_name = 'animals/animal_archive_week.html'
    week_format = '%W'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Animals Added in Week {self.get_week()}, {self.get_year()}'
        return context


# ---------------------------------------------------------------------------
# DayArchiveView — Animals added on a specific day
# ---------------------------------------------------------------------------
class AnimalDayArchiveView(DayArchiveView):
    """
    DayArchiveView filters by year + month + day.
    URL example: /archive/2024/3/15/

    Extra context added:
      - page_title: includes the full date
    """
    model = Animal
    date_field = 'date_added'
    template_name = 'animals/animal_archive_day.html'
    month_format = '%m'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day = context['day']
        context['page_title'] = f'Animals Added on {day.strftime("%B %d, %Y")}'
        return context


# ---------------------------------------------------------------------------
# TodayArchiveView — Animals added today
# ---------------------------------------------------------------------------
class AnimalTodayArchiveView(TodayArchiveView):
    """
    TodayArchiveView is exactly like DayArchiveView but automatically
    uses today's date — no date is needed in the URL.
    URL: /archive/today/

    Extra context added:
      - page_title: says "Today"
    """
    model = Animal
    date_field = 'date_added'
    template_name = 'animals/animal_archive_day.html'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Animals Added Today"
        return context


# ---------------------------------------------------------------------------
# DateDetailView — Single animal identified by date + pk
# ---------------------------------------------------------------------------
class AnimalDateDetailView(DateDetailView):
    """
    DateDetailView retrieves a single object using both its pk AND the
    date_field value from the URL. This prevents URL guessing attacks
    (the date must match the object's date_added).

    URL example: /archive/2024/3/15/7/

    Extra context added:
      - page_title: includes the animal's name
      - is_elderly: same derived boolean as in DetailView
    """
    model = Animal
    date_field = 'date_added'
    template_name = 'animals/animal_detail.html'
    context_object_name = 'animal'
    month_format = '%m'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.get_object()
        context['page_title'] = f'Animal: {animal.name} (Archive)'
        context['is_elderly'] = animal.age > 15
        return context