package checkers;

import javafx.scene.paint.Color;
import javafx.scene.shape.Ellipse;
import javafx.scene.layout.Pane;

public class Piece {
    public enum Type { RED, BLACK }
    private final Type type;
    private boolean king;
    private int x, y;

    private Pane unit;      // atomic container
    private Ellipse ellipse;
    private Ellipse crown;

    public Piece(Type type, int x, int y) { this(type, x, y, false); }
    public Piece(Type type, int x, int y, boolean king) {
        this.type = type; this.king = king; this.x = x; this.y = y;
        unit = new Pane();
        unit.setPrefSize(0, 0);
        ellipse = createEllipse();
        crown = createCrown();
        crown.setVisible(false);
        unit.getChildren().addAll(ellipse, crown);
        setActive(false);
        unit.setOnMouseClicked(ev -> trySetActive());
        reposition();
        BoardController.addChild(unit);
        BoardController.getSquare(x, y).placePiece(this);
    }

    private Ellipse createEllipse() {
        Ellipse e = new Ellipse();
        e.setRadiusX(25.0f); e.setRadiusY(12.0f);
        e.setStroke(Color.WHITE);
        e.setFill(type == Type.RED ? Color.RED : Color.BLACK);
        return e;
    }

    private Ellipse createCrown() {
        Ellipse c = new Ellipse();
        c.setRadiusX(25.0f); c.setRadiusY(12.0f);
        c.setStroke(Color.WHITE);
        c.setFill(type == Type.RED ? Color.RED : Color.BLACK);
        return c;
    }

    private void reposition() {
        double cx = x * BoardController.SQUARE_SIZE + BoardController.SQUARE_SIZE / 2.0;
        double cy = y * BoardController.SQUARE_SIZE + BoardController.SQUARE_SIZE / 2.0;
        unit.setLayoutX(cx - 25); // align so ellipse center matches cx/cy
        unit.setLayoutY(cy - 12);
        ellipse.setLayoutX(25); // relative to pane
        ellipse.setLayoutY(12);
        crown.setLayoutX(25);
        crown.setLayoutY(-2); // directly above main ellipse, slight overlap
        if (king) crown.setVisible(true);
        else crown.setVisible(false);
    }

    private void trySetActive() { BoardController.trySetActive(this); }

    public void setActive(boolean isActive) {
        ellipse.setStrokeWidth(isActive ? 3 : 1);
        crown.setStrokeWidth(isActive ? 3 : 1);
    }

    public void tryMove(checkers.Square target_square) {
        if (target_square.getPiece() != null) {
            BoardController.setMessage("That location is already occupied!\nPlease select a different location or piece.");
        } else {
            if (isValidOrdinaryMove(target_square)) {
                move(target_square);
            } else if (isValidCapture(target_square)) {
                captureMoveTo(target_square);
            } else {
                BoardController.setMessage("The piece can neither move nor capture to that position.\nPlease try a different square.");
            }
        }
    }

    private void move(checkers.Square target_square) {
        BoardController.getSquare(x, y).removePiece();
        placeOnSquare(target_square);
        BoardController.switchTurns();
        setActive(false);
        if (type == Type.BLACK && y == 0) king = true;
        if (type == Type.RED && y == BoardController.BOARD_WIDTH - 1) king = true;
        reposition();
    }

    private void placeOnSquare(checkers.Square square) {
        this.x = square.getX();
        this.y = square.getY();
        BoardController.getSquare(x, y).placePiece(this);
        reposition();
    }

    private void captureMoveTo(checkers.Square square) {
        checkers.Piece captured = getCapturedPiece(square);
        if (captured == null) throw new IllegalArgumentException("Cannot capture");
        captured.removeSelf();
        move(square);
    }

    public void removeSelf() {
        BoardController.getSquare(x, y).removePiece();
        BoardController.removeChild(unit);
    }

    public boolean isValidOrdinaryMove(checkers.Square square) {
        int dy = square.getY() - y, dx = square.getX() - x;
        if (Math.abs(dx) != 1 || Math.abs(dy) != 1) return false;
        if (king) return true;
        return (type == Type.BLACK) ? dy == -1 : dy == 1;
    }

    private boolean isValidCapture(checkers.Square square) {
        return getCapturedPiece(square) != null;
    }

    public checkers.Piece getCapturedPiece(checkers.Square square) {
        int dy = square.getY() - y, dx = square.getX() - x;
        if (Math.abs(dx) != 2 || Math.abs(dy) != 2) return null;
        if (!king) {
            if (type == Type.BLACK && dy != -2) return null;
            if (type == Type.RED && dy != 2) return null;
        }
        checkers.Piece mid = getMiddlePiece(square);
        if (mid != null && mid.getType().equals(this.type)) return null;
        return mid;
    }

    private checkers.Piece getMiddlePiece(checkers.Square square) {
        return BoardController.getSquare((square.getX() + x) / 2, (square.getY() + y) / 2).getPiece();
    }

    public Type getType() { return type; }
    public String toString() { return "Piece at " + x + "," + y; }
}
