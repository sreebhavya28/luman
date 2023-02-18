from flask import Flask,render_template,request
from sql import my_cursor,my_connection

app = Flask("lumen")

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/view')
def view_events():
    query = "select * from events"
    my_cursor.execute(query)
    data = my_cursor.fetchall()
    return render_template('view_events.html',data=data)

@app.route('/create-event',methods=['GET'])
def create_event():
    return render_template('create_event_form.html')

@app.route('/event-form-data',methods=['POST'])
def get_event_form_data():
    try:
        if request.method == 'POST':
            event_name = request.form['event_name']
            event_date = request.form['date']
            org_email = request.form['email']
            org_phone = request.form['phone']
            event_des = request.form['event_desc']
            event_type = request.form['event_type']
            event_loc = request.form['event_loc']
            event_status = request.form['event_status']
            max_seats = request.form['max_seats']

            query = f"""
                        INSERT INTO events(event_name,event_date,org_phone,org_email,event_des,event_type,event_loc,event_status,max_seats)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
            values = (event_name,event_date,org_phone,org_email,event_des,event_type,event_loc,event_status,max_seats)
            my_cursor.execute(query,values)
            my_connection.commit()
            return {'response':'Event created successfully'}
    except Exception as e:
        return render_template('response.html',context=str(e))

@app.route('/search',methods=['POST'])
def search_event():
    raw = request.get_json()
    _id = raw['event_id']
    print(raw)
    query = f"SELECT * FROM events where event_id={_id};"
    my_cursor.execute(query)
    data = my_cursor.fetchone()
    return {'response':data}

@app.route('/book-event',methods=['POST'])
def book_event():
    raw = request.get_json()
    event_id = raw['event_id']
    seats = raw['seats_req']
    event_type = raw['event_type']
    date = str(raw['event_date'])
    query = f"""
            INSERT INTO bookings(event_id,event_type,seats_req,date) VALUES(%s,%s,%s)
    """
    values = (event_id,event_type,seats,date)
    my_cursor.execute(query,values)
    my_connection.commit()
    return {'response':'event boooked successfully'}

@app.route('/view-booked-events',methods=['GET'])
def view_booked_events():
    query = f"""
            SELECT * FROM bookings
    """
    my_cursor.execute(query)
    data = my_cursor.fetchall()
    return render_template('response.html',context=data)


