from flask import Flask, render_template, request
import os
import json
import requests
import pandas as pd
from enum import Enum

app = Flask(__name__)


class tipoletra(Enum):
	ledes = 1
	lecer = 2

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index(chartID = 'chart_ID', chart_height = 400): #
	if request.method == 'GET':
		return render_template('/ticker_block.html', chartID='', series=[], title='', container=[])

	if request.method == "POST":
		letras = request.form['letra']
		if letras == 'both':
			letras = ['ledes', 'lecer']
		else:
			letras = [letras]
		date = request.form['date']

		series = {}
		title = {}
		container = {}

		for s in letras:
			url = f"https://api-letras.onrender.com/letras?tipo={s}&date={date}"
			r = requests.get(url)
			data = r.json()

			if not data:
				series[s] = [[0,0],[0,0]]
			else:
				values = [list(d) for d in zip(data['DM'], data['TIR'])]
				fitted = [list(d) for d in zip(data['DMF'], data['FIT'])]
				series[s] = [values, fitted]
			title[s] = {"text": s}
			container[s] = s
		return render_template('/ticker_block.html', chartID=chartID, series=series, title=title, container=container)


#if __name__ == "__main__":
	#app.run(debug = True, passthrough_errors=True, port=8080) #, host='0.0.0.0', port=8080
