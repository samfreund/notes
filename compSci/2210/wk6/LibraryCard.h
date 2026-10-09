#ifndef LIBRARYCARD_H
#define LIBRARYCARD_H

#include <string>

/**
 * A LibraryCard represents one physical library card. It tracks the
 * holder's name, a unique card number assigned by the class, how many
 * books are checked out, and outstanding fines.
 *
 * Invariants:
 *  - holder always has at least 2 characters (otherwise "Guest").
 *  - number is unique per card, assigned sequentially from 5001, never changed.
 *  - fines is never negative.
 *  - booksOut is between 0 and MAX_BOOKS inclusive.
 *
 * Cards cannot be copied (one card object = one physical card) and
 * announce themselves on std::cout when destroyed.
 */
class LibraryCard {
public:
    /**
     * Creates a card for the given holder with no fines.
     * If the name has fewer than 2 characters, the holder becomes "Guest".
     * The constructor is explicit so a std::string never converts
     * silently into a LibraryCard.
     */
    explicit LibraryCard(std::string name);

    /**
     * Creates a card for the given holder owing startingFines dollars.
     * A negative starting fine becomes 0; invalid names become "Guest".
     */
    explicit LibraryCard(std::string name, double startingFines);

    /** Creates a card held by "Guest" with no fines. */
    LibraryCard();

    /** Closes the card and prints "Card <number> closed" on its own line. */
    ~LibraryCard();

    /* Cards stand for physical cards: copying one is not allowed. */
    LibraryCard(const LibraryCard&) = delete;
    LibraryCard& operator=(const LibraryCard&) = delete;

    /** Returns the holder's name. */
    std::string getHolder() const;

    /** Returns this card's unique number. */
    int getNumber() const;

    /** Returns how many books are currently checked out. */
    int getBooksOut() const;

    /** Returns the fines owed, in dollars. */
    double getFines() const;

    /**
     * Changes the holder's name if it has at least 2 characters.
     * Returns true on success; otherwise changes nothing and returns false.
     */
    bool setHolder(std::string name);

    /**
     * Adds one book, unless the card already holds MAX_BOOKS books
     * or owes more than $5.00 in fines. Returns true on success.
     */
    bool checkOut();

    /**
     * Removes one book and adds $0.25 in fines per day late.
     * Fails (returns false) if no books are checked out.
     */
    bool returnBook(int daysLate);

    /**
     * Pays amount dollars toward the fines.
     * Fails (returns false) if amount is not positive or exceeds the
     * fines owed; otherwise subtracts it and returns true.
     */
    bool payFine(double amount);

    /**
     * Prints one line in the form:
     * Card 5001 | Ana | books: 2 | fines: $0.50
     */
    void print() const;

    /** Returns how many LibraryCard objects exist right now. */
    static int activeCards();

private:
    /** The single definition of the 2-character name rule (B5). */
    static bool isValidName(const std::string& name);

    /** The single definition of the negative-fine rule (B5). */
    static double cleanFines(double fines);

    std::string holder;    /**< holder's name, always at least 2 characters */
    const int number;      /**< unique card number, fixed at creation (B4) */
    int booksOut;          /**< books checked out right now, 0..MAX_BOOKS */
    double fines;          /**< fines owed in dollars, never negative */

    static constexpr int MAX_BOOKS = 3;          /**< checkout limit (D2) */
    static constexpr double FINE_LIMIT = 5.00;   /**< blocks checkout */
    static constexpr double DAILY_FINE = 0.25;   /**< per day late */

    static int count;      /**< how many cards exist right now (D1) */
    static int nextNumber; /**< number to assign to the next card (B3) */
};

#endif // LIBRARYCARD_H
