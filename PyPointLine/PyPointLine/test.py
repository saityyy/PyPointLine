import numpy as np
from scipy.optimize import minimize

# 目的関数の定義


def objective(x):
    return (x[0] + x[1] - x[2] - 2 * x[3])**2

# 制約条件の定義


def constraint(x):
    return x[0]**2 + x[1]**2 - 1e-9  # x[0]^2 + x[1]^2 > 0 を満たすように -1e-9 を使用


def constraint2(x):
    return x[0]+x[1]+x[2]+x[3]


# 制約条件を辞書として定義
cons = ({'type': 'ineq', 'fun': constraint},
        {'type': 'eq', 'fun': constraint2})

bnds = [(-1, 1), (-1, 1), (-1, 1), (-1, 1)]

# 初期値の設定
x0 = np.array([0.5, 0.5, 0.5, 0.5])

# 最適化の実行
solution = minimize(objective, x0, bounds=bnds, constraints=cons)

# 結果の表示
print("最適化結果:")
print("最適な変数の値:", solution.x)
print("目的関数の最小値:", solution.fun)
