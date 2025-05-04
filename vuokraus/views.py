from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from .models import Game, Loan
from .forms import RegisterForm, LoanForm


# Lists all games and provides filtering by title, genre and platform
class GameListView(ListView):
    model = Game
    template_name = "vuokraus/game_list.html"
    context_object_name = "games"

    def get_queryset(self):
        queryset = Game.objects.all()
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(title__icontains=q)
        genre = self.request.GET.get("genre")
        if genre:
            queryset = queryset.filter(genre__name__icontains=genre)
        platform = self.request.GET.get("platform")
        if platform:
            queryset = queryset.filter(platform__name__icontains=platform)
        return queryset.distinct()


# Displays detailed information for a specific game
class GameDetailView(DetailView):
    model = Game
    template_name = "vuokraus/game_detail.html"
    context_object_name = "game"


# Handles creation of new loans for games (requires login)
class LoanCreateView(LoginRequiredMixin, CreateView):
    form_class = LoanForm
    template_name = "vuokraus/loan_form.html"

    def form_valid(self, form):
        game = get_object_or_404(Game, pk=self.kwargs["pk"])
        if not game.available:
            return redirect("game_detail", pk=game.pk)

        form.instance.game = game
        form.instance.user = self.request.user

        # Get loan period from POST data (fallback 14 days)
        try:
            loan_days = int(self.request.POST.get("loan_period", 14))
            if loan_days not in [7, 14, 21, 28]:
                loan_days = 14  # default if invalid value
        except (TypeError, ValueError):
            loan_days = 14

        form.instance.due_date = timezone.now() + timedelta(days=loan_days)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("loan_history")


# Shows loan history for the logged-in user
class LoanHistoryView(LoginRequiredMixin, ListView):
    model = Loan
    template_name = "vuokraus/loan_history.html"
    context_object_name = "loans"

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user).order_by("-loan_date")


# Handles the return of a borrowed game
def return_game(request, pk):
    loan = get_object_or_404(Loan, pk=pk, user=request.user, returned_at__isnull=True)
    loan.returned_at = timezone.now()
    loan.save()
    return redirect("loan_history")


# Handles new user registration
class RegisterView(FormView):
    template_name = "vuokraus/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("game_list")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
