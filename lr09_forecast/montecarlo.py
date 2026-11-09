"""Monte Carlo прогноз кількості спринтів (ЛР9).

Одна симуляція: беремо залишок points; поки він більший за нуль, випадково
тягнемо velocity одного зі спринтів історії, віднімаємо і рахуємо спринт.
Повторюємо N разів, сортуємо результати і беремо 50-й і 85-й перцентилі,
округлені вгору до цілого спринта.

Запуск:
    python lr09_forecast/montecarlo.py 220 21 17          # обсяг і velocity
    python lr09_forecast/montecarlo.py reference           # три прогони на навчальних даних
"""
import math
import random
import sys


def simulate(remaining, velocities, runs=10000, seed=2026):
    if not any(v > 0 for v in velocities):
        raise ValueError("усі velocity нульові: прогноз нескінченний")
    rnd = random.Random(seed)          # фіксований seed, щоб прогін повторювався
    results = []
    for _ in range(runs):
        left, sprints = remaining, 0
        while left > 0:
            left -= rnd.choice(velocities)
            sprints += 1
        results.append(sprints)
    results.sort()

    def pct(p):                        # перцентиль: найменше значення, нижче або на рівні якого p частка результатів
        return results[math.ceil(p * runs) - 1]

    return pct(0.50), pct(0.85)


REFERENCE = [21, 17, 26, 14, 23, 6, 28, 12, 22, 25, 18, 9]   # lr09_reference_velocity.csv, points_done

if __name__ == "__main__":
    if sys.argv[1] == "reference":
        for label, vel in [("усі 12 спринтів", REFERENCE),
                           ("спринти 1 і 2", REFERENCE[0:2]),
                           ("спринти 5 і 6", REFERENCE[4:6])]:
            p50, p85 = simulate(220, vel)
            print(f"{label}: P50={p50} P85={p85} ширина={p85 - p50}")
    else:
        remaining = float(sys.argv[1])
        vel = [float(v) for v in sys.argv[2:]]
        p50, p85 = simulate(remaining, vel)
        print(f"remaining={remaining} velocity={vel}: P50={p50} P85={p85}")
