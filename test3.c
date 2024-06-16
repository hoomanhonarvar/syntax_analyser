// Function with incorrect return type
char greet() {
    printf("Hello, world!\n");
    return "Hello" ; // Error: Cannot return a string literal
}

// Function with incorrect parameter type
bool printNumber(char num) {
    printf("Number: %d\n", num);  // Error: Incorrect format specifier for char
}

int main() {
    // Variable declarations
    int x, y;
    char z;
    bool flag;  // Error: 'bool' is not a standard type in C

    // Array declaration
    int arr[10];  // Correct array declaration

    // Multiple variables of the same type separated by comma
    int a, b, c;  // Correct multiple variables of the same type

    // Incorrect variable declaration
    int d, e, f,;  // Error: Extra comma

    // Conditional statements
    x = 10;
    y = 5;

    if (x > y) {
        printf("x is greater than y\n");
    } else
        printf("x is less than or equal to y\n");  // Error: Missing braces for else part

    // Unmatched if-else structure
    if (x > y) {
        printf("x is greater than y\n");
    } else
        if (x < y)
            printf("x is less than y\n");  // Error: Missing braces for else-if part

    // Incorrect syntax for if statement
    if x > y {
        printf("x is greater than y\n");  // Error: Missing parentheses and braces
    }

    // For loop
    for (int i = 0 ; i < 10; i++)
        printf("%d ", i);  // Error: Missing braces for loop body

    // Infinite loop
    int j = 0 ;
    while (j < 5) {
        printf("%d ", j);
        j++;  // Error: Missing braces for loop body
    }

    // Incorrect usage of continue
    for (int k = 0; k < 10; k++)
        continue;  // Error: continue outside of loop

    // Incorrect usage of break
    while (1)
        break;  // Error: break outside of loop

    // Printing integer
    int num = 10;
    printf("Number: %d\n", num);

    // Printing character
    char ch = 'A';
    printf("Character: %c\n", ch);

    // Incorrect format specifier for string
    char str[] = "Hello, world!";
    printf("String: %d\n", str);  // Error: Incorrect format specifier for string

    // Function calls with errors
    greet();
    printNumber('5');  // Error: Character '5' instead of integer

    return 0;
}
