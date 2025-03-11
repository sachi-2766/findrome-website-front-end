import yfinance as yf
import plotly.graph_objects as go
from flask import Flask, render_template, request

app = Flask(__name__)

# Available time periods
time_periods = {
    "1d": "1d",
    "1wk": "1wk",
    "1mo": "1mo",
    "1y": "1y",
    "5y": "5y",
    "10y": "10y",
}

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default period is 10 years
    period = request.form.get('period', '10y')
    
    indices = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "BANKNIFTY": "^NSEBANK",
        "MIDCAP 150": "^CRSMID",
        "NIFTY NEXT 50": "^NSMIDCP",
    }

    data_dict = {}
    for name, ticker in indices.items():
        try:
            data = yf.Ticker(ticker).history(period=period)
            if not data.empty:
                data_dict[name] = data["Close"]
        except Exception as e:
            print(f"Error fetching data for {name}: {e}")
    
    # Create list to hold HTML representations of the plots
    plot_htmls = []
    for name, data in data_dict.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data, mode="lines", name=name))

        fig.update_layout(
            title=f"{name} Performance ({period})",
            xaxis_title="Date",
            yaxis_title="Closing Price"
        )
        
        # Convert the figure to HTML
        plot_htmls.append(fig.to_html(full_html=False))

    return render_template('index.html', plot_htmls=plot_htmls, period=period, time_periods=time_periods)

if __name__ == '__main__':
    app.run(debug=True)
