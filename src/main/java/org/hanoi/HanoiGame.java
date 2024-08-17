package org.hanoi;

import java.util.*;
import java.util.stream.Collectors;

public class HanoiGame
{
    private List<Stack<Integer>> towers = new ArrayList<>(3);

    public HanoiGame(Stack<Integer> initialTower, Integer towerCount)
    {
        towers.add(initialTower);
        for (int i = 0; i < towerCount - 1; i++)
            towers.add(new Stack<>());
    }

    public static HanoiGame DefaultGame()
    {
        var disks = new Integer[] {5, 4, 3, 2, 1};
        var initialTower = new Stack<Integer>();

        for (Integer disk : disks)
            initialTower.push(disk);

        return new HanoiGame(initialTower, 3);
    }

    private void pushDisk(Integer towerIndex, Integer disk)
    {
        Stack<Integer> tower = getTower(towerIndex);
        if (tower.empty() || tower.peek() > disk)
            tower.push(disk);
    }

    private Integer popDisk(Integer towerIndex)
    {
        Stack<Integer> tower = getTower(towerIndex);

        try {
            return tower.pop();
        } catch (Exception e) {
            return null;
        }
    }

    public void applyMove(HanoiMove move)
    {
        Integer disk = popDisk(move.from);
        pushDisk(move.to, disk);
    }

    public List<HanoiMove> getPossibleMoves()
    {
        List<HanoiMove> moves = new ArrayList<>();
        List<Integer> topDisks = getTopDisks();

        for (int i = 0; i < topDisks.size(); i++)
            for (int j = 0; j < topDisks.size(); j++)
                if (topDisks.get(i) != null && (topDisks.get(j) == null || topDisks.get(i) < topDisks.get(j)))
                    moves.add(new HanoiMove(i, j));

        return moves;
    }

    public Integer getTopDisk(Integer towerIndex)
    {
        Stack<Integer> tower = getTower(towerIndex);

        try {
            return tower.peek();
        } catch (Exception e) {
            return null;
        }
    }

    public List<Integer> getTopDisks()
    {
        List<Integer> tops = new ArrayList<>(towers.size());
        for (int i = 0; i < towers.size(); i++)
            tops.add(getTopDisk(i));

        return tops;
    }

    public Stack<Integer> getTower(Integer index)
    {
        return towers.get(index);
    }

    public boolean isComplete()
    {
        return towers.stream()
                .dropWhile(Stack::empty)
                .count() <= 1;
    }

    @Override
    public String toString() {
        return towers.stream().map(tower -> tower.toString().concat("\n")).collect(Collectors.joining());
    }
}
