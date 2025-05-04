from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import date
from .models import Platform, Genre, Game, Loan

from django.utils import timezone

class DueDateFilter(admin.SimpleListFilter):
    title = _('Eräpäivä')
    parameter_name = 'due_date'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Tänään')),
            ('past', _('Mennyt')),
            ('future', _('Tulevaisuudessa')),
        )

    def queryset(self, request, queryset):
        today = timezone.localdate()  # aware date
        if self.value() == 'today':
            return queryset.filter(due_date__date=today)
        elif self.value() == 'past':
            return queryset.filter(due_date__date__lt=today)
        elif self.value() == 'future':
            return queryset.filter(due_date__date__gt=today)
        return queryset

class LoanInline(admin.TabularInline):
    model = Loan
    extra = 0
    readonly_fields = ('user', 'loan_date', 'due_date', 'returned_at')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'age_rating', 'available')
    search_fields = ('title',)
    list_filter = ('platform', 'genre')
    inlines = [LoanInline]

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'loan_date', 'due_date', 'returned_at')
    list_filter = ('returned_at', 'loan_date', DueDateFilter)
    search_fields = ('user__username', 'game__title')

