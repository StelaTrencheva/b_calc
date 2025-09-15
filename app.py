import streamlit as st

st.title("Двоен шанс калкулатор")

# --- INPUT ---
match1_1 = st.number_input("1 - мач 1:", min_value=0.01, value=2.32)
match1_x = st.number_input("Х - мач 1:", min_value=0.01, value=3.35)
match1_2 = st.number_input("2 - мач 1:", min_value=0.01, value=3.7)

match2_1 = st.number_input("1 - мач 2:", min_value=0.01, value=1.32)
match2_2 = st.number_input("2 - мач 2:", min_value=0.01, value=16.5)

boosted_coef_one = match1_1 * match2_1
betting_amount = 1000
profit_margin = 100

# --- CALCULATION ---
S = betting_amount + 100
found = False
max_iterations = 500
iteration = 0

while not found and iteration < max_iterations:
    iteration += 1
    k = 200
    a1_min = (S + k) / boosted_coef_one
    b1_min = (S + k) / match1_x
    c1_min = (S + k) / match1_2
    total_min = a1_min + b1_min + c1_min

    if total_min > S:
        S += 10
        continue

    remaining = S - total_min
    a1 = a1_min + remaining * (a1_min / total_min)
    b1 = b1_min + remaining * (b1_min / total_min)
    c1 = c1_min + remaining * (c1_min / total_min)

    x = k - 10
    e1 = x  # only one remaining variable for match 2
    f1 = 0  # not used anymore

    k_lower = max(x, x - S + profit_margin)
    k_upper = S - 1
    if k_lower >= k_upper:
        S += 10
        continue
    k = (k_lower + k_upper) / 2

    # --- Find minimal z ---
    best_z = None
    for z_guess in range(1, int(S)):
        if z_guess * match2_2 > S:
            if a1 * boosted_coef_one > S + z_guess:
                best_z = z_guess
                break

    if best_z is None:
        S += 10
        continue

    z = best_z

    # Final check
    if S + x < match2_2 * z or a1 * boosted_coef_one <= S + z:
        S += 10
        continue

    found = True

# --- OUTPUT ---
if found:
    st.subheader("Results")
    st.write(f"Залог мач 1 = {S}")
    st.write(f"Умножен коефициент от мач 1 и 2 = {boosted_coef_one}, Залог = {a1}")
    st.write(f"Х на мач 1 = {match1_x}, Залог = {b1}")
    st.write(f"2 на мач 1 = {match1_2}, Залог = {c1}")
    st.write(f"2 на мач 2 = {z}")
else:
    st.warning("Не може да се намери валидна комбинация с текущите коефициенти и залози.")