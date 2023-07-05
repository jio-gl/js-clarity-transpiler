import esprima, re

# https://pypi.org/project/esprima/
# esprima demo https://esprima.org/demo/parse.html?code=

def indent_lines(code, num_spaces):
    lines = code.split("\n")
    indented_lines = [(num_spaces * " ") + line for line in lines]
    return "\n".join(indented_lines)

def transpile_literal(node):
    literal_value = node.value
    if isinstance(literal_value, bool):
        return f"{str(literal_value).lower()}"
    if isinstance(literal_value, str):
        if re.match(r"^(SP|ST)[A-HJ-NP-Za-km-z0-9]{39}(\.[A-Za-z0-9\-_]+)?$", literal_value):
            return f"'{literal_value}"
    return str(literal_value)

def transpile_identifier(node):
    identifier_name = node.name
    return identifier_name

def transpile_function_declaration(node):
    function_name = node.id.name
    function_body = node.body
    transpiled_body = indent_lines(traverse_ast(function_body), 2)
    return f"(define-public ({function_name})\n{transpiled_body}\n)"

def transpile_variable_declaration(node):
    variable_declarations = []
    for declaration in node.declarations:
        variable_name = declaration.id.name
        print('*** kind *** ')
        print(dir(declaration))
        print(declaration)
        print(declaration.kind)
        if node.kind == "const":
            if declaration.init:
                variable_value = traverse_ast(declaration.init)
                variable_declaration = f"(define-constant {variable_name} {variable_value})"
            else:
                raise ValueError(f"Missing initializer for constant variable '{variable_name}'")
        else:
            if declaration.init:
                variable_value = traverse_ast(declaration.init)
                variable_declaration = f"(define-variable {variable_name} {variable_value})"
            else:
                variable_declaration = f"(define-variable {variable_name})"
        variable_declarations.append(variable_declaration)
    return "\n".join(variable_declarations)

def transpile_assignment_expression(node):
    variable_name = node["left"]["name"]
    variable_value = traverse_ast(node["right"])
    return f"(var-set! {variable_name} {variable_value})"

def transpile_call_expression(node):
    function_name = node["callee"]["name"]
    arguments = []
    for arg in node["arguments"]:
        arguments.append(traverse_ast(arg))
    return f"({function_name} {' '.join(arguments)})"

def transpile_if_statement(node):
    test_expression = traverse_ast(node["test"])
    consequent_block = traverse_ast(node["consequent"])
    alternate_block = traverse_ast(node["alternate"]) if "alternate" in node else ""
    return f"(if {test_expression}\n  {consequent_block}\n  {alternate_block})"

def transpile_block_statement(node):
    body = node.body
    statement_code = ""
    for statement in body:
        statement_code += traverse_ast(statement) + "\n"
    return f"(begin\n{statement_code})"

def transpile_binary_expression(node):
    operator = node.operator
    left_operand = traverse_ast(node.left)
    right_operand = traverse_ast(node.right)
    return f"({operator} {left_operand} {right_operand})"

def transpile_return_statement(node):
    argument = traverse_ast(node.argument)
    if argument == "null":
        return '(err "null value")'
    else:
        return f"(ok {argument})"

def transpile_call_expression(node):
    callee = traverse_ast(node.callee)
    arguments = [traverse_ast(arg) for arg in node.arguments]
    arguments_str = " ".join(arguments)
    return f"({callee} {arguments_str})"

def transpile_logical_expression(node):
    operator = node.operator
    if operator == "&&":
        operator = "and"
    elif operator == "||":
        operator = "or"
    left_expression = traverse_ast(node.left)
    right_expression = traverse_ast(node.right)
    return f"({operator} {left_expression} {right_expression})"

def traverse_ast(node):
    if node.type == "Program":
        return traverse_ast(node.body[0])
    elif node.type == "Script":
        return traverse_ast(node.body[0])
    elif node.type == "Literal":
        return transpile_literal(node)
    elif node.type == "Identifier":
        return transpile_identifier(node)
    elif node.type == "FunctionDeclaration":
        return transpile_function_declaration(node)
    elif node.type == "VariableDeclaration":
        return transpile_variable_declaration(node)
    elif node.type == "AssignmentExpression":
        return transpile_assignment_expression(node)
    elif node.type == "CallExpression":
        return transpile_call_expression(node)
    elif node.type == "IfStatement":
        return transpile_if_statement(node)
    elif node.type == "Principal":
        return transpile_principal(node)
    elif node.type == "BlockStatement":
        return transpile_block_statement(node)
    elif node.type == "BinaryExpression":
        return transpile_binary_expression(node)
    elif node.type == "ReturnStatement":
        return transpile_return_statement(node)
    elif node.type == "CallExpression":
        return transpile_call_expression(node)
    elif node.type == "LogicalExpression":
        return transpile_logical_expression(node)
    else:
        raise NotImplementedError(f"Node type '{node.type}' not implemented.")

# Example usage
js_code = """

var x = 5;
var y = 10;
const z = 23;
var myprincipal = "ST1HTBVD3JG9C05J7HBJTHGR0GGW7KXW28M5JS8QE.my-contract";
var mybool = true && false;
function add(a, b) {
    var result = a + b;
    return result;
}

var sum = add(x, y);
"""

#try:
js_code = js_code.strip()
if js_code[0] != '{' or js_code[-1] != '}':
    js_code = '{' + js_code + '}'
ast = esprima.parseScript(js_code)
clarity_code = traverse_ast(ast)[6:-2]
print(clarity_code)
#except Exception as e:
#    print(f"An error occurred: {str(e)}")
