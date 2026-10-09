#include "LibraryCard.h"

#include <iostream>
#include <utility>

int LibraryCard::count = 0;
int LibraryCard::nextNumber = 5001;

LibraryCard::LibraryCard(std::string name, double startingFines)
    : holder(isValidName(name) ? std::move(name) : "Guest"),
      number(nextNumber++),
      booksOut(0),
      fines(cleanFines(startingFines)) {
    ++count;
}

LibraryCard::LibraryCard(std::string name) : LibraryCard(std::move(name), 0.0) {}

LibraryCard::LibraryCard() : LibraryCard("Guest", 0.0) {}

LibraryCard::~LibraryCard() {
    --count;
    std::cout << "Card " << number << " closed\n";
}

std::string LibraryCard::getHolder() const { return holder; }

int LibraryCard::getNumber() const { return number; }

int LibraryCard::getBooksOut() const { return booksOut; }

double LibraryCard::getFines() const { return fines; }

bool LibraryCard::setHolder(std::string name) {
    if (!isValidName(name)) {
        return false;
    }
    holder = std::move(name);
    return true;
}

bool LibraryCard::checkOut() {
    if (booksOut >= MAX_BOOKS || fines > FINE_LIMIT) {
        return false;
    }
    ++booksOut;
    return true;
}

bool LibraryCard::returnBook(int daysLate) {
    if (booksOut == 0) {
        return false;
    }
    --booksOut;
    fines += daysLate * DAILY_FINE;
    return true;
}

bool LibraryCard::payFine(double amount) {
    if (amount <= 0 || amount > fines) {
        return false;
    }
    fines -= amount;
    return true;
}

void LibraryCard::print() const {
    std::cout << "Card " << number << " | " << holder
              << " | books: " << booksOut
              << " | fines: $" << fines << '\n';
}

int LibraryCard::activeCards() { return count; }

bool LibraryCard::isValidName(const std::string& name) {
    return name.size() >= 2;
}

double LibraryCard::cleanFines(double fines) {
    return fines < 0 ? 0.0 : fines;
}
