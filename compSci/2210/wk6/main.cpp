#include <iomanip>
#include <iostream>
#include <string>
#include "LibraryCard.h"

void printReport(const LibraryCard& card) {
    std::cout << "[" << card.getHolder() << "] ";
    card.print();
}

int main() {
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Active: " << LibraryCard::activeCards() << '\n';

    LibraryCard ana{"Ana"};
    LibraryCard ben{"Ben", 2.50};
    LibraryCard x{"X", -4.00};
    std::cout << "Active: " << LibraryCard::activeCards() << '\n';
    printReport(ana);
    printReport(ben);
    printReport(x);

    std::cout << "Ana checkouts:";
    for (int i = 0; i < 4; ++i) {
        std::cout << ' ' << ana.checkOut();
    }
    std::cout << '\n';
    std::cout << "Ana return: " << ana.returnBook(2) << '\n';

    std::cout << "Ben return: " << ben.returnBook(0) << '\n';
    std::cout << "Ben checkout: " << ben.checkOut() << '\n';
    std::cout << "Ben return: " << ben.returnBook(14) << '\n';
    std::cout << "Ben checkout: " << ben.checkOut() << '\n';
    std::cout << "Ben pays 10: " << ben.payFine(10.00) << '\n';
    std::cout << "Ben pays 2: " << ben.payFine(2.00) << '\n';
    std::cout << "Ben checkout: " << ben.checkOut() << '\n';

    std::cout << "Rename x: " << x.setHolder("Xavier") << '\n';
    std::cout << "Rename ana: " << ana.setHolder("A") << '\n';
    printReport(ana);
    printReport(ben);
    printReport(x);

    {
        LibraryCard temp{"Tia"};
        std::cout << "Active: " << LibraryCard::activeCards() << '\n';
    }
    std::cout << "Active: " << LibraryCard::activeCards() << '\n';

    LibraryCard lobby[2];
    lobby[1].setHolder("Lee");
    for (const LibraryCard& card : lobby) {
        printReport(card);
    }
    std::cout << "Active: " << LibraryCard::activeCards() << '\n';

    // Part E check: uncomment ONE line at a time. Each must fail to compile.
    // LibraryCard copy = ana;
    // lobby[0] = ana;
    // std::string name = "Zoe";  printReport(name);
    return 0;
}
