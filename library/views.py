from django.shortcuts import render,redirect
from .models import Book, Member, Transaction
from django.utils import timezone


# Create your views here.
from .models import Member

from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})


def member_list(request):
    members = Member.objects.all()
    return render(request, 'library/member_list.html', {'members': members})

from .models import Transaction

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'library/transaction_list.html', {'transactions': transactions})

def home(request):
    # Your view logic here
    return render(request, 'library/home.html')



def issue_book(request, book_id, member_id):
    try:
        book = Book.objects.get(pk=book_id)
        member = Member.objects.get(pk=member_id)
        
        # Check if the book is available (not already issued)
        if book.quantity > 0:
            # Create a transaction record
            transaction = Transaction(
                book=book,
                member=member,
                date_borrowed=timezone.now(),
            )
            transaction.save()
            
            # Update book quantity
            book.quantity -= 1
            book.save()
            
            return redirect('book_list')
        else:
            # Book not available
            return redirect('book_list')
    except (Book.DoesNotExist, Member.DoesNotExist):
        # Book or member not found
        return redirect('book_list')

from .models import Transaction


def return_book(request, transaction_id):
    try:
        transaction = Transaction.objects.get(pk=transaction_id)
        
        # Check if the book is already returned
        if not transaction.date_returned:
            # Set the return date to the current time
            transaction.date_returned = timezone.now()
            
            # Calculate late fees (if any)
            due_date = transaction.date_borrowed + timezone.timedelta(days=14)  # Assuming a 14-day return policy
            if transaction.date_returned > due_date:
                days_late = (transaction.date_returned - due_date).days
                late_fees = days_late * 5  # Rs. 5 per day as late fee
            else:
                late_fees = 0
            
            transaction.fees = late_fees
            transaction.save()
            
            # Update book quantity
            transaction.book.quantity += 1
            transaction.book.save()
            
            return redirect('transaction_list')
        else:
            # Book already returned
            return redirect('transaction_list')
    except Transaction.DoesNotExist:
        # Transaction not found
        return redirect('transaction_list')

def book_search(request):
    query = request.GET.get('q')
    books = Book.objects.filter(title__icontains=query) | Book.objects.filter(authors__icontains=query)
    return render(request, 'library/book_search.html', {'query': query, 'books': books})

def issue_book(request, book_id, member_id):
    try:
        book = Book.objects.get(pk=book_id)
        member = Member.objects.get(pk=member_id)
        
        # Check if the member's outstanding debt is not more than Rs. 500
        outstanding_debt = Transaction.objects.filter(member=member, fees__gt=0).aggregate(Sum('fees'))['fees__sum']
        if outstanding_debt is None:
            outstanding_debt = 0
        
        if outstanding_debt <= 500:
            # Check if the book is available (not already issued)
            if book.quantity > 0:
                # Create a transaction record
                transaction = Transaction(
                    book=book,
                    member=member,
                    date_borrowed=timezone.now(),
                )
                transaction.save()
                
                # Update book quantity
                book.quantity -= 1
                book.save()
                
                return redirect('book_list')
            else:
                # Book not available
                return redirect('book_list')
        else:
            # Member has outstanding debt
            return redirect('book_list')
    except (Book.DoesNotExist, Member.DoesNotExist):
        # Book or member not found
        return redirect('book_list')
    


import requests
from django.shortcuts import render, redirect
from .models import Book

def import_books(request):
    if request.method == 'POST':
        # Retrieve data from the Frappe API
        page = request.POST.get('page', '1')
        title = request.POST.get('title', '')
        authors = request.POST.get('authors', '')
        isbn = request.POST.get('isbn', '')
        publisher = request.POST.get('publisher', '')
        page = int(page)

        # Construct the API URL
        api_url = f'https://frappe.io/api/method/frappe-library?page=2&title=and'

        try:
            response = requests.get(api_url)
            data = response.json()
            
            # Create book records
            for item in data['message']:
                book = Book(
                    title=item['title'],
                    authors=item['authors'],
                    isbn=item['isbn'],
                    publisher=item['publisher'],
                    pages=item['num_pages'],
                )
                book.save()

            return redirect('book_list')
        except Exception as e:
            # Handle API request or data processing errors
            error_message = str(e)
            return render(request, 'library/import_books.html', {'error_message': error_message})

    return render(request, 'library/import_books.html')

def fetch_external_data():
    url = "https://frappe.io/api/method/frappe-library?page=2&title=and"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        # Handle the case when the API request fails
        return None

def display_books(request):
    # Fetch data from the external API
    external_data = fetch_external_data()

    # Query your local database for books
    local_books = Book.objects.all()

    # Pass the data to your template
    return render(request, 'book_list.html', {'external_data': external_data, 'local_books': local_books})