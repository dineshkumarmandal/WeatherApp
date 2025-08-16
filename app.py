from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = '799f2734d0863b14196ec025d94d2dca'

@app.route('/', methods=['GET', 'POST'])
def index():
    forecast_data = None
    if request.method == 'POST':
        city = request.form['city']
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast_data = []
            seen_dates = set()
            for item in data['list']:
                date = item['dt_txt'].split(' ')[0]
                if date not in seen_dates:
                    seen_dates.add(date)
                    forecast_data.append({
                        'date': date,
                        'temp': item['main']['temp'],
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon']
                    })
                if len(forecast_data) == 5:
                    break
        else:
            forecast_data = 'error'
    return render_template('index.html', forecast=forecast_data)

if __name__ == '__main__':
    app.run(debug=True)