package org.hanoi;

public class HanoiMove
{
    public Integer from, to;

    public HanoiMove(Integer from, Integer to)
    {
        this.from = from;
        this.to = to;
    }

    @Override
    public String toString() {
        return from.toString().concat(" -> ".concat(to.toString()));
    }
}
