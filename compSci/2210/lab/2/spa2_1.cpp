/**
 * SPA2.1: Improved Histogram Program
 * Name: Sam
 *
 * Improvements over the SPA2 submission:
 *  - Corrected the array requirement: replaced dynamic allocation
 *    (new/delete) with a fixed-size C-style array whose capacity is a
 *    compile-time constant, with named constexpr bounds for the
 *    supported range.
 *  - Added interactive prompts so the user can see what to enter.
 *  - Invalid bounds (outside the supported range, or lower > upper)
 *    are rejected with a helpful message and the user can retry.
 *  - Nonnumeric input is detected, reported, and skipped instead of
 *    silently terminating input.
 *  - After each histogram the user may generate another one without
 *    restarting the program.
 */

#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
using namespace std;

constexpr int MIN_VALUE = 1;                     // smallest supported value
constexpr int MAX_VALUE = 100;                   // largest supported value
constexpr int CAPACITY = MAX_VALUE - MIN_VALUE + 1;  // one entry per integer

/**
 * Zero every frequency count before the array is used.
 *
 * @param counts  frequency array of CAPACITY ints
 * @post          counts[i] == 0 for every valid index i
 */
void resetCounts(int counts[]) {
    for (int i = 0; i < CAPACITY; i++) {
        counts[i] = 0;
    }
}

/**
 * Find the largest frequency stored in the array.
 *
 * @param counts  frequency array of CAPACITY ints
 * @return        the maximum count (0 if all counts are zero)
 */
int maxFrequency(const int counts[]) {
    int max = 0;
    for (int i = 0; i < CAPACITY; i++) {
        if (counts[i] > max) max = counts[i];
    }
    return max;
}

/**
 * Compute the horizontal axis width from the maximum frequency.
 * The width is the next multiple of 5, rounded up to an even number
 * of 5-unit groups, so the axis extends slightly past the longest row.
 *
 * @param max_frequency  the largest frequency in the histogram
 * @return               axis width in character columns (at least 10)
 */
int axisWidth(int max_frequency) {
    if (max_frequency <= 0) return 10;
    int groups = (int)ceil(max_frequency / 5.0);
    if (groups % 2 != 0) {
        groups++;
    }
    return groups * 5;
}

/**
 * Draw the horizontal axis with 5-unit tick labels.
 *
 * @param width  total axis width in character columns (multiple of 5)
 */
void drawAxis(int width) {
    int segments = width / 5;
    cout << "    +";
    for (int i = 0; i < segments; i++) {
        cout << "----+";
    }
    cout << endl << "    ";
    cout << left;
    for (int i = 0; i <= segments; i++) {
        int label = i * 5;
        if (label < width) cout << setw(5);
        cout << label;
    }
    cout << endl;
    cout << right;
}

/**
 * Print one histogram row: the value, a pipe, and one '#' per count.
 *
 * @param value  the data value labeling this row
 * @param count  how many times value occurred
 */
void printRow(int value, int count) {
    cout << setw(3) << value << " |";
    for (int i = 0; i < count; i++) cout << "#";
    cout << endl;
}

/**
 * Read the user's lower and upper bounds, validating them against the
 * supported range. Both bounds must lie within MIN_VALUE..MAX_VALUE
 * and lower must not exceed upper. The user retries until valid.
 *
 * @param lower  set to the validated lower bound
 * @param upper  set to the validated upper bound
 * @return       true if valid bounds were read, false if input ended
 */
bool readBounds(int& lower, int& upper) {
    while (true) {
        cout << "Enter the lower and upper bounds (supported range "
             << MIN_VALUE << "-" << MAX_VALUE << "): ";
        cin >> lower >> upper;
        if (cin.fail()) {
            cin.clear();
            if (cin.peek() == EOF) return false;  // input ended
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Error: bounds must be integers; please try again." << endl;
            continue;
        }
        if (lower < MIN_VALUE || lower > MAX_VALUE ||
            upper < MIN_VALUE || upper > MAX_VALUE) {
            cout << "Error: both bounds must be within " << MIN_VALUE
                 << "-" << MAX_VALUE << "." << endl;
        } else if (lower > upper) {
            cout << "Error: the lower bound must not exceed the upper bound."
                 << endl;
        } else {
            return true;
        }
    }
}

/**
 * Read integer data values until the sentinel value 0 is entered.
 * Each value is validated against [lower, upper] before it is used to
 * index the array; valid values are counted at counts[value - MIN_VALUE].
 * Out-of-range values are reported and rejected. Nonnumeric input is
 * reported, discarded, and does not end the reading loop.
 *
 * @param lower   validated lower bound for this run
 * @param upper   validated upper bound for this run
 * @param counts  frequency array of CAPACITY ints
 */
void readData(int lower, int upper, int counts[]) {
    int val;
    cout << "Enter values in [" << lower << ", " << upper
         << "], one per line (0 to finish):" << endl;
    while (true) {
        cout << "> ";
        cin >> val;
        if (cin.fail()) {
            cin.clear();
            if (cin.peek() == EOF) break;  // input ended; stop reading values
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Error: nonnumeric input ignored; please enter an integer."
                 << endl;
            continue;
        }
        if (val == 0) break;
        if (val < lower || val > upper) {
            cout << "Error: value " << val << " is out of range ["
                 << lower << ", " << upper << "] and was rejected." << endl;
        } else {
            counts[val - MIN_VALUE]++;
        }
    }
}

/**
 * Print the histogram for the selected range, rows from upper down to
 * lower, followed by the horizontal axis sized to the maximum count.
 *
 * @param lower   first (smallest) value to display
 * @param upper   last (largest) value to display
 * @param counts  frequency array of CAPACITY ints
 */
void printChart(int lower, int upper, const int counts[]) {
    int maxFreq = maxFrequency(counts);
    for (int i = upper; i >= lower; i--) {
        printRow(i, counts[i - MIN_VALUE]);
    }
    drawAxis(axisWidth(maxFreq));
}

/**
 * Ask the user whether to generate another histogram.
 *
 * @return true if the user answered 'y' or 'Y', false otherwise
 */
bool runAgain() {
    char choice = 'n';
    cout << "Generate another histogram? (y/n): ";
    cin >> choice;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    return (choice == 'y' || choice == 'Y');
}

int main() {
    int counts[CAPACITY];  // fixed-size array, capacity known at compile time
    bool again = true;
    while (again) {
        int lower, upper;
        if (!readBounds(lower, upper)) break;
        resetCounts(counts);
        readData(lower, upper, counts);
        printChart(lower, upper, counts);
        again = runAgain();
    }
    return 0;
}
