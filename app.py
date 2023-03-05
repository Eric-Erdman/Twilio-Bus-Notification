from flask import Flask, request, redirect
import sys
import re
import transitland

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def is_valid_phone_number(phone_number):
    pattern = r'\+1\d{10}'
    return re.fullmatch(pattern, phone_number) is not None


def is_valid_time(time_str):
    time_pattern = re.compile(r'^\d{1,2}:\d{2}[ap]m$')
    return bool(time_pattern.match(time_str))


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    """
    Recieve form data and write as json to data.json

    Request format:
    ImmutableMultiDict([('phone', '+16083773043'), ('monday_time', '11:00am'), ('monday_stop', '6'), ('tuesday_time', '8:00am'), ('tuesday_stop', '6'), ('wednesday_time', '1:00pm'), ('wednesday_stop', '6'), ('thursday_time', '5:00pm'), ('thursday_stop', '4'), ('friday_time', '1:00pm'), ('friday_stop', '6')])

    Output format:
    {"schedule":{"monday":{"time":"1:00pm","stop":"3"},"tuesday":{"time":"1:00pm","stop":"2"},"wednesday":{"time":"3:30pm","stop":"4"},"thursday":{"time":"5:00pm","stop":"7"},"friday":{"time":"9:55am","stop":"2"}},"phone_number":"+16083773043"}
    """
    print(request.form, file=sys.stderr)

    if request.form is None:
        print('No data provided', file=sys.stderr)
        return redirect('/#error-no-data')

    if not is_valid_phone_number(request.form['phone']):
        print('Invalid phone number', file=sys.stderr)
        return redirect('/#error-invalid-phone-number')

    # Uncomment this line to disable the bus logic and only show form
    # return app.send_static_file("submitMessage.html")
    # exit()

    output = {}
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

    output['phone_number'] = request.form['phone']

    output['schedule'] = {}

    for day in days:
        print(f"Checking {day}", file=sys.stderr)
        if not is_valid_time(request.form[day + '_time']):
            return redirect('/#error-invalid-time')
        
        output['schedule'][day] = {
            'time': request.form[day + '_time'],
            'stop': request.form[day + '_stop']
        }

    print(output, file=sys.stderr)

    transitland.set_schedule(output)

    transitland.get_bus_schedule()

    return app.send_static_file("submitMessage.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
