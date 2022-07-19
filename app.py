from flask import Flask, make_response, render_template, request, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)

conn = sql.connect('database.db')
print ("Opened database successfully");

conn.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, amount DECIMAL(14,2) NOT NULL, description TEXT NOT NULL, time_stamp DATE)')
print ("Table succesfully created")


conn.close()


@app.route('/')
def index():
    con = sql.connect('database.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('select * from accounts where amount > 0')

    incomes = cur.fetchall();

    cur.execute('select * from accounts where amount < 0')

    expenses = cur.fetchall();

    cur.execute("select sum(amount) as 'total' from accounts where amount > 0 ")
    totalIncome = cur.fetchall();

    cur.execute("select sum(amount) as 'debit' from accounts where amount < 0 ")
    totalExpense = cur.fetchall();

    cur.execute("select sum(amount) as 'budget' from accounts")
    mainBalance = cur.fetchall();

    return render_template('index.html', incomes = incomes, expenses = expenses, totalIncome = totalIncome, totalExpense = totalExpense, mainBalance = mainBalance)

@app.route('/submit', methods = ['POST','GET'])
def submit():
    if request.method == 'POST':
        if request.form['desc'] == "":
            msg = "empty description field"
            return redirect(url_for('index'))
        elif request.form['val'] == "" or request.form['val'] == 0:
            msg = "invalid value"
            return redirect(url_for('index'))
        else:
            try:
                desc = request.form['desc']
                val = request.form['val']
                date = request.form['date']

                with sql.connect('database.db') as con:
                    cur = con.cursor()

                    cur.execute('INSERT INTO accounts (amount, description, time_stamp) VALUES (?,?,?)',(val,desc,date))
                    con.commit()
                    msg = "Recorded successfully"
            except:
                con.rollback()
                msg = "Error inserting data"
            finally:
                return redirect(url_for('index'))
        con.close()

@app.route('/delete', methods = ['POST'])
def delete():
    try:
        id = request.form['id']

        with sql.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM accounts")
            cur.execute("DELETE FROM accounts WHERE id=?",(id))
            con.commit()
            msg = "Recorded successfully"
    except:
        con.rollback
        print("error deleting data")
    finally:
        return redirect(url_for('index'))
        con.close()

        
