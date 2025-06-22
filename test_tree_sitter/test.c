
float calculateAverage(int arr[], int size);
int findMax(int arr[], int size);
int main() {
    
    int numbers[] = {12, 45, 23, 67, 34, 89, 56};
    int size = sizeof(numbers) / sizeof(numbers[0]); 
    
   
    float avg = calculateAverage(numbers, size);
 
    int max = findMax(numbers, size);
    
    
    return 0;
}

float calculateAverage(int arr[], int size) {
    int sum = 0;
    
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
  
    return (float)sum / size;
}

int findMax(int arr[], int size) {
    int max = arr[0]; 
    
    
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}