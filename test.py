from scipy.optimize import fsolve

# パラメータを設定
r = 5  # 円の半径
x1, y1 = 1, 2  # 点1の初期値
x2, y2 = 4, 3  # 点2の初期値

# 連立方程式を定義


def equations(vars):
    x1, y1, x2, y2 = vars
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return [y1 - a * x1 - b,
            y2 - a * x2 - b,
            a * b - (a**2 + 1) * (b**2 - r**2),
            x1]


def equations2(vars):
    x1, y1, x2, y2 = vars
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return [b, a-1, x1-1, y1-1]


# 初期推定値
initial_guess = [x1, y1, x2, y2]

# 方程式を解く
solution = fsolve(equations2, initial_guess)

# 結果を出力
x1_sol, y1_sol, x2_sol, y2_sol = solution
print(f"点1: ({x1_sol}, {y1_sol})")
print(f"点2: ({x2_sol}, {y2_sol})")
print(equations2(solution))
