// Function to add two numbers
int add(int a, int b) {
    return a + b;
}

// Main function
int main() {
    int x = 10;
    int y = 20;
    int z = add(x, y);
    
    if (x > y) {
        printf("x is greater than y\n");
    } else {
        printf("x is not greater than y\n");
    }

    return z;
}
