from flask import Flask, request


app = Flask(__name__)

# strona startowa - okienko "wyobraż sobie numer mieðzy 1 a 100" - oraz ukryte pola do przechowywania min i max
HTML_START = """ 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Guess The Number</title>
</head>
<body>
<h1>Imagine number between 0 and 1000</h1>
<form action="" method="POST">
    <input type="hidden" name="min" value="{}"></input>
    <input type="hidden" name="max" value="{}"></input>
    <input type="submit" value="OK">
</form>
</body>
</html>
"""

# strona zgadywania wartości - pobiera min i max z wartości poniższej funckji przechowywanej w ukrytych polach min i
# max oraz umozliwia umieszczenie odpowiedzi od gracz czy zgadywana liczba jest za duża, za mała czy dobra
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Guess The Number</title>
</head>
<body>
<h1>It is number {guess}</h1>
<form action="" method="POST">
    <input type="submit" name="user_answer" value="too big">
    <input type="submit" name="user_answer" value="too small">
    <input type="submit" name="user_answer" value="you won">
    <input type="hidden" name="min" value="{min}">
    <input type="hidden" name="max" value="{max}">
    <input type="hidden" name="guess" value="{guess}">
</form>
</body>
</html>
"""

#strona wyświetlająca się gdy komputer zgadnie liczbę, pokazująca komunikat z jej wartością
HTML_WIN = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Guess The Number</title>
</head>
<body>
<h1>I won! Your number is {guess}</h1>

</body>
</html>
"""

#funkcja obliczająca zgadywany numer
@app.route("/", methods=["GET", "POST"])
def guess_the_number():
    if request.method == "GET":
        return HTML_START.format(0, 1000) #włączanie strony startowej z domyślnie ustawionymi wartościami min i max
    else:
        min_number = int(request.form.get("min")) # pobieranie wartości min z ukrytych pól w formularzu
        max_number = int(request.form.get("max")) # pobieranie wartości max z ukrytych pól w formularzu
        user_answer = request.form.get("user_answer")
        guess = int(request.form.get("guess", 500)) #obliczanie nowej wartości zgadywane w zależności od odpowiedzi gracza

        if user_answer == "too big":
            max_number = guess
        elif user_answer == "too small":
            min_number = guess
        elif user_answer == "you won":
            return HTML_WIN.format(guess=guess) #zwracanie strony wygrywającej po prawidłowym odgadnięciu liczby

        guess = (max_number - min_number) // 2 + min_number

        return HTML.format(guess=guess, min=min_number, max=max_number) 


if __name__ == "__main__":
    app.run(debug=True, port=5010)