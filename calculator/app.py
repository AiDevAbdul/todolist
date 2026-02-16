from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import ast
import operator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Define allowed operators
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(expression):
    """
    Safely evaluate a mathematical expression without using eval().
    """
    try:
        # Parse the expression into an AST
        node = ast.parse(expression, mode='eval')
        return _eval_node(node.body)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

def _eval_node(node):
    """
    Recursively evaluate AST nodes.
    """
    if isinstance(node, ast.Num):  # Python 3.7 and earlier
        return node.n
    elif isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type} not allowed")
        return ALLOWED_OPERATORS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type} not allowed")
        return ALLOWED_OPERATORS[op_type](operand)
    else:
        raise ValueError(f"Unsupported expression type: {type(node)}")

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Calculate the result of a mathematical expression.
    """
    try:
        data = request.get_json()
        
        if not data or 'expression' not in data:
            return jsonify({'error': 'No expression provided'}), 400
        
        expression = data['expression'].strip()
        
        # Validate expression contains only allowed characters
        if not re.match(r'^[\d+\-*/%.()\s]+$', expression):
            return jsonify({'error': 'Invalid characters in expression'}), 400
        
        # Handle percentage (convert to division by 100)
        expression = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', expression)
        
        # Calculate result
        result = safe_eval(expression)
        
        # Round to avoid floating point precision issues
        if isinstance(result, float):
            result = round(result, 10)
        
        return jsonify({'result': result, 'expression': expression})
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except Exception as e:
        return jsonify({'error': f'Calculation error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("Starting Calculator Backend Server...")
    print("Server running at http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
