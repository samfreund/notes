#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

int longestRow(int table[], int size) {
    int max = 0;
    for (int i = 0; i < size; i++) {
        if (table[i] > max) max = table[i];
    }
    return max;
}

int axisWidth(int max_frequency) {
    if (max_frequency <= 0) return 10;
    int groups = (int)ceil(max_frequency / 5.0) + 1;
    return groups * 5;
}

void drawAxis(int width) {
    int segments = width / 5;
    cout << "    +";
    for (int i = 0; i < segments; i++) {
        cout << "----+";
    }
    cout << endl << "    ";
    for (int i = 0; i <= segments; i++) {
        int label = i * 5;
        if (i > 0) cout << setw(5);
        if (label <= width) cout << label;
    }
    cout << endl;
}

void printRow(int value, int count) {
    cout << setw(3) << value << " |";
    for (int i = 0; i < count; i++) cout << "#";
    cout << endl;
}

int main() {
    int lower, upper;
    cin >> lower >> upper;
    int size = upper + 1;
    int* counts = new int[size]();
    int val;
    while (cin >> val) {
        if (val < lower || val > upper) {
            cout << "Error: value " << val << " is out of range" << endl;
        } else {
            counts[val]++;
        }
    }
    int maxFreq = longestRow(counts, size);
    int width = axisWidth(maxFreq);
    for (int i = upper; i >= lower; i--) {
        printRow(i, counts[i]);
    }
    drawAxis(width);
    delete[] counts;
    return 0;
}
