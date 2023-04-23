from flask import Flask, request, render_template, send_file
import pandas as pd
import statistics as stats
import seaborn as sns
import matplotlib.pyplot as plt
import os
from analyzer import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(filename)
            result = pd.read_csv(filename)

            cleaned_result = clear_result_data(result)

            CGPI = cleaned_result.iloc[:, -1].values.tolist()
            CGPI = [float(i) for i in CGPI]

            percentage = []
            for i in range(len(CGPI)):
                if CGPI[i] >= 7:
                    percentage.append(round(7.4*CGPI[i] + 12, 4))
                elif CGPI[i] < 7:
                    percentage.append(round(7.1*CGPI[i] + 12, 4))

            avg_cgpa = stats.mean(CGPI)
            avg_perc = stats.mean(percentage)

            sns.displot(CGPI, kde=True, bins=15)
            plt.savefig('plot.png')

            os.remove(filename)

            return render_template('results.html', percentage=percentage, CGPI=CGPI, avg_cgpa=avg_cgpa, avg_perc=avg_perc)
    return render_template('index.html')


@app.route('/plot')
def plot():
    return send_file('plot.png', mimetype='image/png')


if __name__ == '__main__':
    app.run()
