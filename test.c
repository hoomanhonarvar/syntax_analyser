// Comprehensive Syntax Test

// Function to add two numbers
int add(int a, int b) {
    return a + b; // Return the sum of a and b
}

// Function to check if a number is positive
bool isPositive(int num) {
    return num > 0 ;
}

// Main function
int main() {
    // Variable declarations and initializations
    int x = 10;
    int y = 20;
    int z = x + y; // Function call

    // Boolean variable
    bool flag = true;

    // If-else statement
    if (x > y) {
        print("x is greater than y");
    } else {
        print("x is not greater than y");
    }

    // For loop with nested if
    for (int i = 0 ; i < 10; i = i + 1) {
        x = x + i;
        if (isPositive(x)) {
            print("x is positive");
        } else {
            print("x is not positive");
        }
    }

    
        int nestedVar = 100;
        if (nestedVar > 50) {
            print("Nested variable is large");
        }
    
    return z;
}