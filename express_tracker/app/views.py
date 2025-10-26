from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum, Max, Min, Count
from .models import Expense

# ===============================
# HOME VIEW
# ===============================
@login_required(login_url='login')
def home(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # ✅ Handle adding new expense
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        desc = request.POST.get('desc')

        # Always link expense to the logged-in user ✅
        Expense.objects.create(
            user=request.user,
            amount=amount,
            category=category,
            desc=desc
        )

        messages.success(request, "Expense added successfully.")
        return redirect('home')

    # ✅ Average daily spending
    dates = expenses.values_list('date__date', flat=True).distinct()
    day_counts = len(dates)
    average = round(total / day_counts, 2) if day_counts > 0 else 0

    # ✅ Highest & lowest expense
    stats = expenses.aggregate(
        highest=Max('amount'),
        lowest=Min('amount')
    )

    # ✅ Most used category
    most_used = (
        expenses.values('category')
        .annotate(count=Count('category'))
        .order_by('-count')
        .first()
    )

    # ✅ Pagination
    pagination = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    return render(request, 'home.html', {
        'total': total,
        'page_obj': page_obj,
        'average': average,
        'stats': stats,
        'most_used': most_used
    })


# ===============================
# DELETE VIEW
# ===============================
@login_required(login_url='login')
def delete(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    messages.info(request, "Expense deleted successfully.")
    return redirect("home")


# ===============================
# UPDATE VIEW
# ===============================
@login_required(login_url='login')
def update(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        desc = request.POST.get('desc')

        expense.amount = amount
        expense.category = category
        expense.desc = desc
        expense.save()

        messages.success(request, "Expense updated successfully.")
        return redirect("home")

    return render(request, 'update.html', {'data': expense})


# ===============================
# FILTER VIEW
# ===============================
@login_required(login_url='login')
def filter(request, choice):
    expenses = Expense.objects.filter(user=request.user)
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    if choice == 1:
        result = expenses.order_by("-amount")
    elif choice == 2:
        result = expenses.order_by("category")
    else:
        result = expenses.order_by("date")

    pagination = Paginator(result, 5)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj, 'total': total})
