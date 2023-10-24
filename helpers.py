from flask import redirect, render_template, session
from functools import wraps
import openai

AI_KEY = "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"
openai.api_key = AI_KEY
def gpt_ask(question):
    model = "text-davinci-003"
    answer = openai.Completion.create(engine=model, prompt=question, max_tokens=1000)

    return answer.choices

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

