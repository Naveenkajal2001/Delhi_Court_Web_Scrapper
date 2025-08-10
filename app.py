# Importing Essential Libraries
from flask import Flask, render_template, request, redirect
from Data_Scrap import scr
import re
from markupsafe import Markup
from dbase import database
import atexit


#Initialize Web App
app = Flask(__name__)
table=database()
atexit.register(table.close)

@app.route('/', methods=['GET', 'POST'])
def index():
    global a
    a = scr()
    if request.method == 'POST':
        case_type = request.form['case']
        case_number = request.form['case_numb']
        case_year = request.form['case_year']

        try:
            result_html = a.caseInput(case_type, case_number, case_year)
            return render_template(
                'index.html',
                case=a.options(),
                year=a.CaseYear(),
                result=result_html,
                error=None
            )
        except Exception as e:
            return render_template(
                'index.html',
                case=a.options(),
                year=a.CaseYear(),
                result=None,
                error=f"Error: {str(e)}"
            )
    else:
        return render_template(
            'index.html',
            case=a.options(),
            year=a.CaseYear(),
            result=None,
            error=None
        )

@app.route('/status', methods=['GET', 'POST'])
def status():
    try:
        if request.method == 'POST':
            case_type = request.form['case']
            case_number = request.form['case_numb']
            case_year = request.form['case_year']
        else:
            case_type = request.args.get('case')
            case_number = request.args.get('case_numb')
            case_year = request.args.get('case_year')

        # Perform scraping
        a.caseInput(case_type, case_number, case_year)
        table_result = a.casestatus()

        table.insert_case_query(case_type,case_number,case_year,table_result[0])
        # print(table_result)
        if table_result[0][0].lower()=='no data available in table':
            return render_template(
                'CaseFiles.html',
                result=None,
                case_type=case_type,
                case_number=case_number,
                case_year=case_year
            )
        else:
            return render_template(
                'CaseFiles.html',
                result=table_result,
                case_type=case_type,
                case_number=case_number,
                case_year=case_year
            ),a.back()


    except Exception as e:
        return f"Error: {str(e)}"


@app.template_filter('fix_date_spacing')
def fix_date_spacing(text):
    if not isinstance(text, str):
        return text

    replacements = [
        (r'(NEXT DATE:\s*[^L<]+)', r'\1<br>'),
        (r'(Last Date:\s*[^C<]+)', r'\1<br>'),
        (r'(COURT NO:\s*\d+)', r'\1<br>'),
    ]

    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)

    return Markup(text)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
