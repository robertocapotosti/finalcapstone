#==== IMPORT SECTION ====
import sqlite3
# please use the followuing to install the module: pip install tabulate
from tabulate import tabulate

#===== VARIABLES DECLARATIONS ====
# The list will be used to store a list of objects of shoes.
menu: str
db: object
cursor: object
fd: dict

#==== CLASS SECTION ===

class colors:
	'''Colors class:
	- reset all colors with colors.reset
	- two sub classes fg for foreground and bg for background;
	- use as colors.subclass.colorname.
	  - i.e. colors.fg.red or colors.bg.green
	- also, the generic bold, disable, underline, reverse, strike through,
	  and invisible work with the main class.
	  - i.e. colors.bold
	- this class comes from the article below
		- https://www.geeksforgeeks.org/print-colors-python-terminal'''

	reset = '\033[0m'
	bold = '\033[01m'
	disable = '\033[02m'
	underline = '\033[04m'
	reverse = '\033[07m'
	strikethrough = '\033[09m'
	invisible = '\033[08m'

	class fg:
		black = '\033[30m'
		red = '\033[31m'
		green = '\033[32m'
		orange = '\033[33m'
		blue = '\033[34m'
		purple = '\033[35m'
		cyan = '\033[36m'
		lightgrey = '\033[37m'
		darkgrey = '\033[90m'
		lightred = '\033[91m'
		lightgreen = '\033[92m'
		yellow = '\033[93m'
		lightblue = '\033[94m'
		pink = '\033[95m'
		lightcyan = '\033[96m'
 
	class bg:
			black = '\033[40m'
			red = '\033[41m'
			green = '\033[42m'
			orange = '\033[43m'
			blue = '\033[44m'
			purple = '\033[45m'
			cyan = '\033[46m'
			lightgrey = '\033[47m'

#==== FUNCTIONS SECTION ====

def iff(condition: bool, ret_true: any, ret_false: any) -> any:
	'''Implement the IF statement as a function
	- PARAMETERS
		- condition: boolean for the test
		- ret_true: any type of data to return if condition is True
		- ret_false: any type of data to return if condition is False'''
	if condition:
		return ret_true
	else:
		return ret_false


def positive_num(num1: int | float) -> tuple[bool,str]:
	'''Function to be used in conjunction with the function vinput and it
	 tests the validity of the user input.
	- PARAMETERS
		- str_option: string to test for validity
		- valid_ops: valid characters or valid strings in a list
	- RETURNS
	  a Tuple:
		- the result of the test if num1 is >0
		- the message to be use in case of failed test'''
	# return True if the number is positive
	return (num1 > 0,
		"The input is invalid; please input a positive number.")


def yes_no(str_option: str) -> tuple[bool,str]:
	'''Function to be used in conjunction with the function vinput and it
	 tests the validity of the user input.
	- PARAMETERS
		- str_option: string to test for validity
		- valid_ops: valid characters or valid strings in a list
	- RETURNS
	  a Tuple:
		- the result of the test if the str_option starts with y or n
		- the message to be use in case of failed test'''
	# True is the string contains yes or no
	return (str_option.lower()[0] in ["y","n"],
		"The input is invalid; please use yes/no")


def menu_options(str_option: str, valid_ops: str | list) -> tuple[bool,str]:
	'''Function to be used in conjunction with the function vinput and it
	 tests the validity of the user input.
	- PARAMETERS
		- str_option: string to test for validity
		- valid_ops: valid characters or valid strings in a list
	- RETURNS
	  a Tuple:
		- the result of the test if the str_option is in the valid_ops str/list
		- the message to be use in case of failed test'''
	# if the valid_chars are not a list then it needs to be converted
	if type(valid_ops) != type([]):
		valid_ops = list(valid_ops)
	# return True is the string contains the correct options for the menu
	return (str_option.lower() in valid_ops,
		"The input is invalid; valid options are "+"/".join(valid_ops))


def vinput(
	message: str = "",
	example: str| int | float = "",
	empty_ok: bool = True,
	func_name: str = "",
	func_prm: any = None) -> str | int | float:
	'''Function to manage the input of a string and return it
	- PARAMETERS
		- message: message to print
		- example: example of value to understand what to return;
				   only string, int, float are supported
		- empty_ok: if False is passed, an empty string is invalid
		- func_name: if a function is passed, it will be tested for validity;
					 the funtion MUST return a tuple:
					 (1) a boolean that is the result of the test
					 (2) a message that explain the error; if empty
						 it will be visualised a default message
		- func_prm: optional parameter to pass to the validation function
	- RETURNS
	A String or an Int or a Float depending on the type of the example
	parameter'''

	# variable declarations
	u_input: str
	input_t: str
	valid: object
	result: tuple(bool, str)
	
	# if the expected input is not a string then it cannot be empty
	if type(example) != type(""):
		empty_ok = False
		# if the example is an integer
		if type(example) == type(0):
			input_t = "i"
		# if the example is a float
		elif type(example) == type(0.0):
			input_t = "f"
	# the esample is a string
	else:
		input_t = "s"
	# continue to loop until the input is valid
	while True:
		try:
			u_input = input(message)
		# ignore CTRL-Z
		except EOFError:
			pass
		# if the caller specified the an empty input is invalid
		# and the input is invalid then report an error
		if (not empty_ok) and u_input == "":
			print("Empty input invalid.")
			continue
		# if the caller required a number then try to convert the user input
		try:
			if input_t == "i":
				u_input = int(u_input)
			if input_t == "f":
				u_input = float(u_input)
		# if the conversion fails ther report an error
		except ValueError:
			print("Error: the number is incorrect.")
			continue
		if func_name != "":
			# find the function address in the global dictionary
			valid = globals()[func_name]
			# if the optional parameter has not been specified then call
			# the validation function with the user input only
			if func_prm == None:
				result = valid(u_input)
			# if the optional parameter has been specified then call
			# the validation function with the user input and the parameter
			else:
				result = valid(u_input,func_prm)
			# if the test is not True then is invalid
			if not result[0]:
				# if the error message is empty, it prints a default error
				if result[1] == "":
					print("The input is invalid.")
				# otherwise it prints the error message returned
				else:
					print(result[1])
				continue
		# all validity check passed; return the result
		return u_input


def initialize_books() -> ...:
	'''Initialise the database if it does not exist'''
	# variable declarations
	books: list
	check_table: list
	global db, cursor

	# manage possible errors
	try:
		# open the database
		db = sqlite3.connect('ebookstore')
		# get a cursor object
		cursor = db.cursor()
		# search if the table books exist
		check_table = cursor.execute("SELECT name FROM sqlite_master \
			WHERE type='table' AND name='books' ").fetchall()
		# if the table books is found do nothing
		if len(check_table) > 0:
			return
		# create the table
		cursor.execute("CREATE TABLE books \
				(id INTEGER PRIMARY KEY, title VARCHAR(250), \
				author VARCHAR(100), quantity INTEGER)")
		db.commit()
		books = [(3001,"A Tale of Two Cities","Charles Dickens",30),
			(3002,"Harry Potter and the Philosopher's Stone","J.K. Rowling",40),
			(3003,"The Lion, the Witch and the Wardrobe","C. S. Lewis",25),
			(3004,"The Lord of the Rings","J.R.R Tolkien",37),
			(3005,"Alice in Wonderland","Lewis Carroll",12),
			(3006,"The Time Machine","H. G. Wells",15),
			(3007,"2001: A Space Odyssey","Arthur C. Clarke",9)
			]
		# save the books's data in the database
		cursor.executemany(
			"INSERT INTO books(id, title, author, quantity) \
				VALUES(?,?,?,?)",
			books)
		db.commit()
	# manages errors
	except Exception as err:
		# Roll back any change if something goes wrong
		db.rollback()
		raise err


def enter_book() -> ...:
	'''input a new book and add it to the database'''
	# variable declarations
	id: int
	title: str
	author: str
	quantity: int
	global db, cursor

	id = vinput(f"Input the book ID (next available {next_id()}): ",
		0, False, "positive_num")
	title = vinput("Input the book title: ", "", False)
	author = vinput("Input the book author: ", "", False)
	quantity = vinput("Input the quantity: ", 0, False, "positive_num")
	print("New book.",
		f"ID: {id}",
		f"Title: {title}",
		f"Author: {author}",
		f"Quantity: {quantity}",
		sep = "\n")
	# if the user does not confirm then go back to the main menu
	if vinput(colors.bold+colors.fg.blue+"\nPlease, confirm yes/no: "
				+colors.reset,
			"", False, "yes_no").lower()[0] != "y":
		return
	# manage what to do in case of error
	try:
		# save the books's data in the database
		cursor.execute(
			"INSERT INTO books(id, title, author, quantity) \
				VALUES(?,?,?,?)",
			(id, title, author, quantity))
		db.commit()
	# manages the attempt to dplicate a primary key
	except sqlite3.IntegrityError as err:
		# Roll back any change if something goes wrong
		db.rollback()
		print(colors.bold+colors.fg.red,"\nERROR: The ID already exist.",colors.reset)
	# manages unexpected errors
	except Exception as err:
		# Roll back any change if something goes wrong
		db.rollback()
		print(colors.bold+colors.fg.red,"\nI cannot save to the database.",colors.reset)
		raise err


def update_book(book_id: str) -> bool:
	'''Update a book
	- PARAMETERS
		- book_id: book ID as a string
	- RETURNS
		- True if a record as been updated
		- False if no changes made'''
	pass
	# variable declarations
	book: list
	changed: bool
	menu: str
	field_name: str
	sql_str: str
	field_num: int
	new_data: str | int
	global cursor, db, fd

	# set to False the flag that records if data is changed
	changed = False
	# loop until the user decide to finish updating the selected book
	while True:
		# search the book in the database
		book = cursor.execute("SELECT * FROM books \
			WHERE id = "+book_id+";").fetchone()
		# if nothing found then report error and go back
		if len(book) == 0:
			print(f"\nError: book with ID {book_id} not found.")
			return False
		# show the book selected
		print("\nYou selected the following book",
			f"ID: {book[fd['id']]}",
			f"Title: {book[fd['Title']]}",
			f"Author: {book[fd['Author']]}",
			f"Quantity: {book[fd['Quantity']]}",
			sep = "\n")
		# ask the user what to do
		menu = vinput("\nWhat information would you like to change?\n"
			+"1 - ID\n"
			+"2 - Title\n"
			+"3 - Author\n"
			+"4 - Quantity\n"
			+"Q - Go back to the search: ",
			"", False, "menu_options","1234q").lower()
		# if the user chose to update data, set the field number and name
		if menu in "1234":
			field_num = int(menu)-1
			# convert the field-dictionary's keys in a list and extract 
			# the field name based on the user's selection
			field_name = list(fd.keys())[field_num]
		# the user chose to end the the book update session
		elif menu == "q":
			return changed
		# ask the user for the new value of the choosen field
		new_data = vinput("\nThe current "+field_name.capitalize()
				+" is: "+str(book[field_num])
				+"\nInput the new "+field_name.capitalize()+": ",
			book[field_num],False)
		print("\nThe new "+field_name.capitalize()+" is: "+str(new_data))
		# if the user does not confirm then ask again what to do
		if vinput(colors.bold+colors.fg.blue
					+"Please, confirm to UPDATE the book (yes/no): "
					+colors.reset,
				"", False, "yes_no").lower()[0] != "y":
			continue
		# makes the sql command to update a field of the selected book
		if type(new_data) == type(""):
			sql_str = ("UPDATE books SET " + field_name + " = "
				+"'" + new_data + "'"
				+" WHERE " + field_name + " = "
				+"'" + book[field_num] + "'" + ";"
					)
		else:
			sql_str = ("UPDATE books SET " + field_name + " = "
				+str(new_data) + " WHERE " + field_name + " = "
				+str(book[field_num]) + ";"
					)
		# manage what to do in case of error
		try:
			# save the books's data in the database
			cursor.execute(sql_str)
			db.commit()
			# if the ID was changed, the new ID is the reference
			# of this update session
			if field_name == "id":
				book_id = str(new_data)
			changed = True
		# manages the attempt to dplicate a primary key
		except sqlite3.IntegrityError as err:
			# Roll back any change if something goes wrong
			db.rollback()
			print(colors.fg.red,"\nERROR: The ID already exist.",colors.reset)
		# manages unexpected errors
		except Exception as err:
			# Roll back any change if something goes wrong
			db.rollback()
			print("\nERROR: I cannot save to the database.")
			print(err)


def delete_book(book_id: str) -> bool:
	'''Delete a book
	- PARAMETERS
		- book_id: book ID as a string
	- RETURNS
		- True if a record as been deleted
		- False if no changes made'''
	# variable declarations
	book: list
	global cursor, db, fd

	# search the book in the database
	book = cursor.execute("SELECT * FROM books WHERE id = "+book_id+";").fetchone()
	# if nothing found then report error and go back
	if len(book) == 0:
		print(f"\nError: book with ID {book_id} not found.")
		return False
	# show the book selected
	print("\nYou selected the following book",
		f"ID: {book[fd['id']]}",
		f"Title: {book[fd['Title']]}",
		f"Author: {book[fd['Author']]}",
		f"Quantity: {book[fd['Quantity']]}",
		sep = "\n")
	# if the user does not confirm then go back to the main menu
	if vinput(colors.bold+colors.fg.blue
				+"\nPlease, confirm to DELETE the book (yes/no): "
				+colors.reset,
			"", False, "yes_no").lower()[0] != "y":
		return
	# manage what to do in case of error
	try:
		# save the books's data in the database
		cursor.execute("DELETE FROM books WHERE id = "+book_id+";")
		db.commit()
		return True
	# manages errors
	except Exception as err:
		# Roll back any change if something goes wrong
		db.rollback()
		print(colors.fg.red,"\nI cannot save to the database.")
		print(err,colors.reset)
		return False
	

def search_kind(value: str) -> str:
	'''Asks the user what kind of search to do and add search operators
	 to the string used for a database search 
	- PARAMETERS
		- value: string with what to search
	- RETURNS
	 the string possibly modified with the search options specified
	 by the user'''
	# variable declarations
	menu: str

	# loop until a valid option is choosen
	while True:
		# presenting the menu to the user and 
		# making sure that the user input is valid
		menu = vinput("\nHow do you want to search?\n"
					+f"1 - Search exactly '{value}'\n"
					+f"2 - Search starting by '{value}'\n"
					+f"3 - Search ending by '{value}'\n"
					+f"4 - Search containing '{value}'\n"
					+"Select one of the Options above: ",
					"",False,"menu_options",
					"1234").lower()

		# option to search exactly
		if menu == '1':
			return value

		# option to search starting by
		elif menu == '2':
			return value+"%"

		# option to search ending by
		elif menu == '3':
			return "%"+value

		# option to search containing
		elif menu == '4':
			return "%"+value+"%"

def search_book(automation: str = "") -> ...:
	'''Manages the user interface for searching books
	- PARAMETERS
		- automation: optional parameters that contains the name of a function
		  to be used in case the user select a book'''
	# variable declarations
	s_query_p1: str
	s_query_p2: str
	s_query: str
	s_str: str
	menu: str
	global cursor

	# loop until the user wants to exit the search
	while True:
		# presenting the menu to the user and 
		# making sure that the user input is valid
		menu = vinput("\nSEARCH MENU\n"
					+"0 - List all books\n"
					+"1 - Search by ID\n"
					+"2 - Search by title\n"
					+"3 - Search by author\n"
					+"Q - QUIT the search\n"
					+"Select one of the Options above: ",
					"",False,"menu_options",
					"0123q").lower()
		print()
		# option to search by ID
		if menu == '1':
			s_query_p2 = "CAST(id AS TEXT)"
		# option to search by title
		elif menu == '2':
			s_query_p2 = "title"
		# option to search by author
		elif menu == '3':
			s_query_p2 = "author"
		# back to the caller to the function
		elif menu == 'q':
			return
		# option to simply list the books
		if menu == '0':
			s_query="SELECT * FROM books"
		else:
			# ask the user a string to search in the database
			s_str = vinput("Value to search: ", "", False).lower().strip()
			# ask the user about which kind of search they want to do in the
			# database and create the expression for the LIKE instruction 
			s_query_p1 = search_kind(s_str)
			# make the query string
			s_query="SELECT * FROM books WHERE "+s_query_p2+f" LIKE '{s_query_p1}';"
		# execute the query
		cursor.execute(s_query)
		# converts all the returned records in a grid (list of lists)
		books = [list(row) for row in cursor.fetchall()]
		# if the search found books then show them
		if len(books):
			show_books(books, automation)
		# no books found
		else:
			print("\nThe search did not have any result\n")


def show_books(books: list, automation: str) -> ...:
	'''Function that shows books and if a function name is specified,
	 permits the user to select a book and call that function with the ID
	 of that book
	 - PARAMETERS
	 	- books: table (list of list) of books
		- automation: name of a function to call if the user select a book'''
	# variable declarations
	u_input: str
	menu_text: str
	x: str
	curr_n_books: int
	scursor: int
	n_books: int
	rows: list
	book_ids: list
	menu_ops: list
	global fd

	# total books to show
	curr_n_books = len(books)
	# current position of the 5-books-window to visualise on the screen
	scursor = 0
	# continue to loop until the user decide to quit or manage a book
	while True:
		# set the top index of the emails to see
		# which could be current position+5 or the lenght of the list
		n_books = iff(scursor+5 > curr_n_books, curr_n_books, scursor+5)
		# create a table with header and max 5 books
		rows = books[scursor:n_books]
		# extract the IDs of the books on the screeen
		book_ids = [str(row[0]) for row in rows]
		# add the option supported by the menu
		# add the header to the table
		rows = [[x.capitalize() for x in fd.keys()]] + rows
		print("\nBOOKS LIST.")
		# print max 5 books on the screen
		print(tabulate(rows, headers="firstrow",tablefmt="grid"))
		# initialise the variables for the menu
		menu_text = ""
		menu_ops = ["q"]
		if scursor:
			menu_text += "(P)revious "
			menu_ops += ["p"]
		if n_books != curr_n_books:
			menu_text += "(N)ext "
			menu_ops += ["n"]
		if scursor or n_books != curr_n_books:
			menu_text += "page or "
		if automation != "":
			menu_text = "Input the book ID or\n" + menu_text
			menu_ops += book_ids
		menu_text = "\n" + menu_text + "(Q)uit : "
		# ask the user what to do
		u_input = vinput(menu_text, "", False,
			"menu_options", menu_ops).lower()
		# the user wants to see the previous page of books
		if u_input == "p" and cursor != 0:
			scursor -= 5
		# the user wants to see the next page of books
		elif u_input == "n" and n_books != curr_n_books:
			scursor += 5
		# the user want to go back to the previous menu
		elif u_input == "q":
			return
		# if this function was called for editing and the user input a book ID
		# then call the function that manages a book
		elif automation != "" and u_input.isdigit():
			auto_func = globals()[automation]
			# if the function returns true, it means that data has been changed
			# and that the current search can be closed
			if auto_func(u_input):
				return


def next_id() -> int:
	'''returns the next available ID as an integer'''
	# variable declarations
	result: int
	global cursor

	# querys the maximum ID
	result = cursor.execute("SELECT MAX(id) FROM books;").fetchone()[0]
	# if the books table is empty returns 1
	if result == None:
		return 1
	else:
		return result+1


#==== MAIN PROGRAM ====
# set up the disctionary of the fields
fd = {"id":0,"Title":1,"Author":2,"Quantity":3}
# set up the database
initialize_books()
# loop until a valid option is choosen
while True:
	# presenting the menu to the user and 
	# making sure that the user input is valid
	menu = vinput("\nMAIN MENU\n"
				+"1 - Enter book\n"
				+"2 - Update book\n"
				+"3 - Delete book\n"
				+"4 - Search book\n"
				+"Q - QUIT\n"
				+"Select one of the Options above: ",
				"",False,"menu_options",
				"1234q").lower()
	print()

	# option to enter a book
	if menu == '1':
		enter_book()

	# option to update a book
	elif menu == '2':
		search_book("update_book")

	# option to delete a book
	elif menu == '3':
		search_book("delete_book")

	# option to search books
	elif menu == '4':
		search_book()

	elif menu == 'q':
		print('Bye.')
		db.close()
		exit()