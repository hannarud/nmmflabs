# NMMF Lab Two

from math import exp, sin, cos

# Метод прогонки
def progonka(n,c,a,b,f,x):
    alpha = [0 for i in range(n)]
    beta = [0 for i in range(n)]
    
    alpha[0] = b[0]/c[0]
    beta[0] = f[0]/c[0]
    
    for i in range(1,n):
        alpha[i] = b[i]/(c[i] - alpha[i-1]*a[i])
        beta[i] = (f[i] + beta[i-1]*a[i])/(c[i] - alpha[i-1]*a[i])
    
    x[n-1] = (f[n-1] + beta[n-2]*a[n-1])/(c[n-1] - alpha[n-2]*a[n-1]) 
    for i in range(n-2,-1,-1):
        x[i] = alpha[i]*x[i+1] + beta[i]

# Параметры задачи

# Ограничения на x и t
L = 1
T = 1

# Решение
def u(x,t):
    return (1+t**2)*(1-exp(-x))

# Правая часть
def f(x,t):
    return 2+(-1+t**2)*exp(-x)

# Начальные условия
def u_0(x):
    return 1-exp(-x)

def u_1(x):
    return 0

# Параметры третьей краевой задачи на обеих границах
alpha_1 = 2
def beta_1(t):
    return 1+t**2

alpha_2 = -1
def beta_2(t):
    return 1+t**2

# sigma = 0, явная схема

# Параметры сетки
h = 0.1
tau = 0.05
N = int(L/h)
M = int(T/tau)

# Задаем нужные функции на сетке
phi = [[f(h*i, tau*j) for j in range(M+1)] for i in range(N+1)]
y = [[0 for j in range(M+1)] for i in range(N+1)]

# Инициализируем нулевой слой
for i in range(N+1):
    y[i][0] = u_0(h*i)

# Инициализируем первый слой
for i in range(N+1):
    y[i][1] = tau*u_1(h*i)+y[i][0]

# Начинаем послойное заполнение согласно разработанной схеме (слой j+1, j=0,M-1)
# y[i][j+1], i = 1,N-1
for j in range(1, M):
    for i in range(1, N):
        y[i][j+1] = tau**2/h**2*(y[i+1][j]-2*y[i][j]+y[i-1][j])+\
        tau**2*phi[i][j]+2*y[i][j]-y[i][j-1]
    # в следующей строке где-то ошибка!
    y[0][j+1] = (h*(beta_1(tau*(j+1))-h/2*phi[0][j+1]+h/(2*tau**2)*\
    (-2*y[0][j]+y[0][j-1]))-y[1][j+1])/(-1-alpha_1*h-h**2/(2*tau**2))
    y[N][j+1] = y[N-1][j+1] + h*(alpha_2*y[N-1][j+1]+beta_2(tau*(j+1))+\
    h/2*(phi[N-1][j+1]-1/tau**2*(y[N-1][j+1]-2*y[N-1][j]+y[N-1][j-1])))

print("sigma = 0")
for j in range(M+1):
    for i in range(N+1):
        print('({}, {}) & {} & {}'.format(h*i, tau*j, y[i][j], u(h*i,tau*j)))
    print("\n")

# sigma = 1/2, неявная схема

# Параметры сетки
h = 0.1
tau = 0.1
N = int(L/h)
M = int(T/tau)

# Задаем нужные функции на сетке
phi = [[f(h*i, tau*j) for j in range(M+1)] for i in range(N+1)]
y = [[0 for j in range(M+1)] for i in range(N+1)]

# Инициализируем нулевой слой
for i in range(N+1):
    y[i][0] = u_0(h*i)

# Инициализируем первый слой
for i in range(N+1):
    y[i][1] = tau*u_1(h*i)+y[i][0]

# Решение систем методом прогонки для каждого j+1
for j in range(1,M):
    # Готовим систему для метода прогонки
    c = [0 for i in range(N+1)]
    a = [0 for i in range(N+1)]
    b = [0 for i in range(N+1)]
    d = [0 for i in range(N+1)]
    a[0] = 0
    c[0] = -1/h-alpha_1-h/(2*tau**2)
    b[0] = -1/h
    d[0] = beta_1(tau*(j+1))-h/2*phi[0][j+1]-h/(2*tau**2)*(-2*y[0][j]+y[0][j-1])
    for i in range(1,N):
        a[i] = 1/(2*h**2)
        c[i] = 1/(tau**2)+1/(h**2)
        b[i] = 1/(2*h**2)
        d[i] = (2*y[i][j]-y[i][j-1])/(tau**2)+(y[i+1][j-1]-2*y[i][j-1]+\
        y[i-1][j-1])/(2*h**2)+phi[i][j]
    a[N] = 1/h+alpha_2-h/(2*tau**2)
    c[N] = 1/h
    b[N] = 0
    d[N] = beta_2(tau*(j+1))+h/2*phi[N-1][j+1]+h/(2*tau**2)*(2*y[N-1][j]-\
    y[N-1][j-1])
    # Решаем систему методом прогонки
    # Тут что-то не так с индексацией, приходится делать финт
    pr = [0 for i in range(N+1)]
    progonka(N+1,c,a,b,d,pr)
    for i in range(N+1):
        y[i][j+1] = pr[i]

print("sigma = 1/2")
for j in range(M+1):
    for i in range(N+1):
        print('({}, {}) & {} & {}'.format(h*i, tau*j, y[i][j], u(h*i,tau*j)))
    print("\n")

# sigma = 1, полностью неявная схема

# Параметры сетки
h = 0.1
tau = 0.1
N = int(L/h)
M = int(T/tau)

# Задаем нужные функции на сетке
phi = [[f(h*i, tau*j) for j in range(M+1)] for i in range(N+1)]
y = [[0 for j in range(M+1)] for i in range(N+1)]

# Инициализируем нулевой слой
for i in range(N+1):
    y[i][0] = u_0(h*i)

# Инициализируем первый слой
for i in range(N+1):
    y[i][1] = tau*u_1(h*i)+y[i][0]

# Решение систем методом прогонки для каждого j+1
for j in range(1,M):
    # Готовим систему для метода прогонки
    c = [0 for i in range(N+1)]
    a = [0 for i in range(N+1)]
    b = [0 for i in range(N+1)]
    d = [0 for i in range(N+1)]
    a[0] = 0
    c[0] = -1/h-alpha_1-h/(2*tau**2)
    b[0] = -1/h
    d[0] = beta_1(tau*(j+1))-h/2*phi[0][j+1]-h/(2*tau**2)*(-2*y[0][j]+y[0][j-1])
    for i in range(1,N):
        a[i] = 1/(h**2)
        c[i] = 1/(tau**2)+2/(h**2)
        b[i] = 1/(h**2)
        d[i] = (2*y[i][j]-y[i][j-1])/(tau**2)+(-y[i+1][j]+2*y[i][j]-\
        y[i-1][j]+y[i+1][j-1]-2*y[i][j-1]+y[i-1][j-1])/(h**2)+phi[i][j]
    a[N] = 1/h+alpha_2-h/(2*tau**2)
    c[N] = 1/h
    b[N] = 0
    d[N] = beta_2(tau*(j+1))+h/2*phi[N-1][j+1]+h/(2*tau**2)*(2*y[N-1][j]-\
    y[N-1][j-1])
    # Решаем систему методом прогонки
    # Тут что-то не так с индексацией, приходится делать финт
    pr = [0 for i in range(N+1)]
    progonka(N+1,c,a,b,d,pr)
    for i in range(N+1):
        y[i][j+1] = pr[i]

print("sigma = 1")
for j in range(M+1):
    for i in range(N+1):
        print('({}, {}) & {} & {}'.format(h*i, tau*j, y[i][j], u(h*i,tau*j)))
    print("\n")
