# NMMF Lab 01

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
    return exp(-t)*(sin(x)+cos(x))

# Правая часть
def f(x,t):
    return 0

# Начальное условие
def u_0(x):
    return sin(x)+cos(x)

# Параметры третьей краевой задачи на обеих границах
alpha_1 = 2
def beta_1(t):
    return -exp(-t)

alpha_2 = -1
def beta_2(t):
    return 2*cos(1)*exp(-t)

# sigma = 0, явная схема

# Параметры сетки
h = 0.25
tau = 0.025
N = int(L/h)
M = int(T/tau)

# Задаем нужные функции на сетке
phi = [[f(h*i, tau*j) for j in range(M+1)] for i in range(N+1)]
y = [[0 for j in range(M+1)] for i in range(N+1)]

# Инициализируем нулевой слой
for i in range(N+1):
    y[i][0] = u_0(h*i)

# Начинаем послойное заполнение согласно разработанной схеме (слой j+1, j=0,M-1)
# y[i][j+1], i = 1,N-1
for j in range(M):
    for i in range(1, N):
        y[i][j+1] = y[i][j] + tau/(h**2)*(y[i+1][j] - 2*y[i][j] + y[i-1][j]) + tau*phi[i][j]
    y[0][j+1] = (h*(beta_1(tau*(j+1))-h/2*phi[0][j+1]-h/(2*tau)*y[0][j])-y[1][j+1])/(-1-alpha_1*h-h**2/(2*tau))
    y[N][j+1] = y[N-1][j+1] + h*(alpha_2*y[N-1][j+1]+beta_2(tau*(j+1))+h/2*(phi[N-1][j+1]-1/tau*(y[N-1][j+1]-y[N-1][j])))

for j in range(M+1):
    for i in range(N+1):
        print(y[i][j])
        print(u(h*i,tau*j))
    print("\n")

# sigma = 1/2, неявная схема

# Параметры сетки
h = 0.25
tau = 0.05
N = int(L/h)
M = int(T/tau)

# Задаем нужные функции на сетке
phi = [[f(h*i, tau*j) for j in range(M+1)] for i in range(N+1)]
y = [[0 for j in range(M+1)] for i in range(N+1)]

# Инициализируем нулевой слой
for i in range(N+1):
    y[i][0] = u_0(h*i)

# Решение систем методом прогонки для каждого j+1
for j in range(M):
    # Готовим систему для метода прогонки
    c = [0 for i in range(N+1)]
    a = [0 for i in range(N+1)]
    b = [0 for i in range(N+1)]
    d = [0 for i in range(N+1)]
    a[0] = 0
    c[0] = -1/h-alpha_1-h/(2*tau)
    b[0] = -1/h
    d[0] = beta_1(tau*(j+1))-h/2*phi[0][j+1]-h/(2*tau)*y[0][j]
    for i in range(1,N):
        a[i] = 1/(2*h**2)
        c[i] = 1/tau+1/(h**2)
        b[i] = 1/(2*h**2)
        d[i] = y[i][j]/tau+(y[i+1][j]-2*y[i][j]+y[i-1][j])/(2*h**2)+phi[i][j]
    a[N] = 1/h+alpha_2-h/(2*tau)
    c[N] = 1/h
    b[N] = 0
    d[N] = beta_2(tau*(j+1))+h/2*phi[N-1][j+1]+h/(2*tau)*y[N-1][j]
    # Решаем систему методом прогонки
    # Тут что-то не так с индексацией, приходится делать финт
    pr = [0 for i in range(N+1)]
    progonka(N+1,c,a,b,d,pr)
    for i in range(N+1):
        y[i][j+1] = pr[i]

for j in range(M+1):
    for i in range(N+1):
        print(y[i][j])
        print(u(h*i,tau*j))
    print("\n")

# sigma = 1, полностью неявная схема

# Параметры сетки
h = 0.1
tau = 0.1
N = int(L/h)
M = int(T/tau)

# Задаем нужные функции на сетке
phi = [[f(h*i,tau*j) for j in range(M+1)] for i in range(N+1)]
y = [[0 for j in range(M+1)] for i in range(N+1)]

# Инициализируем нулевой слой
for i in range(N+1):
    y[i][0] = u_0(h*i)

# Решение систем методом прогонки для каждого j+1
for j in range(M):
    # Готовим систему для метода прогонки
    c = [0 for i in range(N+1)]
    a = [0 for i in range(N+1)]
    b = [0 for i in range(N+1)]
    d = [0 for i in range(N+1)]
    a[0] = 0
    c[0] = -1/h-alpha_1-h/(2*tau)
    b[0] = -1/h
    d[0] = beta_1(tau*(j+1))-h/2*phi[0][j+1]-h/(2*tau)*y[0][j]
    for i in range(1,N):
        a[i] = 1/(h**2)
        c[i] = 1/tau+2/(h**2)
        b[i] = 1/(h**2)
        d[i] = y[i][j]/tau+phi[i][j]
    a[N] = 1/h+alpha_2-h/(2*tau)
    c[N] = 1/h
    b[N] = 0
    d[N] = beta_2(tau*(j+1))+h/2*phi[N-1][j+1]+h/(2*tau)*y[N-1][j]
    # Решаем систему методом прогонки
    # Тут что-то не так с индексацией, приходится делать финт
    pr = [0 for i in range(N+1)]
    progonka(N+1,c,a,b,d,pr)
    for i in range(N+1):
        y[i][j+1] = pr[i]

for j in range(M+1):
    for i in range(N+1):
        print(y[i][j])
        print(u(h*i,tau*j))
    print("\n")
