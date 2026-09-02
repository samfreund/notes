   javac --module-path /usr/lib/jvm/java-25-openjfx/lib --add-modules javafx.controls,javafx.fxml -d out src/checkers/*.java
   java --module-path /usr/lib/jvm/java-25-openjfx/lib --add-modules javafx.controls,javafx.fxml -cp "out:src" checkers.Main
