from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from orders.models import Orders
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import json


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        # Get recent orders (last 5)
        recent_orders = Orders.objects.all().order_by('-order_date')[:5]

        # Get pending order count for notifications
        pending_orders = Orders.objects.filter(status='Pending').count()

        # Calculate recent order stats for the dashboard cards
        today = timezone.now().date()
        last_month = today - timedelta(days=30)

        # Total revenue calculation
        total_revenue = sum(
            order.total_price for order in Orders.objects.filter(status='Delivered'))

        # Recent orders count (last 30 days)
        recent_orders_count = Orders.objects.filter(
            order_date__gte=last_month
        ).count()

        context = {
            'recent_orders': recent_orders,
            'pending_order_count': pending_orders,
            'total_revenue': total_revenue,
            'recent_orders_count': recent_orders_count,
        }
        return render(request, 'dashboard/dashboard.html', context)


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Orders
    template_name = 'dashboard/order_history.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-order_date')

        # Add search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(shipping_first_name__icontains=search_query) |
                Q(shipping_last_name__icontains=search_query)
            )

        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Orders
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Debug output - check your console
        print("Order Items:", self.object.order_items)
        return context


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Orders
    fields = ['status']
    template_name = 'dashboard/order_update.html'

    def get_success_url(self):
        messages.success(
            self.request, f'Order #{self.object.id} status updated to {self.object.status}')
        return reverse('dashboard:order_detail', kwargs={'pk': self.object.id})


@require_GET
def process_order(request, pk, action):
    try:
        order = Orders.objects.get(pk=pk)
        if action == 'process':
            order.status = 'Processing'
        elif action == 'ship':
            order.status = 'Shipped'
        elif action == 'deliver':
            order.status = 'Delivered'
        order.save()
        return JsonResponse({
            'success': True,
            'message': f'Order #{order.id} has been marked as {order.status}'
        })
    except Orders.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


def generate_receipt_pdf(request, pk):
    order = Orders.objects.get(pk=pk)
    user = order.user

    template_path = 'dashboard/receipt_pdf.html'
    context = {
        'order': order,
        'user': user,
        'order_items': order.order_items,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Order_Receipt_{order.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors generating the PDF')
    return response
