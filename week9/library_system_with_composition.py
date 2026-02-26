class Book: 
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def get_info(self):
        return (f"-> Title: {self.title} by {self.author} | ISBN: {self.isbn}.\n")

# contains a collection of books.
class Library():
    def __init__(self, name):
        self.name = name
        self.book_list = []

    def add_book(self, book):
        self.book_list.append(book)
        print(f"* Confirmation: '{book.title}' added to {self.name}.")

    def remove_book(self, title):
        for book in self.book_list:
            if title.lower() == book.title.lower():
                self.book_list.remove(book)
                print(f"* Confirmation: '{title}' has been removed.")
                return # ALWAYS RETURN after loop/if is done.
        print("Error: Book not found.")

    def list_books(self):
        # has to be looped then formatted with .join([]), because book_list contains objects, not strings. 
        out_list = []
        for book in self.book_list:
            out_list.append(book.get_info())
       #books = ''.join([book.get_info() for book in self.book_list]) -> Alternative for single line loop.
        books = ''.join(out_list)
        print(f"\n{self.name}'s available books:\n{books}")

    def search_book(self, title):
        for book in self.book_list:
            if title.lower() == book.title.lower():
                print(book.get_info())
                return  # ALWAYS RETURN after loop/if is done. 
        print(f"Sorry, book '{title}' not found.")

my_library = Library("City Central Library")

book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
book2 = Book("1984", "George Orwell", "9780451524935")
book3 = Book("The Hobbit", "J.R.R. Tolkien", "9780547928227")

my_library.add_book(book1)
my_library.add_book(book2)
my_library.add_book(book3)

print("\n=== Listing Books After Adding ===")
my_library.list_books()

print("=== Searching an existent book ===")
my_library.search_book("1984")
print("=== Searching an non-existent book ===")
my_library.search_book("The Catcher in the Rye") # Test a non-existent book

print("\n=== List Books After Removing ===")
my_library.remove_book("The Great Gatsby")
my_library.list_books()