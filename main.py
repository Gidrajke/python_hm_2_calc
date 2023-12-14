from flask import Flask, request, jsonify
import re

app = Flask(__name__)

class Calculator:
    def __init__(self):
        self.precedence = {'*': 2, '/': 2, '+': 1, '-': 1}

    def evaluate_expression(self, expression):
        expression = expression.replace(' ', '')
        tokens = re.findall(r'(\d+\.\d+|\d+|\+|\-|\*|\/|\(|\))', expression)
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.isdigit() or '.' in token:
                output_queue.append(float(token))
            elif token in self.precedence:
                while operator_stack and self.precedence.get(operator_stack[-1], 0) >= self.precedence[token]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()

        while operator_stack:
            output_queue.append(operator_stack.pop())

        result_stack = []
        for token in output_queue:
            if isinstance(token, float):
                result_stack.append(token)
            elif token in self.precedence:
                b = result_stack.pop()
                a = result_stack.pop()
                if token == '+':
                    result_stack.append(a + b)
                elif token == '-':
                    result_stack.append(a - b)
                elif token == '*':
                    result_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError
                    result_stack.append(a / b)

        return result_stack[0]

@app.route('/calculate', methods=['POST'])
def handle_calculation():
    data = request.get_json()
    expression = data.get('expression')

    if expression:
        calc = Calculator()
        result = calc.evaluate_expression(expression)
        return jsonify({'result': str(result)})
    else:
        return jsonify({'error': 'Не указано математическое выражение'})

if __name__ == '__main__':
    app.run(debug=True)
