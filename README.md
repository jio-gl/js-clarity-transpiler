# JS to Clarity Transpiler

This is a transpiler that converts JavaScript code into Clarity smart contracts. It allows developers to write smart contracts in JavaScript syntax and automatically converts them into Clarity syntax.

## Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/jio-gl/js-to-clarity-transpiler.git
cd js-to-clarity-transpiler
pip install -r requirements.txt
```

## Usage

To transpile a JavaScript file into a Clarity smart contract, use the `transpile` command:

```bash
python transpiler.py path/to/input.js -o path/to/output.clar
```

This will transpile the `input.js` file and generate the Clarity code in the `output.clar` file.

## Example

Input (input.js):

```javascript
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
```

Output (output.clar):

```
(define-variable x 5)
(define-variable y 10)
(define-constant z 23)
(define-variable myprincipal 'ST1HTBVD3JG9C05J7HBJTHGR0GGW7KXW28M5JS8QE.my-contract)
(define-variable mybool (and true false))
(define-public (add)
  (begin
  (define-variable result (+ a b))
  (return result)
  )
)
(define-variable sum (add x y))
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).
```
