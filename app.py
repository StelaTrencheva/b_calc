import streamlit as st

st.title("Betting Calculator")

# --- INPUT ---
match1_1 = st.number_input("1 - мач 1:", min_value=0.01, value=2.32)
match1_x = st.number_input("Х - мач 1:", min_value=0.01, value=3.35)
match1_2 = st.number_input("2 - мач 1:", min_value=0.01, value=3.7)

match2_1 = st.number_input("1 - мач 2:", min_value=0.01, value=1.32)
match2_x = st.number_input("Х - мач 2:", min_value=0.01, value=7.6)
match2_2 = st.number_input("2 - мач 2:", min_value=0.01, value=16.5)

boosted_coef_one = match1_1 * match2_1

betting_amount = 1000
profit_margin = 100

# --- CALCULATION ---
S = betting_amount + 100
found = False

while not found:
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
    e1 = x / 2
    f1 = x / 2

    k_lower = max(x, x - S + profit_margin)
    k_upper = S - 1
    if k_lower >= k_upper:
        S += 10
        continue
    k = (k_lower + k_upper) / 2

    # --- Find minimal y+z ---
    best_y = None
    best_z = None
    best_sum = float('inf')
    max_yz = int(S / 2)

    for y_guess in range(1, max_yz):
        for z_guess in range(1, max_yz):
            total = y_guess + z_guess
            if total >= best_sum:
                continue
            if (y_guess * match2_x > S + total) and (z_guess * match2_2 > S + total):
                best_y = y_guess
                best_z = z_guess
                best_sum = total

    if best_y is None:
        S += 10
        continue

    y, z = best_y, best_z

    if S + x < match2_2 * e1 or S + x < match2_x * f1:
        S += 10
        continue

    found = True

# --- OUTPUT ---
st.subheader("Results")
st.write(f"Залог мач 1 = {S}")
st.write(f"Умножен ккоефициент от мач 1 и 2 = {boosted_coef_one}, Залог = {a1}")
st.write(f"Х на мач 1 = {match1_x}, Залог = {b1}")
st.write(f"2 на мач 1 = {match1_2}, Залог = {c1}")
st.write(f"Х на мач 2 = {y}, 2 на мач 2 = {z} (Общо = {y+z})")