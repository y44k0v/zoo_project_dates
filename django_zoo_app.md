# Django Zoo Animal Management App — Complete Guide

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Setup](#2-project-setup)
3. [Project Structure](#3-project-structure)
4. [Django Settings](#4-django-settings)
5. [The Animal Model](#5-the-animal-model)
6. [URL Configuration](#6-url-configuration)
7. [Generic Class-Based Views — Complete Reference](#7-generic-class-based-views--complete-reference)
8. [All Views Implemented](#8-all-views-implemented)
9. [Templates](#9-templates)
10. [Running and Testing the App](#10-running-and-testing-the-app)
11. [Key Concepts Summary](#11-key-concepts-summary)

---

## 1. Project Overview

This guide walks you through building a Django application to manage animals in a zoo. The app supports full **CRUD** operations (Create, Read, Update, Delete) and **search** functionality across all animal attributes. Every page includes a navigation bar and uses plain, unstyled HTML.

### Animal Attributes

| Field              | Type         | Description                              |
|--------------------|--------------|------------------------------------------|
| `name`             | `CharField`  | The animal's name                        |
| `age`              | `IntegerField` | Age in years                           |
| `weight`           | `FloatField` | Weight in kilograms                      |
| `born_in_captivity`| `BooleanField` | Whether the animal was born in captivity |

### Django Generic Class-Based Views Used

Every generic CBV available in `django.views.generic` is used in this project:

| View Class         | Purpose                                  |
|--------------------|------------------------------------------|
| `TemplateView`     | Home / landing page                      |
| `ListView`         | List all animals                         |
| `DetailView`       | View a single animal                     |
| `CreateView`       | Add a new animal                         |
| `UpdateView`       | Edit an existing animal                  |
| `DeleteView`       | Delete an animal                         |
| `FormView`         | Search animals by attributes             |
| `ArchiveIndexView` | Archive index of animals by year         |
| `YearArchiveView`  | Animals added in a specific year         |
| `MonthArchiveView` | Animals added in a specific month        |
| `WeekArchiveView`  | Animals added in a specific week         |
| `DayArchiveView`   | Animals added on a specific day          |
| `TodayArchiveView` | Animals added today                      |
| `DateDetailView`   | Date-based detail view of one animal     |
| `RedirectView`     | Redirect from old/shortcut URLs          |

---

## 2. Project Setup

### Step 1 — Create a Virtual Environment and Install Django

```bash
# Create a project directory
mkdir zoo_project
cd zoo_project

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install Django
pip install django
```

### Step 2 — Create the Django Project and App

```bash
# Create the Django project (named 'zoo_site')
django-admin startproject zoo_site .

# Create the Django app (named 'animals')
python manage.py startapp animals
```

> **Note:** The `.` at the end of `startproject` places `manage.py` in the current directory rather than creating a nested folder.

### Step 3 — Register the App

Open `zoo_site/settings.py` and add `'animals'` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'animals',   # <-- Add this line
]
```

---

## 3. Project Structure

After setup, your project should look like this:

```
zoo_project/
├── manage.py
├── zoo_site/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── animals/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py          ← You will create this
    ├── models.py
    ├── urls.py           ← You will create this
    ├── views.py
    ├── migrations/
    │   └── __init__.py
    └── templates/
        └── animals/
            ├── base.html               ← Shared layout with navbar
            ├── home.html               ← TemplateView
            ├── animal_list.html        ← ListView
            ├── animal_detail.html      ← DetailView
            ├── animal_form.html        ← CreateView / UpdateView
            ├── animal_confirm_delete.html ← DeleteView
            ├── animal_search.html      ← FormView (form + results on same page)
            ├── animal_archive.html     ← ArchiveIndexView
            ├── animal_archive_year.html  ← YearArchiveView
            ├── animal_archive_month.html ← MonthArchiveView
            ├── animal_archive_week.html  ← WeekArchiveView
            ├── animal_archive_day.html   ← DayArchiveView
            └── animal_detail_date.html   ← DateDetailView
```

---

## 4. Django Settings

### Add Template Directory

In `zoo_site/settings.py`, ensure the `TEMPLATES` setting has `APP_DIRS` set to `True`. This tells Django to look for templates inside each app's `templates/` folder:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],        # You can add project-wide template dirs here
        'APP_DIRS': True,  # Looks in each app's templates/ folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

---

## 5. The Animal Model

### `animals/models.py`

```python
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Animal(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(help_text="Age in years")
    weight = models.FloatField(help_text="Weight in kilograms")
    born_in_captivity = models.BooleanField(default=False)

    # date_added is required for all date-based archive views.
    # It records when the animal was added to the system.
    date_added = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['name']   # Default queryset ordering: alphabetical by name

    def __str__(self):
        return f"{self.name} (age {self.age})"

    def get_absolute_url(self):
        # Returns the canonical URL for a single animal's detail page.
        # Django's CreateView and UpdateView use this after a successful save.
        return reverse('animals:animal-detail', kwargs={'pk': self.pk})
```

**Why `date_added`?** Django's date-based generic views (`ArchiveIndexView`, `YearArchiveView`, etc.) require a `DateField` or `DateTimeField` on the model. We use `date_added` for this purpose.

### Create and Apply Migrations

```bash
python manage.py makemigrations animals
python manage.py migrate
```

### Register in Admin

In `animals/admin.py`:

```python
from django.contrib import admin
from .models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'weight', 'born_in_captivity', 'date_added']
    list_filter = ['born_in_captivity', 'date_added']
    search_fields = ['name']
```

---

## 6. URL Configuration

### Project URLs — `zoo_site/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('animals.urls', namespace='animals')),
]
```

### App URLs — `animals/urls.py`

Create this file inside the `animals/` directory:

```python
from django.urls import path
from . import views

app_name = 'animals'   # Enables URL namespacing (e.g., {% url 'animals:animal-list' %})

urlpatterns = [
    # --- RedirectView: redirects /zoo/ to the home page ---
    path('zoo/', views.ZooRedirectView.as_view(), name='zoo-redirect'),

    # --- TemplateView: Home page ---
    path('', views.HomeView.as_view(), name='home'),

    # --- ListView: All animals ---
    path('animals/', views.AnimalListView.as_view(), name='animal-list'),

    # --- DetailView: Single animal ---
    path('animals/<int:pk>/', views.AnimalDetailView.as_view(), name='animal-detail'),

    # --- CreateView: Add new animal ---
    path('animals/add/', views.AnimalCreateView.as_view(), name='animal-create'),

    # --- UpdateView: Edit existing animal ---
    path('animals/<int:pk>/edit/', views.AnimalUpdateView.as_view(), name='animal-update'),

    # --- DeleteView: Delete animal ---
    path('animals/<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal-delete'),

    # --- FormView: Search animals ---
    path('animals/search/', views.AnimalSearchView.as_view(), name='animal-search'),

    # --- ArchiveIndexView: All years with animals ---
    path('animals/archive/', views.AnimalArchiveIndexView.as_view(), name='animal-archive-index'),

    # --- YearArchiveView: Animals added in a given year ---
    path('animals/archive/<int:year>/', views.AnimalYearArchiveView.as_view(), name='animal-year-archive'),

    # --- MonthArchiveView: Animals added in a given month ---
    path('animals/archive/<int:year>/<int:month>/', views.AnimalMonthArchiveView.as_view(), name='animal-month-archive'),

    # --- WeekArchiveView: Animals added in a given week ---
    path('animals/archive/<int:year>/week/<int:week>/', views.AnimalWeekArchiveView.as_view(), name='animal-week-archive'),

    # --- DayArchiveView: Animals added on a given day ---
    path('animals/archive/<int:year>/<int:month>/<int:day>/', views.AnimalDayArchiveView.as_view(), name='animal-day-archive'),

    # --- TodayArchiveView: Animals added today ---
    path('animals/archive/today/', views.AnimalTodayArchiveView.as_view(), name='animal-today-archive'),

    # --- DateDetailView: A single animal identified by date + pk ---
    path('animals/archive/<int:year>/<int:month>/<int:day>/<int:pk>/',
         views.AnimalDateDetailView.as_view(), name='animal-date-detail'),
]
```

---

## 7. Generic Class-Based Views — Complete Reference

Before implementing the views, here is a clear explanation of every Django generic CBV and the additional context/variables this project injects into each one.

### Display Views

| View | What it does | Key attributes |
|------|-------------|----------------|
| `TemplateView` | Renders a static template. No model needed. | `template_name` |
| `ListView` | Queries a model and passes a list to the template as `object_list` or `<model>_list`. | `model`, `paginate_by`, `queryset` |
| `DetailView` | Looks up one object by `pk` or `slug` and passes it as `object` or `<model>`. | `model` |

### Editing Views

| View | What it does | Key attributes |
|------|-------------|----------------|
| `CreateView` | Displays a form, validates it, and saves a new object. | `model`, `fields`, `success_url` |
| `UpdateView` | Displays a pre-filled form for an existing object and saves changes. | `model`, `fields`, `success_url` |
| `DeleteView` | Displays a confirmation page and deletes the object on POST. | `model`, `success_url` |
| `FormView` | Displays any form and processes its submission. Not tied to a model. | `form_class`, `template_name`, `success_url` |

### Date-Based Views

All date-based views require `date_field` (the name of the field to filter by) on the view class.

| View | What it does |
|------|-------------|
| `ArchiveIndexView` | Lists all objects grouped by year; provides `date_list` (years). |
| `YearArchiveView` | Lists months that have objects in the given year. |
| `MonthArchiveView` | Lists all objects for a given year+month. |
| `WeekArchiveView` | Lists all objects for a given year+week. |
| `DayArchiveView` | Lists all objects for a given year+month+day. |
| `TodayArchiveView` | `DayArchiveView` but always uses today's date. |
| `DateDetailView` | Retrieves a single object identified by date + pk. |

### Navigation View

| View | What it does |
|------|-------------|
| `RedirectView` | Issues an HTTP redirect to another URL. Can be permanent or temporary. |

### Adding Extra Context

All CBVs support `get_context_data()`, which you override to inject any additional variables into the template:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['my_extra_variable'] = some_value
    return context
```

These extra variables are then available in templates as `{{ my_extra_variable }}`.

---

## 8. All Views Implemented

### `animals/forms.py`

Create this file to define the search form used by `FormView`:

```python
from django import forms


class AnimalSearchForm(forms.Form):
    """
    A form for searching animals by any of their attributes.
    All fields are optional so users can search by one or more criteria.
    """
    name = forms.CharField(
        required=False,
        label="Name contains",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Lion'})
    )
    min_age = forms.IntegerField(
        required=False,
        label="Minimum age",
        min_value=0
    )
    max_age = forms.IntegerField(
        required=False,
        label="Maximum age",
        min_value=0
    )
    min_weight = forms.FloatField(
        required=False,
        label="Minimum weight (kg)",
        min_value=0
    )
    max_weight = forms.FloatField(
        required=False,
        label="Maximum weight (kg)",
        min_value=0
    )
    born_in_captivity = forms.NullBooleanField(
        required=False,
        label="Born in captivity",
        widget=forms.Select(choices=[
            ('', 'Any'),
            ('true', 'Yes'),
            ('false', 'No'),
        ])
    )
```

### `animals/views.py`

```python
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
    FormView for searching animals. Uses GET so results are bookmarkable
    and no CSRF token is needed.

    The key challenge: FormView only binds form data on POST by default.
    We override get_form_kwargs() to also bind GET params, which makes the
    form validate when the user submits the search via GET.

    All search logic lives in get_context_data() so it runs on every request.
    form_valid() is not used.

    Extra context added:
      - page_title: describes the page
      - results: the QuerySet of matching animals (after form submission)
      - result_count: number of matches
      - search_performed: boolean flag so the template knows to show results
    """
    template_name = 'animals/animal_search.html'
    form_class = AnimalSearchForm

    def get_form_kwargs(self):
        """
        By default, FormView only binds form data on POST.
        This override also binds GET params so the form validates on GET.
        Without this, the form is always unbound on GET and is_valid()
        never returns True, so no search ever runs.
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
        # Only run the search if GET params are present and the form is valid
        if self.request.GET and form.is_valid():
            data = form.cleaned_data
            queryset = Animal.objects.all()

            # Filter by name (case-insensitive partial match)
            if data.get('name'):
                queryset = queryset.filter(name__icontains=data['name'])

            # Filter by age range
            if data.get('min_age') is not None:
                queryset = queryset.filter(age__gte=data['min_age'])
            if data.get('max_age') is not None:
                queryset = queryset.filter(age__lte=data['max_age'])

            # Filter by weight range
            if data.get('min_weight') is not None:
                queryset = queryset.filter(weight__gte=data['min_weight'])
            if data.get('max_weight') is not None:
                queryset = queryset.filter(weight__lte=data['max_weight'])

            # Filter by born_in_captivity
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
```

---

## 9. Templates

### `animals/templates/animals/base.html` — Shared Layout with Navigation Bar

Every other template extends this file. The `{% block %}` tags define regions that child templates can override.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Zoo App{% endblock %}</title>
</head>
<body>

<nav>
    <strong>Zoo Management</strong> |
    <a href="{% url 'animals:home' %}">Home</a> |
    <a href="{% url 'animals:animal-list' %}">All Animals</a> |
    <a href="{% url 'animals:animal-create' %}">Add Animal</a> |
    <a href="{% url 'animals:animal-search' %}">Search</a> |
    <a href="{% url 'animals:animal-archive-index' %}">Archive</a> |
    <a href="{% url 'animals:animal-today-archive' %}">Added Today</a>
</nav>

<hr>

<h1>{% block heading %}{% endblock %}</h1>

{% block content %}{% endblock %}

<hr>
<footer>Zoo Animal Management System</footer>

</body>
</html>
```

> **How template inheritance works:** Child templates use `{% extends 'animals/base.html' %}` and fill in named blocks. Everything outside a block in the child is ignored.

---

### `animals/templates/animals/home.html` — TemplateView

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
{# page_title, total_animals, captive_count, wild_count come from HomeView.get_context_data() #}
<p>Welcome to the Zoo Animal Management System.</p>

<p>
    The zoo currently has <strong>{{ total_animals }}</strong> animal(s) on record.
    Of these, <strong>{{ captive_count }}</strong> were born in captivity and
    <strong>{{ wild_count }}</strong> were born in the wild.
</p>

<ul>
    <li><a href="{% url 'animals:animal-list' %}">Browse all animals</a></li>
    <li><a href="{% url 'animals:animal-create' %}">Add a new animal</a></li>
    <li><a href="{% url 'animals:animal-search' %}">Search animals</a></li>
    <li><a href="{% url 'animals:animal-archive-index' %}">View archive by date</a></li>
</ul>
{% endblock %}
```

---

### `animals/templates/animals/animal_list.html` — ListView

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }} ({{ total_count }} total){% endblock %}

{% block content %}
{# 'animals' = context_object_name; 'total_count' and 'page_title' from get_context_data() #}

{% if animals %}
<table border="1">
    <thead>
        <tr>
            <th>Name</th>
            <th>Age (years)</th>
            <th>Weight (kg)</th>
            <th>Born in Captivity</th>
            <th>Date Added</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for animal in animals %}
        <tr>
            <td><a href="{{ animal.get_absolute_url }}">{{ animal.name }}</a></td>
            <td>{{ animal.age }}</td>
            <td>{{ animal.weight }}</td>
            <td>{{ animal.born_in_captivity|yesno:"Yes,No" }}</td>
            <td>{{ animal.date_added }}</td>
            <td>
                <a href="{% url 'animals:animal-update' animal.pk %}">Edit</a> |
                <a href="{% url 'animals:animal-delete' animal.pk %}">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

{# Pagination — paginator and page_obj are provided automatically by ListView #}
<p>
    Page {{ page_obj.number }} of {{ paginator.num_pages }}
    {% if page_obj.has_previous %}
        | <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
    {% endif %}
    {% if page_obj.has_next %}
        | <a href="?page={{ page_obj.next_page_number }}">Next</a>
    {% endif %}
</p>

{% else %}
<p>No animals found.</p>
{% endif %}

{% endblock %}
```

---

### `animals/templates/animals/animal_detail.html` — DetailView

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
{# 'animal' = context_object_name from DetailView #}
{# 'is_elderly' and 'weight_category' are extra variables from get_context_data() #}

<table border="1">
    <tr><th>Name</th><td>{{ animal.name }}</td></tr>
    <tr><th>Age</th><td>{{ animal.age }} year(s)
        {% if is_elderly %}<em>(Elderly animal)</em>{% endif %}
    </td></tr>
    <tr><th>Weight</th><td>{{ animal.weight }} kg ({{ weight_category }})</td></tr>
    <tr><th>Born in Captivity</th><td>{{ animal.born_in_captivity|yesno:"Yes,No" }}</td></tr>
    <tr><th>Date Added</th><td>{{ animal.date_added }}</td></tr>
</table>

<p>
    <a href="{% url 'animals:animal-update' animal.pk %}">Edit this animal</a> |
    <a href="{% url 'animals:animal-delete' animal.pk %}">Delete this animal</a> |
    <a href="{% url 'animals:animal-list' %}">Back to list</a>
</p>
{% endblock %}
```

---

### `animals/templates/animals/animal_form.html` — CreateView / UpdateView

This single template is shared by both `AnimalCreateView` and `AnimalUpdateView`. The `form_action` extra context variable ("Create" or "Update") differentiates the heading and button label.

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
{# 'form' is provided automatically by CreateView/UpdateView #}
{# 'form_action' and 'page_title' are extra variables from get_context_data() #}

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">{{ form_action }} Animal</button>
</form>

<p><a href="{% url 'animals:animal-list' %}">Cancel — Back to list</a></p>
{% endblock %}
```

---

### `animals/templates/animals/animal_confirm_delete.html` — DeleteView

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
{# 'animal' or 'object' is the Animal instance provided by DeleteView #}

<p>Are you sure you want to permanently delete <strong>{{ object.name }}</strong>?</p>
<p>This action cannot be undone.</p>

<form method="post">
    {% csrf_token %}
    <button type="submit">Yes, Delete</button>
    <a href="{{ object.get_absolute_url }}">Cancel</a>
</form>
{% endblock %}
```

---

### `animals/templates/animals/animal_search.html` — FormView

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
{# 'form' is the AnimalSearchForm provided by FormView #}
{# 'results', 'result_count', 'search_performed' are extra variables from get_context_data() #}

{# method="get" so results are bookmarkable and no CSRF token is needed #}
<form method="get">
    {{ form.as_p }}
    <button type="submit">Search</button>
</form>

{% if search_performed %}
<hr>
<h2>Results ({{ result_count }} found)</h2>

{% if results %}
<table border="1">
    <thead>
        <tr>
            <th>Name</th>
            <th>Age</th>
            <th>Weight (kg)</th>
            <th>Born in Captivity</th>
            <th>Date Added</th>
            <th>Details</th>
        </tr>
    </thead>
    <tbody>
        {% for animal in results %}
        <tr>
            <td>{{ animal.name }}</td>
            <td>{{ animal.age }}</td>
            <td>{{ animal.weight }}</td>
            <td>{{ animal.born_in_captivity|yesno:"Yes,No" }}</td>
            <td>{{ animal.date_added }}</td>
            <td><a href="{{ animal.get_absolute_url }}">View</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p>No animals matched your search criteria.</p>
{% endif %}
{% endif %}

{% endblock %}
```

---

### `animals/templates/animals/animal_archive.html` — ArchiveIndexView

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
{# 'date_list' is provided by ArchiveIndexView — a list of years with animals #}
{# 'total_years' is an extra variable from get_context_data() #}

<p>The archive spans <strong>{{ total_years }}</strong> year(s).</p>

{% if date_list %}
<ul>
    {% for year in date_list %}
    <li>
        <a href="{% url 'animals:animal-year-archive' year.year %}">
            {{ year.year }}
        </a>
    </li>
    {% endfor %}
</ul>
{% else %}
<p>No animals have been added yet.</p>
{% endif %}

{% endblock %}
```

---

### `animals/templates/animals/animal_archive_year.html` — YearArchiveView

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }} — {{ animal_count }} animal(s){% endblock %}

{% block content %}
{# 'year' = the year as a datetime object; 'object_list' = animals that year #}
{# 'date_list' = list of months with animals #}
{# 'animal_count' and 'page_title' are extra variables #}

<h2>Browse by month</h2>
{% if date_list %}
<ul>
    {% for month in date_list %}
    <li>
        <a href="{% url 'animals:animal-month-archive' year.year month.month %}">
            {{ month|date:"F" }}
        </a>
    </li>
    {% endfor %}
</ul>
{% endif %}

<h2>All Animals Added in {{ year.year }}</h2>
{% if object_list %}
<ul>
    {% for animal in object_list %}
    <li><a href="{{ animal.get_absolute_url }}">{{ animal }}</a> — {{ animal.date_added }}</li>
    {% endfor %}
</ul>
{% else %}
<p>No animals were added this year.</p>
{% endif %}

{% endblock %}
```

---

### `animals/templates/animals/animal_archive_month.html` — MonthArchiveView

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
{# 'month' = the month as a datetime; 'object_list' = animals that month #}

{% if object_list %}
<ul>
    {% for animal in object_list %}
    <li>
        <a href="{{ animal.get_absolute_url }}">{{ animal }}</a>
        — added {{ animal.date_added }}
    </li>
    {% endfor %}
</ul>
{% else %}
<p>No animals were added during this month.</p>
{% endif %}

<p>
    <a href="{% url 'animals:animal-year-archive' month.year %}">
        Back to {{ month.year }} archive
    </a>
</p>
{% endblock %}
```

---

### `animals/templates/animals/animal_archive_week.html` — WeekArchiveView

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
{# 'week' = the week start date; 'object_list' = animals that week #}

{% if object_list %}
<ul>
    {% for animal in object_list %}
    <li><a href="{{ animal.get_absolute_url }}">{{ animal }}</a></li>
    {% endfor %}
</ul>
{% else %}
<p>No animals were added during this week.</p>
{% endif %}
{% endblock %}
```

---

### `animals/templates/animals/animal_archive_day.html` — DayArchiveView / TodayArchiveView

This template is shared by both `DayArchiveView` and `TodayArchiveView`:

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
{# 'day' = the date; 'object_list' = animals added on that day #}

{% if object_list %}
<ul>
    {% for animal in object_list %}
    <li><a href="{{ animal.get_absolute_url }}">{{ animal }}</a></li>
    {% endfor %}
</ul>
{% else %}
<p>No animals were added on this day.</p>
{% endif %}
{% endblock %}
```

---

## 10. Running and Testing the App

### Create a Superuser (for Admin)

```bash
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

### Key URLs to Test

| URL | View | What to test |
|-----|------|-------------|
| `/` | HomeView | Counts of animals |
| `/zoo/` | ZooRedirectView | Should redirect to `/` |
| `/animals/` | AnimalListView | Paginated table |
| `/animals/add/` | AnimalCreateView | Create an animal |
| `/animals/1/` | AnimalDetailView | View one animal |
| `/animals/1/edit/` | AnimalUpdateView | Edit form pre-filled |
| `/animals/1/delete/` | AnimalDeleteView | Confirmation page |
| `/animals/search/` | AnimalSearchView | Search by any attribute |
| `/animals/archive/` | ArchiveIndexView | List of years |
| `/animals/archive/2024/` | YearArchiveView | Animals in 2024 |
| `/animals/archive/2024/3/` | MonthArchiveView | Animals in March 2024 |
| `/animals/archive/2024/week/12/` | WeekArchiveView | Animals in week 12 |
| `/animals/archive/2024/3/15/` | DayArchiveView | Animals on Mar 15 2024 |
| `/animals/archive/today/` | TodayArchiveView | Animals added today |
| `/animals/archive/2024/3/15/1/` | DateDetailView | Animal #1 verified by date |

### Add Sample Data via Admin

```bash
# Navigate to:
http://127.0.0.1:8000/admin/
```

Login with your superuser credentials and add several Animal objects with different `date_added` values so you can test all the archive views.

---

## 11. Key Concepts Summary

### Why Generic Class-Based Views?

Django's generic CBVs eliminate boilerplate. Instead of writing the same queryset lookup, pagination logic, and form handling in every view, you inherit from a generic class and only override what's specific to your use case.

### Why `get_context_data()`?

Every CBV calls `get_context_data()` to build the dictionary passed to the template. By calling `super().get_context_data(**kwargs)` first, you get all the automatic variables (like `object_list`, `form`, `page_obj`) and then simply add your own keys.

### Why `reverse_lazy()`?

`reverse_lazy()` is used in class-level attributes (like `success_url`) because Python evaluates class bodies at import time — before the URL configuration is loaded. `reverse_lazy()` defers the URL lookup until the first actual request.

### Why `date_added` on the Model?

All date-based archive views require a `DateField` or `DateTimeField` to filter against. Adding `date_added` to the `Animal` model satisfies this requirement and also serves as a useful audit field.

### How Template Inheritance Works

```
base.html        — defines {% block %} placeholders and shared layout (navbar, footer)
  └── home.html  — extends base.html and fills in its blocks
  └── animal_list.html
  └── ...
```

Child templates only provide content for the blocks they need. Everything else is inherited from the parent.

### The `yesno` Template Filter

`{{ animal.born_in_captivity|yesno:"Yes,No" }}` converts a boolean into a human-readable string. This is one of Django's built-in template filters and avoids writing `{% if %}{% else %}{% endif %}` blocks for simple boolean display.
