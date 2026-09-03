#include <iostream>
#include <string>

using namespace std;

int main() {
    const int THRESHOLD = 1000;
    string time, item;
    int amount;
    int total = 0;

    // Read initial values
    cin >> time >> item >> amount;

    // Process each subsequent line
    while (cin) {
        if (item == "urine" || item == "bloodloss" || item == "diarrhea") {
            total -= amount;
        } else {
            total += amount;
            if (total >= THRESHOLD) {
                cout << "after consuming " << item << " at " << time 
                     << ", intake exceeds output by " << total << " ml" << endl;
            }
        }
        cin >> time >> item >> amount;
    }

    cout << "the final fluid differential is " << total << " ml" << endl;
    return 0;
}
