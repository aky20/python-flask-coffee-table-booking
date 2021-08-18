from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.fields.html5 import TelField, TimeField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class BookingFrom(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()],
        render_kw={"placeholder": "name"},
    )
    phone_number = TelField('phone number', validators=[DataRequired()], render_kw={"placeholder": "phone number"})
    total_consumers = IntegerField(
        label='total consumers',
        validators=[DataRequired(), NumberRange(min=1, max=20, message='consumers in total must be between 1 and 20')],
        render_kw={"placeholder": "total consumers"}
    )
    floors = RadioField(
        'floors',
        choices=[('first', 'first floor'), ('second', 'second floor')],
        validators=[DataRequired()]
    )
    time = TimeField('time', validators=[DataRequired()])

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretissecret"

total_booking = []

@app.route("/", methods=['GET', 'POST'])
def home():
    form = BookingFrom()
    return render_template("index.html", form=form)

@app.route("/list", methods=['GET', 'POST'])
def list():
    print(request.method)
    if request.method == 'POST':
        if int(request.form['total_consumers']) > 20:
            return redirect('/')
        new_booking = {'name': request.form['name'],
                          "phone_number": request.form['phone_number'],
                          'total_consumers': request.form['total_consumers'],
                      "floors": request.form['floors'],
                      "time": request.form['time']}
        if not new_booking in total_booking:
            total_booking.append(new_booking)
    return render_template("table_book.html", form_data=total_booking)

if __name__ == "__main__":
    app.run(debug=True)


