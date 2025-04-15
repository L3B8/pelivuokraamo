from django.contrib import admin
from .models import Platform, Genre, Game, Loan

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
    list_filter = ('returned_at', 'loan_date')
    search_fields = ('user__username', 'game__title')
