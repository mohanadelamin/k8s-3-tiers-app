import time, os
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

DBUSER = os.environ['POSTGRES_USER']
DBPASS = os.environ['POSTGRES_PASSWORD']
DBNAME = os.environ['POSTGRES_DB']
DBHOST = 'postgresdb'
DBPORT = '5432'
DBSCRT = os.environ['APP_SECRET_KEY']

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = DBSCRT

db = SQLAlchemy(app)

class customers(db.Model):
    """
    Example customer database
    """
    id = db.Column('customer_id',db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    name = db.Column(db.String(256))
    universe = db.Column(db.String(256))
    revenue = db.Column(db.String(256))

    def __init__(self, rank, name, universe, revenue):
        self.rank = rank
        self.name = name
        self.universe = universe
        self.revenue = revenue

def database_sample_data_init():
    sample_data = [[1,'CHOAM','Dune','$1.7 trillion'],
                   [2,'Acme Corp.','Looney Tunes','$348.7 billion'],
                   [3,'Sirius Cybernetics Corp.',"Hitchhiker's Guide",'$327.2 billion'],
                   [4,'Buy n Large','Wall-E','$291.8 billion'],
                   [5,'Aperture Science, Inc.','Valve','$163.4 billion'],
                   [6,'SPECTRE','007','$157.1 billion'],
                   [7,'Very Big Corp. of America','Monty Python','$146.6 billion'],
                   [8,'Frobozz Magic Co.','Zork','$112.9 billion'],
                   [9,'Warbucks Industries',"Lil' Orphan Annie",'$61.5 billion'],
                   [10,'Tyrell Corp.','Bladerunner','$59.4 billion']]

    for i in range(len(sample_data)):
        db.session.add(customers(*sample_data[i]))
        db.session.commit()

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if not request.form['rank'] or not request.form['name'] or not request.form['universe'] or not request.form['revenue']:
            flash('Please enter all the fields','error')
        else:
            customer = customers(request.form['rank'],
                                request.form['name'],
                                request.form['universe'],
                                request.form['revenue'])
            db.session.add(customer)
            db.session.commit()
            flash('Record was succesfully added')
            return redirect(url_for('home'))
    return render_template('index.html', customers=customers.query.all(), ip=request.remote_addr, host=request.host)

if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
         try:
             db.create_all()
         except:
             time.sleep(2)
         else:
             dbstatus = True
    database_sample_data_init()
    app.run(debug=True, use_reloader=False, port=5090, host='0.0.0.0')
