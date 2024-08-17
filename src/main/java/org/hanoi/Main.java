package org.hanoi;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    public static void main(String[] args) {
        HanoiGame game = HanoiGame.DefaultGame();

        game.applyMove(new HanoiMove(0, 1));
        game.applyMove(new HanoiMove(1, 0));

        System.out.println(game);
        System.out.println(game.getPossibleMoves());
    }
}