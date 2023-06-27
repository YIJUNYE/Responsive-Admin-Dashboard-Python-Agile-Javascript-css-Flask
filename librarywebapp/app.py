from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

 #  public interface route___search fuction and direct to "searchbooks.html"
@app.route("/searchbooks")
def searchbooks():
    return render_template("searchbooks.html")

#  public interface route___get a list of books
@app.route("/listbooks")
def listbooks():
    connection = getCursor()
    connection.execute("SELECT * FROM books;")
    bookList = connection.fetchall()
    print(bookList)
    return render_template("booklist.html", booklist = bookList)    


# staff and public interface route___search by booktitle
@app.route("/searchbooktitle", methods=["POST"])
def searchbooktitle():
    searchterm = request.form.get('booktitle')
    searchterm = "%" + searchterm + "%"
    connection = getCursor()
    connection.execute('''select b.bookid, b.booktitle, b.author, bc.format,l.loandate, 
adddate(loandate,interval 28 day) as duedate,l.returned
            from books b
                inner join bookcopies bc on b.bookid = bc.bookid
                    inner join loans l on bc.bookcopyid = l.bookcopyid WHERE b.booktitle LIKE %s;''',(searchterm,))  #partial search by matching some keys words
    searchBook = connection.fetchall()
    print(searchBook)
    return render_template("searchbookresult.html", searchbook = searchBook)  #new table "searchbook" pass to "searchbookresult.html"         

# staff and public interface route___search by author
@app.route("/searchauthor", methods=["POST"])
def searchauthor():
    searchterm = request.form.get('author')
    searchterm = "%" + searchterm + "%"
    connection = getCursor()
    connection.execute('''select b.bookid, b.booktitle, b.author, bc.format,l.loandate, 
adddate(loandate,interval 28 day) as duedate,l.returned
            from books b
                inner join bookcopies bc on b.bookid = bc.bookid
                    inner join loans l on bc.bookcopyid = l.bookcopyid WHERE b.author LIKE %s;''',(searchterm,))  #partial search by matching some keys words
    searchBook = connection.fetchall()
    print(searchBook)
    return render_template("searchbookresult.html", searchbook = searchBook)  #new table "searchbook" pass to "searchbookresult.html"     

# staff interface route
@app.route("/staff")
def staff(): 
    return render_template("staff.html")   

# staff interface__search books direct to "staffsearch.html"
@app.route("/staff/staffsearch")
def staffsearch(): 
    return render_template("staffsearch.html")   

# staff interface__report most loaned books 
@app.route("/staff/mostloanlist")
def mostloanlist():
    connection = getCursor()
    sql=""" select 
        bs.booktitle, 
        count(l.bookcopyid) as timesborrowered 
        from loans l
        left join bookcopies bc on l.bookcopyid=bc.bookcopyid
        inner join books bs on bs.bookid=bc.bookid  
        group by bc.bookid 
        order by timesborrowered desc;""" #sql to get info and count(l.bookcopyid) to show the times been borrowered
    connection.execute(sql)
    mostloanList = connection.fetchall()
    return render_template("mostloanlist.html", mostloanlist = mostloanList)  #data pass to mostloanlist.html

# staff interface__report overdue books 
@app.route("/staff/overduebooks")
def overduebooks():
    connection = getCursor()
    sql='''select 
        b.borrowerid,
        bs.booktitle,
        b.firstname,
        b.familyname,
        datediff(curdate(),loandate) as daysonloan,
        bc.format
        from loans l
        inner join borrowers b on l.borrowerid=b.borrowerid
        left join bookcopies bc on l.bookcopyid=bc.bookcopyid
        inner join books bs on bs.bookid=bc.bookid
        where datediff(curdate(),loandate)>35 
        order by b.familyname, b.firstname, l.loandate; '''
    connection.execute(sql)
    overdueBooks = connection.fetchall()
    print(overdueBooks)
    return render_template("overduebooks.html", overduebooks = overdueBooks) #data pass to overduebooks.html

# staff interface__borrower summary shows how many books a borrower lent
@app.route("/staff/borrowersummary")
def borrowersummary():
    connection = getCursor()
    sql=""" select  b.firstname, b.familyname,
        count(l.bookcopyid) as timesborrowered 
        from borrowers b
       inner join loans l on l.borrowerid=b.borrowerid
       inner join bookcopies bc on l.bookcopyid=bc.bookcopyid
       inner join books bs on bs.bookid=bc.bookid
        group by b.borrowerid
        order by b.firstname, b.familyname ;"""  # sql to get borrower's info
    connection.execute(sql)
    borrowerSummary = connection.fetchall()
    print(borrowerSummary)
    return render_template("borrowersummary.html", borrowersummary = borrowerSummary)

# staff interface__search a borrower
@app.route("/staff/borrowersearch")
def borrowersearch(): 
    return render_template("borrowersearch.html") 

# staff interface__search borrower by firstname
@app.route("/searchname", methods=["POST"])
def searchname():
    searchterm = request.form.get('name')
    connection = getCursor()
    connection.execute('''SELECT * from borrowers
      WHERE firstname LIKE %s ;''',(searchterm,))   #search a specified borrower then edit it
    Search = connection.fetchall()
    print(Search)
    return render_template("borrowerlist.html", search = Search)  #data pass to borrowerlist.html, then edit any information of a borrower
    
# staff interface__search borrower by ID
@app.route("/searchid", methods=["POST"])
def searchid():
    searchterm = request.form.get('id')
    connection = getCursor()
    connection.execute('''SELECT * from borrowers
      WHERE borrowerid LIKE %s ;''',(searchterm,))  #search a specified borrower then edit it
    Search = connection.fetchall()
    print(Search)
    return render_template("borrowerlist.html", search = Search) #data pass to borrowerlist.html, then edit any information of a borrower

#"/staff/borroweradd" AND "/borrower/add" for adding new borrower function
@app.route("/staff/borroweradd")
def borroweradd(): 
    return render_template("borroweradd.html")

#"/staff/borroweradd" AND "/borrower/add" for adding new borrower function
@app.route("/borrower/add", methods=["POST"])
def addborrower(): 
    Firstname = request.form.get('firstname')  # get data from input=text from borroweradd.html
    Familyname = request.form.get('familyname')
    Dateofbirth = request.form.get('dateofbirth')
    Housenumbername = request.form.get('housenumbername')
    Street = request.form.get('street')
    Town = request.form.get('town')
    City = request.form.get('city')
    Postalcode = request.form.get('postalcode')
    sql ='''INSERT INTO borrowers (firstname, familyname, 
    dateofbirth,housenumbername,street,town,city,postalcode) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);'''
    parameters=(Firstname,Familyname,Dateofbirth,Housenumbername,Street,Town,City,Postalcode)  #excute sql query pass data to table in order to add a new borrower
    cur = getCursor()
    cur.execute(sql,parameters)
    A = cur.fetchall()
    print(A)
    return render_template("borroweradd.html") 


# staff interface("/staff/loanbook")AND("/loan/add")_____issue a book to a borrower
@app.route("/staff/loanbook")
def loanbook():
    todaydate = datetime.now().date()
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    sql = """SELECT * FROM bookcopies
inner join books on books.bookid = bookcopies.bookid
 WHERE bookcopyid not in (SELECT bookcopyid from loans where (returned <> 1 or returned is NULL))
 OR (format='eBook' or format='Audio Book');"""  #any physical books been returned or digital books regardless of loan status
    connection.execute(sql)
    bookList = connection.fetchall()
    return render_template("addloan.html", loandate = todaydate,borrowers = borrowerList, books= bookList)

# staff interface("/staff/loanbook")AND("/loan/add")_____issue a book to a borrower
@app.route("/loan/add", methods=["POST"])  #using post method to pass data to the server
def addloan():
    borrowerid = request.form.get('borrower')
    bookid = request.form.get('book')
    loandate = request.form.get('loandate')
    cur = getCursor()
    cur.execute("INSERT INTO loans (borrowerid, bookcopyid, loandate, returned) VALUES(%s,%s,%s,0);",(borrowerid, bookid, str(loandate),))
    return render_template("addloan.html")

# staff interface("/staff/returnbook")AND("/loan/return")_____return a book to library
@app.route("/staff/returnbook")
def returnbook():
    connection = getCursor()
    sql = """SELECT * FROM loans
inner join bookcopies on loans.bookcopyid=bookcopies.bookcopyid
inner join books on books.bookid = bookcopies.bookid
 WHERE loans.returned <> 1 or returned is NULL;"""  #get all the books that returned value is 0
    connection.execute(sql)
    Loanbook = connection.fetchall()
    print(Loanbook)
    return render_template("returnloan.html",loanbook=Loanbook)  #get new database loanbook

# staff interface("/loan/return")AND("/loan/return")_____return a book to library
@app.route("/loan/return", methods=["POST"])  
def returnloan():
    returnloan = request.form.get('returnloan')
    sql = "UPDATE loans SET returned = 1 where loanid=%s;"   #updata returned value to 1 meaning the book has been returned
    parameters=(returnloan,)
    cur = getCursor()
    cur.execute(sql,parameters)
    Returnloan = cur.fetchall()
    print(Returnloan)
    return render_template("staff.html")    


# staff interface("/borrower/edit")_____edit any information of a borrower
@app.route("/borrower/edit", methods=["POST"])
def editborrower(): 
    Firstname = request.form.get('firstname')  #get all the data from @app.route("/searchid" or "/searchname")
    Familyname = request.form.get('familyname')
    Dateofbirth = request.form.get('dateofbirth')
    Housenumbername = request.form.get('housenumbername')
    Street = request.form.get('street')
    Town = request.form.get('town')
    City = request.form.get('city')
    Postalcode = request.form.get('postalcode')
    Borrowerid=request.form.get('borrowerid')
    sql = '''UPDATE borrowers SET firstname=%s,familyname=%s,dateofbirth=%s,housenumbername=%s,street=%s,town=%s,city=%s,postalcode=%s WHERE borrowerid =%s;'''
    parameters=(Firstname,Familyname,Dateofbirth,Housenumbername,Street,Town,City,Postalcode,Borrowerid)   #Borrowerid set to 'Hidden'  %s as parameters later pass data to SQL to update borrowers' information
    cur = getCursor()
    cur.execute(sql,parameters)
    A = cur.fetchall()
    print(A)
    return render_template("staff.html") 
  