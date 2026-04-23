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